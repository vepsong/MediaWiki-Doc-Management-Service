virtual_machines = {
    "vm-1" = {
      vm_name       = "vm-1-monitoring-system"             # Имя ВМ
      vm_desc       = "Система мониторинга Zabbix-Server"  # Описание
      disk_name     = "vm-1-disk"                          # Название диска
      disk_size     = 21                                   # Объём диска в ГБ
      external_disk = ["vhdd-1"]                           # Внешние жесткие диски
      ip_address    = "192.168.10.11"                      # Cтатичный внутренний IP из данных ВМ
    },
    "vm-2" = {
      vm_name       = "vm-2-proxy-server"                  # Имя ВМ
      vm_desc       = "Nginx proxy server"                 # Описание
      disk_name     = "vm-2-disk"                          # Название диска
      disk_size     = 22                                   # Объём диска в ГБ
      ip_address    = "192.168.10.12"                      # Cтатичный внутренний IP из данных ВМ
    },
    "vm-3" = {
      vm_name       = "vm-3-mediawiki-server-1"            # Имя ВМ
      vm_desc       = "MediaWiki server-1"                 # Описание
      disk_name     = "vm-3-disk"                          # Название диска
      disk_size     = 23                                   # Объём диска в ГБ
      ip_address    = "192.168.10.13"                      # Cтатичный внутренний IP из данных ВМ
    },
    "vm-4" = {
      vm_name       = "vm-4-mediawiki-server-2"            # Имя ВМ
      vm_desc       = "MediaWiki server-2"                 # Описание
      disk_name     = "vm-4-disk"                          # Название диска
      disk_size     = 24                                   # Объём диска в ГБ
      ip_address    = "192.168.10.14"                      # Cтатичный внутренний IP из данных ВМ
    },
    "vm-5" = {
      vm_name       = "vm-5-proxy-server"                  # Имя ВМ
      vm_desc       = "Haproxy proxy server-2"             # Описание
      disk_name     = "vm-5-disk"                          # Название диска
      disk_size     = 25                                   # Объём диска в ГБ
      ip_address    = "192.168.10.15"                      # Cтатичный внутренний IP из данных ВМ
    },
    "vm-6" = {
      vm_name       = "vm-6-primary-db"                    # Имя ВМ
      vm_desc       = "PostgreSQL Primary db"              # Описание
      disk_name     = "vm-6-disk"                          # Название диска
      disk_size     = 26                                   # Объём диска в ГБ
      external_disk = ["vssd-1"]                           # Внешние жесткие диски
      ip_address    = "192.168.10.16"                      # Cтатичный внутренний IP из данных ВМ
    },
    "vm-7" = {
      vm_name       = "vm-7-standby-db"                    # Имя ВМ
      vm_desc       = "PostgreSQL Standby db"              # Описание
      disk_name     = "vm-7-disk"                          # Название диска
      disk_size     = 27                                   # Объём диска в ГБ
      external_disk = ["vhdd-2", "vhdd-3"]                 # Внешние жесткие диски
      ip_address    = "192.168.10.17"                      # Cтатичный внутренний IP из данных ВМ
    }
} 


external_disks = {
    "vhdd-1" = {
      disk_name     = "vhdd-1-monitoring-system-db"        # Имя ВМ
      disk_desc     = "Хранилище БД Zabbix-Server"         # Описание
      disk_size     = 28                                   # Объём диска в ГБ
    },
    "vhdd-2" = {
      disk_name     = "vhdd-2-standby-db"                  # Имя ВМ
      disk_desc     = "Хранилище PostgreSQL Standby db"    # Описание
      disk_size     = 29                                   # Объём диска в ГБ
    },
    "vhdd-3" = {
      disk_name     = "vhdd-3-dump-db"                     # Имя ВМ
      disk_desc     = "Хранилище db_dump"                  # Описание
      disk_size     = 30                                   # Объём диска в ГБ
    },
    "vssd-1" = {
      disk_name     = "vssd-1-primary-db"                  # Имя ВМ
      disk_desc     = "Хранилище PostgreSQL Primary db"    # Описание
      disk_size     = 31                                   # Объём диска в ГБ
      disk_type     = "network-ssd"                        # Тип диска
    }
}