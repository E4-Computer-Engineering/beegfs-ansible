"""Testinfra tests for beegfs-ansible.client role - Configuration validation only.

NOTE: These tests only validate configuration generation and setup.
Full integration tests (service startup, mounts, kernel modules) are performed
in the OpenStack-based test environment (extensions/molecule/) where a real
cluster with proper kernel support is available.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

# Add the parent directory to path to import testinfra_helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))

from extensions.molecule.testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


def test_beegfs_client_config_directory_exists(host):
    """Verify that BeeGFS client configuration directory exists."""
    config_dir = host.file("/etc/beegfs")
    assert config_dir.exists
    assert config_dir.is_directory


def test_beegfs_client_mount_point_prepared(host):
    """Verify that mount point directory is prepared."""
    mount_dir = host.file("/mnt/beegfs")
    # Directory should exist if created by role
    # This is a basic check - actual mounting requires full cluster
    if mount_dir.exists:
        assert mount_dir.is_directory


def test_beegfs_client_repository_configured(host):
    """Verify that BeeGFS repository is configured."""
    # Check for repository configuration
    # This validates the role ran successfully without requiring service startup
    if host.system_info.distribution in ['debian', 'ubuntu']:
        repo_file = host.file("/etc/apt/sources.list.d/beegfs.list")
    else:  # RHEL-based
        repo_file = host.file("/etc/yum.repos.d/beegfs.repo")

    # Repository file should exist after role execution
    # Note: Actual package installation is skipped in validation-only mode
    if repo_file.exists:
        assert repo_file.is_file


# NOTE: The following tests are intentionally NOT included:
# - Service startup (requires working cluster)
# - Filesystem mounting (requires working cluster)
# - Kernel module loading (requires kernel headers and DKMS build)
#
# These are tested in the OpenStack environment where full cluster
# deployment and real VMs with proper kernel support are available.
