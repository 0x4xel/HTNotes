from typing import List, cast, Optional

from . import htb
from .user import User
from .errors import IncorrectFlagException


class Endgame(htb.HTBObject):
    """The class representing Hack The Box endgames

    Attributes:
        name: The name of the Endgame
        avatar: The relative URL of the Endgame's avatar
        cover_image: The relative URL of the Endgame's cover image
        retired: Whether the Endgame is retired
        vip: Whether the Endgame requires VIP
        points: The points awarded by the Endgame
        completions: The number of players who have completed the Endgame
        reset_votes: The number of votes to reset the Endgame
        entry_points: IP addresses the Endgame can be contacted on
        description: The HTML description of the Endgame

    """

    name: str
    avatar: str
    cover_image: str
    retired: bool
    vip: bool

    _detailed_attributes = (
        "points",
        "completions",
        "reset_votes",
        "entry_points",
        "description",
    )
    points: int
    completions: int
    reset_votes: int
    entry_points: List[str]
    description: str

    _authors: Optional[List[User]] = None
    _author_ids: Optional[List[int]] = None

    def submit(self, flag: str):
        """Submits a flag for an Endgame

        Args:
            flag: The flag for the Endgame

        """
        submission = cast(
            dict,
            self._client.do_request(
                f"endgame/{self.id}/flag",
                json_data={
                    "flag": flag,
                },
            ),
        )
        if submission["message"] == "Wrong flag":
            raise IncorrectFlagException
        return True

    @property
    def authors(self):
        """
        The creators of the Endgame
        Returns: A list of Users

        """
        if self._authors is None:
            self._authors = []
            for user_id in self._author_ids:
                self._authors.append(self._client.get_user(user_id))
        return self._authors

    def __repr__(self):
        return f"<Endgame '{self.name}'>"

    def __init__(self, data: dict, client: htb.HTBClient, summary=False):
        self._client = client
        self._detailed_func = client.get_endgame  # type: ignore
        self.id = data["id"]
        self.name = data["name"]
        self.avatar = data["avatar_url"]
        self.cover_image = data["cover_image_url"]
        self.retired = data["retired"]
        self._author_ids = []
        self.vip = data["vip"]
        for user in data["creators"]:
            self._author_ids.append(user["id"])
        if not summary:
            self.points = int(data["points"])
            self.entry_points = data["entry_points"]
            self.completions = data["players_completed"]
            self.reset_votes = data["endgame_reset_votes"]
            self.description = data["description"]
        else:
            self._is_summary = True
