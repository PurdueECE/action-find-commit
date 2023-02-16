import json
import os
from datetime import datetime, timezone

from actions_toolkit import core
from dateutil import parser
from github import Github, GithubObject
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.Tag import Tag


def compare_dt(first: dict, second: dict):
    dt1 = parser.parse(first['commit']['committer']['date'])
    dt2 = parser.parse(second['commit']['committer']['date'])
    return 1 if dt1 > dt2 else -1 if dt1 < dt2 else 0


def search_bycommit(repo: Repository, args: dict):
    commits = repo.get_commits(sha=args[
        'INPUT_SHA'] or GithubObject.NotSet, since=args['INPUT_AFTER'], until=args['INPUT_BEFORE'])
    result = None
    remaining = commits.totalCount
    page_num = 0
    while remaining > 0:
        # get next page
        page_results = commits.get_page(page_num)
        for commit in page_results:
            commit = commit.raw_data
            if result == None or compare_dt(result, commit) < 0:
                result = commit
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    return result


def search_bytag(repo: Repository, args: dict):
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
            matches.append(tag.name == args['INPUT_TAG'])
            # time window filter
            timestamp = parser.parse(tag.commit.last_modified)
            matches.append(args['INPUT_AFTER'] <=
                           timestamp <= args['INPUT_BEFORE'])
            # most recent filter
            matches.append(result == None or compare_dt(result, commit) < 0)
            # check filters
            result = commit if all(matches) else result
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    return result


def search(args):
    repo = Github(args['INPUT_TOKEN']).get_repo(args['INPUT_REPOSITORY'])
    if args['INPUT_TAG']:
        result = search_bytag(repo, args)
    else:
        result = search_bycommit(repo, args)
    if result == None:
        raise Exception(f'No commit found.')
    return result['sha']


def setup():
    if os.environ.get('INPUT_SHA') and os.environ.get('INPUT_TAG'):
        raise Exception('Cannot filter by tag and by SHA')
    return {
        'INPUT_TOKEN': os.environ.get('INPUT_TOKEN'),
        'INPUT_REPOSITORY': os.environ['INPUT_REPOSITORY'],
        'INPUT_SHA': os.environ.get('INPUT_SHA'),
        'INPUT_TAG': os.environ.get('INPUT_TAG'),
        'INPUT_AFTER': parser.parse(
            os.environ.get('INPUT_AFTER', datetime(1970, 1, 1).replace(tzinfo=timezone.utc).isoformat())),
        'INPUT_BEFORE': parser.parse(
            os.environ.get('INPUT_BEFORE', datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()))
    }


def main():
    try:
        args = setup()
        core.debug('args: {0}'.format(
            json.dump({**args, 'INPUT_TOKEN': '***'})))
        commit = search(args)
        core.set_output('commit', commit)
        core.export_variable('OUTPUT_COMMIT', commit)
    except Exception as e:
        core.set_failed(e)


if __name__ == "__main__":
    main()
