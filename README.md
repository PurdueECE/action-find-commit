# Find Commit Action

This aciton will search a repo for a commit that matches a set of filters.

# Usage
```yaml
- uses: PurdueECE/action-find-commit@main
  id: get_commit
  with:
    # Repository name with owner. Defaults to ${{ github.repository }}
    repository: 'PurdueECE/action-find-commit'
    # Personal access token. Defaults to ${{ github.token }}
    token: ${{ github.token }}
    # Find commit closest to but before a timestamp (ISO 8601 format). Defaults to current time.
    before: '2022-04-01T23:59:00'
# Print the resulting SHA that was found.
- run: "echo results: ${{ steps.get_commit.outputs.commit }}"
```

# Testing
Unit tests are in the `test-unit/` directory. They can be run with `pytest`.