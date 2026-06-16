#!/usr/bin/env bash
# Validator for Bootstrap Eval
# Verifies creation of project and cleans it up.

PROJECT_PATH="sandbox/eval-test-bootstrap"
STATUS=0

# 1. Verify folder exists and has .agents
if [ ! -d "$PROJECT_PATH/.agents" ]; then
  echo "Error: $PROJECT_PATH/.agents does not exist"
  STATUS=1
fi

# 2. Verify Hub config exists
python3 -c "
import os, json, glob
projects_dir = os.path.expanduser('~/.gemini/config/projects')
found = False
for path in glob.glob(os.path.join(projects_dir, '*.json')):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            if data.get('name') == './sandbox/eval-test-bootstrap':
                found = True
                break
    except: pass
if not found:
    print('Error: Hub config not found for ./sandbox/eval-test-bootstrap')
    exit(1)
" || STATUS=1

# 3. Cleanup
python3 tests/cleanup_project.py "./sandbox/eval-test-bootstrap"

exit $STATUS
