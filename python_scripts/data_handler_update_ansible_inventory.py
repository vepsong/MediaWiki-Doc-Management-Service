# Auxiliary file for update_ansible_inventory.py

def create_group_vars(ansible_meta):
    """Creation of group variables from the ansible_meta.json file."""
    return {
        "ansible_user": ansible_meta.get("ansible_user"),
        "ansible_password": ansible_meta.get("ansible_password"),
        "connection_protocol": ansible_meta.get("connection_protocol"),
        # "ansible_become": ansible_meta.get("ansible_become")
    }


def get_external_disks_info(vm_name, external_disks, terraform_vm_data):
    """Retrieving information about external disks for a given VM."""
    disk_info_list = []
    for disk in external_disks:
        if isinstance(disk, dict):
            disk_name = disk.get("disk_name")
            matching_disk = next(
                (d for d in terraform_vm_data.get("vm_external_disk", {}).get(vm_name, [])
                 if d["disk_name"] == disk_name), None
            )

            if matching_disk:
                disk_info = {
                    "disk_id": matching_disk["disk_id"],
                    "disk_name": disk_name,
                    "mount_point": disk.get("mount_point"),
                    "filesystem": disk.get("filesystem")
                }
                disk_info_list.append(disk_info)
    return disk_info_list


def get_vm_info(vm_name, terraform_vm_data, external_disks):
    """Retrieving information about the VM, including external disks."""
    nat_ip = terraform_vm_data["vm_nat_ip"].get(vm_name)
    vm_ip = terraform_vm_data["vm_ip"].get(vm_name)
    vm_info = {"ansible_host": nat_ip, "ip_addr": vm_ip}

    if external_disks:
        vm_info["external_disks"] = get_external_disks_info(vm_name, external_disks, terraform_vm_data)

    return vm_info