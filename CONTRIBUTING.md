# Contributing guide

To contribute please use pull requests.

This collection works only with supported Ansible versions mentioned in [requirements file](requirements.txt).

Automated tests will be run against all PRs, these tests need to pass in order to have them reviewed.

## Tooling

You can use Pyenv to setup a working Python environment with the needed packages.

```text
pyenv install 3.10.6
pyenv virtualenv 3.10.6 beegfs-ansible
pyenv activate beegfs-ansible
pip install --upgrade pip
pip install -r requirements.txt
pre-commit install -c .pre-commit-config.yaml
```

After the first time it should pick up the virtual environment automatically by entering the directory and detecting the `.python-version` file.
For VSCode make sure to "Set the Python Interpreter" to the Pyenv virtualenv from the command palette `CTRL + SHIFT + P`

## Workflow

1. Create a new feature branch:

    ```text
    git checkout main
    git pull --rebase
    git checkout -b <myuser>/<mybranch>
    ```

2. Make your changes and create the PR.
3. Wait for the GitHub workflows to complete successfully.

## Creating a new role

Follow the instructions available in the [Molecule documentation](https://ansible.readthedocs.io/projects/molecule/getting-started/).

NOTE: if adding new roles make sure to write the necessary [Molecule tests](extensions/molecule)

## Handling changes on default branch

If you need to get the latest changes from the `main` branch, you need to rebase and workout the merge conflicts:

```text
git checkout main
git pull --rebase
git checkout <customer_branch>  # OR from the correct worktree path
git rebase main
git push --force
```

WARNING: always use `git pull` with `--rebase` to avoid bad surprises.

## Commits

Guidelines can be found in the [Conventional Commits specification](https://www.conventionalcommits.org/).

## Releases

This project uses [antsibull-changelog](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_changelogs.html#generating-changelogs) to generate changelogs and has an automated release process via GitHub Actions.

### Automated Release Process

Releases are automatically created when you push a version tag to the repository. The automation handles changelog generation, building, and publishing to Ansible Galaxy.

#### Creating a Release

1. **Update the version** in [galaxy.yml](galaxy.yml):

   ```bash
   # Edit galaxy.yml and update the version field
   version: 2.2.0
   ```

2. **Create changelog fragments** for your changes in the [changelogs/fragments/](changelogs/fragments/) directory:

   **Option A - Using the helper script (recommended):**

   ```bash
   ./.github/scripts/create-release-fragment.sh 2.2.0 "Description of this release"
   ```

   This automatically creates the fragment with the correct date.

   **Option B - Manual creation:**

   Create a `release_summary` fragment (e.g., `2.2.0.yml`):

   ```yaml
   release_summary: |
      | Release Date: YYYY-MM-DD
      | Description of this release
   ```

   **Note**: Replace `YYYY-MM-DD` with the actual release date (e.g., `2025-12-21`).

   For new features, create additional fragments with appropriate keywords:

   ```yaml
   add object.playbook:
   - name: site.yml
     description: |
       Execute all the playbooks in `playbooks/` directory in the correct order to deploy a Beegfs cluster.
   ```

   See [antsibull-changelog documentation](https://github.com/ansible-community/antsibull-changelog/blob/main/docs/changelogs.md) for all available fragment types (`bugfixes`, `major_changes`, `minor_changes`, `breaking_changes`, etc.).

3. **Generate the CHANGELOG.rst** file:

   ```bash
   uv pip install ansible-core antsibull-changelog
   antsibull-changelog release
   ```

   Note: The project uses `uv` for fast package installation. If you don't have `uv` installed, you can install it with:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   This will:
   - Update `CHANGELOG.rst` with the new version
   - Process all fragments in `changelogs/fragments/`
   - Update `changelogs/changelog.yaml`
   - Remove the processed fragments

   Review the updated `CHANGELOG.rst` to ensure it looks correct.

4. **Commit and push your changes** to the main branch via a pull request:

   ```bash
   git checkout -b release-2.2.0
   git add galaxy.yml CHANGELOG.rst changelogs/
   git commit -m "chore: prepare release 2.2.0"
   git push origin release-2.2.0
   ```

   Create a pull request, get it reviewed and merged to main.

5. **Create and push a version tag** from the main branch:

   ```bash
   git checkout main
   git pull
   git tag v2.2.0
   git push origin v2.2.0
   ```

   **Important**: The tag must:
   - Start with `v` (e.g., `v2.2.0`)
   - Follow semantic versioning format `X.X.X`
   - Match the version in `galaxy.yml` exactly

6. **The automation will**:
   - Validate that the tag version matches the version in `galaxy.yml`
   - Verify that `CHANGELOG.rst` has been updated
   - Build the Ansible collection tarball
   - Publish the collection to [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/e4_computer_engineering/beegfs/)
   - Build and publish documentation to GitHub Pages
   - Create a GitHub Release with the collection tarball and changelog

7. **Monitor the release** by checking the [GitHub Actions workflow](../../actions/workflows/Release.yml)

### Manual Changelog Generation (for testing)

If you want to preview changelog changes locally before creating a release:

```bash
uv pip install ansible-core antsibull-changelog
antsibull-changelog release --version X.X.X
```

**Note**: When creating roles, be sure to include the `argument_specs.yml` file in the `meta` folder like the existing roles, as this is used for documentation generation.

### Requirements

The automated release process requires the following GitHub secret to be configured:

- **GALAXY_TOKEN**: An Ansible Galaxy API token with permissions to publish the collection. This can be obtained from your [Ansible Galaxy profile](https://galaxy.ansible.com/me/preferences).

## Documentation

Documentation is automatically generated and published by the [Release.yml GitHub action](.github/workflows/Release.yml) when a version tag (v*) is pushed as part of the release process.

The workflow uses the [GitHub Docs Build project](https://github.com/ansible-community/github-docs-build) from the Ansible community. The documentation artifact is pushed to the `gh-pages` branch that feeds the GitHub Pages site at <https://e4-computer-engineering.github.io/beegfs-ansible/>.

**Note**: Documentation is only rebuilt on releases. If you need to update documentation outside of a release, you can manually trigger the workflow from the GitHub Actions tab.
