from datetime import datetime, timedelta
from typing import List, Union, cast, Optional, TYPE_CHECKING

import dateutil.parser

from . import htb, vpn
from .errors import (
    IncorrectArgumentException,
    IncorrectFlagException,
    TooManyResetAttempts,
    MachineException,
    UserAlreadySubmitted,
    RootAlreadySubmitted,
    SolveError,
)
from .solve import MachineSolve
from .utils import parse_delta

if TYPE_CHECKING:
    from .user import User


class Machine(htb.HTBObject):
    """The class representing Hack The Box machines

    Attributes:
        name: The Machine name
        os: The name of the operating system
        points: The points awarded for completion
        release_date: The date the Machine was released
        user_owns: The number of user owns the Machine has
        root_owns: The number of root owns the Machine has
        free: Whether the Machine is available on free servers
        user_owned: Whether the active User has owned the Machine's user account
        root_owned: Whether the active User has owned the Machine's user account
        reviewed: Whether the active User has reviewed the Machine
        stars: The average star rating of the Machine
        avatar: The relative URL of the Machine avatar
        difficulty: The difficulty of the machine
        :noindex: ip: The IP address of the machine

        active: Whether the Machine is active
        retired: Whether the Machine is retired
        avg_difficulty: The average numeric difficulty of the Machine
        completed: Whether the active User has completed the Machine
         :noindex: user_own_time: How long the active User took to own user
         :noindex: root_own_time: How long the active User took to own root
        user_blood: The Solve of the Machine's first user blood
        root_blood: The Solve of the Machine's first root blood
        user_own_time: How long the first User took to own user
        root_own_time: How long the first User took to own root
        difficulty_ratings: A dict of difficulty ratings given
    """

    name: str
    os: str
    points: int
    release_date: datetime
    root_owns: int
    free: bool
    user_owned: bool
    root_owned: bool
    reviewed: bool
    stars: float
    avatar: str
    difficulty: str

    _detailed_attributes = (
        "active",
        "retired",
        "user_own_time",
        "root_own_time",
        "user_blood",
        "root_blood",
        "user_blood_time",
        "root_blood_time",
        "difficulty_ratings",
    )
    active: bool
    retired: bool
    avg_difficulty: int
    completed: bool
    user_own_time: timedelta
    root_own_time: timedelta
    user_blood: MachineSolve
    root_blood: MachineSolve
    user_blood_time: timedelta
    root_blood_time: timedelta
    difficulty_ratings: dict

    # noinspection PyUnresolvedReferences
    _authors: Optional[List["User"]] = None
    _author_ids: List[int]
    _is_release: Optional[bool] = None
    _ip: Optional[str] = None

    def submit(self, flag: str, difficulty: int) -> str:
        """Submits a flag for a Machine

        Args:
            flag: The flag for the Machine
            difficulty: A rating between 10 and 100 of the Machine difficulty.
                        Must be a multiple of 10.
        """
        if difficulty < 10 or difficulty > 100 or difficulty % 10 != 0:
            raise IncorrectArgumentException(
                reason="Difficulty must be a multiple of 10, between 10 and 100"
            )

        submission = cast(
            dict,
            self._client.do_request(
                "machine/own",
                json_data={"flag": flag, "id": self.id, "difficulty": difficulty},
            ),
        )
        if submission["status"] == 400:
            if submission["message"] == "Incorrect flag!":
                raise IncorrectFlagException
            elif submission["message"] == f"{self.name} user is already owned.":
                raise UserAlreadySubmitted
            elif submission["message"] == f"{self.name} root is already owned.":
                raise RootAlreadySubmitted
            else:
                raise SolveError
        return submission["message"]

    # noinspection PyUnresolvedReferences
    @property
    def authors(self) -> List["User"]:
        """Fetch the author(s) of the Machine

        Returns: List of Users

        """
        if not self._authors:
            self._authors = []
            for uid in self._author_ids:
                self._authors.append(self._client.get_user(uid))
        return self._authors

    @property
    def is_release(self):
        if self._is_release is not None:
            return self._is_release
        self._is_release = False

        data = self._client.do_request("connections")["data"]
        try:
            if data["release_arena"]["machine"]["id"] == self.id:
                self._is_release = True
        except AttributeError:
            pass
        return self._is_release

    @property
    def ip(self):
        """The IP of an active machine."""
        if self._ip is not None:
            return self._ip
        listing = self._client.do_request("machine/list")["info"]
        m = next(filter(lambda x: x["id"] == self.id, listing))
        self._ip = m["ip"]
        return self._ip

    def start(self, release_arena=False) -> Union["MachineInstance", None]:
        """Alias for `Machine.spawn()`"""
        return self.spawn(release_arena)

    def spawn(self, release_arena=False) -> "MachineInstance":
        """Spawn an instance of this machine.

        Args:
            release_arena: Whether to use Release Arena to spawn the machine

        Returns:
            The spawned `MachineInstance`
        """
        if release_arena:
            if not self.is_release:
                # TODO: Better exception
                raise Exception("Machine is not on release arena")
            data = cast(dict, self._client.do_request("release_arena/spawn", post=True))
            if data.get("success") != 1:
                raise Exception(f"Failed to spawn: {data}")
            ip = cast(dict, self._client.do_request("release_arena/active"))["info"][
                "ip"
            ]
            server = self._client.get_current_vpn_server(release_arena=True)
        else:
            data = cast(
                dict,
                self._client.do_request("vm/spawn", json_data={"machine_id": self.id}),
            )
            if "Machine deployed" in cast(
                str, data.get("message")
            ) or "You have been assigned" in cast(str, data.get("message")):
                ip = cast(dict, self._client.do_request(f"machine/profile/{self.id}"))[
                    "info"
                ]["ip"]
                server = self._client.get_current_vpn_server()
            else:
                raise Exception(f"Failed to spawn: {data}")
        return MachineInstance(ip, server, self, self._client)

    def __repr__(self):
        return f"<Machine '{self.name}'>"

    def __init__(self, data: dict, client: htb.HTBClient, summary: bool = False):
        self._client = client
        self._detailed_func = client.get_machine  # type: ignore
        self.id = data["id"]
        self.name = data["name"]
        self.os = data["os"]
        self.points = data["points"]
        self.release_date = dateutil.parser.parse(data["release"])
        self.user_owns = data["user_owns_count"]
        self.root_owns = data["root_owns_count"]
        self.user_owned = data["authUserInUserOwns"]
        self.root_owned = data["authUserInRootOwns"]
        self.reviewed = data["authUserHasReviewed"]
        self.stars = float(data["stars"])
        self.avatar = data["avatar"]
        self.difficulty = data["difficultyText"]
        self.free = data["free"]
        self._author_ids = [data["maker"]["id"]]

        
        if data.get("ip"):
            self._ip = data["ip"]
        if data["maker2"]:
            self._author_ids.append(data["maker2"]["id"])
        if not summary:
            self.active = bool(data["active"])
            self.retired = bool(data["retired"])
            if data["authUserInUserOwns"]:
                self.user_own_time = parse_delta(data["authUserFirstUserTime"])
            if data["authUserInRootOwns"]:
                self.root_own_time = parse_delta(data["authUserFirstRootTime"])
            self.difficulty_ratings = data["feedbackForChart"]
            if data["userBlood"]:
                user_blood_data = {
                    "date": dateutil.parser.parse(data["userBlood"]["created_at"]),
                    "first_blood": True,
                    "id": data["id"],
                    "name": data["name"],
                    "type": "user",
                }
                self.user_blood = MachineSolve(user_blood_data, self._client)
                self.user_blood_time = parse_delta(
                    data["userBlood"]["blood_difference"]
                )
            if data["rootBlood"]:
                user_blood_data = {
                    "date": dateutil.parser.parse(data["rootBlood"]["created_at"]),
                    "first_blood": True,
                    "id": data["id"],
                    "name": data["name"],
                    "type": "root",
                }
                self.root_blood = MachineSolve(user_blood_data, self._client)
                self.root_blood_time = parse_delta(
                    data["rootBlood"]["blood_difference"]
                )
        else:
            self._is_summary = True


class MachineInstance:
    """Representation of an active machine instance

    Attributes:
        ip: The IP the instance can be reached at
        server: The `VPNServer` that the machine is on
        machine: The `Machine` this is an instance of
        client: The passed-through API client
    """

    ip: str
    server: vpn.VPNServer
    client: htb.HTBClient
    machine: Machine

    def __init__(
        self, ip: str, server: vpn.VPNServer, machine: Machine, client: htb.HTBClient
    ):
        self.client = client
        self.ip = ip
        self.server = server
        self.machine = machine

    def __repr__(self):
        return f"<'{self.machine.name}'@{self.server.friendly_name} - {self.ip}>"

    def stop(self):
        """Request the instance be stopped."""
        if self.machine.is_release:
            self.client.do_request("release_arena/terminate", post=True)
        else:
            self.client.do_request(
                "vm/terminate", json_data={"machine_id": self.machine.id}
            )

        # Can't delete references to the object from here so we just have
        # to set everything to None and prevent further usage
        self.server = None
        self.ip = None
        self.client = None
        self.machine = None

    def reset(self):
        """Request the instance be reset."""
        if self.machine.is_release:
            resp = self.client.do_request(
                "release_arena/reset", json_data={"machine_id": self.machine.id}
            )
        else:
            resp = self.client.do_request(
                "vm/reset", json_data={"machine_id": self.machine.id}
            )
        # VM
        if resp["message"].endswith(" will be reset in 1 minute."):
            return True
        elif resp["message"] == "Too many reset machine attempts. Try again later!":
            raise TooManyResetAttempts
        # RA
        elif resp["success"]:
            return True
        elif resp["message"].startswith("You must wait"):
            raise TooManyResetAttempts
        raise MachineException
