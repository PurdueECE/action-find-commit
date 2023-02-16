import os
from datetime import datetime, timezone
from dateutil import parser

from actions_toolkit import core
from github import Github, GithubObject
from github.Repository import Repository
from github.PaginatedList import PaginatedList
from github.Tag import Tag


def compare_dt(first: dict, second: dict):
    dt1 = parser.parse(first['commit']['committer']['date'])
    dt2 = parser.parse(second['commit']['committer']['date'])
    return 1 if dt1 > dt2 else -1 if dt1 < dt2 else 0


def search_bycommit(repo: Repository):
    commits = repo.get_commits(sha=os.getenv('INPUT_SHA') or GithubObject.NotSet, since=parser.parse(
        os.environ['INPUT_AFTER']), until=parser.parse(os.environ['INPUT_BEFORE']))
    result = None
    remaining = commits.totalCount
    page_num = 0
    while remaining > 0:
        # get next page
        page_results = commits.get_page(page_num)
        for commit in page_results:
            commit = commit.raw_data
            result = commit if result == None or compare_dt(
                result, commit) < 0 else result
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    return result


def search_bytag(repo: Repository):
    after = parser.parse(os.environ['INPUT_AFTER'])
    before = parser.parse(os.environ['INPUT_BEFORE'])
    tags: PaginatedList[Tag] = repo.get_tags()
    result = None
    remaining = tags.totalCount
    page_num = 0
    while remaining > 0:
        # get next page
        page_results = tags.get_page(page_num)
        for tag in page_results:
            tag: Tag = tag
            commit = tag.commit.raw_data
            # filters
            matches = []
            # tag filter
            matches.append(tag.name == os.environ['INPUT_TAG'])
            # time window filter
            timestamp = parser.parse(tag.commit.last_modified)
            matches.append(after <= timestamp <= before)
            # most recent filter
            matches.append(result == None or compare_dt(result, commit) < 0)
            # check filters
            result = commit if all(matches) else result
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    return result


def search():
    g = Github(os.getenv('INPUT_TOKEN'))
    repo = g.get_repo(os.environ['INPUT_REPOSITORY'])
    result = search_bytag(
        repo) if 'INPUT_TAG' in os.environ else search_bycommit(repo)
    if result == None:
        raise Exception(f'No commit found.')
    return result['sha']


def setup():
    os.environ.setdefault(
        'INPUT_AFTER', datetime(1970, 1, 1).replace(tzinfo=timezone.utc).isoformat())
    os.environ.setdefault(
        'INPUT_BEFORE', datetime.utcnow().replace(tzinfo=timezone.utc).isoformat())
    if os.getenv('INPUT_SHA') and os.getenv('INPUT_TAG'):
        raise Exception('Cannot filter by tag and by SHA')


def main():
    try:
        setup()
        core.debug(
            f'Running with: after = {os.environ["INPUT_AFTER"]}, before = {os.environ["INPUT_BEFORE"]}')
        commit = search()
        core.set_output('commit', commit)
        core.export_variable('OUTPUT_COMMIT', commit)
    except Exception as e:
        core.set_failed(e)


if __name__ == "__main__":
    main()
