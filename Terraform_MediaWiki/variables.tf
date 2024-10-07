variable "virtual_machines" {
 default = ""
}

variable "external_disks" {
 default = ""
}

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

variable "image_id" {
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


variable "disk_type" {
  description = "Тип внешних жестких дисков"
  type        = string
}

variable "disk_size" {
  description = "Размер диска для ВМ по умолчанию"
  type        = number
}