#!/bin/bash
set -euo pipefail

# Script to update CHANGELOG.rst using antsibull-changelog
# This script assumes antsibull-changelog is installed

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Installing antsibull-changelog..."
pip install antsibull-changelog

echo -e "${YELLOW}Generating changelog...${NC}"

# Initialize changelog if not already initialized (safe to run multiple times)
if [ ! -d "changelogs" ]; then
    echo "Initializing changelog..."
    antsibull-changelog init .
fi

# Release the changelog
# This will:
# 1. Read the version from galaxy.yml
# 2. Process all fragment files in changelogs/fragments/
# 3. Update CHANGELOG.rst
# 4. Create an entry in changelogs/changelog.yaml
antsibull-changelog release

echo -e "${GREEN}Changelog updated successfully!${NC}"

# Display the changes
if [ -f "CHANGELOG.rst" ]; then
    echo "CHANGELOG.rst has been updated:"
    echo "---"
    head -n 30 CHANGELOG.rst
    echo "---"
fi

exit 0
