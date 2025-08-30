# Call Stack Manager Role

## Overview

The Call Stack Manager role is a core component of the VMware VM provisioning automation system (version 2.0). It provides centralized call chain tracking, execution context management, and seamless integration with Ansible Automation Platform (AAP) artifacts.

## Features

### Core Functionality
- **Session-based Call Stack Tracking**: Maintains execution context throughout the entire deployment workflow
- **Component Execution Order Management**: Tracks the sequence and dependencies of component execution
- **Unique Call Chain Identifiers**: Generates unique identifiers for traceability and debugging
- **AAP Artifacts Integration**: Seamlessly integrates with AAP for enhanced monitoring and reporting
- **Error Handling and Cleanup**: Provides robust error handling with automatic cleanup capabilities

### Advanced Features
- **Performance Monitoring**: Optional tracking of execution time and resource usage
- **Multiple Output Formats**: Support for JSON, YAML, and CSV output formats
- **Configurable Retention**: Automatic cleanup of old call stack files
- **Validation and Integrity Checks**: Ensures call stack integrity and prevents circular dependencies
- **Integration Ready**: Designed to work seamlessly with other v2 core components

## Requirements

### Ansible Requirements
- Ansible >= 2.12
- Python >= 3.8
- Jinja2 >= 3.0.0
- PyYAML >= 5.4.0

### Platform Support
- Red Hat Enterprise Linux 8, 9
- Ubuntu 20.04, 22.04
- Windows Server 2019, 2022

### AAP Compatibility
- Ansible Automation Platform 2.4, 2.5
- Job Templates and Workflow Templates
- Artifacts and Statistics features

## Installation

This role is part of the VMware provisioning automation system. No separate installation is required if you have the complete system.

## Usage

### Basic Usage

```yaml
- name: Initialize call stack tracking
  include_role:
    name: call_stack_manager
  vars:
    call_stack_current_component: "vm_provision"
```

### Advanced Configuration

```yaml
- name: Initialize call stack with custom configuration
  include_role:
    name: call_stack_manager
  vars:
    call_stack_current_component: "network_config"
    call_stack_manager:
      session_id_prefix: "prod_deploy"
      max_stack_depth: 15
      file_output: true
      output_file: "/var/log/ansible/call_stack.json"
      artifacts_integration: true
      debug_mode: true
```

### Integration with Other Components

```yaml
# Example: VM provisioning with call stack tracking
- name: Start VM provisioning with call stack
  include_role:
    name: call_stack_manager
  vars:
    call_stack_current_component: "vmware_vm_provision"

- name: Provision VM
  include_role:
    name: vmware_vm_provision
  vars:
    # VM provisioning variables
    vm_name: "{{ vm_name }}"
    vm_template: "{{ vm_template }}"
  notify:
    - update call stack component status

- name: Configure networking
  include_role:
    name: vmware_network_config
  vars:
    call_stack_current_component: "vmware_network_config"
  notify:
    - update call stack component status

- name: Finalize deployment
  include_role:
    name: call_stack_manager
  vars:
    call_stack_current_component: "finalization"
  notify:
    - finalize call stack
```

## Configuration

### Main Configuration Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `call_stack_manager.session_id_prefix` | string | `vm_deploy` | Prefix for session ID generation |
| `call_stack_manager.max_stack_depth` | integer | `10` | Maximum allowed call stack depth |
| `call_stack_manager.file_output` | boolean | `true` | Enable file output for call stack data |
| `call_stack_manager.output_file` | string | `""` | Custom output file path |
| `call_stack_manager.artifacts_integration` | boolean | `true` | Enable AAP artifacts integration |
| `call_stack_manager.debug_mode` | boolean | `false` | Enable debug output |

### Component Tracking Settings

```yaml
call_stack_manager:
  component_tracking:
    track_execution_time: true
    track_resources: false
    track_dependencies: true
```

### Error Handling Settings

```yaml
call_stack_manager:
  error_handling:
    continue_on_error: true
    log_errors: true
    error_log_file: "/tmp/call_stack_errors.log"
```

### Output Format Configuration

```yaml
output_formats:
  json:
    enabled: true
    pretty_print: true
    include_metadata: true
  yaml:
    enabled: false
    include_comments: true
  csv:
    enabled: false
    include_headers: true
    delimiter: ","
```

## Output

### Call Stack Data Structure

```json
{
  "session_id": "vm_deploy_1640995200_123456",
  "start_time": "2023-12-01T10:00:00Z",
  "deployment_context": {
    "environment": "production",
    "location": "datacenter1",
    "vm_os": "rhel8",
    "domain": "corp.example.com"
  },
  "call_chain": [
    {
      "component": "call_stack_manager",
      "timestamp": "2023-12-01T10:00:00Z",
      "depth": 0,
      "status": "completed",
      "host": "ansible-controller",
      "user": "ansible",
      "duration": 2
    }
  ],
  "current_depth": 1,
  "max_depth": 10,
  "status": "active"
}
```

### AAP Artifacts

The role automatically registers the following artifacts in AAP:

- `call_stack_session_id`: Unique session identifier
- `call_chain_id`: Current call chain identifier
- `call_stack_status`: Current status of the call stack
- `call_stack_depth`: Current depth in the call stack
- `call_stack_component`: Current component being executed
- `call_stack_timestamp`: Current timestamp
- `call_stack_data`: Complete call stack data structure

## Handlers

The role provides several handlers for different scenarios:

### finalize call stack
Finalizes the call stack when deployment is complete.

```yaml
notify:
  - finalize call stack
```

### cleanup call stack on error
Cleans up call stack data when an error occurs.

```yaml
notify:
  - cleanup call stack on error
```

### update call stack component status
Updates the status of a specific component in the call chain.

```yaml
notify:
  - update call stack component status
```

### cleanup old call stack files
Cleans up old call stack files based on retention settings.

```yaml
notify:
  - cleanup old call stack files
```

## Integration with Other Roles

### Output Manager Integration

```yaml
call_stack_manager:
  integration:
    output_manager: true
```

### Retry Manager Integration

```yaml
call_stack_manager:
  integration:
    retry_manager: true
```

### Idempotency Checker Integration

```yaml
call_stack_manager:
  integration:
    idempotency_checker: true
```

### AAP State Manager Integration

```yaml
call_stack_manager:
  integration:
    aap_state_manager: true
```

## Troubleshooting

### Common Issues

1. **Call Stack Depth Exceeded**
   - Check for circular dependencies in your playbook
   - Increase `max_stack_depth` if legitimate deep nesting is required

2. **File Permission Issues**
   - Ensure the output directory is writable
   - Check file permissions for call stack output files

3. **AAP Integration Issues**
   - Verify AAP connectivity and permissions
   - Check if artifacts feature is enabled in AAP

### Debug Mode

Enable debug mode for detailed troubleshooting:

```yaml
call_stack_manager:
  debug_mode: true
```

### Log Files

- Call stack data: `/tmp/call_stack_<session_id>.json`
- Error logs: `/tmp/call_stack_errors.log`
- Performance data: `/tmp/call_stack_performance.json`

## Performance Considerations

- **Execution Time**: Typically < 5 seconds, maximum < 30 seconds
- **Memory Usage**: Typically < 50MB, maximum < 200MB
- **Disk Usage**: < 10MB per session for call stack files

## Security Considerations

- Call stack data may contain deployment context information
- Session IDs should be treated as sensitive in production environments
- Use secure file paths for call stack output
- Implement log rotation for long-running environments
- Consider encryption for sensitive deployment contexts

## Contributing

This role is part of the VMware automation system. Please follow the project's contribution guidelines when making changes.

## License

MIT License - see the project's main LICENSE file for details.

## Support

For support and questions, please refer to the main project documentation or contact the VMware Automation Team.