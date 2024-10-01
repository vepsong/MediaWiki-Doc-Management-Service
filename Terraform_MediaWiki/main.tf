
# Используем цикл for_each, который перебирает значения сначала в variables.tf и потом в terraform.tfvars


# Виртуальные машины для group1 (VM-2, VM-3)
resource "yandex_compute_instance" "group1" {
  for_each = var.group1_unique_names  # Используем уникальные имена для каждой ВМ в группе 1

  name        = each.value  # Уникальное имя ВМ
  description = "Виртуальная машина ${each.value}"

  resources {
    cores  = var.group1_vm_cpu  # Количество ядер
    memory = var.group1_ram * 1024  # Оперативная память в МБ
  }

  boot_disk {
    initialize_params {
      image_id = var.group1_OC_template  # Шаблон ОС
      size     = var.group1_disk_size  # Размер диска
    }
  }

  scheduling_policy {
    preemptible = var.group1_preemptible  # Прерываемость ВМ
  }

  network_interface {
    subnet_id = "yandex_vpc_subnet.subnet-1.id"  # Подсеть
    nat       = true  # Включаем NAT для доступа в интернет
  }

  zone = var.group1_zone  # Зона для создания ВМ
}















# OLD

resource "yandex_compute_disk" "boot-disk" {
  for_each = var.virtual_machines
  name     = each.value["disk_name"]
  type     = "network-hdd"
  zone     = "ru-central1-a"
  size     = each.value["disk"]
  image_id = each.value["template"]
}


resource "yandex_vpc_network" "network-1" {
  name = "network1"
}


resource "yandex_vpc_subnet" "subnet-1" {
  name           = "subnet1"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}


resource "yandex_compute_instance" "virtual_machine" {
  for_each = var.virtual_machines
  name     = each.value["vm_name"]


  resources {
    cores  = each.value["vm_cpu"]
    memory = each.value["ram"]
  }


  boot_disk {
    disk_id = yandex_compute_disk.boot-disk[each.key].id
  }


  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }


  metadata = {
    user-data = "${file("~/terraform_yandex/meta.txt")}"
  }
  
  scheduling_policy {
    preemptible = each.value["preemptible"]
  }
}
