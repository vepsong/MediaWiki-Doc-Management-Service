resource "yandex_compute_disk" "external_disks" {
  for_each = var.external_disks
  name     = each.value["disk_name"]
  type     = lookup(each.value, "disk_type", var.disk_type)
  size     = each.value["disk_size"]
}

resource "yandex_compute_disk" "boot-disk" {
  for_each = var.virtual_machines
  name     = each.value["disk_name"]
  size     = each.value["disk_size"]
}

resource "yandex_compute_instance" "virtual_machine" {
  for_each        = var.virtual_machines
  name = each.value["vm_name"]
  allow_stopping_for_update = lookup(each.value, "allow_stopping_for_update", var.allow_stopping_for_update)

  resources {
    cores  = var.vm_cpu
    memory = var.ram
    core_fraction = var.core_fraction
  }


  boot_disk {
    disk_id = yandex_compute_disk.boot-disk[each.key].id
  }

  network_interface {
    subnet_id  = var.subnet_id
    nat        = var.nat
    ip_address = each.value["ip_address"]
  }

  scheduling_policy {
    preemptible = var.preemptible
  }

  metadata = {
    user-data = file(var.TERRAFORM_META_DIR_ABSOLUTE_PATH)
  }

  # Подключаем внешние диски, если они указаны в external_disk
  dynamic "secondary_disk" {
    for_each = try(each.value["external_disk"], [])

    content {
      disk_id = yandex_compute_disk.external_disks[secondary_disk.value].id
    }
  }


} 

