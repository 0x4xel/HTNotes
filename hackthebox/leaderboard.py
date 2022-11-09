from typing import List, Iterator

from . import htb
from .team import Team
from .user import User


class Leaderboard(htb.HTBObject):
    """The class representing a Leaderboard

    Args:
        data: A list of Leaderboard entries
        leaderboard_type: The Type of entries in the Leaderboard

    """

    _type: type
    _items: List[htb.HTBObject]
    _iter: Iterator[None]

    def __getitem__(self, key):
        return self._items[key]

    def __iter__(self):
        # noinspection PyTypeChecker
        self._iter = iter(self._items)
        return self

    def __next__(self):
        return next(self._iter)

    def __len__(self):
        return len(self._items)

    def __init__(self, data: List[dict], client: htb.HTBClient, leaderboard_type: type):
        self._type = leaderboard_type
        self._client = client
        if leaderboard_type == User:
            self._items = [User(usr, client, summary=True) for usr in data]
        elif leaderboard_type == Team:
            self._items = [Team(team, client, summary=True) for team in data]
        elif leaderboard_type == Country:
            self._items = [Country(country) for country in data]
        elif leaderboard_type == University:
            self._items = [University(university) for university in data]


class Country(htb.HTBObject):
    """The class representing a Country

    Attributes:
        rank: The Country's global rank
        country_code: The Country's country code
        members: The number of members from the Country
        points: The Country's total points
        user_owns: The Country's total user owns
        root_owns: The Country's total root owns
        challenge_owns: The Country's total challenge owns
        user_bloods: The Country's total user bloods
        root_bloods: The Country's total root bloods
        fortress: The Country's total Fortress flags
        endgame: The Country's total Endgame flags
        name: The name of the Country
    Args:
        data: The data of the country

    """

    # TODO: Move this into its own file, maybe `misc.py`?

    rank: int
    country_code: str
    members: int
    points: int
    user_owns: int
    root_owns: int
    challenge_owns: int
    user_bloods: int
    root_bloods: int
    fortress: int
    endgame: int
    name: str

    def __init__(self, data: dict):
        self.rank = data["rank"]
        self.country_code = data["country"]
        self.members = data["members"]
        self.points = data["points"]
        self.user_owns = data["user_owns"]
        self.root_owns = data["root_owns"]
        self.challenge_owns = data["challenge_owns"]
        self.user_bloods = data["user_bloods"]
        self.root_owns = data["root_bloods"]
        self.fortress = data["fortress"]
        self.endgame = data["endgame"]
        self.name = data["name"]


class University(htb.HTBObject):
    """The class representing a University

    Attributes:
        rank: The University's global rank
        students: The number of students from the University
        points: The University's total points
        user_owns: The University's total user owns
        root_owns: The University's total root owns
        challenge_owns: The University's total challenge owns
        user_bloods: The University's total user bloods
        root_bloods: The University's total root bloods
        fortress: The University's total Fortress flags
        endgame: The University's total Endgame flags
        name: The name of the University
    Args:
        data: The data of the University

    """

    rank: int
    students: int
    points: int
    user_owns: int
    root_owns: int
    challenge_owns: int
    user_bloods: int
    root_bloods: int
    fortress: int
    endgame: int
    name: str

    def __init__(self, data: dict):
        self.rank = data["rank"]
        self.students = data["students"]
        self.points = data["points"]
        self.user_owns = data["user_owns"]
        self.root_owns = data["root_owns"]
        self.challenge_owns = data["challenge_owns"]
        self.user_bloods = data["user_bloods"]
        self.root_owns = data["root_bloods"]
        self.fortress = data["fortress"]
        self.endgame = data["endgame"]
        self.name = data["name"]
