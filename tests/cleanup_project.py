#!/usr/bin/env python3
#
# Helper to cleanly deregister a Jetski project and delete its directory.
# Matches by project name or directory path.
#

import os
import sys
import json
import shutil

def is_framework_root(path):
    return os.path.exists(os.path.join(path, "global", "skills", "project-bootstrap"))

def cleanup_project(project_path_or_name):
    # Resolve absolute path
    abs_path = os.path.abspath(project_path_or_name)
    
    if is_framework_root(abs_path):
        print(f"[Cleanup] Error: Target path appears to be the framework root. Deletion blocked: {abs_path}", file=sys.stderr)
        return
    
    projects_dir = os.path.expanduser("~/.gemini/config/projects")
    if not os.path.isdir(projects_dir):
        print(f"[Cleanup] Projects directory not found: {projects_dir}")
        return

    deleted_config = False
    for filename in os.listdir(projects_dir):
        if not filename.endswith(".json"):
            continue
        config_path = os.path.join(projects_dir, filename)
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            
            # Check if name matches or any resource folderUri matches
            match = False
            if config.get("name") == project_path_or_name:
                match = True
            
            resources = config.get("projectResources", {}).get("resources", [])
            for res in resources:
                uri = res.get("folderUri") or res.get("gitFolder", {}).get("folderUri")
                if uri:
                    # Strip file:// prefix
                    path = uri.replace("file://", "")
                    if os.path.abspath(path) == abs_path:
                        match = True
                        break
            
            if match:
                print(f"[Cleanup] Deleting Hub project config: {config_path} (Project: {config.get('name')})")
                os.remove(config_path)
                deleted_config = True
        except Exception as e:
            print(f"[Cleanup] Error reading {config_path}: {e}", file=sys.stderr)

    # Path resolution fallbacks
    resolved_path = None
    if os.path.exists(abs_path):
        resolved_path = abs_path
    else:
        # Fallback 1: Default bootstrap folder (~/projects/<name>)
        default_path = os.path.expanduser(f"~/projects/{project_path_or_name}")
        if os.path.exists(default_path):
            resolved_path = default_path
        else:
            # Fallback 2: Sandbox relative folder (sandbox/<name>)
            rel_sandbox = os.path.join(os.getcwd(), "sandbox", project_path_or_name)
            if os.path.exists(rel_sandbox):
                resolved_path = rel_sandbox

    if resolved_path:
        if is_framework_root(resolved_path):
            print(f"[Cleanup] Error: Target path appears to be the framework root. Deletion blocked: {resolved_path}", file=sys.stderr)
            return
        print(f"[Cleanup] Deleting project folder: {resolved_path}")
        shutil.rmtree(resolved_path)
        print(f"[Cleanup] Success: Project folder removed.")
    else:
        print(f"[Cleanup] Project folder not found on disk (checked absolute, ~/projects/, and sandbox/).")
        
    if not deleted_config:
        print(f"[Cleanup] Warning: No registered Jetski Hub project config found matching: {project_path_or_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cleanup_project.py <project_name_or_path>")
        sys.exit(1)
    cleanup_project(sys.argv[1])
