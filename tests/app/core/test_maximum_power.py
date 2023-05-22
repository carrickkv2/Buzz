from app.core.common import set_maximum_power
from app.core.common import check_if_maximum_power_is_set
from app.core.common import total_power_consumption_of_machines


def test_maximum_power():
    """
    Test that the all maximum_power functions work as expected.
    """
    set_maximum_power(100)
    assert check_if_maximum_power_is_set() is True
    assert total_power_consumption_of_machines(50) is True
    assert total_power_consumption_of_machines(150) is False
