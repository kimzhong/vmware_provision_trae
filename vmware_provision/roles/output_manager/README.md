# Output Manager Role

## Overview

The Output Manager role is a core component of the VMware VM provisioning automation system (version 2.0). It provides standardized output management, multi-format support, data validation, sanitization, and seamless integration with Ansible Automation Platform (AAP) artifacts and external systems.

## Features

### Core Functionality
- **Multi-Format Output Support**: Generate outputs in JSON, YAML, XML, and CSV formats
- **Data Validation and Sanitization**: Automatic validation and sensitive data redaction
- **AAP Artifacts Integration**: Seamless integration with AAP for enhanced monitoring and reporting
- **External Systems Integration**: Send outputs to monitoring, ticketing, and notification systems
- **Configurable Output Destinations**: Flexible file and directory management
- **Performance Optimization**: Compression and archiving for large outputs

### Advanced Features
- **Automated Cleanup and Archiving**: Configurable retention policies and automatic cleanup
- **Comprehensive Error Handling**: Robust error handling with retry mechanisms
- **Integration with Call Stack Manager**: Automatic correlation with execution context
- **Metrics and Monitoring**: Performance tracking and health monitoring
- **Security Features**: Encryption support and access control
- **Template-Based Output**: Customizable output templates for different use cases

## Requirements

### Ansible Requirements
- Ansible >= 2.12
- Python >= 3.8
- Jinja2 >= 3.0.0
- PyYAML >= 5.4.0
- lxml >= 4.6.0 (for XML processing)
- requests >= 2.25.0 (for external systems integration)

### Platform Support
- Red Hat Enterprise Linux 8, 9
- Ubuntu 20.04, 22.04
- Windows Server 2019, 2022

### AAP Compatibility
- Ansible Automation Platform 2.4, 2.5
- Job Templates and Workflow Templates
- Artifacts, Statistics, and Logging features

## Installation

This role is part of the VMware provisioning automation system. No separate installation is required if you have the complete system.

## Usage

### Basic Usage

```yaml
- name: Generate standardized output
  include_role:
    name: output_manager
  vars:
    output_current_component: "vm_provision"
    output_current_data:
      vm_name: "{{ vm_name }}"
      vm_status: "created"
      vm_ip: "{{ vm_ip }}"
    output_current_format: "json"
```

### Advanced Configuration

```yaml
- name: Generate multi-format output with custom settings
  include_role:
    name: output_manager
  vars:
    output_current_component: "network_config"
    output_current_data: "{{ network_configuration_results }}"
    output_manager:
      formats:
        json:
          enabled: true
          pretty_print: true
          output_dir: "/var/log/ansible/outputs"
        yaml:
          enabled: true
          include_comments: true
        xml:
          enabled: true
          include_schema: true
      sanitization:
        enabled: true
        redact_fields:
          - "password"
          - "secret"
          - "token"
      external_integration: true
      external_systems:
        - name: "monitoring_system"
          url: "https://monitoring.example.com/api/data"
          method: "POST"
          enabled: true
```

### Integration with Other Components

```yaml
# Example: Complete deployment with output management
- name: Initialize call stack and output tracking
  include_role:
    name: call_stack_manager
  vars:
    call_stack_current_component: "deployment_start"

- name: Provision VM with output tracking
  include_role:
    name: vmware_vm_provision
  vars:
    vm_name: "{{ vm_name }}"
    vm_template: "{{ vm_template }}"
  notify:
    - update call stack component status

- name: Generate VM provisioning output
  include_role:
    name: output_manager
  vars:
    output_current_component: "vmware_vm_provision"
    output_current_data:
      vm_name: "{{ vm_name }}"
      vm_state: "{{ vm_provision_result.state }}"
      vm_ip: "{{ vm_provision_result.ip }}"
      provision_time: "{{ vm_provision_result.duration }}"
  notify:
    - finalize output session

- name: Configure networking with output tracking
  include_role:
    name: vmware_network_config
  vars:
    vm_name: "{{ vm_name }}"
    network_config: "{{ network_settings }}"

- name: Generate network configuration output
  include_role:
    name: output_manager
  vars:
    output_current_component: "vmware_network_config"
    output_current_data: "{{ network_config_result }}"
  notify:
    - finalize output session
```

## Configuration

### Main Configuration Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `output_manager.session_id_prefix` | string | `output` | Prefix for session ID generation |
| `output_manager.file_output` | boolean | `true` | Enable file output |
| `output_manager.artifacts_integration` | boolean | `true` | Enable AAP artifacts integration |
| `output_manager.external_integration` | boolean | `false` | Enable external systems integration |

### Output Format Configuration

```yaml
output_manager:
  formats:
    json:
      enabled: true
      pretty_print: true
      include_metadata: true
      output_dir: "/tmp/ansible_outputs"
      compression: false
    
    yaml:
      enabled: false
      include_comments: true
      output_dir: "/tmp/ansible_outputs"
      flow_style: false
    
    xml:
      enabled: false
      include_schema: true
      output_dir: "/tmp/ansible_outputs"
      pretty_print: true
    
    csv:
      enabled: false
      include_headers: true
      delimiter: ","
      output_dir: "/tmp/ansible_outputs"
```

### Data Sanitization Settings

```yaml
output_manager:
  sanitization:
    enabled: true
    password_pattern: "(password|passwd|pwd|secret|key|token)\\s*[:=]\\s*[^\\s]+"
    redact_fields:
      - "password"
      - "secret"
      - "token"
      - "key"
      - "credential"
    redaction_text: "[REDACTED]"
```

### Validation Settings

```yaml
output_manager:
  validation:
    enabled: true
    validate_json: true
    validate_yaml: true
    validate_xml: true
    max_size_bytes: 10485760  # 10MB
    fail_on_validation_error: false
```

### External Systems Integration

```yaml
output_manager:
  external_integration: true
  external_systems:
    - name: "prometheus"
      url: "https://prometheus.example.com/api/v1/write"
      method: "POST"
      auth_header: "Bearer your-token-here"
      timeout: 30
      enabled: true
      retry_count: 3
      retry_delay: 5
    
    - name: "slack_webhook"
      url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
      method: "POST"
      timeout: 15
      enabled: true
```

### Performance and Retention Settings

```yaml
output_manager:
  performance:
    enable_compression: true
    compression_threshold: 1048576  # 1MB
    async_processing: false
    batch_size: 50
  
  retention:
    days: 30
    auto_cleanup: true
    max_files_per_component: 100
  
  archiving:
    enabled: true
    format: "tar.gz"
    archive_dir: "/var/lib/ansible/archives"
    retention_days: 365
    compression_level: 6
```

## Output Formats

### JSON Output

```json
{
  "session_id": "output_1640995200_123456",
  "timestamp": "2023-12-01T10:00:00Z",
  "component": "vmware_vm_provision",
  "call_stack_session_id": "vm_deploy_1640995200_789012",
  "deployment_context": {
    "environment": "production",
    "location": "datacenter1",
    "vm_os": "rhel8",
    "domain": "corp.example.com"
  },
  "status": "completed",
  "outputs": [
    {
      "component": "vmware_vm_provision",
      "timestamp": "2023-12-01T10:00:00Z",
      "data": {
        "vm_name": "web-server-01",
        "vm_state": "poweredOn",
        "vm_ip": "192.168.1.100"
      },
      "format": "json",
      "status": "processed",
      "size_bytes": 256,
      "validation_status": "valid"
    }
  ]
}
```

### YAML Output

```yaml
# Output Manager - Component Output
# Generated: 2023-12-01T10:00:00Z
# Component: vmware_vm_provision
# Session: output_1640995200_123456

session_id: output_1640995200_123456
timestamp: '2023-12-01T10:00:00Z'
component: vmware_vm_provision
deployment_context:
  environment: production
  location: datacenter1
  vm_os: rhel8
  domain: corp.example.com
status: completed
outputs:
  - component: vmware_vm_provision
    timestamp: '2023-12-01T10:00:00Z'
    data:
      vm_name: web-server-01
      vm_state: poweredOn
      vm_ip: 192.168.1.100
    format: json
    status: processed
    size_bytes: 256
    validation_status: valid
```

### XML Output

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ansible_output>
  <metadata>
    <session_id>output_1640995200_123456</session_id>
    <timestamp>2023-12-01T10:00:00Z</timestamp>
    <component>vmware_vm_provision</component>
  </metadata>
  <deployment_context>
    <environment>production</environment>
    <location>datacenter1</location>
    <vm_os>rhel8</vm_os>
    <domain>corp.example.com</domain>
  </deployment_context>
  <outputs>
    <output>
      <component>vmware_vm_provision</component>
      <timestamp>2023-12-01T10:00:00Z</timestamp>
      <status>processed</status>
      <validation_status>valid</validation_status>
      <data>
        <vm_name>web-server-01</vm_name>
        <vm_state>poweredOn</vm_state>
        <vm_ip>192.168.1.100</vm_ip>
      </data>
    </output>
  </outputs>
</ansible_output>
```

## AAP Artifacts

The role automatically registers the following artifacts in AAP:

- `output_session_id`: Unique output session identifier
- `output_component`: Current component being processed
- `output_timestamp`: Current timestamp
- `output_status`: Current status of output processing
- `output_formats_generated`: List of generated output formats
- `output_validation_status`: Validation status of outputs
- `output_total_size`: Total size of generated outputs
- `output_data_summary`: Summary of output data

## Handlers

The role provides several handlers for different scenarios:

### finalize output session
Finalizes the output session and generates consolidated output.

```yaml
notify:
  - finalize output session
```

### cleanup output on error
Cleans up output data when an error occurs.

```yaml
notify:
  - cleanup output on error
```

### compress output files
Compresses large output files to save disk space.

```yaml
notify:
  - compress output files
```

### cleanup old output files
Cleans up old output files based on retention settings.

```yaml
notify:
  - cleanup old output files
```

### archive output session
Archives output session files for long-term storage.

```yaml
notify:
  - archive output session
```

### send output to external systems
Sends output data to configured external systems.

```yaml
notify:
  - send output to external systems
```

## Integration with Other Roles

### Call Stack Manager Integration

```yaml
output_manager:
  integration:
    call_stack_manager: true
```

### Retry Manager Integration

```yaml
output_manager:
  integration:
    retry_manager: true
```

### Idempotency Checker Integration

```yaml
output_manager:
  integration:
    idempotency_checker: true
```

### AAP State Manager Integration

```yaml
output_manager:
  integration:
    aap_state_manager: true
```

## Troubleshooting

### Common Issues

1. **Output Validation Failures**
   - Check data format and structure
   - Verify JSON/YAML/XML syntax
   - Review validation settings

2. **File Permission Issues**
   - Ensure output directories are writable
   - Check file permissions and ownership
   - Verify directory creation permissions

3. **External System Integration Issues**
   - Verify network connectivity
   - Check authentication credentials
   - Review API endpoint configurations

4. **Large Output Performance Issues**
   - Enable compression for large outputs
   - Use async processing for bulk operations
   - Implement output batching

### Debug Mode

Enable debug output for detailed troubleshooting:

```yaml
- name: Debug output processing
  include_role:
    name: output_manager
  vars:
    output_current_component: "debug_test"
    output_current_data: "{{ test_data }}"
  tags:
    - debug
```

### Log Files

- Output session logs: `/tmp/ansible_outputs/`
- Error logs: `/tmp/output_manager_errors.log`
- Session logs: `/tmp/output_manager_sessions.log`
- Metrics: `/tmp/output_manager_metrics.json`

## Performance Considerations

- **Execution Time**: Typically < 10 seconds, maximum < 60 seconds
- **Memory Usage**: Typically < 100MB, maximum < 500MB
- **Disk Usage**: < 50MB per session for output files
- **Throughput**: 1000+ JSON records/second, 500+ XML records/second

## Security Considerations

- Output data may contain deployment credentials and sensitive information
- Session IDs should be treated as sensitive in production environments
- Use secure file paths and proper access controls
- Enable encryption for sensitive environments
- Implement regular security audits of output data
- Secure external system credentials and API tokens

## Best Practices

1. **Output Organization**
   - Use descriptive component names
   - Implement consistent naming conventions
   - Organize outputs by environment and date

2. **Data Management**
   - Enable automatic cleanup and archiving
   - Implement appropriate retention policies
   - Use compression for large outputs

3. **Security**
   - Enable data sanitization
   - Use secure output directories
   - Implement proper access controls
   - Regular security reviews

4. **Performance**
   - Enable compression for large outputs
   - Use appropriate batch sizes
   - Monitor disk usage and cleanup regularly

5. **Integration**
   - Use consistent session IDs across components
   - Implement proper error handling
   - Monitor external system integrations

## Contributing

This role is part of the VMware automation system. Please follow the project's contribution guidelines when making changes.

## License

MIT License - see the project's main LICENSE file for details.

## Support

For support and questions, please refer to the main project documentation or contact the VMware Automation Team.