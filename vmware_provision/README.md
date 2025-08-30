# VMware VM Provisioning Playbook

This Ansible playbook collection automates the provisioning of VMware virtual machines using Ansible Automation Platform (AAP) 2.4.

## Features

- Multi-environment support (dev/sit/uat/prod)
- Multiple OS template support (Windows 2019/2022, SUSE 15, RHEL 8/9)
- Network configuration management
- Storage configuration management
- State tracking and retry capability
- AAP inventory integration
- Workflow-based deployment

## Prerequisites

- Ansible Automation Platform 2.4
- VMware vCenter 8.0
- Appropriate network and storage access
- Required credentials stored in AAP

## Directory Structure

```
vmware_provision/
├── site.yml                 # Main playbook
├── vars/
│   ├── common.yml          # Common variables
│   ├── os_templates.yml    # OS template definitions
│   ├── dev/
│   ├── sit/
│   ├── uat/
│   └── prod/
└── roles/
    ├── vmware_state_check/
    ├── vmware_vm_provision/
    ├── vmware_network_config/
    ├── vmware_disk_config/
    ├── inventory_update/
    └── status_tracking/
```

## Usage

### Setting up in AAP

1. Create a project pointing to this repository
2. Create credentials for vCenter access
3. Create Job Templates:
   - VM Provisioning
   - Network Configuration
   - Inventory Update

### Creating a Workflow Template

1. Create a new Workflow Template
2. Add the following nodes:
   - VM State Check
   - VM Provisioning
   - Network Configuration
   - Disk Configuration
   - Inventory Update
   - Status Tracking

### Required Variables

- `env`: Environment (dev/sit/uat/prod)
- `location`: Datacenter location
- `domain`: Domain name
- `vm_os`: OS type (windows2019/windows2022/suse15/rhel8/rhel9)
- `vm_name`: Name of the VM
- `vm_purpose`: Purpose of the VM
- `sequence_number`: Sequence number for the VM

### Running the Playbook

```bash
ansible-playbook site.yml -e "env=dev location=dc1 domain=example.com vm_os=windows2022"
```

## Role Descriptions

### vmware_state_check

- Validates VM existence
- Checks resource availability
- Initializes state tracking

### vmware_vm_provision

- Creates VM from template
- Configures basic VM settings
- Handles VM customization

### vmware_network_config

- Configures network interfaces
- Sets up IP addressing
- Configures DNS settings

### vmware_disk_config

- Manages disk configurations
- Handles storage provisioning
- Configures additional disks

### inventory_update

- Updates AAP inventory
- Adds host variables
- Manages group assignments

### status_tracking

- Tracks deployment progress
- Handles state management
- Provides deployment status

## Error Handling

The playbook includes comprehensive error handling:

- Automatic retries for transient failures
- State tracking for resume capability
- Detailed logging and status reporting

## Contributing

Please follow these steps for contributing:

1. Create a feature branch
2. Make your changes
3. Submit a pull request
4. Include test cases
5. Update documentation

## License

MIT License
