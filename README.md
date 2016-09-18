# bundlewrap-nfs-server

`bundlewrap-nfs-server` installs various packages and services required for running an NFS server.
Additionally it is possible to to define 1 to n exports.

(!) Please note that this bundle doesn't work on CentOS and RHEL 7 die to this bug: https://bugs.centos.org/view.php?id=9753

## Compatibility

This bundle has been tested on the following systems:

| OS          | `[x]` |
| ----------- | ----- |
| Fedora 24   | `[x]` |
| Fedberry 23 | `[ ]` |

## Metadata

    'metadata': {
        'fedora-nfs-server': {
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
