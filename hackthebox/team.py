from . import htb

from typing import TYPE_CHECKING, cast, Optional

if TYPE_CHECKING:
    from .user import User


class Team(htb.HTBObject):
    """The class representing Hack The Box teams

    Attributes:
        name: The name of the Team
        points: The Team's total points
        motto: The Team motto
        description: The Team description
        country_name: The name of the country the Team is based in
        avatar_url: The relative URL of the Tean's avatar
        twitter: The Team's Twitter account
        facebook: The Team's Facebook account
        discord: The Team's Discord
        public: Whether the Team is publicly visible
        can_delete_avatar: Whether the active User can delete the avatar
        is_respected: Whether the active User has respected the Team
        join_request_sent: Whether the active User has sent a request to join the Team

    """

    name: str

    _detailed_attributes = (
        "points",
        "motto",
        "description",
        "country_name",
        "avatar_url",
        "cover_image_url",
        "twitter",
        "facebook",
        "discord",
        "public",
        "can_delete_avatar",
        "captain",
        "is_respected",
        "join_request_sent",
    )
    points: int
    motto: str
    description: str
    country_name: str
    avatar_url: str
    cover_image_url: str
    twitter: str
    facebook: str
    discord: str
    public: bool
    can_delete_avatar: bool
    # noinspection PyUnresolvedReferences
    _captain: Optional["User"] = None
    is_respected: Optional[bool] = None
    join_request_sent: Optional[bool] = None
    _ranking: Optional[int] = None
    _captain_id: int

    def __repr__(self):
        return f"<Team '{self.name}'>"

    def __init__(self, data: dict, client: htb.HTBClient, summary: bool = False):
        self._client = client
        self._detailed_func = client.get_team  # type: ignore
        self.id = data["id"]
        self.name = data["name"]
        if not summary:
            self.points = data["points"]
            self.motto = data["motto"]
            self.description = data["description"]
            self.country_name = data["country_name"]
            self.avatar_url = data["avatar_url"]
            self.cover_image_url = data["cover_image_url"]
            self.twitter = data["twitter"]
            self.facebook = data["facebook"]
            self.discord = data["facebook"]
            self.public = data["public"]
            self.can_delete_avatar = data["can_delete_avatar"]
            self._captain_id = data["captain"]["id"]
            self.is_respected = data["is_respected"]
            self.join_request_sent = data["join_request_sent"]
        else:
            self._is_summary = True

    @property
    def ranking(self) -> int:
        """Retrieve the global ranking of the team

        Returns:

        """
        if not self._ranking:
            data = cast(dict, self._client.do_request(f"team/stats/owns/{self.id}"))
            self._ranking = data["rank"]
        return cast(int, self._ranking)

    # noinspection PyUnresolvedReferences
    @property
    def captain(self) -> "User":
        from .user import User

        if not self._captain:
            self._captain = self._client.get_user(self._captain_id)
        return cast(User, self._captain)
