"""Testinfra tests for beegfs-ansible.mgmtd role with BeeGFS v7."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

# Add the parent directory to path to import testinfra_helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))

from extensions.molecule.testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()

# Default configuration values
MGMTD_TCP_PORT = "8008"
MGMTD_UDP_PORT = "8008"


def test_beegfs_mgmtd_service_running(host):
    """Verify that BeeGFS management server service is running."""
    service = host.service("beegfs-mgmtd")
    assert service.is_running
    assert service.is_enabled


def test_beegfs_mgmtd_tcp_port_listening(host):
    """Verify that BeeGFS management server is listening on default TCP port."""
    socket = host.socket(f"tcp://0.0.0.0:{MGMTD_TCP_PORT}")
    assert socket.is_listening


def test_beegfs_mgmtd_udp_port_listening(host):
    """Verify that BeeGFS management server is listening on default UDP port."""
    socket = host.socket(f"udp://0.0.0.0:{MGMTD_UDP_PORT}")
    assert socket.is_listening


def test_beegfs_mgmtd_listening_all_interfaces(host):
    """Verify that BeeGFS management server is listening on all interfaces (default)."""
    # When no specific interfaces are configured, service should listen on 0.0.0.0
    tcp_socket = host.socket(f"tcp://0.0.0.0:{MGMTD_TCP_PORT}")
    assert tcp_socket.is_listening
