# Retry Manager Role

## Overview

The Retry Manager role is a core component of the VMware VM provisioning automation system (version 2.0). It provides intelligent retry mechanisms with configurable retry policies, exponential backoff, comprehensive error handling, and seamless integration with Ansible Automation Platform (AAP) and external monitoring systems.

## Features

### Core Functionality
- **Intelligent Retry Logic**: Configurable retry policies including exponential backoff, linear backoff, and fixed delay
- **Error Classification**: Automatic error type detection and retry eligibility determination
- **Performance Monitoring**: Comprehensive statistics collection and performance metrics tracking
- **Session Management**: Complete session lifecycle management with detailed logging and tracking
- **AAP Integration**: Seamless integration with AAP artifacts, job templates, and workflow templates
- **External Systems Integration**: Support for sending metrics and alerts to monitoring and notification systems

### Advanced Features
- **Circuit Breaker Pattern**: Automatic failure detection and service protection
- **Bulkhead Pattern**: Resource isolation and concurrent operation management
- **Adaptive Retry**: Dynamic retry parameter adjustment based on success rates
- **Jitter Support**: Random delay variation to prevent thundering herd problems
- **Operation-Specific Configuration**: Customizable retry settings per operation type
- **Comprehensive Alerting**: Configurable alert thresholds and notification systems

## Requirements

### Ansible Requirements
- Ansible >= 2.12
- Python >= 3.8
- requests >= 2.25.0 (for external systems integration)
- jinja2 >= 3.0.0
- PyYAML >= 5.4.0
- jsonschema >= 3.2.0 (optional, for configuration validation)

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
- name: Execute operation with retry logic
  include_role:
    name: retry_manager
  vars:
    retry_current_operation: "vmware_vm_create"
    retry_component_context:
      vm_name: "{{ vm_name }}"
      vm_template: "{{ vm_template }}"
      datacenter: "{{ datacenter }}"
```

### Advanced Configuration

```yaml
- name: Execute operation with custom retry settings
  include_role:
    name: retry_manager
  vars:
    retry_current_operation: "vmware_vm_create"
    retry_component_context:
      vm_name: "{{ vm_name }}"
      vm_template: "{{ vm_template }}"
    retry_manager:
      max_attempts: 5
      retry_policy: "exponential_backoff"
      base_delay: 10
      max_delay: 600
      backoff_multiplier: 1.5
      jitter_enabled: true
      retry_conditions:
        - "connection_error"
        - "timeout"
        - "temporary_failure"
        - "resource_busy"
      external_integration: true
      external_systems:
        - name: "slack_alerts"
          url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
          method: "POST"
          enabled: true
```

### Integration with Other Components

```yaml
# Example: Complete deployment with retry management
- name: Initialize call stack tracking
  include_role:
    name: call_stack_manager
  vars:
    call_stack_current_component: "deployment_start"

- name: Execute VM provisioning with retry logic
  include_role:
    name: retry_manager
  vars:
    retry_current_operation: "vmware_vm_provision"
    retry_component_context:
      vm_name: "{{ vm_name }}"
      vm_template: "{{ vm_template }}"
      call_stack_session_id: "{{ call_stack_session_id }}"
  notify:
    - finalize retry session
    - update call stack with retry status

- name: Configure networking with retry protection
  include_role:
    name: retry_manager
  vars:
    retry_current_operation: "network_configuration"
    retry_component_context:
      vm_name: "{{ vm_name }}"
      network_config: "{{ network_settings }}"
  notify:
    - finalize retry session

- name: Generate standardized output
  include_role:
    name: output_manager
  vars:
    output_current_component: "retry_manager"
    output_current_data: "{{ retry_final_statistics }}"
```

## Configuration

### Main Configuration Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `retry_manager.max_attempts` | integer | `3` | Maximum number of retry attempts (1-10) |
| `retry_manager.retry_policy` | string | `exponential_backoff` | Retry policy strategy |
| `retry_manager.base_delay` | integer | `5` | Base delay in seconds before first retry |
| `retry_manager.max_delay` | integer | `300` | Maximum delay in seconds between retries |
| `retry_manager.backoff_multiplier` | float | `2.0` | Multiplier for exponential backoff |
| `retry_manager.jitter_enabled` | boolean | `true` | Enable jitter to prevent thundering herd |

### Retry Policies

#### Exponential Backoff (Default)
```yaml
retry_manager:
  retry_policy: "exponential_backoff"
  base_delay: 5
  max_delay: 300
  backoff_multiplier: 2.0
  jitter_enabled: true
```

**Delay Calculation**: `delay = min(base_delay * (multiplier ^ attempt), max_delay) + jitter`

**Example delays**: 5s, 10s, 20s, 40s, 80s (with jitter)

#### Linear Backoff
```yaml
retry_manager:
  retry_policy: "linear_backoff"
  base_delay: 10
  max_delay: 120
```

**Delay Calculation**: `delay = min(base_delay * attempt, max_delay)`

**Example delays**: 10s, 20s, 30s, 40s, 50s

#### Fixed Delay
```yaml
retry_manager:
  retry_policy: "fixed_delay"
  base_delay: 15
```

**Delay Calculation**: `delay = base_delay`

**Example delays**: 15s, 15s, 15s, 15s, 15s

### Error Classification

The retry manager automatically classifies errors and determines retry eligibility:

#### Retryable Errors (Default)
- `connection_error`: Network connectivity issues
- `timeout`: Operation timeouts
- `temporary_failure`: Temporary service unavailability
- `network_error`: Network-related failures
- `service_unavailable`: Service temporarily unavailable
- `rate_limit_exceeded`: API rate limiting
- `resource_busy`: Resource temporarily busy

#### Non-Retryable Errors
- `authentication_error`: Invalid credentials
- `authorization_error`: Insufficient permissions
- `permission_error`: Access denied
- `resource_not_found`: Resource does not exist
- `configuration_error`: Invalid configuration
- `invalid_parameter`: Invalid input parameters
- `quota_exceeded`: Resource quota exceeded

### Operation-Specific Configuration

```yaml
retry_manager:
  operation_configs:
    vmware_vm_create:
      max_attempts: 5
      base_delay: 10
      max_delay: 600
      retry_policy: "exponential_backoff"
      backoff_multiplier: 1.5
    
    network_configuration:
      max_attempts: 3
      base_delay: 8
      max_delay: 240
      retry_policy: "exponential_backoff"
    
    api_call:
      max_attempts: 5
      base_delay: 2
      max_delay: 60
      retry_policy: "exponential_backoff"
      backoff_multiplier: 2.5
```

### External Systems Integration

```yaml
retry_manager:
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
    
    - name: "datadog"
      url: "https://api.datadoghq.com/api/v1/series"
      method: "POST"
      auth_header: "DD-API-KEY your-api-key"
      timeout: 20
      enabled: true
```

### Monitoring and Alerting

```yaml
retry_manager:
  monitoring:
    enabled: true
    metrics:
      - "success_rate"
      - "average_retry_count"
      - "total_execution_time"
      - "error_distribution"
      - "operation_throughput"
    
    alerts:
      min_success_rate: 85
      max_average_retries: 2.5
      max_execution_time: 1800
      max_error_rate: 15
```

## Output Data

### Session Statistics

```json
{
  "session_id": "retry_1640995200_123456",
  "session_start": "2023-12-01T10:00:00Z",
  "session_end": "2023-12-01T10:05:30Z",
  "session_duration": 330,
  "session_status": "completed",
  "final_statistics": {
    "total_operations": 5,
    "successful_operations": 4,
    "failed_operations": 1,
    "retried_operations": 2,
    "total_retry_attempts": 3,
    "average_retry_count": 0.6,
    "max_retry_count": 2,
    "total_execution_time": 330,
    "average_execution_time": 66,
    "success_rate": 80.0,
    "failure_rate": 20.0,
    "retry_rate": 40.0,
    "operations_per_minute": 0.91
  }
}
```

### Operation Details

```json
{
  "operation_id": "vmware_vm_create_1640995200_789012",
  "operation_name": "vmware_vm_create",
  "session_id": "retry_1640995200_123456",
  "start_time": "2023-12-01T10:00:00Z",
  "end_time": "2023-12-01T10:02:15Z",
  "status": "completed",
  "attempt_count": 3,
  "max_attempts": 5,
  "execution_time": 135,
  "attempts": [
    {
      "attempt_number": 1,
      "start_time": "2023-12-01T10:00:00Z",
      "end_time": "2023-12-01T10:00:30Z",
      "status": "failed",
      "error_type": "connection_error",
      "error_message": "Connection timeout to vCenter",
      "should_retry": true,
      "delay_before_retry": 5,
      "execution_time": 30
    },
    {
      "attempt_number": 2,
      "start_time": "2023-12-01T10:00:35Z",
      "end_time": "2023-12-01T10:01:20Z",
      "status": "failed",
      "error_type": "timeout",
      "error_message": "VM creation timeout",
      "should_retry": true,
      "delay_before_retry": 10,
      "execution_time": 45
    },
    {
      "attempt_number": 3,
      "start_time": "2023-12-01T10:01:30Z",
      "end_time": "2023-12-01T10:02:15Z",
      "status": "success",
      "error_type": null,
      "error_message": null,
      "should_retry": false,
      "delay_before_retry": 0,
      "execution_time": 45
    }
  ]
}
```

## AAP Artifacts

The role automatically registers the following artifacts in AAP:

- `retry_session_id`: Unique retry session identifier
- `retry_current_operation`: Current operation being retried
- `retry_operation_id`: Unique operation identifier
- `retry_operation_status`: Current status of the operation
- `retry_attempt_count`: Number of attempts made
- `retry_execution_time`: Total execution time
- `retry_session_statistics`: Complete session statistics
- `retry_operation_success`: Boolean success indicator
- `retry_timestamp`: Current timestamp

## Handlers

The role provides several handlers for different scenarios:

### finalize retry session
Finalizes the retry session and generates comprehensive statistics.

```yaml
notify:
  - finalize retry session
```

### cleanup retry session on error
Cleans up retry session data when an error occurs.

```yaml
notify:
  - cleanup retry session on error
```

### compress retry files
Compresses large retry session files to save disk space.

```yaml
notify:
  - compress retry files
```

### cleanup old retry files
Cleans up old retry session files based on retention settings.

```yaml
notify:
  - cleanup old retry files
```

### send retry metrics to external systems
Sends retry metrics and statistics to configured external systems.

```yaml
notify:
  - send retry metrics to external systems
```

### send retry alerts
Sends alert notifications when configured thresholds are exceeded.

```yaml
notify:
  - send retry alerts
```

## Integration with Other Roles

### Call Stack Manager Integration

```yaml
retry_manager:
  integration:
    call_stack_manager: true
```

Provides correlation between retry operations and execution call stack.

### Output Manager Integration

```yaml
retry_manager:
  integration:
    output_manager: true
```

Sends retry statistics and session data for standardized output.

### Idempotency Checker Integration

```yaml
retry_manager:
  integration:
    idempotency_checker: true
```

Validates operation state before retry attempts.

### AAP State Manager Integration

```yaml
retry_manager:
  integration:
    aap_state_manager: true
```

Synchronizes retry state with AAP job and workflow templates.

## Troubleshooting

### Common Issues

1. **High Retry Rates**
   - Check network connectivity to target systems
   - Verify service availability and performance
   - Review retry conditions and error classification
   - Consider adjusting retry policies

2. **Long Execution Times**
   - Review delay settings and retry policies
   - Check for excessive retry attempts
   - Monitor external system response times
   - Consider implementing circuit breaker pattern

3. **External Integration Failures**
   - Verify network connectivity to external systems
   - Check authentication credentials and API keys
   - Review endpoint URLs and configurations
   - Monitor external system availability

4. **File System Issues**
   - Ensure output directories are writable
   - Check available disk space
   - Verify file permissions and ownership
   - Review retention and cleanup settings

### Debug Mode

Enable debug output for detailed troubleshooting:

```yaml
- name: Debug retry operations
  include_role:
    name: retry_manager
  vars:
    retry_current_operation: "debug_test"
    retry_manager:
      debug_mode: true
      log_individual_attempts: true
  tags:
    - debug
```

### Log Files

- Retry session logs: `/tmp/ansible_retry/retry_session_*.json`
- Individual attempt logs: `/tmp/ansible_retry/attempt_*.json`
- Performance metrics: `/tmp/ansible_retry/retry_performance_*.json`
- Error logs: `/tmp/ansible_retry/retry_session_error_*.json`

## Performance Considerations

- **Execution Time**: Typically < 30 seconds per operation, maximum < 300 seconds
- **Memory Usage**: Typically < 50MB per session, maximum < 200MB
- **Disk Usage**: Typically < 10MB per session, maximum < 100MB
- **Throughput**: 20-100 operations per minute, 1-10 concurrent sessions

### Performance Optimization

1. **Retry Policy Tuning**
   - Use appropriate base delays for your environment
   - Set reasonable maximum delays to prevent excessive waits
   - Enable jitter to prevent thundering herd problems

2. **Resource Management**
   - Enable file compression for large sessions
   - Implement appropriate retention policies
   - Monitor disk usage and cleanup regularly

3. **External Integration**
   - Use reasonable timeouts for external systems
   - Implement retry logic for external system calls
   - Monitor external system performance

## Security Considerations

- Retry session data may contain operation parameters and sensitive information
- Error messages may expose system details and configuration
- External system credentials require secure handling and storage
- File permissions should be configured appropriately for the environment
- Access controls should be implemented for retry session data
- Regular security audits should be performed on retry configurations

## Best Practices

1. **Retry Configuration**
   - Use operation-specific retry settings for optimal performance
   - Implement appropriate retry conditions for your environment
   - Monitor retry statistics and adjust policies as needed

2. **Error Handling**
   - Classify errors appropriately for retry eligibility
   - Implement fail-fast behavior for non-retryable errors
   - Use comprehensive error logging for troubleshooting

3. **Monitoring**
   - Enable performance monitoring and alerting
   - Integrate with external monitoring systems
   - Regular review of retry statistics and trends

4. **Integration**
   - Use consistent session IDs across components
   - Implement proper error handling and cleanup
   - Monitor component integration health

5. **Security**
   - Use secure file paths and proper access controls
   - Implement encryption for sensitive environments
   - Regular security reviews and audits

## Contributing

This role is part of the VMware automation system. Please follow the project's contribution guidelines when making changes.

## License

MIT License - see the project's main LICENSE file for details.

## Support

For support and questions, please refer to the main project documentation or contact the VMware Automation Team.