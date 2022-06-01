import os
from datetime import datetime
from dateutil import parser

from actions_toolkit import core
from github import Github, GithubObject, Tag
from github.Repository import Repository

def compare_dt(first: dict, second: dict):
    dt1 = parser.parse(first['commit']['committer']['date'])
    dt2 = parser.parse(second['commit']['committer']['date'])
    return 1 if dt1 > dt2 else -1 if dt1 < dt2 else 0

def search_bycommit(repo: Repository):
    commits = repo.get_commits(sha=os.getenv('INPUT_SHA') or GithubObject.NotSet, since=parser.parse(os.environ['INPUT_AFTER']), until=parser.parse(os.environ['INPUT_BEFORE']))
    result = None; remaining = commits.totalCount; page_num = 0
    while remaining > 0:
        # get next page
        page_results = commits.get_page(page_num)
        for commit in page_results:
            commit = commit.raw_data
            result = commit if result == None or compare_dt(result, commit) < 0 else result
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    return result['sha']

def search_bytag(repo: Repository):
    tags = repo.get_tags()
    result = None; remaining = tags.totalCount; page_num = 0
    while remaining > 0:
        # get next page
        page_results = tags.get_page(page_num)
        for tag in page_results:
            commit = tag.commit.raw_data
            # filters
            matches = []
            ## tag filter
            matches.append(tag.name == os.environ['INPUT_TAG'])
            ## time window filter
            matches.append(result == None or compare_dt(result, commit) < 0)
            if all(matches):
                result = commit
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    return result['sha']

def search():
    g = Github(os.environ['INPUT_TOKEN'])
    repo = g.get_repo(os.environ['INPUT_REPOSITORY'])
    result = search_bytag(repo) if 'INPUT_TAG' in os.environ else search_bycommit(repo)
    if result == None:
        raise Exception(f'No commit found.')
    return result

def setup():
    os.environ['INPUT_AFTER'] = os.getenv('INPUT_AFTER') or datetime.min.isoformat()
    os.environ['INPUT_BEFORE'] = os.getenv('INPUT_BEFORE') or datetime.utcnow().isoformat()
    if os.getenv('INPUT_SHA') and os.getenv('INPUT_TAG'):
        raise Exception('Cannot filter by tag and by SHA')

def main():
    try:
        setup()
        core.debug(f'Running with: after = {os.environ["INPUT_AFTER"]}, before = {os.environ["INPUT_BEFORE"]}')
        commit = search()
        core.set_output('commit', commit)
    except Exception as e:
        core.set_failed(str(e))
        
if __name__ == "__main__":
    main()
