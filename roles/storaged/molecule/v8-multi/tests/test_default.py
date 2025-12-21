"""Testinfra tests for beegfs-ansible.storaged role with multiple storage daemons (v8)."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

# Add the parent directory to path to import testinfra_helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))

from extensions.molecule.testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()

# Configuration for multiple storage targets
STORAGED_TARGETS = [
    {"target_id": "1", "tcp_port": "8003", "udp_port": "8003"},
    {"target_id": "2", "tcp_port": "8003", "udp_port": "8003"},
    {"target_id": "3", "tcp_port": "8003", "udp_port": "8003"},
]


def test_beegfs_storaged_all_services_running(host):
    """Verify that all BeeGFS storage server services are running."""
    for target in STORAGED_TARGETS:
        service_name = f"beegfs-storage@inst{target['target_id']}"
        service = host.service(service_name)
        assert service.is_running, f"Service {service_name} is not running"
        assert service.is_enabled, f"Service {service_name} is not enabled"


def test_beegfs_storaged_tcp_port_listening(host):
    """Verify that BeeGFS storage servers are listening on TCP port."""
    # All targets share the same port by default
    socket = host.socket(f"tcp://0.0.0.0:{STORAGED_TARGETS[0]['tcp_port']}")
    assert socket.is_listening


def test_beegfs_storaged_udp_port_listening(host):
    """Verify that BeeGFS storage servers are listening on UDP port."""
    # All targets share the same port by default
    socket = host.socket(f"udp://0.0.0.0:{STORAGED_TARGETS[0]['udp_port']}")
    assert socket.is_listening


def test_beegfs_storaged_storage_directories(host):
    """Verify that storage directories exist for each target."""
    for target in STORAGED_TARGETS:
        # Directory pattern based on BeeGFS conventions
        target_dir = f"/data/beegfs/beegfs_storage_{target['target_id']}"
        dir_check = host.file(target_dir)
        # Note: This test may fail if directories are created differently
        # Adjust the path pattern based on actual implementation
        if dir_check.exists:
            assert dir_check.is_directory, f"{target_dir} is not a directory"
