variable "virtual_machines" {
 default = ""
}

variable "external_disks" {
 default = ""
}

variable "vm_cpu" {
  description = "Количество ядер процессора для ВМ по умолчанию"
  type        = number
  default     = 2
}

variable "core_fraction" {
  description = "Гарантированная доля vCPU (%)"
  type        = number
  default     = 100
}

variable "ram" {
  description = "Объем оперативной памяти для ВМ по умолчанию"
  type        = number
  default     = 2
}

variable "image_id" {
  description = "Образ (шаблон) ОС для ВМ по умолчанию Ubuntu 22.04"
  type        = string
  default = "fd8903kfblsnlo483hoj"
}

variable "preemptible" {
  description = "Прерываемость ВМ по умолчанию"
  type        = bool
  default     = "true"
}

variable "zone" {
  description = "Зона для ВМ"
  type        = string
  default     = "ru-central1-a"
}

variable "network_id" {
  description = "Сеть для всех ВМ"
  type        = string
  default     = "enpq8hrot41agq9ug68l"
}

variable "subnet_id" {
  description = "Подсеть для всех ВМ"
  type        = string
  default     = "e9bsdtj7vme4iddaq7qb"
}

variable "nat" {
  description = "Внешний ip-адрес"
  type        = bool
  default     = "true"
}

variable "disk_type" {
  description = "Тип внешних жестких дисков"
  type        = string
  default = "network-hdd"
}

variable "disk_size" {
  description = "Размер диска для ВМ по умолчанию"
  type        = number
  default = 15
}

variable "allow_stopping_for_update" {
  description = "Разрешаем остановку ВМ для обновления"
  type        = bool
  default     = "true"
}

variable "TERRAFORM_META_DIR_ABSOLUTE_PATH" {
  description = "Путь к файлу с метаданными для виртуальной машины - terraform_meta.txt"
  type        = string
}