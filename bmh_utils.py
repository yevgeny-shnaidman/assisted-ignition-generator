import re
import base64
import yaml
import json


BMH_CR_FILE_PATTERN = 'openshift-cluster-api_hosts'


def is_bmh_cr_file(path):
    if BMH_CR_FILE_PATTERN in path:
        return True
    return False


def get_bmh_dict_from_file(file_data):
    source_string = file_data['contents']['source']
    base64_string = re.split("base64,", source_string)[1]
    decoded_string = base64.b64decode(base64_string).decode()
    return yaml.safe_load(decoded_string)


def set_new_bmh_dict_in_file(file_data, bmh_dict):
    decoded_string = yaml.dump(bmh_dict)
    base64_string = base64.b64encode(decoded_string.encode())
    source_string = 'data:text/plain;charset=utf-8;' + 'base64,' + base64_string.decode()
    file_data['contents']['source'] = source_string


def is_master_bmh(bmh_dict):
    if "-master-" in bmh_dict['metadata']['name']:
        return True
    return False


def set_baremtal_annotation_in_bmh_dict(bmh_dict, annot_dict):
    bmh_dict['metadata']['annotations'] = annot_dict


def find_available_inventory_host(hosts_list, is_master):
    role = 'master' if is_master else 'worker'
    for host in hosts_list:
        if host.is_role(role):
            return host
    return None


def prepare_bmh_annotation_dict(status_dict, hosts_list, is_master):
    inventory_host = find_available_inventory_host(hosts_list, is_master)
    if inventory_host is None:
        return None

    annot_dict = dict.copy(status_dict)
    nics = inventory_host.get_inventory_host_nics_data()
    cpu = inventory_host.get_inventory_host_cpu_data()
    storage = inventory_host.get_inventory_host_storage_data()
    ram = inventory_host.get_inventory_host_memory()
    hostname = inventory_host.get_inventory_host_name()
    system_vendor = inventory_host.get_inventory_host_system_vendor()
    hardware = {'nics': nics, 'cpu': cpu, 'storage': storage, 'ramMebibytes': ram, 'hostname': hostname, 'systemVendor': system_vendor}
    annot_dict['hardware'] = hardware
    annot_dict['poweredOn'] = True
    hosts_list.remove(inventory_host)
    return {'baremetalhost.metal3.io/status': json.dumps(annot_dict)}


def update_bmh_cr_file(file_data, hosts_list):
    bmh_dict = get_bmh_dict_from_file(file_data)
    annot_dict = prepare_bmh_annotation_dict(bmh_dict['status'], hosts_list, is_master_bmh(bmh_dict))
    if annot_dict is not None:
        set_baremtal_annotation_in_bmh_dict(bmh_dict, annot_dict)
        set_new_bmh_dict_in_file(file_data, bmh_dict)
