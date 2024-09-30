Файл динамических переменных terraform.tfvars

virtual_machines = {
  "vm-2" = {
    vm_name   = "vm-sprint12-02" # Имя ВМ
    vm_desc   = "Описание vm-sprint12-02" # Описание
    vm_cpu    = 2 # Кол-во ядер процессора
    ram       = 2 # Оперативная память в ГБ
    disk      = 20 # Объём диска в ГБ
    disk_name = "vm-2-disk" # Название диска
    template  = "fd8qh3qqmbq35jn5920n" # ID образа ОС для использования. При необходимости, id всех образов доступны по команде: yc compute image list --folder-id standard-images
    preemptible = true
  },
  "vm-3" = {
    vm_name   = "vm-sprint12-03"
    vm_desc   = "Описание vm-sprint12-03"
    vm_cpu    = 2
    ram       = 2
    disk      = 20
    disk_name = "vm-3-disk"
    template  = "fd8849jlk3ok903lqcuv"
    preemptible = true
  },
  "vm-4" = {
    vm_name   = "vm-sprint12-04"
    vm_desc   = "Описание vm-sprint12-04"
    vm_cpu    = 2
    ram       = 2
    disk      = 20
    disk_name = "vm-4-disk"
    template  = "fd8qh3qqmbq35jn5920n"
    preemptible = true
  }
}
