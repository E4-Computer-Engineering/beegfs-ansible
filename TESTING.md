# Testing Guide for BeeGFS Ansible Collection

This document describes the testing strategy and infrastructure for the BeeGFS Ansible collection.

## Testing Levels

### 1. GitHub Actions - Docker-based Unit Tests

**Location**: `.github/workflows/molecule-tests.yml`

**Purpose**: Fast, automated testing of individual server roles without requiring a full cluster.

**Tested Roles**:
- `mgmtd` - Management server
- `mon` - Monitoring server
- `metad` - Metadata server
- `storaged` - Storage server

**NOT Tested in GitHub Actions**:
- `client` - Requires full cluster and kernel module support (see Integration Tests below)

#### Supported Operating Systems
All server roles are tested against:
- Ubuntu 22.04
- AlmaLinux 8
- AlmaLinux 9

#### Test Scenarios
Each server role is tested with multiple scenarios:
- **Default configuration** - Standard BeeGFS deployment
- **Custom ports/interfaces** - Custom network configuration
- **Multi-daemon** (metad/storaged only) - Multiple service instances per node
- **v7 and v8** - Both BeeGFS 7.x and 8.x versions

#### Running Locally
```bash
# Test a specific role
cd roles/mgmtd
molecule test

# Test with specific distro
MOLECULE_DISTRO=ubuntu2204 molecule test

# Test specific scenario
molecule test -s v8
```

### 2. OpenStack Integration Tests

**Location**: `extensions/molecule/`

**Purpose**: Full integration testing with real VMs, complete cluster deployment, and kernel module support.

**Test Scenarios**:
- `default` - BeeGFS v8 cluster deployment
- `v7` - BeeGFS v7 cluster deployment
- `openstack` - Infrastructure provisioning and cluster deployment

#### What's Tested
- Complete BeeGFS cluster deployment
- All roles including client
- Kernel module compilation and loading (DKMS)
- Actual filesystem mounting
- Multi-node cluster operation
- Cross-distribution compatibility

#### Components
- **Management nodes**: mgmtd + mon
- **Storage nodes**: metad + storaged with real volumes
- **Client nodes**: Multiple OS variants (AlmaLinux, Rocky Linux, Ubuntu)

#### Running OpenStack Tests
```bash
# Configure OpenStack credentials first
# Either use clouds.yaml or source openrc.sh

# Run default scenario (v8)
molecule test -s default

# Run v7 scenario
molecule test -s v7

# Run specific stages
molecule create -s default
molecule converge -s default
molecule verify -s default
molecule destroy -s default
```

#### Infrastructure Requirements
- OpenStack cloud access
- SSH key configured (`med-deployer`)
- Network access (`private_tech_dev`)
- External network (`external_1632`)
- Sufficient quota for:
  - 6+ VMs (1 mgmt, 2 storage, 3+ clients)
  - Multiple volumes for metadata/storage targets
  - Floating IPs

## Test Matrix Summary

### GitHub Actions (Docker-based)
| Role | Scenarios | OS | Total Tests |
|------|-----------|-----|-------------|
| mgmtd | 4 | 3 | 12 |
| mon | 4 | 3 | 12 |
| metad | 6 | 3 | 18 |
| storaged | 6 | 3 | 18 |
| **Total** | | | **60** |

### OpenStack Integration
| Scenario | Nodes | BeeGFS Version | Full Cluster |
|----------|-------|----------------|--------------|
| default | 6+ | v8.x | ✓ |
| v7 | 6+ | v7.x | ✓ |

## Why Two Testing Approaches?

### Docker Tests (GitHub Actions)
**Advantages**:
- Fast execution (minutes)
- Free on GitHub
- Automated PR testing
- Matrix testing across multiple OS

**Limitations**:
- Cannot load kernel modules
- Cannot mount filesystems
- Limited to single-container scenarios
- No real networking

### OpenStack Tests
**Advantages**:
- Real VMs with real kernels
- Full cluster deployment
- Actual kernel module compilation
- Real filesystem operations
- Multi-node networking

**Limitations**:
- Slower execution (15-30 minutes)
- Requires OpenStack access
- Resource costs
- Manual execution

## Client Role Testing

The client role has special requirements that make Docker-based testing impractical:

1. **Kernel Modules**: Requires DKMS to build `beegfs` kernel module
   - Needs kernel headers matching the running kernel
   - Cannot load modules in unprivileged containers
   - Requires actual kernel support, not just container isolation

2. **Cluster Dependency**: Must have:
   - Running mgmtd (management server)
   - Running metad (metadata server)
   - Running storaged (storage server)
   - Network connectivity to all services

3. **Filesystem Operations**: Needs to:
   - Mount BeeGFS filesystem
   - Perform I/O operations
   - Test POSIX compliance

**Solution**: Client is only tested in the OpenStack environment where these requirements can be met.

## Continuous Integration

### Pull Request Workflow
1. GitHub Actions automatically run on PR creation/update
2. Server roles tested across all supported OS
3. Fast feedback (10-15 minutes)
4. Blocks merge if tests fail

### Manual Integration Testing
1. Run OpenStack tests before major releases
2. Validate full cluster functionality
3. Test client kernel module compatibility
4. Verify cross-version upgrades

## Adding New Tests

### For Server Roles (mgmtd, mon, metad, storaged)
1. Add test scenarios in `roles/<role>/molecule/`
2. Update `.github/workflows/molecule-tests.yml` to include new scenario
3. Tests run automatically on PR

### For Client Role
1. Add tests to OpenStack scenarios in `extensions/molecule/`
2. Run manually in OpenStack environment
3. Document test procedures

### For New Roles
1. Create `molecule/default/` directory structure
2. Add testinfra tests
3. Update GitHub Actions workflow to include the role

## Troubleshooting

### GitHub Actions Failures
```bash
# Run the same test locally
cd roles/<role>
MOLECULE_DISTRO=ubuntu2204 molecule test -s <scenario>
```

### OpenStack Test Failures
```bash
# Check VM status
molecule login -s default -h <hostname>

# View logs
molecule login -s default -h mgmt-alma95-01
journalctl -u beegfs-mgmtd -f

# Cleanup stuck resources
molecule destroy -s default
```

## Dependencies

### GitHub Actions
- Docker
- Python 3.12
- molecule
- molecule-plugins[docker]
- testinfra
- pytest

### OpenStack Testing
- OpenStack access
- ansible
- molecule
- molecule-plugins (no specific driver, uses delegated)
- openstack.cloud collection
- testinfra

## Related Files

- `.github/workflows/molecule-tests.yml` - GitHub Actions workflow
- `.github/workflows/AnsibleTest.yml` - Ansible sanity tests
- `extensions/molecule/` - OpenStack test scenarios
- `molecule-requirements.txt` - Python dependencies for molecule
- Each role's `molecule/` directory - Role-specific tests
