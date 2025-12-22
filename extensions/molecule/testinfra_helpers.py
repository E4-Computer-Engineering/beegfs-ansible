"""Helper module for testinfra tests."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os


def get_target_hosts():
    """Return list of target hosts from MOLECULE_INSTANCE_CONFIG."""
    return [
        "ansible://{0}?ansible_inventory={1}".format(
            host, os.environ["MOLECULE_INVENTORY_FILE"]
        )
        for host in os.environ.get("MOLECULE_HOSTS", "all").split(",")
    ]
