# Используем цикл for_each, который перебирает значения сначала в variables.tf и потом в terraform.tfvars


# Виртуальные машины для group1 (VM-2, VM-3)
resource "yandex_compute_instance" "group1" {
  for_each = var.group1_unique_vm_names  # Используем уникальные имена для каждой ВМ в group1

  name        = each.value  # Уникальное имя ВМ
  description = "Виртуальная машина ${each.value}"

  resources {
    cores  = var.group1_vm_cpu  # Количество ядер
    memory = var.group1_ram # Оперативная память в GB
  }

  boot_disk {
    initialize_params {
      image_id = var.group1_OC_template  # Шаблон ОС
      size     = var.group1_disk_size  # Размер диска
      name     = var.group1_unique_disks_names[each.key]  # Уникальное имя диска
    }
  }

  scheduling_policy {
    preemptible = var.group1_preemptible  # Прерываемость ВМ
  }

  network_interface {
    subnet_id = var.group1_network["existing_subnet_id"]  # Подсеть
    nat       = true  # Включаем NAT для доступа в интернет
  }

  zone = var.group1_zone  # Зона для создания ВМ

  # metadata = {
  #   user-data = "${file("${path.module}/meta.txt")}"
  # }
  metadata = {
    user-data = <<-EOF
      ${file("${path.module}/meta.txt")}

      # Установка hostname для каждой ВМ
      hostname: ${each.value}

      # Дополнительные команды, если необходимо
      runcmd:
        - echo ${each.value} > /etc/hostname
        - hostnamectl set-hostname ${each.value}
    EOF
  }
}



# Виртуальные машины для group2 (VM-4)
resource "yandex_compute_instance" "group2" {
  for_each = var.group2_unique_vm_names  # Используем уникальные имена для каждой ВМ в group2

  name        = each.value  # Уникальное имя ВМ
  description = "Виртуальная машина ${each.value}"

  resources {
    cores  = var.group2_vm_cpu  # Количество ядер
    memory = var.group2_ram # Оперативная память в GB
  }

  boot_disk {
    initialize_params {
      image_id = var.group2_OC_template  # Шаблон ОС
      size     = var.group2_disk_size  # Размер диска
      name     = var.group2_unique_disks_names[each.key]  # Уникальное имя диска
    }
  }

  scheduling_policy {
    preemptible = var.group2_preemptible  # Прерываемость ВМ
  }

  network_interface {
    subnet_id = var.group2_network["existing_subnet_id"]  # Подсеть
    nat       = true  # Включаем NAT для доступа в интернет
  }

  zone = var.group2_zone  # Зона для создания ВМ

  metadata = {
    user-data = <<-EOF
      ${file("${path.module}/meta.txt")}

      # Установка hostname для каждой ВМ
      hostname: ${each.value}

      # Дополнительные команды, если необходимо
      runcmd:
        - echo ${each.value} > /etc/hostname
        - hostnamectl set-hostname ${each.value}
    EOF
  }
}

# Виртуальные машины для group3 (VM-5)
resource "yandex_compute_instance" "group3" {
  for_each = var.group3_unique_vm_names  # Используем уникальные имена для каждой ВМ в group3

  name        = each.value  # Уникальное имя ВМ
  description = "Виртуальная машина ${each.value}"

  resources {
    cores  = var.group3_vm_cpu  # Количество ядер
    memory = var.group3_ram # Оперативная память в GB
  }

  boot_disk {
    initialize_params {
      image_id = var.group3_OC_template  # Шаблон ОС
      size     = var.group3_disk_size  # Размер диска
      name     = var.group3_unique_disks_names[each.key]  # Уникальное имя диска
    }
  }

  scheduling_policy {
    preemptible = var.group3_preemptible  # Прерываемость ВМ
  }

  network_interface {
    subnet_id = var.group3_network["existing_subnet_id"]  # Подсеть
    nat       = true  # Включаем NAT для доступа в интернет
  }

  zone = var.group3_zone  # Зона для создания ВМ

  metadata = {
    user-data = <<-EOF
      ${file("${path.module}/meta.txt")}

      # Установка hostname для каждой ВМ
      hostname: ${each.value}

      # Дополнительные команды, если необходимо
      runcmd:
        - echo ${each.value} > /etc/hostname
        - hostnamectl set-hostname ${each.value}
    EOF
  }

}

# Виртуальные машины для group4 (VM-6)
resource "yandex_compute_instance" "group4" {
  for_each = var.group4_unique_vm_names  # Используем уникальные имена для каждой ВМ в group4

  name        = each.value  # Уникальное имя ВМ
  description = "Виртуальная машина ${each.value}"

  resources {
    cores  = var.group4_vm_cpu  # Количество ядер
    memory = var.group4_ram # Оперативная память в GB
  }

  boot_disk {
    initialize_params {
      image_id = var.group4_OC_template  # Шаблон ОС
      size     = var.group4_disk_size  # Размер диска
      name     = var.group4_unique_disks_names[each.key]  # Уникальное имя диска
    }
  }

  scheduling_policy {
    preemptible = var.group4_preemptible  # Прерываемость ВМ
  }

  network_interface {
    subnet_id = var.group4_network["existing_subnet_id"]  # Подсеть
    nat       = true  # Включаем NAT для доступа в интернет
  }

  zone = var.group4_zone  # Зона для создания ВМ

  # metadata = {
  #   user-data = "${file("${path.module}/meta.txt")}"
  # }

  # Используем внешний файл для основных метаданных + добавляем команды для монтирования диска
  metadata = {
    user-data = <<-EOF
      ${file("${path.module}/meta.txt")}

      # Установка hostname для каждой ВМ
      hostname: ${each.value}

      # Монтирование внешнего диска при загрузке
      mounts:
        - [ /dev/vdb, /mnt/external-hdd, ext4, "defaults", "0", "0" ]

      # Команды для создания точки монтирования и форматирования диска (если необходимо)
      # Принудительная установка hostname
      runcmd:
        - mkdir -p /mnt/external-hdd
        - if [ "$(blkid -o value -s TYPE /dev/vdb)" != "ext4" ]; then mkfs.ext4 /dev/vdb; fi
        - mount /dev/vdb /mnt/external-hdd
        - echo "/dev/vdb /mnt/external-hdd ext4 defaults 0 0" >> /etc/fstab
  
        # Принудительная установка hostname
        - echo ${each.value} > /etc/hostname
        - hostnamectl set-hostname ${each.value}
    EOF
  }
  # Подключаем внешний диск (HDD-1) только к vm-6
  secondary_disk {
    disk_id = yandex_compute_disk.group5["hdd-1"].id
  }

}


# Диски для group5 (HDD-1)
resource "yandex_compute_disk" "group5" {
  for_each = var.group5_unique_disks_names  # Используем уникальные имена для каждого диска в group5

  name     = each.value  # Уникальное имя диска group5
  type     = var.group5_type  # Тип диска (например, HDD)
  zone     = var.group5_zone  # Зона для создания диска
  size     = var.group5_disk_size  # Размер диска в ГБ

}