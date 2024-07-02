Beegfs System Ansible Role
=========

This is role is used to configure the base system of the nodes making up the Beegfs cluster. For base system we intend those tasks that are common to all the other roles and does not necessarly mean system tuning.

It is compatible with the Beegfs versions specvified in the `system_beegfs_version` variable choices and RedHat and Rocky 8.X and Ubuntu Jammy LTS.

Requirements
------------

In order to secure correctly the cluster, the authentication file needs to be the same generated for all the cluster services:

```text
# pwd
beegfs/roles/client
dd if=/dev/random of=./files/connauthfile bs=128 count=1
```

>WARNING: do not use the authfile provided in this role.

Role Variables
--------------

Check the [argument_specs file](meta/argument_specs.yml) or consult the wiki pages.

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
