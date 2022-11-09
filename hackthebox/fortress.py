from __future__ import annotations
from typing import List, cast

from . import htb
from .errors import IncorrectFlagException


class Fortress(htb.HTBObject):
    """The class representing Hack The Box fortresses

    Attributes:
        id: The ID of the Fortress
        name: The name of the Fortress
        image: The relative URL of the Fortress' image
        num_flags: The number of available flags

        reset_votes: The number of votes to reset the Fortress
        progress: The active user's progress through the Fortress, out of 100
        flags: The list of flags available
        company: The Fortress' associated Company
        ip: IP address the Fortress can be contacted on

    """

    name: str
    image: str
    num_flags: int

    _detailed_attributes = ("reset_votes", "progress", "flags", "company", "ip")
    reset_votes: int
    progress: int
    flags: List
    company: Company
    ip: str

    def submit(self, flag: str):
        """Submits a flag for an Fortress

        Args:
            flag: The flag for the Fortress

        """
        submission = cast(
            dict,
            self._client.do_request(
                f"fortress/{self.id}/flag",
                json_data={
                    "flag": flag,
                },
            ),
        )
        if submission["message"] == "Wrong flag":
            raise IncorrectFlagException
        return True

    def __repr__(self):
        return f"<Fortress '{self.name}'>"

    def __init__(self, data: dict, client: htb.HTBClient, summary=False):
        self._client = client
        self._detailed_func = client.get_fortress  # type: ignore
        self.id = data["id"]
        self.name = data["name"]
        self.image = data["image"]
        if summary:
            self.num_flags = data["number_of_flags"]
            self._is_summary = True
        else:
            self.num_flags = len(data["flags"])
            self.company = Company(data["company"])
            self.reset_votes = data["reset_votes"]
            self.progress = data["progress_percent"]
            self.flags = data["flags"]
            self.ip = data["ip"]


class Company:
    """Representation of a company registered on Hack The Box

    Attributes:
        id: The Company ID
        name: The Company name
        description: The Company description
        url: The Company website
        image: The Company logo

    """

    id: int
    name: str
    description: str
    url: str
    image: str

    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.url = data["url"]
        self.image = data["image"]
