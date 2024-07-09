# Ansible Collection - e4_computer_engineering.beegfs

[![License](https://img.shields.io/badge/license-Apache%20V2-blue.svg)](https://github.com/E4-Computer-Engineering/beegfs/blob/main/LICENSE)
[![Documentation](https://github.com/E4-Computer-Engineering/beegfs-ansible/actions/workflows/DocsPush.yml/badge.svg)](https://e4-computer-engineering.github.io/beegfs-ansible/branch/main)

This Ansible collection aims to deploy Beegfs cluster components in the following scenarios:

* single node cluster: a node that runs all [Beegfs components](#components)
* multi node cluster: the Beegfs services are running on different nodes
* multiple clusters in single or multi node: a single Beegfs client node can be part of two or more Beegfs clusters in single or multi node

This collection takes care of deployng the following [Beegfs features](https://doc.beegfs.io/latest/architecture/overview.html):

* Storage pools
* Buddy Mirroring
* Striping rules and custom mountpoints
* Beeond
* Monitoring service

This collection is compatible with the Beegfs versions allowed by the variable [system_beegfs_version](roles/system/meta/argument_specs.yml) of the system role.

Collection documentation is available [here](https://e4-computer-engineering.github.io/beegfs-ansible/branch/main/).

## Components

* Management: There can be only one cluster handled by a management instance
* Monitoring: There can be only one cluster handled by a monitoring instance
* Metadata: There can be multiple clusters referring to multiple metadata servers on a single node
* Storage: There can be multiple clusters referring to multiple storage servers on a single node
* Client: A client instance is able to handle connectivity to one or multiple clusters

## Deploying the whole cluster

To deploy a whole cluster with, the [site playbook](playbooks/site.yml) should be used, this will esnure the correct ordering and timing for all the Beegfs components.

In the [extensions directory](extensions/molecule/) it is possible to see examples of inventories and variables, such as: the `default` molecule scenario (deploy two single node Beegfs clusters), `buddy_mirror`...

>WARNING: By default the collection will deploy a cluster authentication file `/etc/beegfs/connauthfile` that is already present in the [system role](roles/system/files/connauthfile). You should create your own.
