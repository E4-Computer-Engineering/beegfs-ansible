#!/usr/bin/env bash
set -euo pipefail

# Script to detect changed roles and apply corresponding labels to pull requests
# Used in conventional-label workflow

# Check required environment variables
if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "Error: GITHUB_TOKEN not set"
    exit 1
fi

if [ -z "${PR_NUMBER:-}" ]; then
    echo "Error: PR_NUMBER not set"
    exit 1
fi

if [ -z "${GITHUB_REPOSITORY:-}" ]; then
    echo "Error: GITHUB_REPOSITORY not set"
    exit 1
fi

if [ -z "${PR_BASE_SHA:-}" ] || [ -z "${PR_HEAD_SHA:-}" ]; then
    echo "Error: PR_BASE_SHA and PR_HEAD_SHA must be set"
    exit 1
fi

# Get list of changed files in roles directory
CHANGED_FILES=$(git diff --name-only "$PR_BASE_SHA" "$PR_HEAD_SHA" | grep '^roles/' || true)

if [ -z "$CHANGED_FILES" ]; then
    echo "No role changes detected"
    exit 0
fi

echo "Changed files in roles/:"
echo "$CHANGED_FILES"

# Extract unique role names
ROLES=$(echo "$CHANGED_FILES" | \
    sed 's|^roles/||' | \
    cut -d'/' -f1 | \
    sort -u)

echo "Changed roles: $ROLES"

# Function to add label to PR
add_label() {
    local label="$1"
    echo "Adding label: $label"

    # Check if label exists in the repository
    if ! gh api "repos/${GITHUB_REPOSITORY}/labels/${label}" &>/dev/null; then
        echo "Label '${label}' does not exist, creating it..."
        gh api "repos/${GITHUB_REPOSITORY}/labels" \
            -f name="${label}" \
            -f color="0e8a16" \
            -f description="Changes in ${label}" || true
    fi

    # Add label to PR
    gh api "repos/${GITHUB_REPOSITORY}/issues/${PR_NUMBER}/labels" \
        -f labels[]="${label}" || echo "Failed to add label ${label}"
}

# Check if _common role was changed
if echo "$ROLES" | grep -q '^_common$'; then
    echo "_common role changed - applying all role labels"

    # Get all existing role labels from the repository
    ALL_ROLE_LABELS=$(gh api "repos/${GITHUB_REPOSITORY}/labels?per_page=100" \
        --jq '.[] | select(.name | startswith("roles/")) | .name')

    if [ -n "$ALL_ROLE_LABELS" ]; then
        echo "$ALL_ROLE_LABELS" | while read -r label; do
            add_label "$label"
        done
    else
        echo "No existing role labels found"
    fi
else
    # Add labels for each changed role
    for role in $ROLES; do
        if [ "$role" != "_common" ]; then
            label="roles/${role}"
            add_label "$label"
        fi
    done
fi

echo "Role labeling completed"
