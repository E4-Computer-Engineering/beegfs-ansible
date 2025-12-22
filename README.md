# Ansible Collection - e4_computer_engineering.beegfs

[![License](https://img.shields.io/badge/license-Apache%20V2-blue.svg)](https://github.com/E4-Computer-Engineering/beegfs/blob/main/LICENSE)
[![Collection Docs](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/collection-docs.yml/badge.svg)](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/collection-docs.yml)
[![Ansible CI](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/ansible-ci.yml/badge.svg)](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/ansible-ci.yml)
[![Release](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/release.yml/badge.svg)](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/release.yml)

This Ansible collection aims to deploy Beegfs cluster components in the following scenarios:

* single node cluster: a node that runs all [Beegfs components](#components)
* multi node cluster: the Beegfs services are running on different nodes
* multiple clusters in single or multi node: a single Beegfs client node can be part of two or more Beegfs clusters in single or multi node

This collection is compatible with the Beegfs versions 7.4.X and 8.X

Collection documentation is available at the [Beegfs Ansible Collection Documentation](https://e4-computer-engineering.github.io/beegfs-ansible/branch/main/).

This Beegfs Ansible collection aims to execute the tedious and repetitive tasks to be executed for the configuration of the different Beegfs components ensuring the final setup is consistent across the whole cluster:

* all nodes:
  * deploy beegfs authentication file
  * disable SeLinux
  * optionally populate `/etc/hosts` (disabled by default, controlled by `<role>_populate_etc_hosts` per role)
  * install correct packages
  * deploy interfaces files
  * deploy configuration files
* storage and metadata:
  * create and tune filesystem on block devices
* management:
  * generate and deploy TLS certificates
* client:
  * generate and deploy TLS certificates
  * add vault repositories (Rocky and Alma)
  * install kernel-devel or kernel-headers packages for `beegfs-client` rebuild
  * support for DKMS installation
  * install beeond package if needed
  * create bind mounts

## Components

* Management: There can be only one cluster handled by a management instance
* Monitoring: There can be only one cluster handled by a monitoring instance
* Metadata: There can be multiple clusters referring to multiple metadata servers on a single node
* Storage: There can be multiple clusters referring to multiple storage servers on a single node
* Client: A client instance is able to handle connectivity to one or multiple clusters

## Deploying the whole cluster

To deploy a whole cluster, the [site playbook](playbooks/site.yml) should be used. This will ensure the correct ordering and timing for all the Beegfs components.

In the [extensions directory](extensions/molecule/) it is possible to see examples of inventories and variables, such as:

* the `default` molecule scenario that deploys Beegfs v8
* the `v7` molecule scenario that deploys Beegfs v7

## Playbook Examples

All playbook examples are available in the [`examples/`](examples/) directory.

### Quick Start - Complete Cluster Deployment

Use the provided site playbook for deploying a complete BeeGFS cluster.

**Example:** [`examples/quick-start.yml`](examples/quick-start.yml)

```bash
# Run the playbook
ansible-playbook -i examples/inventory.yml examples/quick-start.yml
```

### Multi-Node Cluster Deployment

Deploy a multi-node BeeGFS cluster with dedicated management, metadata, storage, and client nodes.

**Example:** [`examples/multi-node-cluster.yml`](examples/multi-node-cluster.yml)

```bash
ansible-playbook -i examples/inventory.yml examples/multi-node-cluster.yml
```

### Single-Node Cluster Deployment

Deploy all BeeGFS services on a single node for testing or small deployments.

**Example:** [`examples/single-node-cluster.yml`](examples/single-node-cluster.yml)

```bash
ansible-playbook -i examples/inventory.yml examples/single-node-cluster.yml
```

### Multi-Cluster Client Configuration

Configure a client to access multiple BeeGFS clusters.

**Example:** [`examples/multi-cluster-client.yml`](examples/multi-cluster-client.yml)

### Advanced Configuration Examples

Additional configuration examples are available in the [`examples/`](examples/) directory:

- **[Client with TCP (Disable RDMA)](examples/client-tcp.yml)** - TCP/IP networking instead of RDMA
- **[Client with RDMA Support](examples/client-rdma.yml)** - InfiniBand/RDMA for high-performance networking
- **[Client with DKMS Installation](examples/client-dkms.yml)** - Automatic kernel module rebuilds
- **[Client with NVIDIA GPU Direct Support](examples/client-gpu-direct.yml)** - Direct GPU memory access
- **[Client with Custom Mount Points](examples/client-custom-mounts.yml)** - Custom chunk sizes and RDMA buffers
- **[Quota Enforcement](examples/quota-enforcement.yml)** - Enable quota enforcement across the cluster
- **[Disable TLS for gRPC](examples/disable-tls.yml)** - Disable TLS encryption (BeeGFS 8.x)
- **[Populate /etc/hosts](examples/populate-etc-hosts.yml)** - Automatic /etc/hosts management

### Example Inventory

An example inventory file is available at [`examples/inventory.yml`](examples/inventory.yml).

## Security Considerations

> **WARNING**: By default the collection will deploy a cluster authentication file `/etc/beegfs/connauthfile` that is already present in the [_common role](roles/_common/files/connauthfile). You should create your own.
>
> **WARNING**: By default the collection will generate and deploy TLS certificates from the Ansible controller. If you don't want this to happen, you need to have the certificate files already present in the Ansible controller node `_common_tls_tmp_dir/_common_tls_cert_file`.
