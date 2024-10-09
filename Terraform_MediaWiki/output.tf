# Получение данных о внутренних ip-адресах
output "vm_ip" {
  value = { for k, v in  yandex_compute_instance.virtual_machine : v.name => v.network_interface.0.ip_address }
}

# Получение данных о nat ip-адресах
output "vm_nat_ip" {
  value = { for k, v in yandex_compute_instance.virtual_machine : v.name => v.network_interface.0.nat_ip_address }
}

# Получение данных о boot дисках
output "vm_boot_disk" {
  value = { 
    for k, v in yandex_compute_instance.virtual_machine : v.name => {
      "disk_name" = v.boot_disk[0].initialize_params[0].name,
      "disk_id"   = v.boot_disk[0].disk_id
    }
  }
}


# Получение данных о внешних жестких дисках

# Создаём индекс для связи disk_id с именем
locals {
  disk_name_index = { for id, disk in yandex_compute_disk.external_disks : disk.id => disk.name }
}

output "vm_external_disk" {
  value = {
    for k, v in yandex_compute_instance.virtual_machine :
    v.name => [
      for d in v.secondary_disk : {
        "disk_name" = lookup(local.disk_name_index, d.disk_id, d.disk_id),
        "disk_id"   = d.disk_id
      }
    ]
    if length([
      for d in v.secondary_disk : {
        "disk_name" = lookup(local.disk_name_index, d.disk_id, d.disk_id),
        "disk_id"   = d.disk_id
      }
    ]) > 0
  }
}

