Beegfs Cluster Ansible Role
=========

This role can be used to deploy: storage pools, buddy mirror relationships, directory striping rules and mounts to nodes in the following scenarios:

* single cluster
* multimode (more clusters)

It is compatible with Rocky 8.X and Ubuntu Jammy LTS.

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
