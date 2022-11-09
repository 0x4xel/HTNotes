from . import htb
from datetime import datetime

from typing import Optional, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .htb import HTBClient, HTBObject
    from .machine import Machine


class Solve:
    """Representation of completion of Hack The Box content

    Attributes:
        id: The ID of the solved item
        name: The name of the solved item
        date: The date of the solve
        blood: Whether the solve was a first blood
        points: The points awarded from the solve
        item (HTBObject): The solved item

    """

    _client: "HTBClient"
    _item: Optional["HTBObject"] = None  # The solved item
    id: int
    name: str
    date: datetime
    blood: bool
    points: int

    def __init__(self, data: dict, client: "HTBClient"):
        self._client = client
        self.date = data["date"]
        self.blood = data["first_blood"]
        self.id = data["id"]
        self.name = data["name"]


class MachineSolve(Solve):
    """Representation of solving a Machine"""

    type: str  # User/Root

    def __repr__(self):
        return f"<Solve {self.type}@{self.name}>"

    @property
    def item(self):
        return self.machine

    # noinspection PyUnresolvedReferences
    @property
    def machine(self) -> "Machine":
        """The solved Machine"""
        from .machine import Machine

        if not self._item:
            self._item = self._client.get_machine(self.id)
        return cast(Machine, self._item)

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.type = data["type"]


class ChallengeSolve(Solve):
    """Representation of solving a Challenge"""

    category: str

    def __repr__(self):
        return f"<Solve {self.name}@{self.category}>"

    @property
    def item(self):
        return self.challenge

    @property
    def challenge(self):
        """The solved Challenge"""
        if not self._item:
            self._item = self._client.get_challenge(self.id)
        return self._item

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.category = data["challenge_category"]


class EndgameSolve(Solve):
    """Representation of solving a Endgame"""

    flag_name: str

    def __repr__(self):
        return f"<Solve {self.flag_name}@{self.name}>"

    @property
    def item(self):
        return self.endgame

    @property
    def endgame(self):
        """The solved Endgame"""
        if not self._item:
            self._item = self._client.get_endgame(self.id)
        return self._item

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.flag_name = data["flag_title"]


class FortressSolve(Solve):
    """Representation of solving a Fortress"""

    flag_name: str

    def __repr__(self):
        return f"<Solve {self.flag_name}@{self.name}>"

    @property
    def item(self):
        return self.fortress

    @property
    def fortress(self):
        """The solved Fortress"""
        if not self._item:
            self._item = self._client.get_fortress(self.id)
        return self._item

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.flag_name = data["flag_title"]
