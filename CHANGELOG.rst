==============================================
e4\_computer\_engineering.beegfs Release Notes
==============================================

.. contents:: Topics

v2.4.0
======

Minor Changes
-------------

- All roles - add support for BeeGFS ``8.3`` in the ``<role>_beegfs_version`` choices.
- all roles - add the previously undocumented ``<role>_repo_url`` and ``<role>_deploy_auth_file`` variables with defaults and argument specifications.
- client - add the BeeGFS 8.3 only ``tuneFileOpenRetryTimeoutMS`` and ``tuneFileOpenRetryIntervalMS`` client configuration options (``client_tune_file_open_retry_timeout_ms`` and ``client_tune_file_open_retry_interval_ms``), gated to version 8.3 and above.
- metad, storaged - back up the daemon configuration files on change to match the role documentation.
- mgmtd - align the ``beegfs-mgmtd.toml`` template comments and options (``ipv6-disable``, the new ``interfaces`` filter syntax and the ``node-offline-timeout`` note) with upstream BeeGFS 8.3.
- mon - deploy the connection interfaces file referenced by ``beegfs-mon.conf`` when ``mon_conn_interfaces`` is set.

Bugfixes
--------

- _common - harden the TLS certificate generation so the ``san.cnf`` template no longer fails when ``ansible_host`` or ``ansible_default_ipv4`` are undefined, and set the parent role name fact in ``tls.yml`` so it can run standalone.
- client - remove a stray undefined ``beegfs`` condition from the multimode helperd start task.
- client - template the NVIDIA GPUDirect file globs in the prechecks (they were literal strings), so the GDS file presence assertions work.
- metad - fix the filesystem creation and tune2fs task tags that were tagged for the ``storaged`` role.
- mgmtd - fix ``tls-disable`` in ``beegfs-mgmtd.toml`` always rendering ``false`` due to operator precedence, so that setting ``mgmtd_enable_tls`` to ``false`` now correctly disables gRPC TLS.
- mon - fix the ``mon_db_type`` argument specification default (``influxdbv2``) which was not part of its own ``choices``.
- storaged - fix the swapped success and failure messages in the server targets precheck assertion.
- storaged - use ``storaged_beegfs_version`` instead of ``metad_beegfs_version`` in the storage configuration template, fixing rendering on storage-only hosts.

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
