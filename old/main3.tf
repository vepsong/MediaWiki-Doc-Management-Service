resource "yandex_compute_instance" "vm" {
  # Внешний цикл - по группам
  for_each = var.vm_groups
  
  name = each.value.vm_names
  description = "Виртуальная машина ${each.value.description}"

  resources {
    cores  = each.value.cores  # Количество ядер
    memory = each.value.ram  # Оперативная память в GB
    core_fraction = each.value.core_fraction # Гарантированная доля vCPU (%)
  }

  boot_disk {
    initialize_params {
      image_id = each.value.OC_template  # Шаблон ОС
      size     = each.value.disk_size  # Размер диска
      name     = each.value.disk_names  # Уникальное имя диска
    }
  }

  scheduling_policy {
    preemptible = each.value.preemptible  # Прерываемость ВМ
  }

  network_interface {
    subnet_id = each.value.subnet_id # Подсеть
    nat       = each.value.nat  # Включаем NAT для доступа в интернет
  }
  zone = each.value.zone # Зона для создания ВМ
}