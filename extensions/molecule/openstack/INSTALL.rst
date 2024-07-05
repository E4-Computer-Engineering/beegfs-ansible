***********************************
Delegated driver installation guide
***********************************

Requirements
============
To use the Openstack Molecule driver you need to have access to the Openstack instance. This can either be specified via the `~/.config/openstack/clouds.yaml` file or the environment variable defined by the `*openrc.sh` script. They are both downloadable from your account menu in the Openstack instance.

Install
=======
By installing the `requirements.yml` you should be ready to go.

Use
===
To make use of the `converge` stage you need to assign your hosts in the inventory to the following groups:

* clients
* management
* metadata
* storage

One host can be in all of the groups at the same time, there are no limitations. To assign a Molecule "platform" to a group, add the `groups` key:

```
platforms:
  - name: myhost
...
    groups:
      - client
```
