=======================
e4_computer_engineering.beegfs Release Notes
=======================

.. contents:: Topics

v1.0.0
======

Release Summary
---------------

| Release Date: 2024-07-05
| This is the first proper release of the ``e4_computer_engineering.beegfs`` collection

New Playbooks
-------------

- e4_computer_engineering.beegfs.client.yml - Execute the Beegfs.client role.
- e4_computer_engineering.beegfs.cluster.yml - Execute the Beegfs.cluster role.
- e4_computer_engineering.beegfs.metad.yml - Execute the Beegfs.metad role.
- e4_computer_engineering.beegfs.mgmtd.yml - Execute the Beegfs.mgmtd role.
- e4_computer_engineering.beegfs.mon.yml - Execute the Beegfs.mon role.
- e4_computer_engineering.beegfs.site.yml - Execute all the playbooks in `playbooks/` directory in the correct order to deploy a Beegfs cluster.
- e4.beegfs.storaged.yml - Execute the Beegfs.storaged role.

New Roles
---------

- e4_computer_engineering.beegfs.client - Deploy Beegfs client services.
- e4_computer_engineering.beegfs.cluster - Configure Beegfs cluster features.
- e4_computer_engineering.beegfs.metad - Configure Beegfs Metadata services.
- e4_computer_engineering.beegfs.mgmtd - Configure Beegfs Management services.
- e4_computer_engineering.beegfs.mon - Configure Beegfs Monitoring services.
- e4_computer_engineering.beegfs.storaged - Configure Beegfs Storage services.
- e4_computer_engineering.beegfs.system - Configure Beegfs base system.
