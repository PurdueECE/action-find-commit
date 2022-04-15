import os
from main import main
from unittest import mock

@mock.patch.dict(os.environ, {
    "INPUT_REPOSITORY": "PurdueECE364/prelabs-moffatw",
    "INPUT_BEFORE": '04/10/2022 00:00:00',
    })
def test_ece364sp22prelabs():
    main()