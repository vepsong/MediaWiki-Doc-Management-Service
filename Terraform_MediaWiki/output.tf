output "vm_ip" {
  value = { for k, v in  yandex_compute_instance.virtual_machine : k => v.network_interface.0.ip_address }
}

output "vm_nat_ip" {
  value = { for k, v in  yandex_compute_instance.virtual_machine : k => v.network_interface.0.nat_ip_address}
} 

output "external_disk_types" {
  value = { for k, v in yandex_compute_disk.external_disks : k => v.type }
}

output "boot_disk_types" {
  value = { for k, v in yandex_compute_disk.boot-disk : k => v.type }
}

output "attached_disks_info" {
  value = {
    for vm_id, vm in yandex_compute_instance.virtual_machine : 
    vm_id => {
      vm_name       = vm.name
      boot_disk_name = yandex_compute_disk.boot-disk[vm_id].name
      boot_disk_type = yandex_compute_disk.boot-disk[vm_id].type

      # Проверка и вывод информации о внешнем диске
      external_disk_name = try(yandex_compute_disk.external_disks[vm_id].name, null)
      external_disk_type = try(yandex_compute_disk.external_disks[vm_id].type, null)
    }
  }
}