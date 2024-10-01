# Файл динамических переменных terraform.tfvars
# Переменные используются в файле main.tf

# Общие переменные для group1 (VM-2, VM-3)
# Стек технологий (Ubuntu 22.04, proxy-Nginx, Zabbix-Server, Keepalived, ZooKeeper, HAProxy)
group1_vm_cpu    = 2  # Количество ядер процессора
group1_ram       = 2  # Объем оперативной памяти (в ГБ)
group1_disk_size = 21 # Объем диска (в ГБ)
group1_OC_template  = "fd85bll745cg76f707mq" # Ubuntu 22.04
group1_preemptible = true  # Прерываемость ВМ
group1_zone = "ru-central1-a"  # Зона, где будет создана ВМ
group1_unique_names = {
  "vm-2" = "vm-2-Ubuntu-22.04-Nginx-Zabbix-Keepalived-ZooKeeper-HAProxy"
  "vm-3" = "vm-3-Ubuntu-22.04-Nginx-Zabbix-Keepalived-ZooKeeper-HAProxy"
  "description" = ""
}

# Общие переменные для group2 (VM-4)
# Стек технологий (Ubuntu 22.04, MediaWiki)
group2_vm_cpu    = 2  # Количество ядер процессора
group2_ram       = 4  # Объем оперативной памяти (в ГБ)
group2_disk_size = 22 # Объем диска (в ГБ)
group2_OC_template  = "fd85bll745cg76f707mq" # Ubuntu 22.04
group2_preemptible = true  # Прерываемость ВМ
group2_zone = "ru-central1-a"  # Зона, где будет создана ВМ
group2_unique_names = {
  "vm-4" = "vm-4-Ubuntu-22.04-MediaWiki"
  "description" = ""
}


# Общие переменные для group3 (VM-5, VM-6)
# Стек технологий (Ubuntu 22.04, MediaWiki, PostgreSQL)
group3_vm_cpu    = 2  # Количество ядер процессора
group3_ram       = 8  # Объем оперативной памяти (в ГБ)
group3_disk_size = 23 # Объем диска (в ГБ)
group3_OC_template  = "fd85bll745cg76f707mq" # Ubuntu 22.04
group3_preemptible = true  # Прерываемость ВМ
group3_zone = "ru-central1-a"  # Зона, где будет создана ВМ

group3_unique_names = {
  "vm-5" = "vm-5-Ubuntu-22.04-MediaWiki-PostgreSQL"
  "vm-6" = "vm-6-Ubuntu-22.04-MediaWiki-PostgreSQL"
  "description" = ""
}

# Общие переменные для group4 (HDD-1)
group4_zone = "ru-central1-a"  # Зона, где будет создан диск
group4_type = "network-hdd"  # Тип диска, HDD
group4_disk_size = 24 # Объем диска (в ГБ)
group4_unique_names = {
  "hdd-1" = "hdd-1-disk"
  "description" = "Внешний магнитный жесткий диск для dump'ов БД"
}