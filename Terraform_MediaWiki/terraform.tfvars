vm_cpu        = 2                        # Кол-во ядер процессора по-умолчанию
core_fraction = 20                       # Базовый уровень производительности vCPU (%)
ram           = 2                        # Оперативная память в ГБ
image_id      = "fd8903kfblsnlo483hoj"   # Ubuntu 22.04
preemptible   = "true"                   # Прерываемость
zone          = "ru-central1-a"
network_id    = "enpq8hrot41agq9ug68l"
subnet_id     = "e9bsdtj7vme4iddaq7qb"
nat           = "true"
disk_size     = 15                       # Объём диска в ГБ
disk_type     = "network-hdd"            # Тип диска
      


virtual_machines = {
    "vm-1" = {
      vm_name       = "vm-1-monitoring-system"             # Имя ВМ
      vm_desc       = "Система мониторинга Zabbix-Server"  # Описание
      disk_name     = "vm-1-disk"                          # Название диска
      disk_size     = 21                                   # Объём диска в ГБ
      external_disk = ["vhdd-1"]
    },
    "vm-2" = {
      vm_name       = "vm-2-proxy-server"                  # Имя ВМ
      vm_desc       = "Nginx proxy server"                 # Описание
      disk_name     = "vm-2-disk"                          # Название диска
      disk_size     = 22                                   # Объём диска в ГБ
    },
    "vm-3" = {
      vm_name       = "vm-3-mediawiki-server-1"            # Имя ВМ
      vm_desc       = "MediaWiki server-1"                 # Описание
      disk_name     = "vm-3-disk"                          # Название диска
      disk_size     = 23                                   # Объём диска в ГБ
    },
    "vm-4" = {
      vm_name       = "vm-4-mediawiki-server-2"            # Имя ВМ
      vm_desc       = "MediaWiki server-2"                 # Описание
      disk_name     = "vm-4-disk"                          # Название диска
      disk_size     = 24                                   # Объём диска в ГБ
    },
    "vm-5" = {
      vm_name       = "vm-5-proxy-server"                  # Имя ВМ
      vm_desc       = "Haproxy proxy server-2"             # Описание
      disk_name     = "vm-5-disk"                          # Название диска
      disk_size     = 25                                   # Объём диска в ГБ
    },
    "vm-6" = {
      vm_name       = "vm-6-primary-db"                    # Имя ВМ
      vm_desc       = "PostgreSQL Primary db"              # Описание
      disk_name     = "vm-6-disk"                          # Название диска
      disk_size     = 26                                   # Объём диска в ГБ
      external_disk = ["vssd-1"]
    },
    "vm-7" = {
      vm_name       = "vm-7-standby-db"                    # Имя ВМ
      vm_desc       = "PostgreSQL Standby db"              # Описание
      disk_name     = "vm-7-disk"                          # Название диска
      disk_size     = 27                                   # Объём диска в ГБ
      external_disk = ["vhdd-2", "vhdd-3"]
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