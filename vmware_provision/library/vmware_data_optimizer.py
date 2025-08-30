#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ansible Module: VMware Data Optimizer

This Ansible module provides data structure optimization and standardization
for VMware provisioning operations using the DataStructureOptimizer.

Version: 2.0.0
Compatibility: Ansible 2.12+, Python 3.8+
Author: VMware Provisioning Team
Last Updated: 2024-01-15
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_data_optimizer
short_description: Optimize and standardize VMware data structures
description:
    - This module optimizes and standardizes data structures for VMware operations
    - Provides data validation, transformation, and standardized output formatting
    - Supports multiple output formats including JSON, YAML, XML, CSV, and HTML
    - Includes compression and caching capabilities for performance optimization
version_added: "2.0.0"
author:
    - VMware Provisioning Team
options:
    data:
        description:
            - The data to be optimized and standardized
        required: true
        type: raw
    data_type:
        description:
            - The type of data being processed for validation
        required: false
        type: str
        choices: ['vmware_resource', 'operation_result', 'session_data']
    output_format:
        description:
            - The desired output format for the optimized data
        required: false
        type: str
        choices: ['json', 'yaml', 'xml', 'csv', 'html', 'pickle', 'compressed_json', 'compressed_yaml']
        default: 'json'
    validation_level:
        description:
            - The level of data validation to perform
        required: false
        type: str
        choices: ['basic', 'standard', 'strict', 'comprehensive']
        default: 'standard'
    include_metadata:
        description:
            - Whether to include metadata in the optimized data
        required: false
        type: bool
        default: true
    include_timestamps:
        description:
            - Whether to include timestamps in the metadata
        required: false
        type: bool
        default: true
    include_checksums:
        description:
            - Whether to include checksums for data integrity
        required: false
        type: bool
        default: false
    pretty_print:
        description:
            - Whether to format output for human readability
        required: false
        type: bool
        default: true
    compression:
        description:
            - The compression type to use for output
        required: false
        type: str
        choices: ['none', 'gzip', 'bzip2', 'lzma']
        default: 'none'
    save_to_file:
        description:
            - Path to save the optimized data to a file
        required: false
        type: str
    load_from_file:
        description:
            - Path to load data from a file before optimization
        required: false
        type: str
    enable_caching:
        description:
            - Whether to enable caching for performance optimization
        required: false
        type: bool
        default: true
    cache_ttl_seconds:
        description:
            - Time-to-live for cached data in seconds
        required: false
        type: int
        default: 3600
    max_depth:
        description:
            - Maximum depth for nested data structures
        required: false
        type: int
        default: 10
    max_size_mb:
        description:
            - Maximum size limit for data in megabytes
        required: false
        type: float
        default: 100.0
requirements:
    - python >= 3.8
    - pyyaml
notes:
    - This module is designed to work with VMware provisioning data structures
    - Supports both input data optimization and file-based operations
    - Provides comprehensive validation and error handling
'''

EXAMPLES = r'''
# Optimize VMware VM data with basic validation
- name: Optimize VM data structure
  vmware_data_optimizer:
    data:
      vm_name: "test-vm-01"
      vm_state: "running"
      hardware:
        memory_mb: 4096
        num_cpus: 2
    data_type: "vmware_resource"
    validation_level: "standard"
    output_format: "json"
    include_metadata: true
  register: optimized_vm_data

# Optimize operation result with strict validation
- name: Optimize operation result
  vmware_data_optimizer:
    data:
      operation_id: "op-12345"
      operation_type: "vm_creation"
      operation_name: "Create Test VM"
      status: "completed"
      success: true
      start_time: "2024-01-15T10:00:00Z"
    data_type: "operation_result"
    validation_level: "strict"
    output_format: "yaml"
    pretty_print: true
  register: optimized_operation

# Load data from file and optimize
- name: Load and optimize data from file
  vmware_data_optimizer:
    load_from_file: "/tmp/vmware_data.json"
    data_type: "session_data"
    validation_level: "comprehensive"
    output_format: "html"
    save_to_file: "/tmp/optimized_data.html"
  register: file_optimization_result

# Optimize with compression
- name: Optimize data with compression
  vmware_data_optimizer:
    data: "{{ large_vmware_dataset }}"
    output_format: "compressed_json"
    compression: "gzip"
    include_checksums: true
    max_size_mb: 50.0
  register: compressed_data

# Optimize session data with comprehensive features
- name: Optimize session data comprehensively
  vmware_data_optimizer:
    data:
      session_id: "session-67890"
      session_type: "vm_provisioning"
      session_name: "Production VM Deployment"
      start_time: "2024-01-15T09:00:00Z"
      operations: "{{ vm_operations }}"
    data_type: "session_data"
    validation_level: "comprehensive"
    output_format: "json"
    include_metadata: true
    include_timestamps: true
    include_checksums: true
    pretty_print: true
    save_to_file: "/var/log/ansible/session_data.json"
  register: session_optimization
'''

RETURN = r'''
optimized_data:
    description: The optimized and standardized data structure
    returned: always
    type: dict
    sample:
        data:
            vm_name: "test-vm-01"
            vm_state: "running"
            hardware:
                memory_mb: 4096
                num_cpus: 2
            _metadata:
                data_structure_version: "2.0.0"
                optimizer_version: "2.0.0"
                processing_timestamp: "2024-01-15T10:30:00.123456"
        success: true
        optimization_info:
            original_type: "dict"
            normalized: true
            metadata_added: true
            validation_performed: true
validation_errors:
    description: List of validation errors if any occurred
    returned: when validation fails
    type: list
    sample: ["Missing required field: operation_id", "Invalid type for field success"]
validation_warnings:
    description: List of validation warnings
    returned: when validation has warnings
    type: list
    sample: ["Field 'optional_field' not in schema"]
file_saved:
    description: Whether data was successfully saved to file
    returned: when save_to_file is specified
    type: bool
    sample: true
file_path:
    description: Path where the optimized data was saved
    returned: when save_to_file is specified
    type: str
    sample: "/tmp/optimized_data.json"
processing_time:
    description: Time taken to process the data in seconds
    returned: always
    type: float
    sample: 0.123
data_size:
    description: Size of the optimized data
    returned: always
    type: dict
    sample:
        original_size_bytes: 1024
        optimized_size_bytes: 1200
        compression_ratio: 0.85
'''

import json
import time
import sys
import os
from pathlib import Path

# Add the library directory to the Python path
library_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, library_dir)

try:
    from ansible.module_utils.basic import AnsibleModule
    from data_structure_optimizer import (
        DataStructureOptimizer, DataStructureConfig, DataFormat,
        CompressionType, ValidationLevel
    )
except ImportError as e:
    # Fallback for testing outside Ansible
    class AnsibleModule:
        def __init__(self, **kwargs):
            self.params = kwargs.get('argument_spec', {})
        
        def fail_json(self, **kwargs):
            print(f"FAILED: {kwargs}")
            sys.exit(1)
        
        def exit_json(self, **kwargs):
            print(f"SUCCESS: {kwargs}")
            sys.exit(0)

def get_data_size(data):
    """Calculate the size of data in bytes"""
    try:
        if isinstance(data, (str, bytes)):
            return len(data.encode() if isinstance(data, str) else data)
        else:
            return len(json.dumps(data, default=str).encode())
    except Exception:
        return 0

def run_module():
    """Main module execution function"""
    
    # Define module arguments
    module_args = dict(
        data=dict(type='raw', required=False),
        data_type=dict(type='str', required=False, 
                      choices=['vmware_resource', 'operation_result', 'session_data']),
        output_format=dict(type='str', required=False, default='json',
                          choices=['json', 'yaml', 'xml', 'csv', 'html', 'pickle', 
                                 'compressed_json', 'compressed_yaml']),
        validation_level=dict(type='str', required=False, default='standard',
                             choices=['basic', 'standard', 'strict', 'comprehensive']),
        include_metadata=dict(type='bool', required=False, default=True),
        include_timestamps=dict(type='bool', required=False, default=True),
        include_checksums=dict(type='bool', required=False, default=False),
        pretty_print=dict(type='bool', required=False, default=True),
        compression=dict(type='str', required=False, default='none',
                        choices=['none', 'gzip', 'bzip2', 'lzma']),
        save_to_file=dict(type='str', required=False),
        load_from_file=dict(type='str', required=False),
        enable_caching=dict(type='bool', required=False, default=True),
        cache_ttl_seconds=dict(type='int', required=False, default=3600),
        max_depth=dict(type='int', required=False, default=10),
        max_size_mb=dict(type='float', required=False, default=100.0)
    )
    
    # Create module instance
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[('data', 'load_from_file')],
        required_one_of=[('data', 'load_from_file')]
    )
    
    # Start timing
    start_time = time.time()
    
    try:
        # Get module parameters
        params = module.params
        
        # Create configuration
        config = DataStructureConfig(
            output_format=DataFormat(params['output_format']),
            compression=CompressionType(params['compression']),
            validation_level=ValidationLevel(params['validation_level']),
            include_metadata=params['include_metadata'],
            include_timestamps=params['include_timestamps'],
            include_checksums=params['include_checksums'],
            pretty_print=params['pretty_print'],
            max_depth=params['max_depth'],
            max_size_mb=params['max_size_mb'],
            enable_caching=params['enable_caching'],
            cache_ttl_seconds=params['cache_ttl_seconds']
        )
        
        # Create optimizer instance
        optimizer = DataStructureOptimizer(config)
        
        # Determine data source
        if params['load_from_file']:
            # Load data from file
            result = optimizer.load_and_optimize_data(
                params['load_from_file'], 
                params.get('data_type')
            )
            data = result.get('data')
            original_size = get_data_size(data) if data else 0
        else:
            # Use provided data
            data = params['data']
            original_size = get_data_size(data)
            
            # Optimize data structure
            result = optimizer.optimize_data_structure(data, params.get('data_type'))
        
        # Check if optimization was successful
        if not result['success']:
            module.fail_json(
                msg=f"Data optimization failed: {result.get('error', 'Unknown error')}",
                error=result.get('error'),
                original_data=data
            )
        
        # Get optimized data
        optimized_data = result['data']
        optimized_size = get_data_size(optimized_data)
        
        # Prepare result dictionary
        module_result = {
            'changed': True,
            'optimized_data': result,
            'processing_time': time.time() - start_time,
            'data_size': {
                'original_size_bytes': original_size,
                'optimized_size_bytes': optimized_size,
                'compression_ratio': optimized_size / original_size if original_size > 0 else 1.0
            }
        }
        
        # Handle file saving
        if params['save_to_file']:
            file_saved = optimizer.save_optimized_data(
                optimized_data, 
                params['save_to_file'],
                config.output_format
            )
            module_result['file_saved'] = file_saved
            module_result['file_path'] = params['save_to_file']
            
            if not file_saved:
                module.fail_json(
                    msg=f"Failed to save optimized data to {params['save_to_file']}",
                    **module_result
                )
        
        # Add validation information if available
        if params.get('data_type') and config.validation_level != ValidationLevel.BASIC:
            is_valid, errors = optimizer.validate_data(data, params['data_type'])
            if not is_valid:
                if config.validation_level == ValidationLevel.STRICT:
                    module.fail_json(
                        msg="Data validation failed with strict validation level",
                        validation_errors=errors,
                        **module_result
                    )
                else:
                    module_result['validation_warnings'] = errors
        
        # Return successful result
        module.exit_json(**module_result)
    
    except Exception as e:
        # Handle any unexpected errors
        processing_time = time.time() - start_time
        module.fail_json(
            msg=f"Module execution failed: {str(e)}",
            error=str(e),
            processing_time=processing_time,
            exception_type=type(e).__name__
        )

def main():
    """Main entry point"""
    run_module()

if __name__ == '__main__':
    main()