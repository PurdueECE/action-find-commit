import os
from datetime import datetime
from dateutil import parser

from actions_toolkit import core
from github import Github

def compare_dt(first: dict, second: dict):
    dt1 = parser.parse(first['commit']['committer']['date'])
    dt2 = parser.parse(second['commit']['committer']['date'])
    return 1 if dt1 > dt2 else -1 if dt1 < dt2 else 0

def search_commits():
    g = Github(os.environ['INPUT_TOKEN'])
    repo = g.get_repo(os.environ['INPUT_REPOSITORY'])
    commits = repo.get_commits(until= parser.parse(os.environ['INPUT_BEFORE']))
    result = None; remaining = commits.totalCount; page_num = 0
    while remaining > 0:
        # get next page
        page_results = commits.get_page(page_num)
        # check each commit in page
        for commit in page_results:
            commit = commit.raw_data
            if result == None:
                result = commit
            else:
                result = commit if compare_dt(result, commit) < 0 else result
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    if result == None:
        raise Exception(f'No commit found.')
    return result['sha']

def set_default_env():
    os.environ.setdefault('INPUT_TOKEN', os.environ.get('GITHUB_TOKEN', ''))
    os.environ.setdefault('INPUT_BEFORE', datetime.utcnow().isoformat())

def main():
    try:
        set_default_env()
        core.debug(f'Running with: before = {os.environ["INPUT_BEFORE"]}')
        commit = search_commits()
        core.set_output('commit', commit)
    except Exception as e:
        core.set_failed(str(e))
        
if __name__ == "__main__":
    main()
