# Idempotency Checker Role

## Overview

The **Idempotency Checker** role is a critical component of the VMware provisioning automation framework that ensures operations are safe, reliable, and truly idempotent. This role performs comprehensive pre-execution validation, resource state checking, dependency validation, and conflict detection to prevent unintended changes and ensure consistent infrastructure operations.

## Core Features

### 🔍 **Idempotency Validation**
- Pre-execution validation to ensure operations are safe and idempotent
- Resource existence and state consistency checking
- Operation safety assessment and recommendations
- Comprehensive validation reporting

### 🏗️ **Resource State Checking**
- VMware virtual machine state validation
- Template availability and compatibility checking
- Datastore capacity and accessibility validation
- Network configuration and connectivity verification
- Storage resource state assessment

### 🔗 **Dependency Validation**
- Operation prerequisite verification
- vCenter connectivity and authentication checking
- Resource dependency chain validation
- Cross-component dependency assessment

### ⚠️ **Conflict Detection**
- Concurrent operation conflict identification
- Resource naming conflict detection
- Lock-based operation coordination
- Resource allocation conflict prevention

### 📊 **Session Management**
- Complete session tracking and lifecycle management
- Operation grouping and correlation
- Comprehensive statistics and metrics collection
- Session state persistence and recovery

### 🔌 **AAP Integration**
- Native Ansible Automation Platform integration
- Artifact registration and management
- Job and workflow context preservation
- Platform-specific optimizations

## Advanced Features

### 🌐 **External System Integration**
- Prometheus metrics export
- Slack/Teams notification support
- Elasticsearch logging integration
- Custom webhook support
- Multi-system alerting capabilities

### 📈 **Performance Monitoring**
- Real-time performance metrics collection
- Execution time tracking and optimization
- Resource usage monitoring
- Performance trend analysis
- Bottleneck identification

### 🔄 **Circuit Breaker Pattern**
- Automatic failure detection and isolation
- Configurable failure thresholds
- Automatic recovery mechanisms
- Half-open state testing
- Failure rate monitoring

### 🏢 **Bulkhead Pattern**
- Resource isolation and protection
- Concurrent operation limiting
- Queue management and overflow handling
- Resource pool segregation
- Performance isolation

### 🧠 **Adaptive Checking**
- Machine learning-based optimization
- Historical data analysis
- Dynamic timeout adjustment
- Intelligent check ordering
- Performance learning algorithms

### 🔧 **Custom Check Plugins**
- Extensible plugin architecture
- Custom validation logic support
- Third-party integration capabilities
- Domain-specific check implementations
- Plugin lifecycle management

## Requirements

### Software Dependencies
- **Ansible**: >= 2.12
- **Python**: >= 3.8
- **PyVmomi**: >= 7.0.3
- **Requests**: >= 2.28.0

### Optional Dependencies
- **jsonschema**: >= 4.0.0 (for configuration validation)
- **prometheus_client**: >= 0.14.0 (for Prometheus integration)

### Platform Support
- **VMware vCenter**: 6.7, 7.0, 8.0
- **VMware ESXi**: 6.7, 7.0, 8.0
- **AAP**: 2.2, 2.3, 2.4
- **Linux**: RHEL 8/9, Ubuntu 20.04/22.04, Debian 11/12
- **Windows**: Server 2019/2022

### Network Requirements
- Connectivity to VMware vCenter Server
- Access to external monitoring systems (if configured)
- Sufficient bandwidth for API operations

## Installation

### Using Ansible Galaxy
```bash
ansible-galaxy install vmware_provision.idempotency_checker
```

### Manual Installation
```bash
git clone https://github.com/your-org/vmware-provision-roles.git
cp -r vmware-provision-roles/roles/idempotency_checker /path/to/your/roles/
```

### Collection Installation
```bash
ansible-galaxy collection install community.vmware
ansible-galaxy collection install ansible.posix
ansible-galaxy collection install community.general
```

## Basic Usage

### Simple VM Creation Check
```yaml
- name: Check VM creation idempotency
  include_role:
    name: idempotency_checker
  vars:
    idempotency_current_operation: "vmware_vm_create"
    idempotency_component_context:
      vm_name: "test-vm-001"
      datacenter: "DC1"
      template_name: "ubuntu-20.04-template"
      datastore_name: "datastore1"
      network_name: "VM Network"
```

### Network Configuration Check
```yaml
- name: Check network configuration idempotency
  include_role:
    name: idempotency_checker
  vars:
    idempotency_current_operation: "network_configuration"
    idempotency_component_context:
      network_name: "production-network"
      datacenter: "DC1"
      vlan_id: 100
      ip_range: "192.168.100.0/24"
```

### Storage Configuration Check
```yaml
- name: Check storage configuration idempotency
  include_role:
    name: idempotency_checker
  vars:
    idempotency_current_operation: "storage_configuration"
    idempotency_component_context:
      datastore_name: "production-storage"
      datacenter: "DC1"
      capacity_gb: 1000
      storage_type: "SAN"
```

## Advanced Usage

### Comprehensive Infrastructure Check
```yaml
- name: Comprehensive infrastructure idempotency check
  include_role:
    name: idempotency_checker
  vars:
    idempotency_current_operation: "infrastructure_provision"
    idempotency_component_context:
      infrastructure_name: "production-env"
      datacenter: "DC1"
      components:
        - type: "vm"
          name: "web-server-001"
          template: "centos-8-template"
        - type: "network"
          name: "web-network"
          vlan: 200
        - type: "storage"
          name: "web-storage"
          capacity: 500
    idempotency_checker:
      enabled: true
      fail_on_unsafe: true
      display_summary: true
      resource_state_checking: true
      dependency_validation: true
      conflict_detection: true
      performance:
        parallel_resource_checks: true
        cache_check_results: true
        optimize_for_speed: true
```

### Integration with Other Core Components
```yaml
- name: Integrated idempotency check with full component stack
  include_role:
    name: idempotency_checker
  vars:
    idempotency_current_operation: "vmware_vm_provision"
    idempotency_component_context:
      vm_name: "{{ vm_name }}"
      datacenter: "{{ datacenter }}"
    
    # Integration with call stack manager
    call_stack_session_id: "{{ call_stack_session_id }}"
    call_stack_current_component: "idempotency_checker"
    
    # Integration with retry manager
    retry_session_id: "{{ retry_session_id }}"
    retry_operation_id: "{{ retry_operation_id }}"
    
    # Integration with output manager
    output_session_id: "{{ output_session_id }}"
    output_current_component: "idempotency_checker"
    
    # Integration with AAP state manager
    aap_job_id: "{{ tower_job_id | default(awx_job_id) }}"
    aap_workflow_id: "{{ tower_workflow_job_id | default(awx_workflow_job_id) }}"
    
    # Enhanced configuration
    idempotency_checker:
      integration:
        call_stack_manager: true
        retry_manager: true
        output_manager: true
        aap_state_manager: true
      monitoring:
        enabled: true
        metrics:
          - "check_success_rate"
          - "average_check_time"
          - "resource_conflict_rate"
      external_integration: true
      external_systems:
        - name: "prometheus"
          url: "{{ prometheus_url }}"
          enabled: true
        - name: "slack_webhook"
          url: "{{ slack_webhook_url }}"
          enabled: true
```

## Configuration Variables

### Core Configuration
```yaml
# Main configuration dictionary
idempotency_checker:
  enabled: true                    # Enable/disable idempotency checking
  fail_on_unsafe: true            # Fail execution if operation is unsafe
  display_summary: true           # Display summary information
  check_timeout_seconds: 300      # Maximum time for checks
  max_concurrent_checks: 5        # Maximum concurrent check operations
  
  # Resource state checking
  resource_state_checking: true   # Enable resource state validation
  dependency_validation: true     # Enable dependency validation
  conflict_detection: true        # Enable conflict detection
  
  # File output configuration
  file_output_enabled: true       # Enable file output
  output_directory: "/tmp/ansible_idempotency"
  compress_large_files: true      # Compress large output files
  file_size_threshold_mb: 10      # Size threshold for compression
```

### Operation-Specific Configuration
```yaml
# VMware VM creation checks
idempotency_operation_configs:
  vmware_vm_create:
    checks:
      - "vm_existence"
      - "template_availability"
      - "datastore_capacity"
      - "network_availability"
      - "resource_conflicts"
      - "dependency_validation"
    fail_on_existing: true
    require_template: true
    min_datastore_free_gb: 20
    
  # Network configuration checks
  network_configuration:
    checks:
      - "network_existence"
      - "vlan_availability"
      - "ip_address_availability"
      - "switch_connectivity"
    fail_on_conflicts: true
```

### Check Type Configuration
```yaml
# Individual check configurations
idempotency_check_types:
  vm_existence:
    enabled: true
    timeout_seconds: 30
    check_power_state: true
    check_guest_tools: true
    
  datastore_capacity:
    enabled: true
    timeout_seconds: 30
    min_free_space_gb: 10
    warn_threshold_percent: 80
    critical_threshold_percent: 95
    
  dependency_validation:
    enabled: true
    timeout_seconds: 120
    check_vcenter_connectivity: true
    check_dns_resolution: false
    check_ntp_sync: false
```

### Performance Configuration
```yaml
# Performance optimization settings
idempotency_checker:
  performance:
    async_checks: false           # Enable asynchronous checking
    parallel_resource_checks: true # Enable parallel resource checks
    cache_check_results: true     # Cache check results
    cache_ttl_minutes: 30         # Cache time-to-live
    optimize_for_speed: false     # Optimize for speed vs accuracy
```

### External Integration Configuration
```yaml
# External systems integration
idempotency_checker:
  external_integration: true
  external_systems:
    - name: "prometheus"
      url: "https://prometheus.example.com/api/v1/write"
      method: "POST"
      auth_header: "Bearer your-token-here"
      timeout: 30
      enabled: true
      retry_count: 2
      retry_delay: 5
      
    - name: "slack_webhook"
      url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
      method: "POST"
      timeout: 15
      enabled: true
```

### Monitoring and Alerting
```yaml
# Monitoring configuration
idempotency_checker:
  monitoring:
    enabled: true
    metrics:
      - "check_success_rate"
      - "average_check_time"
      - "resource_conflict_rate"
      - "dependency_failure_rate"
      - "operation_safety_rate"
    
    alerts:
      min_success_rate: 95          # Minimum acceptable success rate
      max_average_check_time: 60    # Maximum acceptable check time
      max_conflict_rate: 5          # Maximum acceptable conflict rate
      max_dependency_failure_rate: 2 # Maximum dependency failure rate
```

## Check Types and Phases

### Available Check Types

#### **Resource Existence Checks**
- `vm_existence`: Verify virtual machine existence and state
- `template_availability`: Check template availability and permissions
- `datastore_existence`: Validate datastore accessibility
- `network_existence`: Verify network and portgroup availability

#### **Capacity and Resource Checks**
- `datastore_capacity`: Check available storage capacity
- `network_availability`: Validate network resource availability
- `resource_conflicts`: Detect resource allocation conflicts

#### **State Consistency Checks**
- `state_consistency`: Verify resource state consistency
- `configuration_validation`: Validate resource configurations
- `hardware_validation`: Check hardware compatibility

#### **Dependency Checks**
- `dependency_validation`: Verify operation dependencies
- `vcenter_connectivity`: Check vCenter connectivity
- `dns_resolution`: Validate DNS resolution
- `ntp_sync`: Check time synchronization

#### **Conflict Detection Checks**
- `conflict_detection`: Detect concurrent operation conflicts
- `naming_conflicts`: Check for naming conflicts
- `resource_locks`: Verify resource lock status

### Check Phases

1. **Pre-Check Phase**: Initial validation and setup
2. **Resource Phase**: Resource existence and state checking
3. **Dependency Phase**: Dependency validation
4. **Conflict Phase**: Conflict detection and resolution
5. **Safety Phase**: Final safety assessment

## Output Data Structures

### Session Data Structure
```json
{
  "session_id": "idempotency_20240115_143022_abc123",
  "session_start": "2024-01-15T14:30:22Z",
  "session_end": "2024-01-15T14:32:45Z",
  "session_status": "completed",
  "operations_checked": [
    {
      "operation_id": "op_001",
      "operation_name": "vmware_vm_create",
      "status": "safe",
      "idempotency_status": "idempotent",
      "safe_to_execute": true,
      "execution_time": 15.3
    }
  ],
  "session_statistics": {
    "total_operations": 1,
    "safe_operations": 1,
    "unsafe_operations": 0,
    "idempotent_operations": 1,
    "total_checks": 6,
    "passed_checks": 6,
    "failed_checks": 0,
    "execution_time": 143.2
  }
}
```

### Operation Data Structure
```json
{
  "operation_id": "op_001",
  "operation_name": "vmware_vm_create",
  "session_id": "idempotency_20240115_143022_abc123",
  "start_time": "2024-01-15T14:30:22Z",
  "end_time": "2024-01-15T14:30:37Z",
  "status": "completed",
  "idempotency_status": "idempotent",
  "safe_to_execute": true,
  "safe_to_retry": true,
  "checks_performed": [
    {
      "check_id": "check_001",
      "check_type": "vm_existence",
      "status": "passed",
      "result": false,
      "message": "VM does not exist, safe to create",
      "execution_time": 2.1
    }
  ],
  "resource_conflicts": [],
  "dependencies_satisfied": true,
  "execution_time": 15.3
}
```

## AAP Artifacts

The role automatically registers the following artifacts with AAP:

### Session Artifacts
- `idempotency_session_data`: Complete session information
- `idempotency_session_statistics`: Session performance metrics
- `idempotency_session_summary`: Human-readable session summary

### Operation Artifacts
- `idempotency_operation_results`: Individual operation results
- `idempotency_check_details`: Detailed check information
- `idempotency_safety_assessment`: Safety assessment results

### Integration Artifacts
- `idempotency_component_integration`: Integration status with other components
- `idempotency_external_metrics`: External system integration results

## Handlers

The role provides several handlers for different scenarios:

### Session Management
- `complete idempotency session`: Finalizes session processing
- `cleanup idempotency session on error`: Cleans up failed sessions

### File Management
- `compress idempotency files`: Compresses large output files
- `cleanup old idempotency files`: Removes old session files
- `archive old idempotency files`: Archives old files

### External Integration
- `send idempotency metrics to external systems`: Sends metrics to monitoring systems
- `send idempotency alerts to external systems`: Sends alerts for issues

### Component Integration
- `update call stack with idempotency results`: Updates call stack manager
- `trigger output manager for idempotency results`: Triggers output formatting
- `update aap state with idempotency status`: Updates AAP state

## Integration with Other Roles

### Call Stack Manager Integration
```yaml
# Automatic integration when call_stack_session_id is provided
call_stack_session_id: "{{ call_stack_session_id }}"
call_stack_current_component: "idempotency_checker"

# Results are automatically added to call stack
```

### Retry Manager Integration
```yaml
# Integration with retry operations
retry_session_id: "{{ retry_session_id }}"
retry_operation_id: "{{ retry_operation_id }}"

# Provides retry safety recommendations
```

### Output Manager Integration
```yaml
# Automatic output formatting and management
output_session_id: "{{ output_session_id }}"
output_current_component: "idempotency_checker"

# Results are automatically formatted and stored
```

### AAP State Manager Integration
```yaml
# Platform integration
aap_job_id: "{{ tower_job_id | default(awx_job_id) }}"
aap_workflow_id: "{{ tower_workflow_job_id | default(awx_workflow_job_id) }}"

# State is automatically synchronized with AAP
```

## Troubleshooting

### Common Issues

#### **Check Timeouts**
```yaml
# Increase timeout for slow environments
idempotency_checker:
  check_timeout_seconds: 600
  
idempotency_check_types:
  vm_existence:
    timeout_seconds: 60
```

#### **vCenter Connectivity Issues**
```yaml
# Enhanced connectivity validation
idempotency_vmware:
  connection_timeout: 120
  operation_timeout: 600
  
idempotency_check_types:
  dependency_validation:
    check_vcenter_connectivity: true
    timeout_seconds: 180
```

#### **Performance Issues**
```yaml
# Performance optimization
idempotency_checker:
  performance:
    parallel_resource_checks: true
    cache_check_results: true
    optimize_for_speed: true
    async_checks: true
```

#### **Large Environment Handling**
```yaml
# Configuration for large environments
idempotency_checker:
  max_concurrent_checks: 10
  
idempotency_vmware:
  max_concurrent_operations: 5
  
idempotency_advanced:
  bulkhead:
    enabled: true
    max_concurrent_operations: 20
    queue_size: 100
```

### Debug Mode
```yaml
# Enable detailed debugging
idempotency_checker:
  display_summary: true
  display_phase_summary: true
  display_resource_summary: true
  
# Enable verbose logging
- name: Debug idempotency check
  include_role:
    name: idempotency_checker
  vars:
    ansible_verbosity: 3
```

### Log Analysis
```bash
# Check session logs
ls -la /tmp/ansible_idempotency/
cat /tmp/ansible_idempotency/idempotency_session_*.json

# Check AAP artifacts
ansible-runner artifact list --job-id <job_id>
```

## Performance Considerations

### Optimization Strategies

1. **Enable Parallel Checking**
   ```yaml
   idempotency_checker:
     performance:
       parallel_resource_checks: true
       max_concurrent_checks: 5
   ```

2. **Use Result Caching**
   ```yaml
   idempotency_checker:
     performance:
       cache_check_results: true
       cache_ttl_minutes: 30
   ```

3. **Optimize Check Selection**
   ```yaml
   idempotency_operation_configs:
     vmware_vm_create:
       checks:
         - "vm_existence"      # Essential
         - "template_availability" # Essential
         # Remove non-essential checks for speed
   ```

4. **Adjust Timeouts**
   ```yaml
   idempotency_check_types:
     vm_existence:
       timeout_seconds: 15    # Reduce for faster environments
   ```

### Resource Usage

- **Memory**: 50-200 MB depending on operation complexity
- **Disk**: 10-100 MB per session for output files
- **Network**: Low bandwidth usage (API calls only)
- **CPU**: Low to moderate during parallel checking

## Security Considerations

### Data Protection
```yaml
# Security configuration
idempotency_checker:
  security:
    no_log_credentials: true      # Never log credentials
    no_log_external: true         # Secure external communications
    encrypt_sensitive_data: true  # Encrypt sensitive data at rest
    file_permissions: "0644"      # Secure file permissions
    directory_permissions: "0755" # Secure directory permissions
```

### Access Control
```yaml
# Access control configuration
idempotency_checker:
  security:
    access_control:
      enabled: true
      allowed_users: ["ansible", "automation"]
      allowed_groups: ["ansible-users", "automation-team"]
```

### Network Security
- Use HTTPS for all external communications
- Implement proper certificate validation
- Use secure authentication methods
- Encrypt data in transit and at rest

## Best Practices

### 1. **Operation Design**
- Always define clear operation contexts
- Use descriptive operation names
- Include all necessary resource information
- Plan for idempotent operations from the start

### 2. **Configuration Management**
- Use environment-specific configurations
- Implement proper variable precedence
- Document custom configurations
- Test configurations in non-production environments

### 3. **Error Handling**
- Implement proper error recovery mechanisms
- Use appropriate timeout values
- Plan for network and system failures
- Implement comprehensive logging

### 4. **Performance Optimization**
- Enable parallel checking for large environments
- Use result caching appropriately
- Optimize check selection based on requirements
- Monitor and tune performance regularly

### 5. **Security**
- Never log sensitive information
- Use secure communication channels
- Implement proper access controls
- Regular security audits and updates

### 6. **Monitoring and Alerting**
- Implement comprehensive monitoring
- Set up appropriate alerting thresholds
- Regular review of metrics and trends
- Proactive issue identification and resolution

### 7. **Integration**
- Use consistent session IDs across components
- Implement proper component communication
- Plan for component failures and recovery
- Test integration scenarios thoroughly

## Contributing

We welcome contributions to improve the Idempotency Checker role:

1. **Bug Reports**: Submit detailed bug reports with reproduction steps
2. **Feature Requests**: Propose new features with clear use cases
3. **Code Contributions**: Follow coding standards and include tests
4. **Documentation**: Help improve documentation and examples

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-org/vmware-provision-roles.git
cd vmware-provision-roles/roles/idempotency_checker

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
ansible-test units
ansible-test integration
```

## License

This role is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

- **Documentation**: Check this README and inline code comments
- **Issues**: Submit GitHub issues for bugs and feature requests
- **Community**: Join our community discussions
- **Enterprise Support**: Contact us for professional support options

---

**Version**: 2.0.0  
**Last Updated**: January 15, 2024  
**Compatibility**: Ansible 2.12+, Python 3.8+, VMware vSphere 6.7+