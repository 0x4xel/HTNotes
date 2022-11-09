from typing import List, cast, Optional

from . import htb
from .challenge import Challenge
from .errors import NotFoundException
from .machine import Machine


class Content:
    """Representation of a content fetch for a user on the platform

    Attributes:
        machines: Machines authored by the given user
        challenges: Challenges authored by the given user
        writeups: Currently not implemented; Write-ups associated with the given user
        items: A dict of all content items

    Args:
        userid: The user id
    """

    _machines: Optional[List[Machine]] = None
    _challenges: Optional[List[Challenge]] = None

    _machine_ids: List[int]
    _challenge_ids: List[int]

    _is_resolved: bool = False
    _user_id: int

    @property
    def machines(self) -> List[Machine]:
        if self._machines is None:
            self._machines = []
            for uid in self._machine_ids:
                try:
                    self._machines.append(self._client.get_machine(uid))
                except NotFoundException:
                    pass
        return self._machines

    @property
    def challenges(self) -> List[Challenge]:
        if self._challenges is None:
            self._challenges = []
            for uid in self._challenge_ids:
                try:
                    self._challenges.append(self._client.get_challenge(uid))
                except NotFoundException:
                    pass
        return self._challenges

    @property
    def items(self) -> dict:
        self._is_resolved = True
        return {"machines": self.machines, "challenges": self.challenges}

    def __len__(self):
        return len(self._machine_ids) + len(self._challenge_ids)

    def __repr__(self):
        return f"<Content '{self._user_id}': {len(self._machine_ids)} machines; {len(self._challenge_ids)} challenges>"

    def __str__(self):
        return repr(self)

    def __init__(self, userid: int, client: htb.HTBClient):
        self._user_id = userid
        self._client = client
        data = cast(dict, self._client.do_request(f"user/profile/content/{userid}"))[
            "profile"
        ]["content"]
        self._machine_ids = [x["id"] for x in data.get("machines", [])]
        self._challenge_ids = [x["id"] for x in data.get("challenges", [])]
