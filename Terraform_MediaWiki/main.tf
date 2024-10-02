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

