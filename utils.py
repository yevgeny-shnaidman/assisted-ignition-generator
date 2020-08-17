import os
import json
from assisted_service_client import ApiClient, Configuration, api, models


class InventoryHost:

    def __init__(self, host_dict):
        self._host = host_dict
        self._inventory = json.loads(host_dict['inventory'])

    def get_inventory_host_nics_data(self):
        interfaces_list = self._inventory['interfaces']
        return [{'name': interface.get('name', ''), 'model': interface.get('product', ''), 'mac': interface.get('mac_address'), 'ip': self._get_network_interface_ip(interface), 'speed': interface.get('speed_mbps', 0)} for interface in interfaces_list]


    def get_inventory_host_cpu_data(self):
        cpu = self._inventory['cpu']
        return {'model': cpu.get('model_name', ''), 'arch': cpu.get('architecture', ''), 'flags': cpu.get('flags', ''), 'clockMegahertz': cpu.get('frequency', 0.0), 'count': cpu.get('count', 0)}


    def get_inventory_host_storage_data(self):
        disks_list = self._inventory['disks']
        return [{'name': disk.get('name', ''), 'vendor': disk.get('vendor', ''), 'sizeBytes': disk.get('size_bytes', 0), 'model': disk.get('model', ''), 'wwn': disk.get('wwn', ''), 'hctl': disk.get('hctl', None), 'serialNumber': disk.get('serial', ''), 'rotational': True if disk.get('drive_type', '') == 'HDD' else False} for disk in disks_list] 


    def get_inventory_host_memory(self):
        memory = self._inventory['memory']
        return int(memory.get('physical_bytes', 0) / 1024 / 1024)


    def get_inventory_host_name(self):
        return self._host.get('requested_hostname', '')


    def get_inventory_host_system_vendor(self):
        system_vendor =self._inventory['system_vendor']
        return {'manufacturer': system_vendor.get('manufacturer', ''), 'productName': system_vendor.get('product_name', ''), 'serialNumber': system_vendor.get('serial_number', None)}

    def is_role(self, role):
        return self._host['role'] == role

    def _get_network_interface_ip(self, interface):
        ipv4_addresses = interface.get('ipv4_addresses', [])
        if len(ipv4_addresses) > 0:
            return ipv4_addresses[0].split("/")[0]
        ipv6_addresses = interface.get('ipv6_addresses', [])
        if len(ipv6_addresses) > 0:
            return ipv6_addresses[0].split("/")[0]
        return " "


def get_inventory_hosts(inventory_endpoint, cluster_id, token, skip_cert_verification=False, ca_cert_path=None):
    configs = Configuration()
    configs.host = inventory_endpoint
    configs.api_key["X-Secret-Key"] = token
    configs.verify_ssl = not skip_cert_verification
    configs.ssl_ca_cert = ca_cert_path
    apiClient = ApiClient(configuration=configs)
    client = api.InstallerApi(api_client=apiClient)
    hosts_list = client.list_hosts(cluster_id=cluster_id)
    hosts_list.sort(key=sortFunc)
    return [InventoryHost(host) for host in hosts_list if host['status'] != 'disabled']


def sortFunc(host):
    return host['requested_hostname']
