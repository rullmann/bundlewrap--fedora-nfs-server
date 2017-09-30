pkg_dnf = {
    "nfs-utils": {},
    "libnfsidmap": {},
}

svc_systemd = {
    'nfs-server': {
        'needs': [
            "pkg_dnf:nfs-utils",
        ],
    },
    'rpcbind': {
        'needs': [
            "pkg_dnf:nfs-utils",
        ],
    },
    'rpc-statd': {
        'needs': [
            "pkg_dnf:nfs-utils",
        ],
    },
    'nfs-idmapd': {
        'needs': [
            "pkg_dnf:nfs-utils",
        ],
    },
}

files = {}

actions = {
    'nfs_export': {
        'command': "exportfs -a",
        'triggered': True,
        'needs': [
            "pkg_dnf:nfs-utils",
        ],
    },
}

for export in node.metadata['nfs-server']['exports']:
    files["/etc/exports.d/{}".format(export['alias'])] = {
        'source': "template",
        'mode': "0644",
        'content_type': "mako",
        'context': {
            'export': export,
        },
        'needs': [
            "pkg_dnf:nfs-utils",
        ],
        'triggers': [
            "action:nfs_export",
            "svc_systemd:nfs-server:restart",
            "svc_systemd:rpcbind:restart",
        ],
    }

if node.has_bundle("firewalld"):
    if node.metadata.get('nfs-server', {}).get('firewalld_permitted_zones'):
        for zone in node.metadata.get('nfs-server', {}).get('firewalld_permitted_zones'):
            actions['firewalld_add_nfs_zone_{}'.format(zone)] = {
                'command': "firewall-cmd --permanent --zone={} --add-service=nfs".format(zone),
                'unless': "firewall-cmd --zone={} --list-services | grep nfs".format(zone),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:firewalld",
                ],
                'triggers': [
                    "action:firewalld_reload",
                ],
            }
            actions['firewalld_add_mountd_zone_{}'.format(zone)] = {
                'command': "firewall-cmd --permanent --zone={} --add-service=mountd".format(zone),
                'unless': "firewall-cmd --zone={} --list-services | grep mountd".format(zone),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:firewalld",
                ],
                'triggers': [
                    "action:firewalld_reload",
                ],
            }
            actions['firewalld_add_rpc-bind_zone_{}'.format(zone)] = {
                'command': "firewall-cmd --permanent --zone={} --add-service=rpc-bind".format(zone),
                'unless': "firewall-cmd --zone={} --list-services | grep rpc-bind".format(zone),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:firewalld",
                ],
                'triggers': [
                    "action:firewalld_reload",
                ],
            }
    elif node.metadata.get('firewalld', {}).get('default_zone'):
        default_zone = node.metadata.get('firewalld', {}).get('default_zone')
        actions['firewalld_add_nfs_zone_{}'.format(default_zone)] = {
            'command': "firewall-cmd --permanent --zone={} --add-service=nfs".format(default_zone),
            'unless': "firewall-cmd --zone={} --list-services | grep nfs".format(default_zone),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
        actions['firewalld_add_mountd_zone_{}'.format(default_zone)] = {
            'command': "firewall-cmd --permanent --zone={} --add-service=mountd".format(default_zone),
            'unless': "firewall-cmd --zone={} --list-services | grep mountd".format(default_zone),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
        actions['firewalld_add_rpc-bind_zone_{}'.format(default_zone)] = {
            'command': "firewall-cmd --permanent --zone={} --add-service=rpc-bind".format(default_zone),
            'unless': "firewall-cmd --zone={} --list-services | grep rpc-bind".format(default_zone),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
    elif node.metadata.get('firewalld', {}).get('custom_zones', False):
        for interface in node.metadata['interfaces']:
            custom_zone = node.metadata.get('interfaces', {}).get(interface).get('firewalld_zone')
            actions['firewalld_add_nfs_zone_{}'.format(custom_zone)] = {
                'command': "firewall-cmd --permanent --zone={} --add-service=nfs".format(custom_zone),
                'unless': "firewall-cmd --zone={} --list-services | grep nfs".format(custom_zone),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:firewalld",
                ],
                'triggers': [
                    "action:firewalld_reload",
                ],
            }
            actions['firewalld_add_mountd_zone_{}'.format(custom_zone)] = {
                'command': "firewall-cmd --permanent --zone={} --add-service=mountd".format(custom_zone),
                'unless': "firewall-cmd --zone={} --list-services | grep mountd".format(custom_zone),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:firewalld",
                ],
                'triggers': [
                    "action:firewalld_reload",
                ],
            }
            actions['firewalld_add_rpc-bind_zone_{}'.format(custom_zone)] = {
                'command': "firewall-cmd --permanent --zone={} --add-service=rpc-bind".format(custom_zone),
                'unless': "firewall-cmd --zone={} --list-services | grep rpc-bind".format(custom_zone),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:firewalld",
                ],
                'triggers': [
                    "action:firewalld_reload",
                ],
            }
    else:
        actions['firewalld_add_nfs'] = {
            'command': "firewall-cmd --permanent --add-service=nfs",
            'unless': "firewall-cmd --list-services | grep nfs",
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
        actions['firewalld_add_mountd'] = {
            'command': "firewall-cmd --permanent --add-service=mountd",
            'unless': "firewall-cmd --list-services | grep mountd",
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
        actions['firewalld_add_rpc-bind'] = {
            'command': "firewall-cmd --permanent --add-service=rpc-bind",
            'unless': "firewall-cmd --list-services | grep rpc-bind",
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
