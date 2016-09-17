pkg_yum = {
    "nfs-utils": {},
    "libnfsidmap": {},
}

svc_systemd = {
    'nfs-server': {
        'enabled': True,
        'needs': [
            "pkg_yum:nfs-utils",
        ],
    },
    'rpcbind': {
        'enabled': True,
        'needs': [
            "pkg_yum:nfs-utils",
        ],
    },
    'rpc-statd': {
        'enabled': True,
        'needs': [
            "pkg_yum:nfs-utils",
        ],
    },
    'nfs-idmapd': {
        'enabled': True,
        'needs': [
            "pkg_yum:nfs-utils",
        ],
    },
}

files = {}

actions = {
    'nfs_export': {
        'command': "exportfs -a",
        'triggered': True,
        'needs': [
            "pkg_yum:nfs-utils",
        ],
    },
}

for export in node.metadata['fedora-nfs-server']['exports']:
    files["/etc/exports.d/{}".format(export['alias'])] = {
        'source': "template",
        'owner': "root",
        'group': "root",
        'mode': "0644",
        'content_type': "mako",
        'context': {
            'export': export,
        },
        'needs': [
            "pkg_yum:nfs-utils",
        ],
        'triggers': [
            "action:nfs_export",
            "svc_systemd:nfs-server:restart",
            "svc_systemd:rpcbind:restart",
        ],
    }
