#!/usr/bin/env python3
#
# Core SDD Simulation Helper Library
# Wraps project registration, agentapi execution, and file assertions.
#

import subprocess
import json
import os
import uuid
import sys

class SDDSimulator:
    def __init__(self, project_name, workspace_dir=None, reuse_active=False):
        self.project_name = project_name
        self.reuse_active = reuse_active
        
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.workspace_dir = os.path.dirname(self.script_dir)
        
        self.temp_path = os.path.join(self.workspace_dir, "sandbox", self.project_name)
        
        self.env = os.environ.copy()
        
        if self.reuse_active and "ANTIGRAVITY_PROJECT_ID" in os.environ:
            self.project_id = os.environ["ANTIGRAVITY_PROJECT_ID"]
            self.config_path = None
            self.log_info(f"Reusing active project ID: {self.project_id}")
        else:
            # Generate a deterministic UUID based on the project name
            self.project_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, project_name))
            self.config_path = f"/usr/local/google/home/brodiem/.gemini/config/projects/{self.project_id}.json"
            self.env["ANTIGRAVITY_PROJECT_ID"] = self.project_id
            
        self.env["GEMINI_WORKSPACE_DIR"] = os.path.join(self.workspace_dir, "workspace")

    def log_info(self, msg):
        print(f"\033[1;34m[{self.project_name} Sim]\033[0m {msg}")

    def log_pass(self, msg):
        print(f"\033[1;32m[PASS]\033[0m {msg}")

    def log_fail(self, msg):
        print(f"\033[1;31m[FAIL]\033[0m {msg}", file=sys.stderr)
        self.cleanup()
        sys.exit(1)

    def setup_workspace(self, initial_files=None, permission_grants=None):
        self.log_info(f"Cleaning previous sandbox residues at {self.temp_path}...")
        subprocess.run(["rm", "-rf", self.temp_path])
        if self.config_path and os.path.exists(self.config_path):
            os.remove(self.config_path)

        # Create sandbox directory first to prevent gRPC daemon mount race conditions
        self.log_info(f"Creating sandbox directory at {self.temp_path}...")
        os.makedirs(self.temp_path, exist_ok=True)

        if self.config_path:
            # Create temporary project config JSON
            self.log_info(f"Registering temporary project config at {self.config_path}...")
            config = {
                "id": self.project_id,
                "name": self.project_name,
                "projectResources": {
                    "resources": [{"folderUri": f"file://{self.temp_path}"}]
                }
            }

            # Handle permission isolation
            if permission_grants:
                config["permissionGrants"] = permission_grants
            else:
                # Default: restrict write access strictly to sandbox, block writing to parent workspace
                config["permissionGrants"] = {
                    "allow": [
                        f"read_file({self.temp_path})",
                        f"write_file({self.temp_path})"
                    ],
                    "deny": [
                        f"write_file({self.workspace_dir})"
                    ]
                }

            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)

        # Init git
        self.log_info(f"Initializing temporary git repository at {self.temp_path}...")
        subprocess.run(["git", "init", "-q"], cwd=self.temp_path)
        subprocess.run(["git", "config", "user.email", "test-agent@google.com"], cwd=self.temp_path)
        subprocess.run(["git", "config", "user.name", "Test Agent"], cwd=self.temp_path)

        # Write any requested initial files
        if initial_files:
            for rel_path, content in initial_files.items():
                abs_path = os.path.join(self.temp_path, rel_path)
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                with open(abs_path, "w") as f:
                    f.write(content)
            
            # Commit them so git is in a clean state
            subprocess.run(["git", "add", "."], cwd=self.temp_path)
            subprocess.run(["git", "commit", "-m", "initial commit", "-q"], cwd=self.temp_path)

    def register_existing_directory(self, target_path, permission_grants=None):
        self.temp_path = target_path
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

        self.log_info(f"Registering existing directory config at {self.config_path} targeting {self.temp_path}...")
        config = {
            "id": self.project_id,
            "name": self.temp_path,
            "projectResources": {
                "resources": [{"folderUri": f"file://{self.temp_path}"}]
            }
        }

        if permission_grants:
            config["permissionGrants"] = permission_grants
        else:
            # Sandbox rules: restrict write access to the worktree folder only
            config["permissionGrants"] = {
                "allow": [
                    f"read_file({self.temp_path})",
                    f"write_file({self.temp_path})"
                ],
                "deny": [
                    f"write_file({self.workspace_dir})"
                ]
            }

        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

    def run_agentapi(self, cmd_list):
        result = subprocess.run(cmd_list, env=self.env, capture_output=True, text=True)
        if result.returncode != 0:
            try:
                err_json = json.loads(result.stderr or result.stdout)
                self.log_fail(f"agentapi execution failed: {err_json.get('error')}")
            except Exception:
                self.log_fail(f"agentapi execution failed (code {result.returncode}): {result.stderr or result.stdout}")
        
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            self.log_fail(f"Failed to parse agentapi JSON output: {result.stdout}")

    def new_conversation(self, prompt):
        self.log_info(f"Triggering conversation with prompt: '{prompt}'...")
        res = self.run_agentapi(["agentapi", "new-conversation", prompt])
        
        resp_data = res.get("response", {})
        conversation_id = resp_data.get("conversationId") or res.get("conversationId") or resp_data.get("newConversation", {}).get("conversationId")
        if not conversation_id:
            conversation_id = resp_data.get("conversationMetadata", {}).get("metadata", {}).get("initializationStateId")
            
        if not conversation_id:
            self.log_fail(f"Could not extract conversationId from response: {res}")
            
        self.log_info(f"Conversation successfully created! ID: {conversation_id}")
        return conversation_id

    def send_message(self, conversation_id, content):
        self.log_info(f"Sending message: '{content}'...")
        return self.run_agentapi(["agentapi", "send-message", conversation_id, content])

    def assert_file_exists(self, rel_path, content_contains=None):
        abs_path = os.path.join(self.temp_path, rel_path)
        if not os.path.isfile(abs_path):
            self.log_fail(f"Assertion failed: File not found: {rel_path}")
        self.log_pass(f"File exists: {rel_path}")
        
        if content_contains:
            with open(abs_path, "r") as f:
                content = f.read()
                if content_contains not in content:
                    self.log_fail(f"Assertion failed: File {rel_path} does not contain '{content_contains}'")
            self.log_pass(f"File {rel_path} contains expected text '{content_contains}'")

    def assert_file_does_not_contain(self, rel_path, content_does_not_contain):
        abs_path = os.path.join(self.temp_path, rel_path)
        if not os.path.isfile(abs_path):
            self.log_fail(f"Assertion failed: File not found: {rel_path}")
        with open(abs_path, "r") as f:
            content = f.read()
            if content_does_not_contain in content:
                self.log_fail(f"Assertion failed: File {rel_path} contains unexpected text '{content_does_not_contain}'")
        self.log_pass(f"File {rel_path} does not contain '{content_does_not_contain}'")

    def cleanup(self):
        self.log_info("Cleaning up simulation environment...")
        if self.config_path and os.path.exists(self.config_path):
            os.remove(self.config_path)
            self.log_pass("Temporary project config deleted.")
        if os.path.exists(self.temp_path):
            subprocess.run(["rm", "-rf", self.temp_path])
            self.log_pass("Temporary sandbox directory cleaned.")
