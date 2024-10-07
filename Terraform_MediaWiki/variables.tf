# Переменные по-умолчанию, используемые всеми группами


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

variable "description" {
  description = "Описание"
  type        = string
}

variable "vm_names" {
  description = "Имена виртуальных машин"
  type        = map(string)
}

variable "disk_names" {
  description = "Имена внешних дисков"
  type        = map(string)
}

variable "disk_type" {
  description = "Тип внешних жестких дисков"
  type        = optional(string)
}

variable "disk_size" {
  description = "Размер диска для ВМ по умолчанию"
  type        = number
}

variable "vm_groups" {
  description = "Параметры для всех групп ВМ"
  type = map(any)
}

variable "external_disk_groups" {
  description = "Параметры для всех групп дисков"
  type = map(any)
}


# variable "vm_groups" {
#   description = "Параметры для всех групп ВМ"
#   type = map(any)
#   type = map(object({
#     description = string
#     ram         = number
#     vm_names    = map(string)
#     disks       = map(string)
#     disk_type   = optional(string)
#     disk_size   = optional(number)
#   }))
# }
