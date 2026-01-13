==============================================
e4\_computer\_engineering.beegfs Release Notes
==============================================

.. contents:: Topics

v2.3.0
======

Release Summary
---------------

| Release Date: 2026-01-13
| This release adds new Ansible version and improved target filesystem
| discovery using labels.

v2.2.0
======

Release Summary
---------------

| Release Date: 2025-12-21
| This release adds automated release workflows with GitHub Actions,
| including automatic publishing to Ansible Galaxy and documentation generation.

v2.1.0
======

Release Summary
---------------

| Release Date: 2025-09-23
| Multiple fixes to the v2.0.0 version

v2.0.0
======

Release Summary
---------------

| Release Date: 2025-08-20
| This release supports Beegfs v8 and removes support for components setup like storage-pools, stripe patterns and buddy-mirror.

New Roles
---------

- e4_computer_engineering.beegfs._common - Beegfs roles common tasks.

v1.1.0
======

Release Summary
---------------

| Release Date: 2025-04-29
| This is a new release of the ``e4_computer_engineering.beegfs`` collection
| This release includes the following changes:
| - Add full filesystem integration for metadata and storage targets
| - targetoffline parametrized and interfacefile for daemons
| - beegfs client dkms install

v1.0.4
======

Release Summary
---------------

| Release Date: 2025-04-15
| This is the new release of ``e4_computer_engineering.beegfs`` collection.
| This release includes the following changes:
| - Added support for Beegfs 7.4.6 and 7.2.5
| - Fixed bug with metadata mirrormd command
| - Added support for mgmtd ID mgmtd_string_id:
| - Docs improvement for storage and meta ID specifics
| - Fix to addition of Alma and Rocky Vault repo only if not on latest OS release
| - Manually control the installation of kernel-devel and kernel-headers if needed

v1.0.3
======

Release Summary
---------------

| Release Date: 2025-14-01
| The release includes:
| - support for rhel like distros version 9 including Almalinux.
| - bump of the Beegfs version to 7.4.5.
| - fixes to the client argument_specs file that blocked execution.

v1.0.2
======

Release Summary
---------------

| Release Date: 2024-21-12
| This is the second release update of the ``e4_computer_engineering.beegfs`` collection

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
- e4_computer_engineering.beegfs.site.yml - Execute all the playbooks in `playbooks/` directory \ in the correct order to deploy a Beegfs cluster.
- e4_computer_engineering.beegfs.storaged.yml - Execute the Beegfs.storaged role.

New Roles
---------

- e4_computer_engineering.beegfs.client - Deploy Beegfs client services.
- e4_computer_engineering.beegfs.cluster - Configure Beegfs cluster features.
- e4_computer_engineering.beegfs.metad - Configure Beegfs Metadata services.
- e4_computer_engineering.beegfs.mgmtd - Configure Beegfs Management services.
- e4_computer_engineering.beegfs.mon - Configure Beegfs Monitoring services.
- e4_computer_engineering.beegfs.storaged - Configure Beegfs Storage services.
- e4_computer_engineering.beegfs.system - Configure Beegfs base system.
