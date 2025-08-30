# AAP State Manager Role

A comprehensive Ansible role for managing state synchronization and integration with Ansible Automation Platform (AAP). This role provides advanced state management capabilities, conflict resolution, and seamless platform integration as part of the version2 architecture.

## Overview

The AAP State Manager role serves as a critical component in enterprise automation workflows, providing:

- **Bidirectional State Synchronization**: Real-time synchronization between local operations and AAP platform
- **Intelligent Conflict Resolution**: Multi-strategy conflict detection and resolution mechanisms
- **Platform Integration**: Seamless integration with AAP Controller, jobs, workflows, and execution environments
- **Session Management**: Advanced session lifecycle management with persistence and recovery
- **Performance Optimization**: Intelligent caching, batch processing, and resource optimization
- **Resilience Patterns**: Circuit breaker and bulkhead patterns for fault tolerance

## Core Features

### 🔄 State Synchronization
- **Real-time Monitoring**: Continuous monitoring of state changes
- **Automated Sync**: Configurable automatic synchronization triggers
- **Batch Operations**: Efficient batch processing for large-scale operations
- **Validation**: Comprehensive state validation and consistency checks
- **Incremental Sync**: Smart incremental synchronization to minimize overhead

### ⚡ Conflict Resolution
- **Multi-Strategy Resolution**: Platform-first, local-first, timestamp-based, and merge strategies
- **Automated Detection**: Intelligent conflict detection algorithms
- **Manual Review**: Workflow for manual conflict review and resolution
- **Prevention**: Proactive conflict prevention mechanisms
- **Audit Trail**: Complete audit trail for all conflict resolution actions

### 🏗️ Platform Integration
- **AAP Controller**: Direct integration with AAP Controller API
- **Job Management**: Comprehensive job status tracking and updates
- **Workflow Orchestration**: Workflow progress monitoring and management
- **Execution Environment**: EE synchronization and compatibility checking
- **Inventory Sync**: Inventory state synchronization and validation

### 📊 Session Management
- **Lifecycle Management**: Complete session creation, tracking, and cleanup
- **Persistence**: Session state persistence and recovery mechanisms
- **Concurrent Handling**: Support for multiple concurrent sessions
- **Timeout Management**: Configurable session timeouts and cleanup
- **Context Propagation**: Session context propagation across components

### 🎯 AAP Artifacts Integration
- **Automatic Registration**: Seamless artifact registration with AAP
- **Lifecycle Management**: Complete artifact lifecycle management
- **Metadata Enrichment**: Automatic metadata enhancement and tagging
- **Retrieval**: Efficient artifact retrieval and access mechanisms
- **Retention**: Configurable retention policies and cleanup

### 🔧 Advanced Features
- **External Integration**: Monitoring, alerting, and webhook integrations
- **Performance Optimization**: Caching, compression, and memory optimization
- **Circuit Breaker**: Fault tolerance and service degradation handling
- **Bulkhead Pattern**: Resource isolation and contention prevention
- **Adaptive Sync**: Dynamic synchronization frequency adjustment
- **Custom Handlers**: Extensible custom state handling mechanisms

## Requirements

### System Requirements
- **Ansible**: >= 2.12
- **Python**: >= 3.8
- **Network**: HTTPS access to AAP Controller
- **Storage**: Minimum 1GB free space for state files
- **Memory**: Minimum 512MB available RAM

### AAP Requirements
- **AAP Controller**: Version 4.0 or higher
- **Authentication**: Valid AAP user account with API access
- **Permissions**: Appropriate RBAC permissions for target operations
- **Network**: Firewall rules allowing API access

### Python Dependencies
```yaml
# Required
requests: ">=2.25.0"
urllib3: ">=1.26.0"
certifi: ">=2021.5.30"

# Optional (for enhanced features)
jsonschema: ">=3.2.0"  # JSON validation
cryptography: ">=3.4.0"  # Encryption support
```

## Installation

### As Part of Collection
```bash
# Install the entire vmware_provision collection
ansible-galaxy collection install vmware_provision
```

### Standalone Installation
```bash
# Clone the role directly
git clone <repository_url> roles/aap_state_manager
```

## Basic Usage

### Simple State Synchronization
```yaml
- name: Basic AAP state synchronization
  include_role:
    name: aap_state_manager
  vars:
    aap_state_manager:
      enabled: true
      aap_api:
        base_url: "https://aap-controller.example.com"
        auth_header: "Bearer {{ aap_token }}"
      state_synchronization:
        enabled: true
        mode: "bidirectional"
```

### Job Status Management
```yaml
- name: Manage job status with AAP
  include_role:
    name: aap_state_manager
  vars:
    aap_state_manager:
      enabled: true
      job_management:
        track_status: true
        update_progress: true
        sync_execution_environment: true
      aap_integration:
        register_artifacts: true
```

### Conflict Resolution Configuration
```yaml
- name: Advanced conflict resolution
  include_role:
    name: aap_state_manager
  vars:
    aap_state_manager:
      conflict_detection:
        enabled: true
        check_types: ["job_status", "execution_environment", "inventory"]
      conflict_resolution:
        strategy: "platform_first"
        allow_manual_review: true
        require_approval: true
```

## Advanced Configuration

### Performance Optimization
```yaml
aap_state_manager:
  performance:
    enable_caching: true
    cache_ttl: 300
    enable_compression: true
    batch_size: 50
    memory_optimization: true
  
  circuit_breaker:
    enabled: true
    failure_threshold: 5
    recovery_timeout: 60
    half_open_max_calls: 3
  
  bulkhead:
    enabled: true
    max_concurrent_syncs: 10
    resource_isolation: true
```

### External System Integration
```yaml
aap_state_manager:
  external_integrations:
    monitoring:
      enabled: true
      prometheus_endpoint: "http://prometheus:9090"
      metrics_prefix: "aap_state_manager"
    
    alerting:
      enabled: true
      webhook_url: "https://alerts.example.com/webhook"
      alert_channels: ["slack", "email"]
    
    logging:
      external_logging: true
      log_aggregator: "elasticsearch"
      log_level: "INFO"
```

### Security Configuration
```yaml
aap_state_manager:
  security:
    mask_sensitive_logs: true
    encrypt_state_files: true
    ssl_verify: true
    api_auth_validation: true
  
  file_management:
    output_permissions: "0640"
    secure_temp_files: true
    cleanup_sensitive_data: true
```

## Configuration Variables

### Core Configuration
| Variable | Default | Description |
|----------|---------|-------------|
| `aap_state_manager.enabled` | `true` | Enable/disable the role |
| `aap_state_manager.fail_on_critical_errors` | `true` | Fail on critical errors |
| `aap_state_manager.operation_timeout` | `300` | Operation timeout in seconds |
| `aap_state_manager.max_concurrent_syncs` | `5` | Maximum concurrent synchronizations |

### AAP API Configuration
| Variable | Default | Description |
|----------|---------|-------------|
| `aap_state_manager.aap_api.base_url` | `""` | AAP Controller base URL |
| `aap_state_manager.aap_api.auth_header` | `""` | Authentication header |
| `aap_state_manager.aap_api.timeout` | `30` | API request timeout |
| `aap_state_manager.aap_api.max_retries` | `3` | Maximum API retries |
| `aap_state_manager.aap_api.rate_limit_requests` | `100` | Rate limit requests per minute |

### State Synchronization
| Variable | Default | Description |
|----------|---------|-------------|
| `aap_state_manager.state_synchronization.enabled` | `true` | Enable state synchronization |
| `aap_state_manager.state_synchronization.mode` | `"bidirectional"` | Sync mode (bidirectional/pull/push) |
| `aap_state_manager.state_synchronization.sync_interval` | `60` | Sync interval in seconds |
| `aap_state_manager.state_synchronization.auto_sync` | `true` | Enable automatic synchronization |

### Conflict Resolution
| Variable | Default | Description |
|----------|---------|-------------|
| `aap_state_manager.conflict_resolution.strategy` | `"platform_first"` | Default resolution strategy |
| `aap_state_manager.conflict_resolution.allow_manual_review` | `false` | Allow manual conflict review |
| `aap_state_manager.conflict_resolution.require_approval` | `false` | Require approval for resolutions |

## Synchronization Types

### 1. Job Status Synchronization
- **Local to Platform**: Update AAP job status based on local execution
- **Platform to Local**: Sync local state with AAP job status
- **Bidirectional**: Maintain consistency between both systems

### 2. Execution Environment Synchronization
- **Availability Check**: Verify EE availability on platform
- **Compatibility Validation**: Check EE compatibility with operations
- **Auto-switching**: Automatic EE switching for compatibility
- **Configuration Sync**: Sync EE configuration and metadata

### 3. Inventory Synchronization
- **Host Status**: Synchronize host availability and status
- **Group Membership**: Update group membership information
- **Variable Sync**: Synchronize host and group variables
- **Metadata Updates**: Update inventory metadata and tags

### 4. Workflow Synchronization
- **Progress Tracking**: Track workflow execution progress
- **Status Updates**: Update workflow status and results
- **Dependency Management**: Manage workflow dependencies
- **Result Aggregation**: Aggregate and sync workflow results

## Conflict Resolution Strategies

### 1. Platform First (`platform_first`)
```yaml
conflict_resolution:
  strategy: "platform_first"
  description: "AAP platform state takes precedence"
  use_cases:
    - "Centralized state management"
    - "Platform as source of truth"
    - "Compliance requirements"
```

### 2. Local First (`local_first`)
```yaml
conflict_resolution:
  strategy: "local_first"
  description: "Local state takes precedence"
  use_cases:
    - "Local execution priority"
    - "Offline operation support"
    - "Local customizations"
```

### 3. Timestamp Based (`timestamp_based`)
```yaml
conflict_resolution:
  strategy: "timestamp_based"
  description: "Most recent change wins"
  use_cases:
    - "Collaborative environments"
    - "Distributed operations"
    - "Time-sensitive updates"
```

### 4. Merge Strategy (`merge`)
```yaml
conflict_resolution:
  strategy: "merge"
  description: "Intelligent merging of states"
  use_cases:
    - "Complementary changes"
    - "Non-conflicting updates"
    - "Additive modifications"
```

### 5. Manual Review (`manual`)
```yaml
conflict_resolution:
  strategy: "manual"
  description: "Human intervention required"
  use_cases:
    - "Critical conflicts"
    - "Business logic conflicts"
    - "Approval workflows"
```

## Output Data Structure

### Session Summary
```yaml
aap_state_manager_session:
  session_id: "aap_state_20240115_143022_abc123"
  operation_id: "op_456789"
  start_time: "2024-01-15T14:30:22Z"
  end_time: "2024-01-15T14:35:45Z"
  duration: 323
  status: "completed"
  
  synchronization:
    operations_synced: 15
    conflicts_detected: 2
    conflicts_resolved: 2
    sync_duration: 45
    
  platform_integration:
    jobs_updated: 8
    workflows_synced: 3
    execution_environments_checked: 5
    artifacts_registered: 12
    
  performance:
    api_calls: 47
    cache_hits: 23
    cache_misses: 24
    average_response_time: 0.8
    
  errors:
    total_errors: 0
    critical_errors: 0
    warnings: 1
    recoverable_errors: 0
```

### Conflict Resolution Report
```yaml
conflict_resolution_report:
  conflicts_detected: 2
  conflicts_resolved: 2
  resolution_strategies_used:
    platform_first: 1
    timestamp_based: 1
  
  conflicts:
    - conflict_id: "conflict_001"
      type: "job_status"
      description: "Job status mismatch between local and platform"
      local_value: "running"
      platform_value: "completed"
      resolution_strategy: "platform_first"
      resolved_value: "completed"
      resolution_time: "2024-01-15T14:32:15Z"
      
    - conflict_id: "conflict_002"
      type: "execution_environment"
      description: "EE version mismatch"
      local_value: "ee-minimal:2.1"
      platform_value: "ee-minimal:2.2"
      resolution_strategy: "timestamp_based"
      resolved_value: "ee-minimal:2.2"
      resolution_time: "2024-01-15T14:33:42Z"
```

## AAP Artifacts

The role automatically registers various artifacts with AAP:

### State Reports
```yaml
artifact_type: "state_report"
artifact_name: "aap_state_sync_report_{{ session_id }}"
content:
  - "Synchronization summary"
  - "Conflict resolution details"
  - "Performance metrics"
  - "Error analysis"
```

### Conflict Analysis
```yaml
artifact_type: "conflict_analysis"
artifact_name: "conflict_analysis_{{ session_id }}"
content:
  - "Detected conflicts"
  - "Resolution strategies applied"
  - "Manual review items"
  - "Prevention recommendations"
```

### Performance Metrics
```yaml
artifact_type: "performance_metrics"
artifact_name: "aap_state_performance_{{ session_id }}"
content:
  - "API response times"
  - "Cache performance"
  - "Resource utilization"
  - "Optimization recommendations"
```

## Handlers

The role provides several handlers for post-execution tasks:

```yaml
# Triggered automatically after successful execution
- name: "Complete AAP state session"
- name: "Send AAP state metrics"
- name: "Update call stack with AAP state"
- name: "Compress AAP state files"
- name: "Clean old AAP state files"
```

## Integration with Other Roles

### Call Stack Manager Integration
```yaml
- name: "Integrated AAP state management"
  include_role:
    name: call_stack_manager
  vars:
    call_stack_manager:
      track_aap_operations: true
      
- include_role:
    name: aap_state_manager
  vars:
    aap_state_manager:
      integration:
        call_stack_session_id: "{{ call_stack_session_id }}"
```

### Output Manager Integration
```yaml
- include_role:
    name: aap_state_manager
    
- include_role:
    name: output_manager
  vars:
    output_manager:
      include_aap_state_data: true
      aap_state_session_id: "{{ aap_state_manager_session.session_id }}"
```

### Retry Manager Integration
```yaml
- include_role:
    name: retry_manager
  vars:
    retry_manager:
      aap_state_aware: true
      
- include_role:
    name: aap_state_manager
  vars:
    aap_state_manager:
      integration:
        retry_session_id: "{{ retry_session_id }}"
```

## Troubleshooting

### Common Issues

#### 1. AAP API Connection Issues
```yaml
# Symptoms
- "Connection timeout to AAP Controller"
- "Authentication failed"
- "SSL certificate verification failed"

# Solutions
- Verify AAP Controller URL and accessibility
- Check authentication credentials and permissions
- Validate SSL certificates or disable verification for testing
- Review firewall rules and network connectivity
```

#### 2. State Synchronization Conflicts
```yaml
# Symptoms
- "Multiple conflicts detected"
- "Manual review required"
- "Synchronization timeout"

# Solutions
- Review conflict resolution strategy
- Enable manual review for complex conflicts
- Increase synchronization timeout
- Implement conflict prevention measures
```

#### 3. Performance Issues
```yaml
# Symptoms
- "Slow synchronization performance"
- "High memory usage"
- "API rate limiting"

# Solutions
- Enable caching and compression
- Adjust batch sizes and concurrent operations
- Implement rate limiting and backoff strategies
- Optimize synchronization intervals
```

### Debug Mode
```yaml
aap_state_manager:
  debug:
    enabled: true
    log_level: "DEBUG"
    log_api_requests: true
    log_state_changes: true
    preserve_temp_files: true
```

### Health Checks
```yaml
# Manual health check
- name: "AAP State Manager Health Check"
  include_role:
    name: aap_state_manager
  vars:
    aap_state_manager:
      health_check:
        enabled: true
        check_connectivity: true
        check_authentication: true
        check_permissions: true
```

## Performance Considerations

### Optimization Guidelines
1. **Enable Caching**: Use intelligent caching for frequently accessed data
2. **Batch Operations**: Process multiple operations in batches
3. **Compression**: Enable compression for large state files
4. **Connection Pooling**: Reuse HTTP connections for API calls
5. **Rate Limiting**: Implement appropriate rate limiting

### Resource Usage
- **Memory**: 50MB baseline + 5MB per active session
- **CPU**: Low usage during normal operations
- **Network**: Moderate bandwidth for API communications
- **Storage**: Variable based on state file retention

### Scalability Limits
- **Max Concurrent Sessions**: 50 (configurable)
- **Max Operations per Session**: 1000 (configurable)
- **Max State File Size**: 100MB (configurable)
- **Recommended Sync Interval**: 60 seconds

## Security Considerations

### Data Protection
- **Sensitive Data Masking**: Automatic masking of sensitive information in logs
- **State File Encryption**: Optional encryption for state files
- **Secure Credential Handling**: Secure handling of AAP credentials
- **SSL/TLS Validation**: Proper certificate validation for API calls

### Access Control
- **RBAC Integration**: Integration with AAP role-based access control
- **API Authentication**: Proper API authentication and authorization
- **Session Security**: Secure session management and isolation
- **Audit Logging**: Comprehensive audit trail for all operations

### Compliance
- **SOC 2 Type II**: Compatible with SOC 2 Type II requirements
- **GDPR**: Compliant data handling practices
- **Enterprise Standards**: Adherence to enterprise security standards
- **Audit Requirements**: Support for audit logging and reporting

## Best Practices

### Configuration
1. **Environment-Specific Settings**: Use different configurations for dev/test/prod
2. **Credential Management**: Use secure credential storage (Ansible Vault, external systems)
3. **Timeout Configuration**: Set appropriate timeouts based on environment
4. **Error Handling**: Configure appropriate error handling strategies

### Operations
1. **Regular Health Checks**: Implement regular health check procedures
2. **Monitoring**: Set up comprehensive monitoring and alerting
3. **Backup Strategy**: Implement backup strategies for state files
4. **Capacity Planning**: Plan for growth in operations and data

### Development
1. **Testing**: Implement comprehensive testing strategies
2. **Documentation**: Maintain up-to-date documentation
3. **Version Control**: Use proper version control for configurations
4. **Change Management**: Implement change management procedures

## Examples

See the `examples/` directory for complete usage examples:
- `basic_sync.yml` - Basic state synchronization
- `advanced_conflict_resolution.yml` - Advanced conflict resolution
- `performance_optimized.yml` - Performance-optimized configuration
- `enterprise_integration.yml` - Enterprise integration example
- `troubleshooting.yml` - Troubleshooting and debugging

## Contributing

Contributions are welcome! Please see the contributing guidelines and code of conduct.

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:
- Internal documentation and knowledge base
- Team issue tracking system
- Code review and collaboration processes

---

**Version**: 2.0.0  
**Last Updated**: 2024-01-15  
**Compatibility**: AAP 4.0+, Ansible 2.12+