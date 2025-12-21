"""Testinfra tests for beegfs-ansible.storaged role with BeeGFS v8."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

# Add the parent directory to path to import testinfra_helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))

from extensions.molecule.testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()

# Default configuration values
STORAGED_TARGET_ID = "1"
STORAGED_TCP_PORT = "8003"
STORAGED_UDP_PORT = "8003"


def test_beegfs_storaged_service_running(host):
    """Verify that BeeGFS storage server service is running."""
    service_name = f"beegfs-storage@inst{STORAGED_TARGET_ID}"
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def test_beegfs_storaged_tcp_port_listening(host):
    """Verify that BeeGFS storage server is listening on default TCP port."""
    socket = host.socket(f"tcp://0.0.0.0:{STORAGED_TCP_PORT}")
    assert socket.is_listening


def test_beegfs_storaged_udp_port_listening(host):
    """Verify that BeeGFS storage server is listening on default UDP port."""
    socket = host.socket(f"udp://0.0.0.0:{STORAGED_UDP_PORT}")
    assert socket.is_listening


def test_beegfs_storaged_listening_all_interfaces(host):
    """Verify that BeeGFS storage server is listening on all interfaces (default)."""
    # When no specific interfaces are configured, service should listen on 0.0.0.0
    tcp_socket = host.socket(f"tcp://0.0.0.0:{STORAGED_TCP_PORT}")
    assert tcp_socket.is_listening
