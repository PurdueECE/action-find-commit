import os
from main import main
from unittest import mock
from pytest import raises
from actions_toolkit import core


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
})
def test_basic():
    main()


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/nonexistent-repo",
})
def test_basic_fail():
    with raises(SystemExit) as e:
        main()


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_AFTER": '2022/03/28 23:59:59 GMT',
    "INPUT_BEFORE": 'Wed, 27 Apr 2022 01:54:37 GMT',
})
def test_bad_timestamp():
    main()


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_BEFORE": '2022-04-27T23:59:59-04:00',
})
def test_before():
    main()
    assert os.environ['OUTPUT_COMMIT'] == '61d8b4ee576df170757e2863c565a274699af2a9'


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_AFTER": '2022-04-25T23:59:59-04:00',
    "INPUT_BEFORE": '2022-04-27T23:59:59-04:00',
})
def test_windowed():
    main()
    assert os.environ['OUTPUT_COMMIT'] == '61d8b4ee576df170757e2863c565a274699af2a9'


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_AFTER": '2022-03-28T23:59:59-04:00',
    "INPUT_BEFORE": '2022-04-14T23:59:59-04:00',
})
def test_windowed_nocommit_fail():
    with raises(SystemExit) as e:
        main()


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_AFTER": '2022-04-02T23:59:59-04:00',
    "INPUT_BEFORE": '2022-04-01T23:59:59-04:00',
})
def test_windowed_invalid_fail():
    with raises(SystemExit) as e:
        main()


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_TAG": "v1",
})
def test_tagged():
    main()
    assert os.environ['OUTPUT_COMMIT'] == '61d8b4ee576df170757e2863c565a274699af2a9'


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_TAG": "v1",
    "INPUT_AFTER": "2022-04-27T01:54:35-00:00",
    "INPUT_BEFORE": "2022-04-27T01:54:37-00:00",
})
def test_tagged_timewindow():
    main()
    assert os.environ['OUTPUT_COMMIT'] == '61d8b4ee576df170757e2863c565a274699af2a9'


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_TAG": "v1",
    "INPUT_AFTER": "2022-04-27T01:54:37-00:00",
})
def test_tagged_timewindow_notfound():
    with raises(SystemExit) as e:
        main()


@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE/action-find-commit",
    "INPUT_TAG": "v0",
})
def test_tagged_notag():
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
