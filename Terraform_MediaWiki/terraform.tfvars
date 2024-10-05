# Файл динамических переменных terraform.tfvars
# Переменные используются в файле main.tf


# Общие переменные для group1 (VM-2, VM-3)
# Стек технологий (Ubuntu 22.04, proxy-Nginx, Zabbix-Server, Keepalived, ZooKeeper, HAProxy)
group1_vm_cpu    = 2  # Количество ядер процессора
group1_ram       = 4  # Объем оперативной памяти (в ГБ)
group1_disk_size = 21 # Объем диска (в ГБ)

# ID образа ОС для использования.
# При необходимости, id всех образов доступны по команде:
# yc compute image list --folder-id standard-images
group1_OC_template  = "fd8903kfblsnlo483hoj" # Ubuntu 22.04

group1_preemptible = true  # Прерываемость ВМ
group1_zone = "ru-central1-a"  # Зона, где будет создана ВМ
group1_description = "Ubuntu 22.04, Nginx, Zabbix, Keepalived, ZooKeeper, HAProxy"

# Уникальные имена для ВМ в group1
group1_unique_vm_names = {
  "vm-2" = "vm-02"
  "vm-3" = "vm-03"
}

# Уникальные имена для дисков ВМ в group1
group1_unique_disks_names = {
  "vm-2" = "vm-02-disk"
  "vm-3" = "vm-03-disk"
}

# Идентификаторы сети group1
group1_network = {
   "existing_network_id" = "enpq8hrot41agq9ug68l"
   "existing_subnet_id" = "e9bsdtj7vme4iddaq7qb"
}


# Общие переменные для group2 (VM-4)
# Стек технологий (Ubuntu 22.04, MediaWiki)
group2_vm_cpu    = 2  # Количество ядер процессора
group2_ram       = 4  # Объем оперативной памяти (в ГБ)
group2_disk_size = 22 # Объем диска (в ГБ)
group2_OC_template  = "fd8903kfblsnlo483hoj" # Ubuntu 22.04
group2_preemptible = true  # Прерываемость ВМ
group2_zone = "ru-central1-a"  # Зона, где будет создана ВМ
group2_description = "Ubuntu-22.04, MediaWiki"

# Уникальные имена для ВМ в group2
group2_unique_vm_names = {
  "vm-4" = "vm-04"
}

# Уникальные имена для дисков ВМ в group2
group2_unique_disks_names = {
  "vm-4" = "vm-04-disk"
}

# Идентификаторы сети group2
group2_network = {
   "existing_network_id" = "enpq8hrot41agq9ug68l"
   "existing_subnet_id" = "e9bsdtj7vme4iddaq7qb"
}


# Общие переменные для group3 (VM-5)
# Стек технологий (Ubuntu 22.04, MediaWiki, PostgreSQL)
group3_vm_cpu    = 2  # Количество ядер процессора
group3_ram       = 8  # Объем оперативной памяти (в ГБ)
group3_disk_size = 23 # Объем диска (в ГБ)
group3_OC_template  = "fd8903kfblsnlo483hoj" # Ubuntu 22.04
group3_preemptible = true  # Прерываемость ВМ
group3_zone = "ru-central1-a"  # Зона, где будет создана ВМ
group3_description = "Ubuntu-22.04, MediaWiki, PostgreSQL"

# Уникальные имена для ВМ в group3
group3_unique_vm_names = {
  "vm-5" = "vm-05"
}

# Уникальные имена для дисков ВМ в group3
group3_unique_disks_names = {
  "vm-5" = "vm-05-disk"
}

# Идентификаторы сети group3
group3_network = {
   "existing_network_id" = "enpq8hrot41agq9ug68l"
   "existing_subnet_id" = "e9bsdtj7vme4iddaq7qb"
}


# Общие переменные для group4 (VM-6)
# Стек технологий (Ubuntu 22.04, MediaWiki, PostgreSQL)
group4_vm_cpu    = 2  # Количество ядер процессора
group4_ram       = 8  # Объем оперативной памяти (в ГБ)
group4_disk_size = 23 # Объем диска (в ГБ)
group4_OC_template  = "fd8903kfblsnlo483hoj" # Ubuntu 22.04
group4_preemptible = true  # Прерываемость ВМ
group4_zone = "ru-central1-a"  # Зона, где будет создана ВМ
group4_description = "Ubuntu-22.04, MediaWiki, PostgreSQL"


# Уникальные имена для ВМ в group4
group4_unique_vm_names = {
  "vm-6" = "vm-06"
}

# Уникальные имена для дисков ВМ в group4
group4_unique_disks_names = {
  "vm-6" = "vm-06-disk"
}

# Идентификаторы сети group4
group4_network = {
   "existing_network_id" = "enpq8hrot41agq9ug68l"
   "existing_subnet_id" = "e9bsdtj7vme4iddaq7qb"
}



# Общие переменные для group5 (HDD-1)
group5_zone = "ru-central1-a"  # Зона, где будет создан диск
group5_type = "network-hdd"  # Тип диска, HDD
group5_disk_size = 24 # Объем диска (в ГБ)
group5_description = "Внешний магнитный жесткий диск для dump'ов БД"

# Уникальные имена для дисков в group5
group5_unique_disks_names = {
  "hdd-1" = "hdd-01-disk"
}

# Идентификаторы сети group5
group5_network = {
   "existing_network_id" = "enpq8hrot41agq9ug68l"
   "existing_subnet_id" = "e9bsdtj7vme4iddaq7qb"
}