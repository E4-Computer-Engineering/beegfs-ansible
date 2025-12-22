#!/usr/bin/env bash
set -euo pipefail

# Script to validate version tag format and ensure it's higher than the current version
# Usage: validate-version.sh <tag>

TAG="$1"
VERSION="${TAG#v}"  # Remove 'v' prefix

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Send all log messages to stderr so they don't interfere with the version output
echo "Validating tag: $TAG" >&2
echo "Version: $VERSION" >&2

# Check if tag starts with 'v'
if [[ ! "$TAG" =~ ^v ]]; then
    echo -e "${RED}Error: Tag must start with 'v' (e.g., v1.2.3)${NC}" >&2
    exit 1
fi

# Validate version format (X.X.X)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Version must follow X.X.X format (e.g., 1.2.3)${NC}" >&2
    exit 1
fi

# Get current version from galaxy.yml
CURRENT_VERSION=$(grep -E "^version:" galaxy.yml | awk '{print $2}')
echo "Current version in galaxy.yml: $CURRENT_VERSION" >&2

# Function to compare versions
version_gt() {
    # Returns 0 if $1 > $2
    test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"
}

# Check if new version is higher than current version
if ! version_gt "$VERSION" "$CURRENT_VERSION"; then
    echo -e "${RED}Error: New version ($VERSION) must be higher than current version ($CURRENT_VERSION)${NC}" >&2
    exit 1
fi

echo -e "${GREEN}Version validation successful!${NC}" >&2

# Output only the version to stdout (this is what gets captured)
echo "$VERSION"
exit 0
