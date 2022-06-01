import os
from main import main
from unittest import mock
from pytest import raises

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    })
def test_basic():
    main()

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE364/prelabs-DOESNOTEXIST",
    })
def test_basic_fail():
    with raises(SystemExit) as e:
        main()

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE364/prelabs-moffatw",
    "INPUT_AFTER": '2022-03-27T11:59:59-04:00',
    "INPUT_BEFORE": '2022-04-01T11:59:59-04:00',
    })
def test_windowed():
    main()

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE364/prelabs-moffatw",
    "INPUT_AFTER": '2022-03-28T11:59:59-04:00',
    "INPUT_BEFORE": '2022-04-01T11:59:59-04:00',
    })
def test_windowed_fail():
    with raises(SystemExit) as e:
        main()

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_TAG": "v1",
    })
def test_tagged():
    main()

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_TAG": "v0",
    })
def test_tagged_fail():
    with raises(SystemExit) as e:
        main()

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_SHA": "main",
    "INPUT_TAG": "v1",
    })
def test_sha_tagged_fail():
    with raises(SystemExit) as e:
        main()