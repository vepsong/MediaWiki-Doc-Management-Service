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

  metadata = {
    user-data = "${file("${path.module}/meta.txt")}"
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
    user-data = "${file("${path.module}/meta.txt")}"
  }
}


# Виртуальные машины для group3 (VM-5, VM-6)
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
    user-data = "${file("${path.module}/meta.txt")}"
  }
}


# Диски для group4 (HDD-1)
resource "yandex_compute_disk" "group4" {
  for_each = var.group4_unique_disks_names  # Используем уникальные имена для каждого диска в group4

  name     = each.value  # Уникальное имя диска group4
  type     = var.group4_type  # Тип диска (например, HDD)
  zone     = var.group4_zone  # Зона для создания диска
  size     = var.group4_disk_size  # Размер диска в ГБ

}