# Общие переменные для всех групп ВМ
variable "vm_cpu" {
  description = "Количество ядер процессора для ВМ по умолчанию"
  type        = number
}

variable "core_fraction" {
  description = "Гарантированная доля vCPU (%)"
  type        = number
}

variable "ram" {
  description = "Объем оперативной памяти для ВМ по умолчанию"
  type        = number
}

variable "disk_size" {
  description = "Размер диска для ВМ по умолчанию"
  type        = number
}

variable "OC_template" {
  description = "Образ (шаблон) ОС для ВМ по умолчанию"
  type        = string
}

variable "preemptible" {
  description = "Прерываемость ВМ по умолчанию"
  type        = bool
}

variable "zone" {
  description = "Зона для ВМ"
  type        = string
}

variable "network_id" {
  description = "Сеть для всех ВМ"
  type        = string
}

variable "subnet_id" {
  description = "Подсеть для всех ВМ"
  type        = string
}

variable "nat" {
  description = "Внешний ip-адрес"
  type        = bool
}


# Одна переменная для всех групп
variable "vm_groups" {
  description = "Параметры для всех групп ВМ"
  type = map(object({
    description = string
    ram         = number
    vm_names    = map(string)
    disks       = map(string)
    disk_type   = optional(string)
    disk_size   = optional(number)
  }))
}
