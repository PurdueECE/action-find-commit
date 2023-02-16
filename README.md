# Find Commit Action
This aciton will search a repo for a commit that matches a set of filters.

# Usage
## Basic
```yaml
- uses: PurdueECE/action-find-commit@v1
  id: get_commit
  with:
    # Repository name with owner. Defaults to ${{ github.repository }}
    repository: 'PurdueECE/action-find-commit'
    # Personal access token. Defaults to ${{ github.token }}
    token: ${{ github.token }}
# Print the resulting SHA that was found.
- run: "echo results: ${{ steps.get_commit.outputs.commit }}"
# Checkout repo at found commit
- uses: actions/checkout@v3
  with:
    repository: 'PurdueECE/action-find-commit'
    ref: '${{ steps.get_commit.outputs.commit }}'
```
## Time Windowed
```yaml
- uses: PurdueECE/action-find-commit@v1
  with:
    # Repository name with owner. Defaults to ${{ github.repository }}
    repository: 'PurdueECE/action-find-commit'
    # Find commits after a timestamp (ISO 8601 format).
    after: '2022-03-01T23:59:00'
    # Find commit closest to but before a timestamp (ISO 8601 format). Defaults to current time.
    before: '2022-04-01T23:59:00'
    # SHA or branch to start searching commits from. Defaults to the repository's default branch. Cannot be used with tag
    sha: 'main'
```
## Tagged
```yaml
- uses: PurdueECE/action-find-commit@v1
  with:
    # Repository name with owner. Defaults to ${{ github.repository }}
    repository: 'PurdueECE/action-find-commit'
    # SHA or branch to start searching commits from. Defaults to the repository's default branch.
    sha: 'main'
    # Commit tag to search for. Cannot be used with sha
    tag: "v1"
```

# Testing
Unit tests are in the `test-unit/` directory. They can be run with `pytest`.