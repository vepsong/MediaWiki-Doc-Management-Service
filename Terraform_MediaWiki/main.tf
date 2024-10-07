resource "yandex_compute_instance" "vm" {
  # Внешний цикл - по группам
  for_each = var.vm_groups


  for_each = { for group_name, group_data in var.vm_groups : 
                group_name => group_data }

  # Внутренний цикл - по виртуальным машинам внутри каждой группы
  dynamic "instance" {
    for_each = each.value.vm_names
    content {
      name        = instance.key  # Имя виртуальной машины
      description = each.value.description

      resources {
        cores         = var.vm_cpu
        core_fraction = var.core_fraction
        memory        = var.ram
      }

      boot_disk {
        initialize_params {
          image_id = var.OC_template
          size     = each.value.disk_size
          name     = each.value.disk_names[instance.key] # Имя диска для ВМ
        }
      }

      scheduling_policy {
        preemptible = var.preemptible
      }

      network_interface {
        subnet_id = var.subnet_id
        nat       = var.nat
      }

      zone = var.zone

      metadata = {
        user-data = <<-EOF
          ${file("${path.module}/terraform_meta.txt")}

          hostname: ${instance.key}

          runcmd:
            - echo ${instance.key} > /etc/hostname
            - hostnamectl set-hostname ${instance.key}
        EOF
      }
    }
  }
}
