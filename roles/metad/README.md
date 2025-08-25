Beegfs Metadata Ansible Role
=========

This role can be used to deploy Beegfs Metadata service(s), `beegfs-meta` to nodes: each targeted node is meant to be part of one or more Beegfs clusters but each `beegfs-meta` instance can belong to only one cluster.

It is compatible with the Beegfs versions specified in the role `metad_beegfs_version` variable choices and RedHat, Almalinux and Rocky 8.X 9.X and Ubuntu Jammy LTS.

Requirements
------------

n/a

Role Variables
--------------

Check the [argument_specs file](meta/argument_specs.yml) or consult the wiki pages.

The variables used in the Beegfs configuration files, are documented in such files as well. Since the role overwrite these files, the originals remain available on the target nodes as <file_name>.<ansible_backup_date>.

Dependencies
------------

Check the `dependencies` list in the [meta definitions](meta/main.yml).

Example Playbook
----------------

Check the [playbooks](../../playbooks/) and [extensions](../../extensions/molecule/) directories for examples on how to execute the roles.

License
-------

license Apache-2.0

Author Information
------------------

<davide.obbi@e4company.com>
