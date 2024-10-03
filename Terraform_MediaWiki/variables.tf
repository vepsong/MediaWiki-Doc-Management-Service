# Файл стандартных переменных variables.tf

# variable "virtual_machines" {
#  default = ""
# }


# Объявляем переменную пути к файлу terraform_meta.txt
variable "meta_file_path" {
  description = "Относительный путь к файлу terraform_meta.txt"
  type     = string
}


# Объявляем переменную group1_unique_names
variable "group1_unique_vm_names" {
  description = "Уникальные имена для ВМ group1"
  type        = map(string)
}

# Объявляем другие переменные, которые используются в main.tf

variable "group1_vm_cpu" {
  description = "Количество ядер для ВМ group1"
  type        = number
}

variable "group1_ram" {
  description = "Объем оперативной памяти для ВМ group1"
  type        = number
}

variable "group1_disk_size" {
  description = "Размер диска для ВМ group1"
  type        = number
}

variable "group1_OC_template" {
  description = "Образ (шаблон) ОС для ВМ group1"
  type        = string
}

variable "group1_preemptible" {
  description = "Прерываемость для ВМ group1"
  type        = bool
}

variable "group1_zone" {
  description = "Зона для ВМ group1"
  type        = string
}

variable "group1_description" {
  description = "Описание group1"
  type        = string
}

variable "group1_network" {
  description = "Cеть и подсеть group1"
  type        = map(string)
}

variable "group1_unique_disks_names" {
  description = "Уникальные имена для дисков ВМ в group1"
  type        = map(string)
}

# Объявляем переменную group2_unique_names
variable "group2_unique_vm_names" {
  description = "Уникальные имена для ВМ group2"
  type        = map(string)
}

# Объявляем другие переменные, которые используются в main.tf

variable "group2_vm_cpu" {
  description = "Количество ядер для ВМ group2"
  type        = number
}

variable "group2_ram" {
  description = "Объем оперативной памяти для ВМ group2"
  type        = number
}

variable "group2_disk_size" {
  description = "Размер диска для ВМ group2"
  type        = number
}

variable "group2_OC_template" {
  description = "Образ (шаблон) ОС для ВМ group2"
  type        = string
}

variable "group2_preemptible" {
  description = "Прерываемость для ВМ group2"
  type        = bool
}

variable "group2_zone" {
  description = "Зона для ВМ group2"
  type        = string
}

variable "group2_description" {
  description = "Описание group2"
  type        = string
}

variable "group2_network" {
  description = "Cеть и подсеть group2"
  type        = map(string)
}

variable "group2_unique_disks_names" {
  description = "Уникальные имена для дисков ВМ в group2"
  type        = map(string)
}


# Объявляем переменную group3_unique_names
variable "group3_unique_vm_names" {
  description = "Уникальные имена для ВМ группы 3"
  type        = map(string)
}

# Объявляем другие переменные, которые используются в main.tf

variable "group3_vm_cpu" {
  description = "Количество ядер для ВМ group3"
  type        = number
}

variable "group3_ram" {
  description = "Объем оперативной памяти для ВМ group3"
  type        = number
}

variable "group3_disk_size" {
  description = "Размер диска для ВМ group3"
  type        = number
}

variable "group3_OC_template" {
  description = "Образ (шаблон) ОС для ВМ group3"
  type        = string
}

variable "group3_preemptible" {
  description = "Прерываемость для ВМ group3"
  type        = bool
}

variable "group3_zone" {
  description = "Зона для ВМ group3"
  type        = string
}

variable "group3_description" {
  description = "Описание group3"
  type        = string
}

variable "group3_network" {
  description = "Cеть и подсеть group3"
  type        = map(string)
}

variable "group3_unique_disks_names" {
  description = "Уникальные имена для дисков ВМ в group3"
  type        = map(string)
}


# Объявляем переменную group4_unique_names
variable "group4_unique_vm_names" {
  description = "Уникальные имена для ВМ группы 4"
  type        = map(string)
}

# Объявляем другие переменные, которые используются в main.tf

variable "group4_vm_cpu" {
  description = "Количество ядер для ВМ group4"
  type        = number
}

variable "group4_ram" {
  description = "Объем оперативной памяти для ВМ group4"
  type        = number
}

variable "group4_disk_size" {
  description = "Размер диска для ВМ group4"
  type        = number
}

variable "group4_OC_template" {
  description = "Образ (шаблон) ОС для ВМ group4"
  type        = string
}

variable "group4_preemptible" {
  description = "Прерываемость для ВМ group4"
  type        = bool
}

variable "group4_zone" {
  description = "Зона для ВМ group4"
  type        = string
}

variable "group4_description" {
  description = "Описание group4"
  type        = string
}

variable "group4_network" {
  description = "Cеть и подсеть group4"
  type        = map(string)
}

variable "group4_unique_disks_names" {
  description = "Уникальные имена для дисков ВМ в group4"
  type        = map(string)
}


# Объявляем переменную group5_unique_names
variable "group5_unique_disks_names" {
  description = "Уникальные имена для HDD group5"
  type        = map(string)
}

variable "group5_zone" {
  description = "Зона для HDD group5"
  type        = string
}

variable "group5_type" {
  description = "Тип диска, HDD group5"
  type        = string
}

variable "group5_disk_size" {
  description = "Объем диска (в ГБ) group5"
  type        = number
}

variable "group5_description" {
  description = "Описание group5"
  type        = string
}

variable "group5_network" {
  description = "Cеть и подсеть group5"
  type        = map(string)
}
