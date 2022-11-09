"""
Examples:
    Retrieving the current VPN server::

        print(client.get_current_vpn_server())

    Switching to a given VPN server::

        req = input("What server? ")
        server = next(filter(lambda x: x.friendly_name == req), client.get_all_vpn_servers()))
        server.switch()
        server.download(path="/tmp/out.ovpn")

"""

from __future__ import annotations

import os

from . import htb
from .errors import VpnException, CannotSwitchWithActive

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .htb import HTBClient


class VPNServer(htb.HTBObject):
    """Class representing individual VPN servers provided by Hack The Box

    Attributes:
        friendly_name: Friendly name of the server

            Example: ``'US Free 1'``

        current_clients: The number of currently connected clients
        location: The physical location of the server

            Example: ``'US'``

    """

    friendly_name: str
    current_clients: int
    location: str
    _detailed_func = lambda x: None

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: "HTBClient", summary=False):
        self._client = client
        self.id = data["id"]
        self.friendly_name = data["friendly_name"]
        self.current_clients = data["current_clients"]
        self.location = data["location"]
        self.summary = summary

    def __repr__(self):
        return f"<VPN Server '{self.friendly_name}'>"

    def __str__(self):
        return f"{self.friendly_name}"

    def switch(self) -> bool:
        """
        Switches the client to use this VPN server

        Returns: Whether the switch was completed successfully
        """
        # TODO: Throw exception on failure
        result = cast(
            dict,
            self._client.do_request(f"connections/servers/switch/{self.id}", post=True),
        )
        if result["status"] is True:
            return True
        if (
            result["message"]
            == "You must stop your active machine before switching VPN"
        ):
            raise CannotSwitchWithActive
        raise VpnException

    def download(self, path=None, tcp=False) -> str:
        """

        Args:
            path: The name of the OVPN file to download to. If none is provided, it is saved to the current directory.
            tcp: Download TCP instead of UDP

        Returns: The path of the file

        """
        if path is None:
            path = os.path.join(os.getcwd(), f"{self.friendly_name}.ovpn")
        url = f"access/ovpnfile/{self.id}/0"
        if tcp:
            # Funky URL
            url += "/1"
        data = self._client.do_request(url, download=True)
        # We can't download VPN packs for servers we're not assigned to
        if b"You are not assigned" in data:
            self.switch()
        data = cast(bytes, self._client.do_request(url, download=True))
        with open(path, "wb") as f:
            f.write(data)
        return path
