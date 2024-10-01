# Файл стандартных переменных variables.tf

# variable "virtual_machines" {
#  default = ""
# }


# Объявляем переменную group1_unique_names
variable "group1_unique_names" {
  description = "Уникальные имена для ВМ группы 1"
  type        = map(string)
}

# Объявляем другие переменные, которые используются в main.tf

variable "group1_vm_cpu" {
  description = "Количество ядер для ВМ группы 1"
  type        = number
}

variable "group1_ram" {
  description = "Объем оперативной памяти для ВМ группы 1"
  type        = number
}

variable "group1_disk_size" {
  description = "Размер диска для ВМ группы 1"
  type        = number
}

variable "group1_OC_template" {
  description = "Шаблон ОС для ВМ группы 1"
  type        = string
}

variable "group1_preemptible" {
  description = "Прерываемость для ВМ группы 1"
  type        = bool
}

variable "group1_zone" {
  description = "Зона для ВМ группы 1"
  type        = string
}


# Объявляем переменную group2_unique_names
variable "group2_unique_names" {
  description = "Уникальные имена для ВМ группы 2"
  type        = map(string)
}

# Объявляем другие переменные, которые используются в main.tf

variable "group2_vm_cpu" {
  description = "Количество ядер для ВМ группы 2"
  type        = number
}

variable "group2_ram" {
  description = "Объем оперативной памяти для ВМ группы 2"
  type        = number
}

variable "group2_disk_size" {
  description = "Размер диска для ВМ группы 2"
  type        = number
}

variable "group2_OC_template" {
  description = "Шаблон ОС для ВМ группы 2"
  type        = string
}

variable "group2_preemptible" {
  description = "Прерываемость для ВМ группы 2"
  type        = bool
}

variable "group2_zone" {
  description = "Зона для ВМ группы 2"
  type        = string
}



# Объявляем переменную group3_unique_names
variable "group3_unique_names" {
  description = "Уникальные имена для ВМ группы 3"
  type        = map(string)
}

# Объявляем другие переменные, которые используются в main.tf

variable "group3_vm_cpu" {
  description = "Количество ядер для ВМ группы 3"
  type        = number
}

variable "group3_ram" {
  description = "Объем оперативной памяти для ВМ группы 3"
  type        = number
}

variable "group3_disk_size" {
  description = "Размер диска для ВМ группы 3"
  type        = number
}

variable "group3_OC_template" {
  description = "Шаблон ОС для ВМ группы 3"
  type        = string
}

variable "group3_preemptible" {
  description = "Прерываемость для ВМ группы 3"
  type        = bool
}

variable "group3_zone" {
  description = "Зона для ВМ группы 3"
  type        = string
}



# Объявляем переменную group4_unique_names
variable "group4_unique_names" {
  description = "Уникальные имена для HDD группы 4"
  type        = map(string)
}

variable "group4_zone" {
  description = "Зона для HDD группы 4"
  type        = string
}

variable "group4_type" {
  description = "Тип диска, HDD"
  type        = string
}

variable "group4_disk_size" {
  description = "Объем диска (в ГБ)"
  type        = number
}