dynamic_groups = {
    "linuxVM": {
        "monitoringSystem": {
            "hosts": ["vm-1-monitoring-system"],
            "external_disks": [
                {
                    "disk_name": "vhdd-1-monitoring-system-db",
                    "mount_point": "/opt/vhdd-1-monitoring-system-db",
                    "filesystem": "ext4"
                }
            ]
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
        "primaryDb": {
            "hosts": ["vm-6-primary-db"],
            "external_disks": [
                {
                    "disk_name": "vssd-1-primary-db",
                    "mount_point": "/opt/vssd-1-primary-db",
                    "filesystem": "ext4"
                }
            ]
        },
        "standbyDb": {
            "hosts": ["vm-7-standby-db"],
            "external_disks": [
                {
                    "disk_name": "vhdd-2-standby-db",
                    "mount_point": "/opt/vhdd-2-standby-db",
                    "filesystem": "ext4"
                },
                {
                    "disk_name": "vhdd-3-dump-db",
                    "mount_point": "/opt/vhdd-3-dump-db",
                    "filesystem": "ext4"
                }
            ]
        }   
    }
}
