# bundlewrap-nfs-server

`bundlewrap-nfs-server` installs various packages and services required for running an NFS server.
Additionally it is possible to to define 1 to n exports.

(!) Please note that this bundle doesn't work on CentOS and RHEL 7 die to this bug: https://bugs.centos.org/view.php?id=9753

## Maintenance notice

As of February 2018 this bundle will not be mainained anymore. If you encounter any issues I cannot help.

## Integrations

* Bundles:
  * [firewalld](https://github.com/rullmann/bundlewrap-firewalld)
    * Zone settings from firewalld bundle will be used, if you do not overwrite this behaviour in the metdata.

## Metadata

    'metadata': {
        'fedora-nfs-server': {
            'firewalld_permitted_zones': [ "public", "internal" ], # optional, will override zone settings from firewalld
            'exports': [
                {
                    'alias': "tmptest",
                    'path': "/tmp/",
                    'allowed': "172.16.88.1/24", # single ip or net
                    'options': "ro,sync,no_root_squash", # optional
                },
            ],
        },
    }
