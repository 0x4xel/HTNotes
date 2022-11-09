from __future__ import annotations

import atexit
import base64
import getpass
import json
import os
import time
from typing import List, Callable, Union, Optional, Tuple, cast, Any, TYPE_CHECKING

import requests

from .constants import API_BASE, USER_AGENT
from .errors import (
    AuthenticationException,
    NotFoundException,
    IncorrectOTPException,
    ApiError,
)

if TYPE_CHECKING:
    from .user import User
    from .search import Search
    from .machine import Machine, MachineInstance
    from .challenge import Challenge
    from .endgame import Endgame
    from .fortress import Fortress
    from .team import Team
    from .leaderboard import Leaderboard
    from .vpn import VPNServer


def jwt_expired(token: str) -> bool:
    """Checks if a JWT token is expired

    Args:
        token: A JWT string - 3 Base64 sequences joined with .

    Returns:
        If the token is expired

    """
    payload = base64.b64decode(token.split(".")[1] + "==").decode()
    if time.time() > json.loads(payload)["exp"]:
        return True
    else:
        return False


class HTBClient:
    """The client via which API requests are made

    Examples:
        Connecting to the API::

            from hackthebox import HTBClient
            client = HTBClient(email="user@example.com", password="S3cr3tP455w0rd!")
    Attributes:
        challenge_cooldown: Time when next download is allowed

    """

    # noinspection PyUnresolvedReferences
    _user: Optional["User"] = None
    _access_token: Optional[str]
    _refresh_token: Optional[str]
    _app_token: Optional[str]
    _api_base: str
    challenge_cooldown: int = 0

    def _refresh_access_token(self):
        """

        Use a saved refresh token to gain a new access token
        when the current one expires

        """
        headers = {"User-Agent": USER_AGENT}
        r = requests.post(
            self._api_base + "login/refresh",
            json={"refresh_token": self._refresh_token},
            headers=headers,
        )
        data = r.json()["message"]
        if isinstance(data, str) and data.startswith("Unauthenticated"):
            raise AuthenticationException
        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]

    def do_request(
        self,
        endpoint,
        json_data=None,
        data=None,
        authorized=True,
        download=False,
        post=False,
    ) -> Union[dict, bytes]:
        """

        Args:
            endpoint: The API endpoint to request
            json_data: Data to be sent in JSON format
            data: Data to be sent in application/x-www-form-urlencoded format
            authorized: If the request requires an Authorization header
            download: If we are downloading raw data
            post: Force POST request
        Returns:
            The JSON response from the API or the raw data (if `download` is set)

        """
        headers = {"User-Agent": USER_AGENT}
        if authorized:
            # Don't use authorization if the API base URL isn't the real one -
            # i.e. we're running a test
            if self._app_token is not None:
                headers["Authorization"] = "Bearer " + self._app_token
            elif self._access_token is not None and self._refresh_token is not None:
                if jwt_expired(self._access_token):
                    self._refresh_access_token()
                headers["Authorization"] = "Bearer " + self._access_token
            else:
                raise AuthenticationException("No authentication tokens available")
        while True:
            if not json_data and not data:
                if post:
                    r = requests.post(
                        self._api_base + endpoint, headers=headers, stream=download
                    )
                else:
                    r = requests.get(
                        self._api_base + endpoint, headers=headers, stream=download
                    )
            else:
                r = requests.post(
                    self._api_base + endpoint,
                    json=json_data,
                    data=data,
                    headers=headers,
                    stream=download,
                )
            if r.status_code != 429:
                break
            # Not sure on the exact ratelimit - loop until we don't get 429
            else:
                time.sleep(1)
        if r.status_code == 404:
            raise NotFoundException
        if download:
            return r.content
        else:
            return r.json()

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        otp: Optional[str | int] = None,
        cache: Optional[str] = None,
        api_base: str = API_BASE,
        remember: Optional[bool] = False,
        app_token: Optional[str] = None,
    ):
        """
        Authenticates to the API.

        If `cache` is set, the client will attempt to load access tokens from the given path. If they cannot be found,
        or are expired, normal API authentication will take place, and the tokens will be dumped to the file for the
        next launch.

        Args:
            email: The authenticating user's email address
            password: The authenticating user's password
            otp: The current OTP of the user, if 2FA is enabled
            cache: The path to load/store access tokens from/to
            remember: Whether to create a long-lasting 'remember me' token
            app_token: Authenticate using a provided App Token
        """
        self._api_base = api_base
        if cache is not None:
            if self.load_from_cache(cache) is False:
                self.do_login(email, password, otp, remember, app_token)
                self.dump_to_cache(cache)
            # Make sure we dump our current tokens out when we exit
            atexit.register(self.dump_to_cache, cache)
        else:
            self.do_login(email, password, otp, remember, app_token)

    def load_from_cache(self, cache: str) -> bool:
        """
        Args:
            cache: The cache file path

        Returns: Whether loading from the cache was successful
        """
        if not os.path.exists(cache):
            return False
        with open(cache, "r") as f:
            data = json.load(f)
        self._access_token = data.get("access_token")
        self._refresh_token = data.get("refresh_token")
        self._app_token = data.get("app_token")
        if self._access_token is not None:
            if jwt_expired(self._access_token):
                try:
                    self._refresh_access_token()
                # Our refresh token is also invalid, we must log in again
                except AuthenticationException:
                    return False
        return True

    def dump_to_cache(self, cache):
        """
        Dumps the current access and refresh tokens to a file
        Args:
            cache: The path to the cache file
        """
        with open(cache, "w") as f:
            json.dump(
                {
                    "access_token": self._access_token,
                    "refresh_token": self._refresh_token,
                    "app_token": self._app_token,
                },
                f,
            )

    def do_login(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        otp: Optional[str | int] = None,
        remember: Optional[bool] = False,
        app_token: Optional[str] = None,
    ):
        """
        Authenticates against the API. If credentials are not provided, they will be prompted for.
        """

        self._app_token = app_token
        if app_token is not None:
            self._access_token = self._refresh_token = None
        else:
            if email is None:
                email = input("Email: ")
            if password is None:
                password = getpass.getpass()

            data = cast(
                dict,
                self.do_request(
                    "login",
                    json_data={
                        "email": email,
                        "password": password,
                        "remember": remember,
                    },
                    authorized=False,
                ),
            )
            msg = data["message"]

            self._access_token = msg.get("access_token")
            if self._access_token is None:
                raise ApiError(f"Failed to get access token: {msg}")
            self._refresh_token = msg.get("refresh_token")
            if self._refresh_token is None:
                raise ApiError(f"Failed to get refresh token: {msg}")
            if data["message"]["is2FAEnabled"] is True:
                if otp is None:
                    otp = input("OTP: ")
                if type(otp) == int:
                    # Optimistically try and create a string
                    otp = f"{otp:06d}"
                resp = cast(
                    dict,
                    self.do_request("2fa/login", json_data={"one_time_password": otp}),
                )
                if "correct" not in resp["message"]:
                    raise IncorrectOTPException

    # noinspection PyUnresolvedReferences
    def search(self, search_term: str) -> "Search":
        """

        Args:
            search_term: The search term to pass to the API

        Returns: A Search object with lists of the items retrieved from the API

        """
        from .search import Search

        return Search(search_term, self)

    # noinspection PyUnresolvedReferences
    def get_machine(self, machine_id: int | str) -> "Machine":
        """

        Args:
            machine_id: The platform ID or name of the `Machine` to fetch

        Returns: The requested `Machine`

        """
        from .machine import Machine

        data = cast(dict, self.do_request(f"machine/profile/{machine_id}"))["info"]
        return Machine(data, self)

    def get_tags_machine(self, machine_id: int | str) -> "Machine":
        """

        Args:
            machine_id: The platform ID or name of the `Machine` to fetch

        Returns: The requested `Machine`

        """
        from .machine import Machine

        data = cast(dict, self.do_request(f"machine/tags/{machine_id}"))["info"]
        return data 

    def get_matrix(self, machine_id: int | str) -> "Machine":
        """

        Args:
            machine_id: The platform ID or name of the `Machine` to fetch

        Returns: The requested `Machine`

        """
        from .machine import Machine

        data = cast(dict, self.do_request(f"machine/graph/matrix/{machine_id}"))["info"]
        return data 

    def get_user_rating(self, machine_id: int | str) -> "Machine":
        """

        Args:
            machine_id: The platform ID or name of the `Machine` to fetch

        Returns: The requested `Machine`

        """
    

        data = cast(dict, self.do_request(f"machine/graph/owns/difficulty/{machine_id}"))["info"]
        return data     


    # noinspection PyUnresolvedReferences
    def get_todo_machines(self, limit: int = None) -> List[int]:
        """

        Retrieve a list of `Machine` ID's from the API based on the users todo list

        Args:
            limit: The maximum number to fetch

        Returns: A list of `Machine` ID's

        """
        data = cast(dict, self.do_request("home/user/todo"))["data"]["machines"][:limit]
        return [m["id"] for m in data]

    # noinspection PyUnresolvedReferences
    def get_active_machine(
        self, release_arena: bool = False
    ) -> Optional["MachineInstance"]:
        """

        Retrieve `Machine` currently assigned to user

        Returns: The `Machine` currently assigned (or active) to user

        """
        from .machine import Machine, MachineInstance

        if release_arena:
            info = cast(dict, self.do_request(f"release_arena/active"))["info"]
        else:
            info = cast(dict, self.do_request(f"machine/active"))["info"]
        if info:
            box = self.get_machine(info["id"])
            server = box._client.get_current_vpn_server(release_arena)
            return MachineInstance(box.ip, server, box, box._client)
        return None

    # noinspection PyUnresolvedReferences
    def get_machines(self, limit: int = None, retired: bool = False) -> List["Machine"]:
        """

        Retrieve a list of `Machine` from the API

        Args:
            limit: The maximum number to fetch
            retired: Whether to fetch from the retired list instead of the active list

        Returns: A list of `Machine`

        """
        from .machine import Machine

        if not retired:
            data = cast(dict, self.do_request("machine/list"))["info"][:limit]
        else:
            data = cast(dict, self.do_request("machine/list/retired"))["info"][:limit]
        machines = [Machine(m, self, summary=True) for m in data]
        for machine in machines:
            machine.retired = retired
        return machines

    # noinspection PyUnresolvedReferences
    def get_challenge(self, challenge_id: int | str) -> "Challenge":
        """

        Args:
            challenge_id: The platform ID or name of the `Challenge` to fetch

        Returns: The requested `Challenge`

        """
        from .challenge import Challenge

        data = cast(dict, self.do_request(f"challenge/info/{challenge_id}"))[
            "challenge"
        ]
        return Challenge(data, self)

    # noinspection PyUnresolvedReferences
    def get_challenges(self, limit=None, retired=False) -> List["Challenge"]:
        """Requests a list of `Challenge` from the API

        Args:
            limit: The maximum number of `Challenge` to fetch
            retired: Whether to fetch from the retired list instead of the active list

        Returns: A list of `Challenge`

        """
        from .challenge import Challenge

        if retired:
            data = cast(dict, self.do_request("challenge/list/retired"))
        else:
            data = cast(dict, self.do_request("challenge/list"))
        challenges = []
        for challenge in data["challenges"][:limit]:
            challenges.append(Challenge(challenge, self, summary=True))
        return challenges

    # noinspection PyUnresolvedReferences
    def get_endgame(self, endgame_id: int) -> "Endgame":
        """Requests an Endgame from the API

        Args:
            endgame_id: The ID of the Endgame to fetch

        Returns: An Endgame

        """
        from .endgame import Endgame

        data = cast(dict, self.do_request(f"endgame/{endgame_id}"))["data"]
        return Endgame(data, self)

    # noinspection PyUnresolvedReferences
    def get_endgames(self, limit: int = None) -> List["Endgame"]:
        """Requests a list of Endgames from the API

        Args:
            limit: The maximum number of Endgames to fetch

        Returns: A list of Endgames

        """
        from .endgame import Endgame

        data = cast(dict, self.do_request(f"endgames"))["data"][:limit]
        endgames = []
        for endgame in data:
            endgames.append(Endgame(endgame, self, summary=True))
        return endgames

    # noinspection PyUnresolvedReferences
    def get_fortress(self, fortress_id: int) -> "Fortress":
        """Requests an Fortress from the API

        Args:
            fortress_id: The ID of the Fortress to fetch

        Returns: A Fortresse

        """
        from .fortress import Fortress

        data = cast(dict, self.do_request(f"fortress/{fortress_id}"))["data"]
        return Fortress(data, self)

    # noinspection PyUnresolvedReferences
    def get_fortresses(self, limit: int = None) -> List["Fortress"]:
        """Requests a list of Fortresses from the API

        Args:
            limit: The maximum number of Fortresses to fetch

        Returns: A list of Fortresses

        """
        from .fortress import Fortress

        data = cast(dict, self.do_request(f"fortresses"))["data"]
        fortresses = []
        # For some  reason, the fortress list is in the format {"1": <fortress1>, "2": <fortress2>}
        # instead of [<fortress1>, <fortress2>], meaning we have to sort it ourselves
        for fortress_id, fortress in sorted(data.items())[:limit]:
            fortresses.append(Fortress(fortress, self, summary=True))
        return fortresses

    # noinspection PyUnresolvedReferences
    def get_user(self, user_id: int) -> "User":
        """

        Args:
            user_id: The platform ID of the `User` to fetch

        Returns: The requested `User`

        """
        from .user import User

        data = cast(dict, self.do_request(f"user/profile/basic/{user_id}"))["profile"]
        return User(data, self)

    # noinspection PyUnresolvedReferences
    def get_team(self, team_id: int) -> "Team":
        """

        Args:
            team_id: The platform ID of the `Team` to fetch

        Returns: The requested `Team`

        """
        from .team import Team

        data = cast(dict, self.do_request(f"team/info/{team_id}"))
        return Team(data, self)

    # noinspection PyUnresolvedReferences
    def get_hof(self, vip: bool = False) -> "Leaderboard":
        """
        Returns: A Leaderboard of the top 100 Users
        """
        from .leaderboard import Leaderboard
        from .user import User

        endpoint = "rankings/users"
        if vip:
            endpoint += "?vip=1"
        data = cast(dict, self.do_request(endpoint))["data"]
        return Leaderboard(data, self, User)

    # noinspection PyUnresolvedReferences
    def get_hof_countries(self) -> "Leaderboard":
        """
        Returns: A Leaderboard of the top 100 Countries
        """
        from .leaderboard import Leaderboard, Country

        data = cast(dict, self.do_request("rankings/countries"))["data"]
        return Leaderboard(data, self, Country)

    # noinspection PyUnresolvedReferences
    def get_hof_teams(self) -> "Leaderboard":
        """

        Returns: A Leaderboard of Teams

        """
        from .leaderboard import Leaderboard
        from .team import Team

        data = cast(dict, self.do_request("rankings/teams"))["data"]
        return Leaderboard(data, self, Team)

    # noinspection PyUnresolvedReferences
    def get_hof_universities(self) -> "Leaderboard":
        """
        Returns: A Leaderboard of Universities

        """
        from .leaderboard import Leaderboard, University

        data = cast(dict, self.do_request("rankings/universities"))["data"]
        return Leaderboard(data, self, University)

    # noinspection PyUnresolvedReferences
    def get_current_vpn_server(self, release_arena=False) -> VPNServer:
        """
        Returns: The currently assigned `VPNServer`

        Args:
            release_arena: Get the current release arena VPN server
        """
        from .vpn import VPNServer

        if release_arena:
            connections = cast(
                dict, self.do_request("connections/servers?product=release_arena")
            )["data"]
            data = connections["assigned"]
        else:
            connections = cast(dict, self.do_request("connections"))["data"]
            data = connections["lab"]["assigned_server"]

        return VPNServer(data, self)

    # noinspection PyUnresolvedReferences
    def get_all_vpn_servers(self, release_arena=False) -> "List[VPNServer]":
        """
        Returns: A list of `VPNServer`

        Args:
            release_arena: Use the release arena VPN servers
        """
        from .vpn import VPNServer

        if release_arena:
            data = cast(
                dict, self.do_request("connections/servers?product=release_arena")
            )["data"]["options"]
        else:
            data = cast(dict, self.do_request("connections/servers?product=labs"))[
                "data"
            ]["options"]
        servers = []
        for location in data.keys():  # 'EU'
            for location_role in data[location].keys():  # 'EU - Free'
                for server in data[location][location_role]["servers"].values():
                    servers.append(VPNServer(server, self))
        return servers

    # noinspection PyUnresolvedReferences
    @property
    def user(self) -> "User":
        """

        Returns: The `User` associated with the current `HTBClient`

        """
        if not self._user:
            uid = cast(dict, self.do_request("user/info"))["info"]["id"]
            self._user = self.get_user(uid)
        return self._user


class HTBObject:
    """Base class of all API objects

    Attributes:
        id: The ID of the associated object
    """

    _client: HTBClient
    # Attributes not fetched by a summary
    _detailed_attributes: Tuple[str, ...]
    _detailed_func: Callable[..., Any]
    _is_summary: bool = False
    id: int

    def __getattr__(self, item):
        """Retrieve attributes not given when initialised from a summary

        Some endpoints only provide a subset of the attributes available for a given object.
        If these extra attributes are requested, the object will request the full data from the
        API and fill out the missing items.

        Args:
            item: The name of the property to retrieve

        """
        if item in self._detailed_attributes and self._is_summary:
            new_obj = self._detailed_func(self.id)
            for attr in self._detailed_attributes:
                setattr(self, attr, getattr(new_obj, attr))
            self._is_summary = False
            return getattr(new_obj, item)
        else:
            raise AttributeError

    def __eq__(self, other):
        return self.id == other.id and type(self) == type(other)
