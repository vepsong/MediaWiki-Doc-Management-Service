# Определяем ресурс для создания виртуальных машин
resource "yandex_compute_instance" "vm_group" {
  # Перебираем все группы ВМ
  for_each = var.vm_groups

  name        = each.value.vm_names[each.key]
  description = each.value.description


  resources {
    cores         = var.vm_cpu          # Количество ядер для ВМ
    core_fraction = var.core_fraction   # Гарантированная доля vCPU (%)
    memory        = var.ram             # Объем оперативной памяти (в GB)
  }

  boot_disk {
    initialize_params {
      image_id = var.OC_template  # Шаблон ОС
      size     = each.value.disk_size  # Размер диска
      name     = each.value.disks[each.key]  # Уникальное имя диска
    }
  }

  scheduling_policy {
    preemptible = var.preemptible  # Прерываемость ВМ
  }

  network_interface {
    subnet_id = var.subnet_id  # Подсеть
    nat       = var.nat   # NAT для доступа в интернет
  }

  zone = var.zone  # Зона для создания ВМ

  metadata = {
    user-data = <<-EOF
      ${file("${path.module}/terraform_meta.txt")}

      # Установка hostname для каждой ВМ
      hostname: ${each.value.vm_names[each.key]}

      # Дополнительные команды, если необходимо
      runcmd:
        - echo ${each.value.vm_names[each.key]} > /etc/hostname
        - hostnamectl set-hostname ${each.value.vm_names[each.key]}
    EOF
  }

  # Присоединение дополнительного диска для группы 5
  # Условие для подключения внешнего диска только к vm-3
  dynamic "secondary_disk" {
    for_each = each.key == "group4" ? [yandex_compute_disk.hdd["hdd-1"]] : []
    content {
      disk_id = secondary_disk.value.id
    }
  }
}

# Ресурс для создания дисков для группы 5 (HDD)
resource "yandex_compute_disk" "hdd" {
  for_each = var.vm_groups["group5"].disks  # Используем уникальные имена для дисков группы 5

  name = each.value                         # Уникальное имя диска
  type = var.vm_groups["group5"].disk_type  # Тип диска (например, HDD)
  zone = var.zone                           # Зона для создания диска
  size = var.vm_groups["group5"].disk_size  # Размер диска в ГБ
}
