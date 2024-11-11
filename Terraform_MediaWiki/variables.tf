variable "virtual_machines" {
 default = ""
}

variable "external_disks" {
 default = ""
}

variable "vm_cpu" {
  description = "Default number of processor cores for the VM"
  type        = number
  default     = 2
}

variable "core_fraction" {
  description = "Guaranteed vCPU share (%)"
  type        = number
  default     = 100
}

variable "ram" {
  description = "Default amount of RAM for the VM"
  type        = number
  default     = 2
}

variable "image_id" {
  description = "Default OS image (template) for the VM: Ubuntu 22.04"
  type        = string
  default = "fd8903kfblsnlo483hoj"
}

variable "preemptible" {
  description = "Default preemptibility of the VM"
  type        = bool
  default     = "true"
}

variable "zone" {
  description = "VM availability zone"
  type        = string
  default     = "ru-central1-a"
}

variable "network_id" {
  description = "Network for all the VMs"
  type        = string
  default     = "enpq8hrot41agq9ug68l"
}

variable "subnet_id" {
  description = "Subnet for all the VMs."
  type        = string
  default     = "e9bsdtj7vme4iddaq7qb"
}

variable "nat" {
  description = "External nat IP addresses"
  type        = bool
  default     = "true"
}

variable "disk_type" {
  description = "Type of the external hard drives"
  type        = string
  default = "network-hdd"
}

variable "disk_size" {
  description = "Default VM disk size"
  type        = number
  default = 15
}

variable "allow_stopping_for_update" {
  description = "Allow VM to stop for updating"
  type        = bool
  default     = "true"
}

variable "TERRAFORM_META_DIR_ABSOLUTE_PATH" {
  description = "Path to the metadata file for the VM - terraform_meta.txt"
  type        = string
}