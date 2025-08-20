Beegfs Common role
=========

This role is not meant to be called directly and it is used by the other roles that have to perform "common tasks".

Requirements
------------

In order to secure correctly the cluster, the authentication file needs to be the same generated for all the cluster services:

```text
# pwd
beegfs/roles/client
dd if=/dev/random of=./files/conn.auth bs=128 count=1
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
