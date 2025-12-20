# Beegfs Client Ansible Role

This role can be used to deploy Beegfs client(s), `beegfs-client` to nodes: each targeted node is meant to be part of one or more Beegfs clusters but each `beegfs-client` instance can belong to only one cluster.

It is compatible with the Beegfs versions specified in the role `client_beegfs_version` variable choices and RedHat, Almalinux and Rocky 8.X 9.X and Ubuntu Jammy LTS.

## Requirements

> **WARNING**: If quota is required, remember to set it up after the deployment with the command:

```bash
beegfs-fsck --enablequota
```

## Role Variables

Check the [argument_specs file](meta/argument_specs.yml) or consult the wiki pages.

The variables used in the Beegfs configuration files, are documented in such files as well. Since the role overwrite these files, the originals remain available on the target nodes as `<file_name>.<ansible_backup_date>`.

## Dependencies

Check the `dependencies` list in the [meta definitions](meta/main.yml).

## Example Playbook

Check the [playbooks](../../playbooks/) and [extensions](../../extensions/molecule/) directories for examples on how to execute the roles.

### Use NVIDIA Mellanox OFED drives and GPU Direct Storage for client build

```yaml
- name: Configure Beegfs Client
  become: true
  gather_facts: false
  hosts: '{{ client_nodes |default("all") }}'
  vars:
    client_ofed_libs_path: /usr/src/ofa_kernel/default/include
    client_nvfs_libs_path: /usr/src/nvidia-fs-2.13.5
    client_nvidia_libs_path: /usr/src/nvidia-520.61.05/nvidia
  tasks:
    - name: Import Beegfs client role
      ansible.builtin.import_role:
        name: client
```

### Disable RDMA for client builds

```yaml
- name: Configure Beegfs Client
  become: true
  gather_facts: false
  hosts: '{{ client_nodes |default("all") }}'
  vars:
    client_rdma_enabled: false
  tasks:
    - name: Import Beegfs client role
      ansible.builtin.import_role:
        name: client
```

### Configure the client in multimode so it can access two different clusters with two different setups

```yaml
- name: Configure Beegfs Client
  become: true
  gather_facts: false
  hosts: '{{ client_nodes |default("all") }}'
  vars:
    client_clusters:
      - sys_mgmtd_host: beemgmtd-01.lan
        conn_client_port_udp: "8014"
        conn_helperd_port_tcp: "8016"
        conn_mgmtd_port_tcp: "8018"
        conn_mgmtd_port_udp: "8018"
      - sys_mgmtd_host: 10.10.10.7
        conn_client_port_udp: "8064"
        conn_helperd_port_tcp: "8066"
        conn_mgmtd_port_tcp: "8068"
        conn_mgmtd_port_udp: "8068"
        conn_rdma_buf_num: "70"
        conn_rdma_buf_size: "16384"
        tune_file_cache_buf_size: "1048576"
        quota_enabled: "true"
        sys_xattrs_enabled: "true"
        sys_acls_enabled: "true"
  tasks:
    - name: Import Beegfs client role
      ansible.builtin.import_role:
        name: client
```

### Install Beegfs Beeond package

```yaml
- name: Configure Beegfs Client
  become: true
  gather_facts: false
  hosts: '{{ client_nodes |default("all") }}'
  vars:
    client_enable_beeond: true
  tasks:
    - name: Import Beegfs client role
      ansible.builtin.import_role:
        name: client
```

## License

Apache-2.0

## Author Information

<davide.obbi@e4company.com>
