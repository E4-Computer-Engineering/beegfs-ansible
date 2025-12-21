# Release Automation Scripts

This directory contains scripts used by the automated release workflow and helper scripts for preparing releases.

## Scripts

### create-release-fragment.sh

Helper script to create a changelog fragment with the correct date automatically.

**Usage:**
```bash
./.github/scripts/create-release-fragment.sh 2.3.0 "Description of this release"
```

**What it does:**
- Creates a new changelog fragment file in `changelogs/fragments/`
- Automatically uses the current date (YYYY-MM-DD format)
- Provides next steps for completing the release process

**Example:**
```bash
./.github/scripts/create-release-fragment.sh 2.3.0 "This release adds support for BeeGFS v8"
```

This will create `changelogs/fragments/2.3.0.yml` with today's date.

### validate-version.sh

Validates that a version tag follows the correct format and is higher than the current version.

**Usage:**
```bash
./validate-version.sh v2.2.0
```

**Validation checks:**
- Tag must start with 'v' (e.g., v1.2.3)
- Version must follow semantic versioning format X.X.X
- Version must be higher than the current version in galaxy.yml

**Output:**
- Prints the version number (without 'v' prefix) to stdout on success
- Exits with code 1 and prints error message on failure

### update-changelog.sh

Updates the CHANGELOG.rst file using antsibull-changelog.

**Usage:**
```bash
./update-changelog.sh
```

**What it does:**
1. Installs antsibull-changelog if not already installed
2. Initializes changelog configuration if needed
3. Processes all changelog fragments in `changelogs/fragments/`
4. Updates CHANGELOG.rst with the new release information
5. Updates changelogs/changelog.yaml with release metadata

**Note:** This script reads the version from galaxy.yml, so ensure that file is updated before running this script.
