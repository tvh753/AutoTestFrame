import pytest

from commons.case_util import get_case_list
from commons.main_util import stand_case_flow


@pytest.mark.parametrize('case_info', get_case_list(), ids=lambda obj: obj.name)
def test_api(case_info):

    stand_case_flow(case_info)
