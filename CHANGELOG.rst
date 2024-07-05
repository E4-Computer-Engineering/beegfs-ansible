=======================
E4.Beegfs Release Notes
=======================

.. contents:: Topics

v1.0.0
======

Release Summary
---------------

| Release Date: 2024-07-05
| This is the first proper release of the ``E4.beegfs`` collection

New Playbooks
-------------

- e4.beegfs.client.yml - Execute the Beegfs.client role.
- e4.beegfs.cluster.yml - Execute the Beegfs.cluster role.
- e4.beegfs.metad.yml - Execute the Beegfs.metad role.
- e4.beegfs.mgmtd.yml - Execute the Beegfs.mgmtd role.
- e4.beegfs.mon.yml - Execute the Beegfs.mon role.
- e4.beegfs.site.yml - Execute all the playbooks in `playbooks/` directory in the correct order to deploy a Beegfs cluster.
- e4.beegfs.storaged.yml - Execute the Beegfs.storaged role.

New Roles
---------

- e4.beegfs.client - Deploy Beegfs client services.
- e4.beegfs.cluster - Configure Beegfs cluster features.
- e4.beegfs.metad - Configure Beegfs Metadata services.
- e4.beegfs.mgmtd - Configure Beegfs Management services.
- e4.beegfs.mon - Configure Beegfs Monitoring services.
- e4.beegfs.storaged - Configure Beegfs Storage services.
- e4.beegfs.system - Configure Beegfs base system.
