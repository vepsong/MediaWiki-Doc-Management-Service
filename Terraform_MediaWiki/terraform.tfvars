# Общие переменные для всех групп ВМ
vm_cpu        = 2  # Количество ядер процессора по умолчанию
core_fraction = 50 # Гарантированная доля vCPU (%)
ram           = 2  # Объем оперативной памяти по умолчанию
disk_size     = 20 # Объем диска по умолчанию
OC_template   = "fd8903kfblsnlo483hoj" # Ubuntu 22.04
preemptible   = true  # Прерываемость ВМ по умолчанию
zone          = "ru-central1-a"  # Зона для всех ВМ
network_id    = "enpq8hrot41agq9ug68l"
subnet_id     = "e9bsdtj7vme4iddaq7qb"
nat           = true


# Параметры для всех групп
vm_groups = {
  group1 = {
    description = "Ubuntu 22.04, Nginx, Zabbix, Keepalived, ZooKeeper, HAProxy"
    vm_names    = { "vm-2" = "vm-02", "vm-3" = "vm-03" }
    disk_size     = 21
    disks       = { "vm-2" = "vm-02-disk", "vm-3" = "vm-03-disk" }
  },
  group2 = {
    description = "Ubuntu-22.04, MediaWiki"
    vm_names    = { "vm-4" = "vm-04" }
    disk_size     = 22
    disks       = { "vm-4" = "vm-04-disk" }
  },
  group3 = {
    description = "Ubuntu-22.04, MediaWiki, PostgreSQL"
    vm_names    = { "vm-5" = "vm-05" }
    disk_size     = 23
    disks       = { "vm-5" = "vm-05-disk" }
  },
  group4 = {
    description = "Ubuntu-22.04, MediaWiki, PostgreSQL"
    vm_names    = { "vm-6" = "vm-06" }
    disk_size     = 24
    disks       = { "vm-6" = "vm-06-disk" }
  },
  group5 = {
    description = "Внешний магнитный жесткий диск"
    disk_type   = "network-hdd"
    disk_size   = 25
    disks       = { "hdd-1" = "hdd-01-disk", "hdd-2" = "hdd-02-disk" }
  }
}