import os
from main import main
from unittest import mock

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE364/prelabs-moffatw",
    "INPUT_BEFORE": '2022-04-01T17:36:16.537880',
    })
def test_ece364sp22prelabs():
    main()