import os
from main import main
from unittest import mock
from pytest import raises

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE364/prelabs-moffatw",
    })
def test_basic():
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
def test_windowed_nocommit():
    # SystemExit exception must be thrown
    with raises(SystemExit) as e:
        main()