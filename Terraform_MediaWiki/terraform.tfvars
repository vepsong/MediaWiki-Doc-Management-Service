virtual_machines = {
    "vm-1" = {
      vm_name       = "vm-1-zabbix-server"                 # VM name
      vm_desc       = "Zabbix Server monitoring system"    # Description
      disk_name     = "vm-1-disk"                          # Disk name
      disk_size     = 21                                   # Disk size (in GB)
      external_disk = ["vhdd-1"]                           # External hard disks
      ip_address    = "192.168.10.11"                      # Static internal IP address
    },
    "vm-2" = {
      vm_name       = "vm-2-nginx-proxy-server"
      vm_desc       = "Nginx proxy server"
      disk_name     = "vm-2-disk"
      disk_size     = 22
      ip_address    = "192.168.10.12"
    },
    "vm-3" = {
      vm_name       = "vm-3-mediawiki-server-1"
      vm_desc       = "MediaWiki server-1"
      disk_name     = "vm-3-disk"
      disk_size     = 23
      ip_address    = "192.168.10.13"
    },
    "vm-4" = {
      vm_name       = "vm-4-mediawiki-server-2"
      vm_desc       = "MediaWiki server-2"
      disk_name     = "vm-4-disk"
      disk_size     = 24
      ip_address    = "192.168.10.14"
    },
    "vm-6" = {
      vm_name       = "vm-6-postgresql-db-1"
      vm_desc       = "PostgreSQL db-1" 
      disk_name     = "vm-6-disk"
      disk_size     = 26
      external_disk = ["vssd-1"]
      ip_address    = "192.168.10.16"
    },
    "vm-7" = {
      vm_name       = "vm-7-postgresql-db-2"
      vm_desc       = "PostgreSQL db-2" 
      disk_name     = "vm-7-disk"
      disk_size     = 27
      external_disk = ["vhdd-2", "vhdd-3"]
      ip_address    = "192.168.10.17"
    }
} 


external_disks = {
    "vhdd-1" = {
      disk_name     = "vhdd-1"
      disk_desc     = "Zabbix Server db storage"
      disk_size     = 28
    },
    "vhdd-2" = {
      disk_name     = "vhdd-2"
      disk_desc     = "MediaWiki db storage"
      disk_size     = 29
    },
    "vhdd-3" = {
      disk_name     = "vhdd-3"
      disk_desc     = "MediaWiki db dump storage"
      disk_size     = 30
    },
    "vssd-1" = {
      disk_name     = "vssd-1"
      disk_desc     = "MediaWiki db storage"
      disk_size     = 31
      disk_type     = "network-ssd"
    }
}