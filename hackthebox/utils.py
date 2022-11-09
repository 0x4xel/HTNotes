import re
from datetime import timedelta


def parse_delta(time: str) -> timedelta:
    """Generates a timedelta from a string

    Args:
        time: The delta as a string

    Returns:
        A datetime.timedelta object

    """
    regex = re.compile(
        r"((?P<years>\d+?)[Yy])? ?((?P<months>\d+?)M)? ?"
        r"((?P<weeks>\d+?)[Ww])? ?"
        r"((?P<days>\d+?)[Dd])? ?((?P<hours>\d+?)[Hh])? ?"
        r"((?P<minutes>\d+?)m)? ?((?P<seconds>\d+?)[Ss])?"
    )
    parts = regex.match(time)
    if not parts or parts.group() == "":
        raise ValueError
    parts_dict = parts.groupdict()
    time_params = {
        "years": 0,
        "months": 0,
        "weeks": 0,
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
    }
    for (name, param) in parts_dict.items():
        if param:
            time_params[name] = int(param)
    # Remove unsupported params for timedelta
    time_params["days"] += time_params["years"] * 365
    del time_params["years"]
    time_params["days"] += time_params["months"] * 30
    del time_params["months"]
    return timedelta(**time_params)
