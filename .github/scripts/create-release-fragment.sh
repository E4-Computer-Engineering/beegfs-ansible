#!/usr/bin/env bash
set -euo pipefail

# Script to create a release summary fragment with the current date
# Usage: create-release-fragment.sh <version> [description]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <version> [description]"
    echo "Example: $0 2.3.0 'This release adds new features'"
    exit 1
fi

VERSION="$1"
DESCRIPTION="${2:-This release includes bug fixes and improvements}"
TODAY=$(date +%Y-%m-%d)

FRAGMENT_FILE="changelogs/fragments/${VERSION}.yml"

if [ -f "$FRAGMENT_FILE" ]; then
    echo "Warning: Fragment file $FRAGMENT_FILE already exists!"
    echo "Do you want to overwrite it? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

cat > "$FRAGMENT_FILE" <<EOF
release_summary: |
  | Release Date: ${TODAY}
  | ${DESCRIPTION}
EOF

echo "Created changelog fragment: $FRAGMENT_FILE"
echo "---"
cat "$FRAGMENT_FILE"
echo "---"
echo ""
echo "Next steps:"
echo "1. Edit $FRAGMENT_FILE to customize the release description if needed"
echo "2. Update galaxy.yml to version ${VERSION}"
echo "3. Run: antsibull-changelog release"
echo "   This will update CHANGELOG.rst and process the fragment"
echo "4. Review the changes to CHANGELOG.rst"
echo "5. Commit all changes and create PR:"
echo "   git add galaxy.yml CHANGELOG.rst changelogs/"
echo "   git commit -m 'chore: prepare release ${VERSION}'"
echo "6. After merge, create and push tag v${VERSION}"
