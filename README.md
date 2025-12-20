# Ansible Collection - e4_computer_engineering.beegfs

[![License](https://img.shields.io/badge/license-Apache%20V2-blue.svg)](https://github.com/E4-Computer-Engineering/beegfs/blob/main/LICENSE)
[![Documentation](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/DocsPush.yml/badge.svg)](https://e4-computer-engineering.github.io/beegfs-ansible/branch/main)
[![AnsibleTest](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/AnsibleTest.yml/badge.svg)](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/AnsibleTest.yml)

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

### Quick Start - Complete Cluster Deployment

Use the provided site playbook for deploying a complete BeeGFS cluster:

```yaml
# playbook.yml
---
- name: Deploy complete BeeGFS cluster
  hosts: all
  tasks:
    - name: Include BeeGFS site playbook
      ansible.builtin.import_playbook: e4_computer_engineering.beegfs.site
```

```bash
# Run the playbook
ansible-playbook -i inventory.yml playbook.yml
```

### Multi-Node Cluster Deployment

Deploy a multi-node BeeGFS cluster with dedicated management, metadata, storage, and client nodes:

```yaml
# deploy_beegfs_cluster.yml
---
- name: Deploy BeeGFS Management Service
  hosts: management
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.mgmtd
      vars:
        mgmtd_beegfs_version: "8.1"
        mgmtd_store_mgmtd_directory: /data/beegfs/mgmtd
        mgmtd_conn_interfaces: ["eth0"]
        mgmtd_auth_file_path: playbooks/files/conn.auth

- name: Deploy BeeGFS Monitoring Service
  hosts: monitoring
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.mon
      vars:
        mon_beegfs_version: "8.1"
        mon_sys_mgmtd_host: mgmt-node-01
        mon_db_type: influxdb
        mon_db_hostname: localhost
        mon_conn_interfaces: ["eth0"]
        mon_auth_file_path: playbooks/files/conn.auth

- name: Deploy BeeGFS Metadata Services
  hosts: metadata
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.metad
      vars:
        metad_beegfs_version: "8.1"
        metad_auth_file_path: playbooks/files/conn.auth
        metad_server_targets:
          - target_id: "1"
            device: "nvme0n1"
            conn_interfaces: ["eth0"]
            sys_mgmtd_host: mgmt-node-01

- name: Deploy BeeGFS Storage Services
  hosts: storage
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.storaged
      vars:
        storaged_beegfs_version: "8.1"
        storaged_auth_file_path: playbooks/files/conn.auth
        storaged_server_targets:
          - target_id: "1"
            device: "sdb"
            conn_interfaces: ["eth0"]
            sys_mgmtd_host: mgmt-node-01

- name: Deploy BeeGFS Clients
  hosts: clients
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          - sys_mgmtd_host: mgmt-node-01
            conn_interfaces: ["eth0"]
```

### Single-Node Cluster Deployment

Deploy all BeeGFS services on a single node for testing or small deployments:

```yaml
# deploy_single_node.yml
---
- name: Deploy single-node BeeGFS cluster
  hosts: beegfs_all_in_one
  become: true
  vars:
    beegfs_version: "8.1"
    mgmt_host: "{{ inventory_hostname }}"
    auth_file: playbooks/files/conn.auth

  tasks:
    - name: Deploy Management Service
      ansible.builtin.include_role:
        name: e4_computer_engineering.beegfs.mgmtd
      vars:
        mgmtd_beegfs_version: "{{ beegfs_version }}"
        mgmtd_store_mgmtd_directory: /data/beegfs/mgmtd
        mgmtd_auth_file_path: "{{ auth_file }}"

    - name: Deploy Metadata Service
      ansible.builtin.include_role:
        name: e4_computer_engineering.beegfs.metad
      vars:
        metad_beegfs_version: "{{ beegfs_version }}"
        metad_auth_file_path: "{{ auth_file }}"
        metad_server_targets:
          - target_id: "1"
            device: "sdb"
            sys_mgmtd_host: "{{ mgmt_host }}"

    - name: Deploy Storage Service
      ansible.builtin.include_role:
        name: e4_computer_engineering.beegfs.storaged
      vars:
        storaged_beegfs_version: "{{ beegfs_version }}"
        storaged_auth_file_path: "{{ auth_file }}"
        storaged_server_targets:
          - target_id: "1"
            device: "sdc"
            sys_mgmtd_host: "{{ mgmt_host }}"

    - name: Deploy Client
      ansible.builtin.include_role:
        name: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "{{ beegfs_version }}"
        client_auth_file_path: "{{ auth_file }}"
        client_clusters:
          - sys_mgmtd_host: "{{ mgmt_host }}"
```

### Multi-Cluster Client Configuration

Configure a client to access multiple BeeGFS clusters:

```yaml
# deploy_multi_cluster_client.yml
---
- name: Deploy BeeGFS client with multi-cluster support
  hosts: compute_nodes
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          # First cluster - production data
          - sys_mgmtd_host: mgmt-prod-01
            conn_client_port_udp: "8004"
            conn_helperd_port_tcp: "8006"
            conn_mgmtd_port_tcp: "8008"
            conn_mgmtd_port_udp: "8008"
            conn_interfaces: ["eth0"]
            client_dir_paths:
              - beegfs_path: production
                fs_path: /mnt/beegfs-prod

          # Second cluster - scratch data
          - sys_mgmtd_host: mgmt-scratch-01
            conn_client_port_udp: "8014"
            conn_helperd_port_tcp: "8016"
            conn_mgmtd_port_tcp: "8018"
            conn_mgmtd_port_udp: "8018"
            conn_interfaces: ["eth1"]
            client_dir_paths:
              - beegfs_path: scratch
                fs_path: /scratch
```

### Advanced Configuration Examples

#### Client with TCP (Disable RDMA)

Deploy BeeGFS client using TCP/IP networking instead of RDMA:

```yaml
- name: Deploy BeeGFS Clients with TCP (disable RDMA)
  hosts: clients
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_rdma_enabled: false
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          - sys_mgmtd_host: mgmt-01
            conn_interfaces: ["eth0"]
            conn_use_rdma: "false"
            conn_tcp_fallback_enabled: "true"
```

#### Client with RDMA Support

Deploy BeeGFS client with InfiniBand/RDMA for high-performance networking:

```yaml
- name: Deploy BeeGFS Clients with RDMA
  hosts: clients
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_rdma_enabled: true
        client_ofed_libs_path: /usr/src/ofa_kernel/default/include
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          - sys_mgmtd_host: mgmt-01
            conn_interfaces: ["ib0"]
            conn_use_rdma: "true"
            conn_rdma_buf_size: "16384"
            conn_rdma_buf_num: "128"
```

#### Client with DKMS Installation

Deploy BeeGFS client with DKMS support for automatic kernel module rebuilds:

```yaml
- name: Deploy BeeGFS Clients with DKMS
  hosts: clients
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_dkms_install: true
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          - sys_mgmtd_host: mgmt-01
            conn_interfaces: ["eth0"]
```

#### Client with NVIDIA GPU Direct Support

Deploy BeeGFS client with NVIDIA GPU Direct Storage for direct GPU memory
access:

```yaml
- name: Deploy BeeGFS Clients with GPU Direct
  hosts: gpu_nodes
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_rdma_enabled: true
        client_nvfs_libs_path: /usr/src/nvidia-fs
        client_nvidia_libs_path: /usr/src/nvidia
        client_ofed_libs_path: /usr/src/ofa_kernel/default/include
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          - sys_mgmtd_host: mgmt-01
            conn_interfaces: ["ib0"]
            conn_use_rdma: "true"
```

#### Client with Custom Mount Points and Chunk Size

Deploy BeeGFS client with custom mount points, custom chunk size, and
properly tuned RDMA buffers:

```yaml
- name: Deploy BeeGFS Clients with custom mount points
  hosts: clients
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          - sys_mgmtd_host: mgmt-01
            conn_interfaces: ["eth0"]
            # RDMA buffer configuration for 1Mi chunk size
            # Formula: conn_rdma_buf_size × conn_rdma_buf_num must be >= chunk_size
            # 16384 × 70 = 1146880 bytes >= 1048576 bytes (1Mi)
            conn_rdma_buf_size: "16384"
            conn_rdma_buf_num: "70"
            # Cache buffer should be a multiple of chunk size
            # 2097152 = 2Mi (2 × 1Mi chunk size)
            tune_file_cache_buf_size: "2097152"
            client_dir_paths:
              # Mount /work with 1Mi chunk size and RAID0 striping
              - beegfs_path: work
                fs_path: /mnt/beegfs/work
                chunk_size: 1m
                pattern: raid0
              # Mount /scratch with default settings
              - beegfs_path: scratch
                fs_path: /scratch
```

#### With Quota Enforcement

```yaml
- name: Deploy BeeGFS Management with quota enforcement
  hosts: management
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.mgmtd
      vars:
        mgmtd_beegfs_version: "8.1"
        mgmtd_auth_file_path: playbooks/files/conn.auth
        mgmtd_quota_enable_enforcement: "true"

- name: Deploy BeeGFS Metadata with quota enforcement
  hosts: metadata
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.metad
      vars:
        metad_beegfs_version: "8.1"
        metad_auth_file_path: playbooks/files/conn.auth
        metad_server_targets:
          - target_id: "1"
            device: "nvme0n1"
            sys_mgmtd_host: mgmt-01
            quota_enable_enforcement: "true"

- name: Deploy BeeGFS Storage with quota enforcement
  hosts: storage
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.storaged
      vars:
        storaged_beegfs_version: "8.1"
        storaged_auth_file_path: playbooks/files/conn.auth
        storaged_server_targets:
          - target_id: "1"
            device: "sdb"
            sys_mgmtd_host: mgmt-01
            quota_enable_enforcement: "true"

- name: Configure clients for quota
  hosts: clients
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.client
      vars:
        client_beegfs_version: "8.1"
        client_auth_file_path: playbooks/files/conn.auth
        client_clusters:
          - sys_mgmtd_host: mgmt-01
            quota_enabled: "true"
```

#### Disable TLS for gRPC (BeeGFS 8.x)

```yaml
- name: Deploy BeeGFS Management without TLS
  hosts: management
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.mgmtd
      vars:
        mgmtd_beegfs_version: "8.1"
        mgmtd_auth_file_path: playbooks/files/conn.auth
        mgmtd_enable_tls: false
```

#### Populate /etc/hosts (Optional)

```yaml
- name: Deploy BeeGFS with /etc/hosts population
  hosts: all
  become: true
  roles:
    - role: e4_computer_engineering.beegfs.mgmtd
      vars:
        mgmtd_beegfs_version: "8.1"
        mgmtd_auth_file_path: playbooks/files/conn.auth
        mgmtd_populate_etc_hosts: true
```

### Example Inventory

```yaml
# inventory.yml
all:
  children:
    management:
      hosts:
        mgmt-01:
          ansible_host: 192.168.1.10

    monitoring:
      hosts:
        mgmt-01:
          ansible_host: 192.168.1.10

    metadata:
      hosts:
        meta-01:
          ansible_host: 192.168.1.20
        meta-02:
          ansible_host: 192.168.1.21

    storage:
      hosts:
        storage-01:
          ansible_host: 192.168.1.30
        storage-02:
          ansible_host: 192.168.1.31
        storage-03:
          ansible_host: 192.168.1.32
        storage-04:
          ansible_host: 192.168.1.33

    clients:
      hosts:
        compute-[01:10]:
          ansible_host: 192.168.1.[40:49]

  vars:
    ansible_user: ansible
    ansible_become: true
```

## Security Considerations

> **WARNING**: By default the collection will deploy a cluster authentication file `/etc/beegfs/connauthfile` that is already present in the [_common role](roles/_common/files/connauthfile). You should create your own.
>
> **WARNING**: By default the collection will generate and deploy TLS certificates from the Ansible controller. If you don't want this to happen, you need to have the certificate files already present in the Ansible controller node `_common_tls_tmp_dir/_common_tls_cert_file`.
