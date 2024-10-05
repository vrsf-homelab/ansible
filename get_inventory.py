#!/usr/bin/env python

import sys
import json
import os
from proxmoxer import ProxmoxAPI

def get_nodes(node_name: str, user: str, token_name: str, token_value: str) -> list:
  pve = ProxmoxAPI(host=node_name, user=f"{user}@pve", token_name=token_name, token_value=token_value)

  cluster_nodes = pve.nodes.get()
  vms = []

  for node in cluster_nodes:
    node_name = node['node']
    node_vms = pve.nodes(node_name).qemu.get()

    for vm in node_vms:
      # Get only running nodes with tags
      if vm['status'] == 'running' and 'tags' in vm:
        vm_config = pve.nodes(node_name).qemu(vm['vmid']).config.get()

        if 'ipconfig0' not in vm_config:
          print(f"There is missing `ipconfig0` property for vm '{vm['name']}'!")
          sys.exit(1)

        # Extract IP from configuration (it cannot be IP from status due to keepalived's vip)
        vm['ip'] = vm_config['ipconfig0'].split(',')[0].split('=')[1].split('/')[0]

        # Save a node name for K8s labeling
        vm['meta'] = {
          'node_name': node_name
        }

        vms.append(vm)

  return vms


def define_vars_on_tags(tags) -> (dict[str, str] | dict):
  if 'k3s_server' in tags:
    return {
      'cluster_type': 'k3s',
      'cluster_role': 'server'
    }

  if 'k3s_agent' in tags:
    return {
      'cluster_type': 'k3s',
      'cluster_role': 'agent'
    }

  if 'vault' in tags:
    return {
      'cluster_type': 'vault',
      'cluster_role': 'member'
    }

  return {}


def get_inventory() -> dict[str, dict[str, dict]]:
  nodes = get_nodes(
    os.getenv('ANSIBLE_PROXMOX_HOST'),
    os.getenv('ANSIBLE_PROXMOX_USER'),
    os.getenv('ANSIBLE_PROXMOX_TOKEN_NAME'),
    os.getenv('ANSIBLE_PROXMOX_TOKEN_VALUE'),
  )

  inventory = {'_meta': {'hostvars': {}}}

  for node in nodes:
    tags = node['tags'].split(';')

    for tag in tags:
      if tag not in inventory:
        inventory[tag] = {'hosts': [], 'vars': {}}

      inventory[tag]['hosts'].append(node['name'])

      inventory['_meta']['hostvars'][node['name']] = {
        'ansible_host': node['ip'],
        'ansible_port': '22',
        'ansible_user': 'vertisan',
        'ansible_python_interpreter': '/usr/bin/python3',
        'vars': {**define_vars_on_tags(tags), **node['meta']}
      }

  return inventory

def main() -> None:
  if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    inventory = get_inventory()
    print(json.dumps(inventory, indent=2))
  else:
    print("Usage: --list")
    sys.exit(1)

if __name__ == '__main__':
  main()
