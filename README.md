# Ansible Collection - e4.beegfs


[![License](https://img.shields.io/badge/license-Apache%20V2-blue.svg)](https://github.com/E4-Computer-Engineering/beegfs/blob/main/LICENSE)
[![CI Status](https://github.com/E4-Computer-Engineering/beegfs/actions/workflows/PullRequest.yml/badge.svg)](https://github.com/E4-Computer-Engineering/beegfs/actions/workflows/PullRequest.yml)
[![Docs Status](https://github.com/E4-Computer-Engineering/beegfs/actions/workflows/DocsPush.yml/badge.svg)](https://github.com/E4-Computer-Engineering/beegfs/actions/workflows/DocsPush.yml)

This Ansible collection aims to deploy Beegfs cluster components in the following scenarios:

* single node cluster: a node that runs all [Beegfs components](#components)
* multi node cluster: the Beegfs services are running on different nodes
* multiple clusters in single or multi node: a single Beegfs client node can be part of two or more Beegfs clusters in single or multi node

This collection takes care of deployng the following [Beegfs features](https://doc.beegfs.io/latest/architecture/overview.html):

* Storage pools
* Buddy Mirroring
* Striping rules and custom mountpoints

## Components

* Management: There can be only one cluster handled by a management instance
* Monitoring: There can be only one cluster handled by a monitoring instance
* Metadata: There can be multiple clusters referring to multiple metadata servers on a single node
* Storage: There can be multiple clusters referring to multiple storage servers on a single node
* Client: A client instance is able to handle connectivity to one or multiple clusters

## Collection Documentation

Documentation is made available via [GitHub pages](https://e4-computer-engineering.github.io/beegfs-ansible/branch/main/), details on how to use each component (role,module, plugin) of the collection, are available there.

To use the playbooks refer to the [Ansible documentation](https://docs.ansible.com/ansible/latest/collections_guide/collections_using_playbooks.html).

All the playbooks require passing the target nodes at runtime as [extra-vars](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#id37), available target nodes variables:

| name | description | default |
|---|---|---|
|client_nodes|nodes or groups in your inventory running `beegfs-client` |all|
|mgmt_nodes|nodes or groups in your inventory running `beegfs-mgmtd` |all|
|storage_nodes|nodes or groups in your inventory running `beegfs-storage`|all|
|metadata_nodes|nodes or groups in your inventory running `beegfs-meta`|all|
|monitoring_nodes|nodes or groups in your inventory running `beegfs-mon`|all|

## How to install

To install a release:

```shell
ansible-galaxy collection install git+git@github.com:E4-Computer-Engineering/beegfs-ansible.git/v1.0.0
```

For details refer to the [Ansible documentation](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html#installing-a-collection-from-a-git-repository).
