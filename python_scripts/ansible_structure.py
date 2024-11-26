dynamic_groups = {
    "linuxVM": {
        "monitoringSystem": {
            "hosts": ["vm-1-zabbix-server"],
            "external_disks": {
                "vm-1-zabbix-server": [
                    {
                        "disk_name": "vhdd-1",
                        "mount_point": "/opt/vhdd-1",
                        "filesystem": "ext4"
                    }
                ]
            }
        },
        "nginxProxyServer": {
            "hosts": ["vm-2-nginx-proxy-server"]
        },
        "mediawikiServer": {
            "hosts": ["vm-3-mediawiki-server-1", "vm-4-mediawiki-server-2"]
        },
        "haproxyProxyServer": {
            "hosts": ["vm-5-haproxy-proxy-server"]
        },

        "database": {
            "hosts": ["vm-6-postgresql-db-1", "vm-7-postgresql-db-2"],
            "external_disks": {
                "vm-6-postgresql-db-1": [
                    {
                        "disk_name": "vssd-1",
                        "mount_point": "/opt/vssd-1",
                        "filesystem": "ext4"
                    }
                ],
                "vm-7-postgresql-db-2": [
                    {
                        "disk_name": "vhdd-2",
                        "mount_point": "/opt/vhdd-2",
                        "filesystem": "ext4"
                    },
                    {
                        "disk_name": "vhdd-3",
                        "mount_point": "/opt/vhdd-3",
                        "filesystem": "ext4"
                    }
                ]
            }
        }
    }
}
