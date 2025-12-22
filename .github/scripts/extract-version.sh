#!/usr/bin/env bash
set -euo pipefail

# Script to extract and validate version from git tag
# Used in release workflow to ensure version consistency

# Check required environment variables
if [ -z "${GITHUB_REF_NAME:-}" ]; then
    echo "Error: GITHUB_REF_NAME not set"
    exit 1
fi

if [ -z "${GITHUB_OUTPUT:-}" ]; then
    echo "Error: GITHUB_OUTPUT not set"
    exit 1
fi

TAG="$GITHUB_REF_NAME"
VERSION="${TAG#v}"  # Remove 'v' prefix

echo "Tag: $TAG"
echo "Version: $VERSION"

# Validate tag format: vX.Y.Z where X is 1-2 digits, Y and Z are 1 digit
if [[ ! "$TAG" =~ ^v[0-9]{1,2}\.[0-9]\.[0-9]$ ]]; then
    echo "Error: Tag must follow format vX.Y.Z where X is 1-2 digits, Y and Z are 1 digit (e.g., v1.2.3 or v12.3.4)"
    exit 1
fi

# Get version from galaxy.yml
GALAXY_VERSION=$(grep -E "^version:" galaxy.yml | awk '{print $2}')
echo "Version in galaxy.yml: $GALAXY_VERSION"

# Verify versions match
if [ "$VERSION" != "$GALAXY_VERSION" ]; then
    echo "Error: Tag version ($VERSION) does not match galaxy.yml version ($GALAXY_VERSION)"
    echo "Please update galaxy.yml to version $VERSION before creating the tag"
    exit 1
fi

echo "Version validation successful!"
echo "version=${VERSION}" >> "$GITHUB_OUTPUT"
