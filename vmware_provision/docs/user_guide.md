# VMware VM Provisioning User Guide

## 1. Prerequisites

### 1.1 System Requirements

- Ansible Automation Platform 2.4 or higher
- VMware vCenter 8.0
- Git for version control
- Sufficient vCenter permissions

### 1.2 Required Credentials

- vCenter credentials with appropriate permissions
- Domain join credentials (for Windows VMs)
- SSH keys (for Linux VMs)
- Git repository access
- AAP API tokens (for inventory updates)

## 2. Quick Start Guide

### 2.1 Basic Usage

```bash
# Clone the repository
git clone https://github.com/kimzhong/vmware_provision.git
cd vmware_provision

# Version 2: Environment-specific deployment with network isolation
ansible-playbook site.yml \
  -e "env=dev" \
  -e "location=dc1" \
  -e "domain=example.com" \
  -e "vm_os=windows2022" \
  -e "network_isolation=true" \
  -e "strict_security=false"

# Version 3: Multi-OS deployment with domain integration
ansible-playbook site.yml \
  -e "env=prod" \
  -e "location=dc1" \
  -e "domain=prod.example.com" \
  -e "vm_os=rhel8" \
  -e "network_isolation=true" \
  -e "strict_security=true" \
  -e "domain_integration=true" \
  -e "os_customization=rhel8-prod"
```

### 2.2 Required Parameters

#### Base Parameters

- `env`: Environment (dev/sit/uat/prod)
- `location`: Datacenter location
- `domain`: Domain name
- `vm_os`: OS type (windows2019/windows2022/suse15/rhel8/rhel9)

#### Version 2 Parameters

- `network_isolation`: Enable network isolation (true/false)
- `strict_security`: Enable strict security policies (true/false)
- `network_policy`: Network policy template to apply
- `traffic_shaping`: Enable traffic shaping (true/false)

#### Version 2 Core Components Parameters

- `call_stack_enabled`: Enable call chain tracking (true/false)
- `output_format`: Output format (json/yaml/xml)
- `retry_enabled`: Enable centralized retry logic (true/false)
- `idempotency_check`: Enable idempotency validation (true/false)
- `aap_state_sync`: Enable AAP state synchronization (true/false)

#### Version 3 Parameters

- `domain_integration`: Enable domain integration (true/false)
- `os_customization`: OS customization template
- `multi_nic`: Enable multiple NIC support (true/false)
- `ip_allocation`: IP allocation method (dhcp/static)

## 3. Configuration Guide

### 3.1 Version 2 Core Components Configuration

#### 3.1.1 Call Stack Manager Configuration

```yaml
# Call stack tracking configuration
call_stack_manager:
  enabled: true
  session_id_prefix: "vm_deploy"
  max_stack_depth: 10
  artifacts_integration: true
  output_file: "/tmp/call_stack_{{ ansible_date_time.epoch }}.json"
```

#### 3.1.2 Output Manager Configuration

```yaml
# Standardized output configuration
output_manager:
  enabled: true
  format: "json"  # json, yaml, xml
  file_output: true
  aap_artifacts: true
  validation_schema: "vmware_deployment_v2"
  output_directory: "/tmp/deployment_outputs"
```

#### 3.1.3 Retry Manager Configuration

```yaml
# Centralized retry configuration
retry_manager:
  enabled: true
  default_max_retries: 3
  default_delay: 30
  exponential_backoff: true
  jitter: true
  operation_specific:
    vm_creation:
      max_retries: 5
      delay: 60
    network_config:
      max_retries: 3
      delay: 30
    disk_config:
      max_retries: 4
      delay: 45
```

#### 3.1.4 Idempotency Checker Configuration

```yaml
# Idempotency validation configuration
idempotency_checker:
  enabled: true
  check_vm_existence: true
  check_network_config: true
  check_disk_config: true
  state_comparison: true
  skip_existing: true
  detailed_reporting: true
```

#### 3.1.5 AAP State Manager Configuration

```yaml
# AAP state synchronization configuration
aap_state_manager:
  enabled: true
  inventory_name: "vmware_inventory"
  auto_create_hosts: true
  update_host_vars: true
  token_refresh: true
  state_tracking: true
  api_timeout: 30
```

### 3.2 Environment Configuration

```yaml
# Example: vars/prod/main.yml
---
# vCenter Configuration
vcenter:
  hostname: "vcenter-prod.example.com"
  datacenter: "DC-PROD"
  cluster: "PROD-Cluster"
  validate_certs: true

# Network Isolation (Version 2)
network_isolation:
  enabled: true
  security_groups:
    - name: "web-servers"
      rules:
        - port: 443
          source: "10.0.0.0/24"
    - name: "db-servers"
      rules:
        - port: 5432
          source: "10.0.1.0/24"

# Network Policies (Version 2)
network_policies:
  traffic_shaping:
    enabled: true
    average_bandwidth: 1048576000 # 1 Gbps
    peak_bandwidth: 2097152000 # 2 Gbps
    burst_size: 1048576000 # 1 Gbps
  security:
    strict: true
  failover:
    active_uplinks: ["uplink1", "uplink2"]
    standby_uplinks: ["uplink3", "uplink4"]

# Multi-OS Support (Version 3)
os_templates:
  windows2022:
    template: "win2022-prod-template"
    customization: "win2022-prod-sysprep"
    domain_join: true
    domain_ou: "OU=Servers,DC=prod,DC=example,DC=com"
  rhel8:
    template: "rhel8-prod-template"
    customization: "rhel8-prod-cloud-init"
    domain_join: false
    security_baseline: "cis-rhel8-level1"
    name: "DEV-NETWORK"
    type: "standard"
    gateway: "10.0.0.1"
```

### 3.2 OS Template Configuration

```yaml
# vars/os_templates.yml
templates:
  windows2019:
    template_name: "template-windows2019-latest"
    customization: "win2019-sysprep"
  rhel8:
    template_name: "template-rhel8-latest"
    customization: "rhel8-cloud-init"
```

## 4. Advanced Usage

### 4.1 Multiple Network Interfaces

```yaml
vm_networks:
  - name: "PROD-NET-1"
    type: "vmxnet3"
    ip: "10.0.1.10"
    netmask: "255.255.255.0"
  - name: "PROD-NET-2"
    type: "vmxnet3"
    ip: "10.0.2.10"
    netmask: "255.255.255.0"
```

### 4.2 Custom Storage Configuration

```yaml
additional_disks:
  - size_gb: 100
    type: "thin"
    datastore: "FastStorage"
    unit_number: 1
```

## 5. AAP Integration

### 5.1 Creating Job Templates

1. Create a new Job Template

   - Name: "VM Provisioning"
   - Project: vmware_provision
   - Playbook: site.yml
   - Credentials: Add VMware credentials

2. Configure Extra Variables
   ```yaml
   env: "{{ env }}"
   location: "{{ location }}"
   domain: "{{ domain }}"
   vm_os: "{{ vm_os }}"
   ```

### 5.2 Creating Workflow Templates

1. Create a new Workflow Template
2. Add nodes in sequence:
   - VM State Check
   - VM Provisioning
   - Network Configuration
   - Storage Configuration
   - Inventory Update

## 6. Troubleshooting

### 6.1 Common Issues

1. **Network Configuration Fails**

   - Check VLAN availability
   - Verify network permissions
   - Validate IP address availability

2. **Template Issues**
   - Verify template existence
   - Check template permissions
   - Validate customization specifications

### 6.2 Log Locations

- Ansible logs: `/var/log/ansible.log`
- State files: `/tmp/vm_state_*.json`
- AAP job logs: Available in the job output

## 7. Maintenance

### 7.1 Template Updates

1. Update templates monthly
2. Test in dev environment
3. Document changes in changelog

### 7.2 Network Updates

1. Update network configurations
2. Validate connectivity
3. Update documentation

## 8. Best Practices

### 8.1 Naming Conventions

```yaml
vm_name_pattern: "{{ env }}-{{ location }}-{{ vm_os }}-{{ purpose }}-{{ sequence }}"
Example: "dev-dc1-win2022-web-001"
```

### 8.2 Resource Allocation

- Start with minimum requirements
- Scale based on monitoring
- Document resource changes

### 8.3 Security

- Use secure credentials
- Implement least privilege
- Regular security updates

## 9. Version Control

### 9.1 Branch Strategy

- main: Production-ready code
- develop: Development branch
- feature/\*: New features
- hotfix/\*: Emergency fixes

### 9.2 Release Process

1. Merge to develop
2. Test in dev/sit
3. Create release branch
4. Test in uat
5. Merge to main

## 10. Support and Maintenance

### 10.1 Regular Tasks

- Monthly template updates
- Quarterly security reviews
- Annual architecture review

### 10.2 Support Contacts

- Technical Support: support@example.com
- Security Team: security@example.com
- Infrastructure Team: infra@example.com
