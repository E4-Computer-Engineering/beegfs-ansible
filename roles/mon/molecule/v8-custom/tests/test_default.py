"""Testinfra tests for beegfs-ansible.mon role with BeeGFS v8 and custom configuration."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

# Add the parent directory to path to import testinfra_helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))

from extensions.molecule.testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()

# Custom configuration values
MON_TCP_PORT = "9008"
MON_UDP_PORT = "9008"
MON_INTERFACES = ["eth0"]


def test_beegfs_mon_service_running(host):
    """Verify that BeeGFS monitoring service is running."""
    service = host.service("beegfs-mon")
    assert service.is_running
    assert service.is_enabled


def test_beegfs_mon_tcp_port_listening(host):
    """Verify that BeeGFS monitoring service is listening on custom TCP port."""
    socket = host.socket(f"tcp://0.0.0.0:{MON_TCP_PORT}")
    assert socket.is_listening


def test_beegfs_mon_udp_port_listening(host):
    """Verify that BeeGFS monitoring service is listening on custom UDP port."""
    socket = host.socket(f"udp://0.0.0.0:{MON_UDP_PORT}")
    assert socket.is_listening


def test_beegfs_mon_interface_binding(host):
    """Verify that BeeGFS monitoring service is bound to specified interfaces."""
    # Check that the service is listening on the specified interface
    for interface in MON_INTERFACES:
        # Get the IP address of the interface
        cmd = host.run(f"ip -4 addr show {interface} | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){{3}}'")
        if cmd.rc == 0 and cmd.stdout.strip():
            ip_address = cmd.stdout.strip()
            # Check if service is listening on this IP
            tcp_socket = host.socket(f"tcp://{ip_address}:{MON_TCP_PORT}")
            assert tcp_socket.is_listening, f"Service not listening on {ip_address}:{MON_TCP_PORT}"
