from .task import Task


test_cases = [
    # Block is for the weekend and current date set on a Monday
    {
        "settings": {"block_times": ["* * * * 6,0"]},
        "current_time": (2021, 2, 22, 14, 6),
        "expected": True,
    },
    # Block is for the weekend and current date set on a Sunday
    {
        "settings": {"block_times": ["* * * * 6,0"]},
        "current_time": (2021, 2, 21, 14, 6),
        "expected": False,
    },
    # Block is for the weekend and between 5pm - 8am on Weekdays
    #  and current date set on a Thursday at 2pm
    {
        "settings": {
            "block_times": ["* * * * 6,0", "* 17-23 * * 1-5", "* 0-8 * * 1-5"]
        },
        "current_time": (2021, 2, 25, 14, 6),
        "expected": True,
    },
    # Block is for the weekend and between 5pm - 8am on Weekdays
    # and current date set on a Thursday at 10pm
    {
        "settings": {
            "block_times": ["* * * * 6,0", "* 17-23 * * 1-5", "* 0-8 * * 1-5"]
        },
        "current_time": (2021, 2, 23, 22, 6),
        "expected": False,
    },
]


def test():
    task = Task()
    for test_case in test_cases:
        settings = test_case["settings"]

        assert (
            task.execute({}, settings, test_case["current_time"])
            is test_case["expected"]
        )
