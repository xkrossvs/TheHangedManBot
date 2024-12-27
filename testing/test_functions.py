import pytest
from utils.units import ProgressBarInfo, get_progress_bar_info


@pytest.mark.parametrize(
    "completed, total, bar",
    [
        (0, 12, ProgressBarInfo(0, 10, 0)),
        (1, 12, ProgressBarInfo(0, 10, 8)),
        (2, 12, ProgressBarInfo(1, 9, 17)),
        (3, 12, ProgressBarInfo(2, 8, 25)),
        (4, 12, ProgressBarInfo(3, 7, 33)),
        (6, 12, ProgressBarInfo(5, 5, 50)),
        (12, 12, ProgressBarInfo(10, 0, 100)),
    ]
)

def test_progress_bar(completed, total, bar):
    assert get_progress_bar_info(completed, total) == bar
