# Переменные по-умолчанию, используемые всеми группами

vm_cpu        = 2  # Количество ядер процессора по умолчанию
core_fraction = 50 # Гарантированная доля vCPU (%)
ram           = 2  # Объем оперативной памяти по умолчанию
disk_type     = "network-hdd" # Тип диска по умолчанию
disk_size     = 20 # Объем диска по умолчанию
OC_template   = "fd8903kfblsnlo483hoj" # Ubuntu 22.04
preemptible   = true  # Прерываемость ВМ по умолчанию
zone          = "ru-central1-a"  # Зона для всех ВМ
network_id    = "enpq8hrot41agq9ug68l"
subnet_id     = "e9bsdtj7vme4iddaq7qb"
nat           = true
description   = "Описание"

# Специцикация параметров для каждой группы ВМ
# У каждой группы уникальные имена ВМ, описание и пр.

vm_groups = {
  group1_monitoring_system = {
    description = "Система мониторинга Zabbix-Server"
    vm_names    = { "vm-1" = "vm-01" }
    disk_names  = { "vm-1" = "vm-01-disk" }
    disk_size   = 21
  },
  group2_nginx_proxy_servers = {
    description = "Proxy-серверы Nginx для перераспределения пользовательских запросов между серверами MediaWiki"
    vm_names    = { "vm-2" = "vm-02", "vm-5" = "vm-05" }
    disk_names  = { "vm-2" = "vm-02-disk", "vm-5" = "vm-05-disk",}
    disk_size   = 22
  },
  group3_mediawiki_servers = {
    description = "Серверы MediaWiki"
    vm_names    = { "vm-3" = "vm-03", "vm-4" = "vm-04" }
    disk_names  = { "vm-3" = "vm-03-disk", "vm-4" = "vm-04-disk" }
    disk_size   = 23
  },
  group4_haproxy_proxy_servers = {
    description = "Прокси-серверы Haproxy для перераспределения запросов с серверов MediaWiki между БД"
    vm_names    = { "vm-5" = "vm-05" }
    disk_names  = { "vm-5" = "vm-05-disk" }
    disk_size   = 24
  }
}

external_disk_groups = {
  group1_external_vhdd_1 = {
    description = "Внешние магнитные жесткие диски для системы мониторинга"
    disk_names  = { "vhdd-1" = "vhdd-01-disk" }
    disk_size   = 25
  },
  group2_external_vhdd_2 = {
    description = "Внешние магнитные жесткие диски для standby БД"
    disk_names  = { "vhdd-2" = "vhdd-02-disk" }
    disk_size   = 26
  },
  group3_external_vssd_1 = {
    description = "Внешние твердотельные жесткие диски для Primary БД"
    disk_names   = { "vssd-1" = "vssd-01-disk" }
    disk_type   = "network-ssd"
    disk_size   = 27
  }
}