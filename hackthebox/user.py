from typing import List, Optional, TYPE_CHECKING

from hackthebox.content import Content

from . import htb
from .solve import MachineSolve, ChallengeSolve, EndgameSolve, FortressSolve, Solve


if TYPE_CHECKING:
    from .htb import HTBClient
    from .team import Team


class User(htb.HTBObject):
    """The class representing Hack The Box Users

    Attributes:
        name: The username of the User
        avatar: The relative URL of the User's avatar
        ranking: The User's position on the Hall of Fame
        points: The User's current total points
        user_owns: The User's total Machine user owns
        root_owns: The User's total Machine root owns
        user_bloods: The User's total Machine user bloods
        root_bloods: The User's total Machine root bloods
        rank_name: The name of the User's current rank
        country_name: The name of the User's country
        team: The User's Team
        public: Whether the User's profile is publicly visible

        timezone: The User's timezone
        vip: Whether the User is VIP
        vip_plus: Whether the user is VIP+
        respects: The number of respects the User has
        university: The User's University
        university_name: The User's university's name
        description: The User's description
        github: The User's Github profile
        linkedin: The User's LinkedIn profile
        twitter: The User's Twitter account
        website: The User's website
        respected: Whether the active User respects the User
        followed: Whether the active User follows the User
        rank_id: The ID of the User's rank
        rank_progress: The User's progress to the next rank
        next_rank: The next rank the User will reach
        next_rank_points: The points required to reach the next rank
        rank_requirement: The ownership required for the current Rank

    """

    name: str
    avatar: str
    ranking: int
    points: int
    root_owns: int
    user_owns: int
    root_bloods: int
    user_bloods: int
    rank_name: str

    _detailed_attributes = (
        "timezone",
        "vip",
        "vip_plus",
        "respects",
        "university",
        "university_name",
        "description",
        "github",
        "linkedin",
        "twitter",
        "website",
        "respected",
        "followed",
        "rank_id",
        "rank_progress",
        "next_rank",
        "next_rank_points",
        "rank_ownership",
        "rank_requirement",
        "country_name",
        "team",
        "public",
    )
    timezone: str
    vip: bool
    vip_plus: bool
    respects: int
    # TODO: University object
    university = None
    university_name: str
    description: str
    github: str
    linkedin: str
    twitter: str
    website: str
    respected: bool
    followed: bool
    rank_id: int
    rank_progress: int
    next_rank: str
    next_rank_points: int
    rank_ownership: float
    rank_requirement: int
    country_name: str
    # noinspection PyUnresolvedReferences
    team: "Team"
    public: bool

    _activity: Optional[List[Solve]] = None

    @property
    def activity(self):
        if not self._activity:
            self._activity = []
            solve_list = (self._client.do_request(f"user/profile/activity/{self.id}"))[
                "profile"
            ]["activity"]
            for solve_item in solve_list:
                solve_type = solve_item["object_type"]
                if solve_type == "machine":
                    self._activity.append(MachineSolve(solve_item, self._client))
                elif solve_type == "challenge":
                    self._activity.append(ChallengeSolve(solve_item, self._client))
                elif solve_type == "endgame":
                    self._activity.append(EndgameSolve(solve_item, self._client))
                elif solve_type == "fortress":
                    self._activity.append(FortressSolve(solve_item, self._client))

        return self._activity

    def __repr__(self):
        return f"<User '{self.name}'>"

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: "HTBClient", summary: bool = False):
        """Initialise a `User` using API data"""
        self._client = client
        self._detailed_func = client.get_user  # type: ignore
        self.id = data["id"]
        self.name = data["name"]
        self.user_owns = data["user_owns"]
        self.points = data["points"]

        if summary:
            self._is_summary = True
            self.ranking = data["rank"]
            self.root_owns = data["root_owns"]
            self.user_bloods = data.get("user_bloods_count") or 0
            self.root_bloods = data.get("root_bloods_count") or 0
            self.rank_name = data.get("rank_text") or ""
        else:
            self.ranking = data["ranking"]
            self.root_owns = data["system_owns"]
            self.user_bloods = data["user_bloods"]
            self.root_bloods = data["system_bloods"]
            self.rank_name = data["rank"]

            self.respects = data["respects"]
            self.university = data["university"]
            self.university_name = data["university_name"]
            self.description = data["description"]
            self.github = data["github"]
            self.linkedin = data["linkedin"]
            self.twitter = data["twitter"]
            self.website = data["website"]
            self.respected = data.get("isRespected", False)
            self.followed = data.get("isFollowed", False)
            self.rank_progress = data["current_rank_progress"]
            self.next_rank = data["next_rank"]
            self.next_rank_points = data["next_rank_points"]
            self.rank_ownership = float(data["rank_ownership"])
            self.rank_requirement = data["rank_requirement"]
            self.country_name = data["country_name"]
            self.team = data["team"]
            self.public = bool(data["public"])

    # noinspection PyUnresolvedReferences
    def get_content(self):
        return Content(self.id, self._client)

    # noinspection PyUnresolvedReferences
    def get_machines(self):
        return self.get_content().machines

    # noinspection PyUnresolvedReferences
    def get_challenges(self):
        return self.get_content().challenges
