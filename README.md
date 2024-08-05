# VRSF Homelab Ansible

A monorepo with Ansible roles, playbooks, etc. for homelab management.

## Invetory

Run on destination PVE node (or just on one if you have a cluster)

```shell
PVE_ROLE_NAME=Ansible
PVE_USERNAME=ansible
PVE_TOKEN_NAME=ansible

# Create role with a required permissions
pveum role add $PVE_ROLE_NAME -privs "VM.Audit"

# Create user
pveum user add $PVE_USERNAME@pve

# Assign created role for user
pveum aclmod / -user $PVE_USERNAME@pve -role $PVE_ROLE_NAME

# Create a token for user
pveum user token add $PVE_USERNAME@pve $PVE_TOKEN_NAME --privsep 0
```

## Playbooks

- [X] System - *Configuring & hardening system as base*
- [X] K3s Cluster - *Preparing & configuring a K3s cluster*
- [X] K3s cluster destroy - *Preparing & configuring a K3s cluster*
- [ ] K3s Upgrade - *Draining node & running K3s upgrade process*
- [ ] K8s Node Deregister - *Removing node from the K3s cluster properly and removes K3s from system*
- [ ] K8s Node Labeling - *Getting informations about hardware and role and setting a proper labels for the Kubernetes node*
- [X] Vault initialize - *Preparing & configuring Vault HA*
- [X] Vault Unseal - *Unsealing an existing Vault*

## Roles

### Vault Unseal

```shell
ap playbooks/vault-unseal.yaml --extra-vars "$(cat ansible-remote-data/vault-init.json | jq '. | {vault_unseal_keys: .unseal_keys_hex}')"
```
