"""Testinfra tests for beegfs-ansible.storaged role with custom configuration."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

# Add the parent directory to path to import testinfra_helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))

from extensions.molecule.testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()

# Custom configuration values
STORAGED_TARGET_ID = "5"
STORAGED_TCP_PORT = "9003"
STORAGED_UDP_PORT = "9003"
STORAGED_INTERFACES = ["eth0"]


def test_beegfs_storaged_service_running(host):
    """Verify that BeeGFS storage server service is running with custom target_id."""
    service_name = f"beegfs-storage@inst{STORAGED_TARGET_ID}"
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def test_beegfs_storaged_tcp_port_listening(host):
    """Verify that BeeGFS storage server is listening on custom TCP port."""
    socket = host.socket(f"tcp://0.0.0.0:{STORAGED_TCP_PORT}")
    assert socket.is_listening


def test_beegfs_storaged_udp_port_listening(host):
    """Verify that BeeGFS storage server is listening on custom UDP port."""
    socket = host.socket(f"udp://0.0.0.0:{STORAGED_UDP_PORT}")
    assert socket.is_listening


def test_beegfs_storaged_interface_binding(host):
    """Verify that BeeGFS storage server is bound to specified interfaces."""
    # Check that the service is listening on the specified interface
    for interface in STORAGED_INTERFACES:
        # Get the IP address of the interface
        cmd = host.run(f"ip -4 addr show {interface} | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){{3}}'")
        if cmd.rc == 0 and cmd.stdout.strip():
            ip_address = cmd.stdout.strip()
            # Check if service is listening on this IP
            tcp_socket = host.socket(f"tcp://{ip_address}:{STORAGED_TCP_PORT}")
            assert tcp_socket.is_listening, f"Service not listening on {ip_address}:{STORAGED_TCP_PORT}"
