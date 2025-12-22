#!/usr/bin/env bash
set -euo pipefail

# Script to detect which BeeGFS roles have changed
# Used in CI to determine which roles need testing

# Check required environment variables
if [ -z "${GITHUB_EVENT_NAME:-}" ]; then
    echo "Error: GITHUB_EVENT_NAME not set"
    exit 1
fi

# Determine base and head SHA based on event type
if [ "$GITHUB_EVENT_NAME" = "pull_request" ]; then
    if [ -z "${PR_BASE_SHA:-}" ] || [ -z "${PR_HEAD_SHA:-}" ]; then
        echo "Error: PR_BASE_SHA and PR_HEAD_SHA must be set for pull_request events"
        exit 1
    fi
    BASE_SHA="$PR_BASE_SHA"
    HEAD_SHA="$PR_HEAD_SHA"
else
    # For workflow_dispatch, compare with main branch
    BASE_SHA="origin/main"
    HEAD_SHA="HEAD"
fi

# Get changed files in roles directory
CHANGED_FILES=$(git diff --name-only "$BASE_SHA" "$HEAD_SHA" | grep '^roles/' || true)

echo "Changed files in roles/:"
echo "$CHANGED_FILES"

# Check if _common role was changed
if echo "$CHANGED_FILES" | grep -q '^roles/_common/'; then
    echo "test-all=true" >> "$GITHUB_OUTPUT"
    echo "roles=[\"metad\", \"mgmtd\", \"storaged\", \"mon\"]" >> "$GITHUB_OUTPUT"
    echo "_common role changed, testing all server roles (client requires full cluster)"
    exit 0
fi

# Extract unique role names from changed files (excluding _common and client)
# Client role requires full cluster and kernel modules, tested separately in OpenStack
ROLES=$(echo "$CHANGED_FILES" | \
    grep '^roles/' | \
    sed 's|^roles/||' | \
    cut -d'/' -f1 | \
    grep -v '^_common$' | \
    grep -v '^client$' | \
    sort -u)

if [ -z "$ROLES" ]; then
    echo "test-all=false" >> "$GITHUB_OUTPUT"
    echo "roles=[]" >> "$GITHUB_OUTPUT"
    echo "No role changes detected"
else
    echo "test-all=false" >> "$GITHUB_OUTPUT"
    # Convert to JSON array format
    ROLES_JSON=$(echo "$ROLES" | jq -R -s -c 'split("\n") | map(select(length > 0))')
    echo "roles=$ROLES_JSON" >> "$GITHUB_OUTPUT"
    echo "Changed roles: $ROLES_JSON"
fi
