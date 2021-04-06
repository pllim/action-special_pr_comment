# GitHub Action to comment on special day(s)

Comment on issues and pull requests opened on special day(s).
Create a `.github/workflows/special_comment.yml` with this:

```
name: Special comment

on:
  issues:
    types: [opened]
  pull_request_target:
    types: [opened]

jobs:
  special_comment:
    name: Comment if today is special
    runs-on: ubuntu-latest
    steps:
    - name: Special comment
      uses: pllim/action-special_pr_comment@main
      with:
        SPECIAL_DAYS: 04-01,12-23
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

`SPECIAL_DAYS` must contain a comma-separate list of dates in the format of
`MM-DD`. If it is not provided, a built-in default is used.


## Dev notes

```
npm install
npm run build
```