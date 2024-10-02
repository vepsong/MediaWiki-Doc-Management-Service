# Настройка вывода результатов работы Terraform в консоль

# Вывод IP-адресов виртуальных машин для group1
output "group1_vm_ip" {
  description = "IP-адреса виртуальных машин из группы 1"
  value = { for vm_name, vm in yandex_compute_instance.group1 : vm_name => vm.network_interface[0].ip_address }
}

# Вывод NAT IP-адресов виртуальных машин для group1
output "group1_vm_nat_ip" {
  description = "NAT IP-адреса виртуальных машин из группы 1"
  value = { for vm_name, vm in yandex_compute_instance.group1 : vm_name => vm.network_interface[0].nat_ip_address }
}

# Вывод IP-адресов виртуальных машин для group2
output "group2_vm_ip" {
  description = "IP-адреса виртуальных машин из группы 2"
  value = { for vm_name, vm in yandex_compute_instance.group2 : vm_name => vm.network_interface[0].ip_address }
}

# Вывод NAT IP-адресов виртуальных машин для group2
output "group2_vm_nat_ip" {
  description = "NAT IP-адреса виртуальных машин из группы 2"
  value = { for vm_name, vm in yandex_compute_instance.group2 : vm_name => vm.network_interface[0].nat_ip_address }
}

# Вывод IP-адресов виртуальных машин для group3
output "group3_vm_ip" {
  description = "IP-адреса виртуальных машин из группы 3"
  value = { for vm_name, vm in yandex_compute_instance.group3 : vm_name => vm.network_interface[0].ip_address }
}

# Вывод NAT IP-адресов виртуальных машин для group3
output "group3_vm_nat_ip" {
  description = "NAT IP-адреса виртуальных машин из группы 3"
  value = { for vm_name, vm in yandex_compute_instance.group3 : vm_name => vm.network_interface[0].nat_ip_address }
}