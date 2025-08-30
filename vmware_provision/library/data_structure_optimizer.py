#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Structure Optimizer Module

This module provides comprehensive data structure optimization and standardization
for VMware provisioning operations. It includes data validation, transformation,
compression, and standardized output formatting capabilities.

Version: 2.0.0
Compatibility: Ansible 2.12+, Python 3.8+
Author: VMware Provisioning Team
Last Updated: 2024-01-15
"""

import json
import yaml
import xml.etree.ElementTree as ET
import csv
import gzip
import pickle
import hashlib
import datetime
import re
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFormat(Enum):
    """Supported data formats for output"""
    JSON = "json"
    YAML = "yaml"
    XML = "xml"
    CSV = "csv"
    HTML = "html"
    PICKLE = "pickle"
    COMPRESSED_JSON = "compressed_json"
    COMPRESSED_YAML = "compressed_yaml"

class CompressionType(Enum):
    """Supported compression types"""
    NONE = "none"
    GZIP = "gzip"
    BZIP2 = "bzip2"
    LZMA = "lzma"

class ValidationLevel(Enum):
    """Data validation levels"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    COMPREHENSIVE = "comprehensive"

@dataclass
class DataStructureConfig:
    """Configuration for data structure optimization"""
    output_format: DataFormat = DataFormat.JSON
    compression: CompressionType = CompressionType.NONE
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    include_metadata: bool = True
    include_timestamps: bool = True
    include_checksums: bool = False
    pretty_print: bool = True
    max_depth: int = 10
    max_size_mb: float = 100.0
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600

@dataclass
class VMwareResourceData:
    """Standardized VMware resource data structure"""
    resource_id: str
    resource_type: str
    resource_name: str
    resource_state: str
    properties: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    checksum: Optional[str] = None

@dataclass
class OperationResult:
    """Standardized operation result data structure"""
    operation_id: str
    operation_type: str
    operation_name: str
    status: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    duration_seconds: Optional[float]
    success: bool
    error_message: Optional[str] = None
    warnings: List[str] = None
    results: Dict[str, Any] = None
    performance_metrics: Dict[str, Any] = None
    resource_changes: List[VMwareResourceData] = None

@dataclass
class SessionData:
    """Standardized session data structure"""
    session_id: str
    session_type: str
    session_name: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    operations: List[OperationResult]
    total_operations: int
    successful_operations: int
    failed_operations: int
    session_metadata: Dict[str, Any]
    performance_summary: Dict[str, Any]

class DataStructureOptimizer:
    """Main data structure optimizer class"""
    
    def __init__(self, config: Optional[DataStructureConfig] = None):
        """Initialize the data structure optimizer"""
        self.config = config or DataStructureConfig()
        self.cache = {} if self.config.enable_caching else None
        self.validation_schemas = self._load_validation_schemas()
        
    def _load_validation_schemas(self) -> Dict[str, Dict]:
        """Load validation schemas for different data types"""
        return {
            "vmware_resource": {
                "required_fields": ["resource_id", "resource_type", "resource_name", "resource_state"],
                "field_types": {
                    "resource_id": str,
                    "resource_type": str,
                    "resource_name": str,
                    "resource_state": str,
                    "properties": dict,
                    "metadata": dict
                },
                "valid_states": ["creating", "created", "updating", "updated", "deleting", "deleted", "error"]
            },
            "operation_result": {
                "required_fields": ["operation_id", "operation_type", "operation_name", "status", "start_time", "success"],
                "field_types": {
                    "operation_id": str,
                    "operation_type": str,
                    "operation_name": str,
                    "status": str,
                    "success": bool
                },
                "valid_statuses": ["pending", "running", "completed", "failed", "cancelled"]
            },
            "session_data": {
                "required_fields": ["session_id", "session_type", "session_name", "start_time", "operations"],
                "field_types": {
                    "session_id": str,
                    "session_type": str,
                    "session_name": str,
                    "operations": list,
                    "total_operations": int,
                    "successful_operations": int,
                    "failed_operations": int
                }
            }
        }
    
    def validate_data(self, data: Any, data_type: str) -> Tuple[bool, List[str]]:
        """Validate data against schema"""
        errors = []
        
        if data_type not in self.validation_schemas:
            errors.append(f"Unknown data type: {data_type}")
            return False, errors
        
        schema = self.validation_schemas[data_type]
        
        # Check required fields
        if isinstance(data, dict):
            for field in schema.get("required_fields", []):
                if field not in data:
                    errors.append(f"Missing required field: {field}")
        
        # Check field types
        if isinstance(data, dict):
            for field, expected_type in schema.get("field_types", {}).items():
                if field in data and not isinstance(data[field], expected_type):
                    errors.append(f"Invalid type for field {field}: expected {expected_type.__name__}, got {type(data[field]).__name__}")
        
        # Check valid values
        if isinstance(data, dict):
            if "valid_states" in schema and "resource_state" in data:
                if data["resource_state"] not in schema["valid_states"]:
                    errors.append(f"Invalid resource state: {data['resource_state']}")
            
            if "valid_statuses" in schema and "status" in data:
                if data["status"] not in schema["valid_statuses"]:
                    errors.append(f"Invalid status: {data['status']}")
        
        return len(errors) == 0, errors
    
    def normalize_data(self, data: Any) -> Any:
        """Normalize data structure"""
        if isinstance(data, dict):
            normalized = {}
            for key, value in data.items():
                # Normalize key names (snake_case)
                normalized_key = re.sub(r'([A-Z])', r'_\1', key).lower().strip('_')
                normalized[normalized_key] = self.normalize_data(value)
            return normalized
        elif isinstance(data, list):
            return [self.normalize_data(item) for item in data]
        elif isinstance(data, str):
            # Normalize string values
            return data.strip()
        else:
            return data
    
    def add_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata to data structure"""
        if not self.config.include_metadata:
            return data
        
        metadata = {
            "data_structure_version": "2.0.0",
            "optimizer_version": "2.0.0",
            "processing_timestamp": datetime.datetime.utcnow().isoformat(),
            "data_format": self.config.output_format.value,
            "compression": self.config.compression.value,
            "validation_level": self.config.validation_level.value
        }
        
        if self.config.include_checksums:
            data_str = json.dumps(data, sort_keys=True, default=str)
            metadata["checksum"] = hashlib.sha256(data_str.encode()).hexdigest()
        
        if "_metadata" not in data:
            data["_metadata"] = {}
        
        data["_metadata"].update(metadata)
        return data
    
    def compress_data(self, data: bytes) -> bytes:
        """Compress data using specified compression type"""
        if self.config.compression == CompressionType.GZIP:
            return gzip.compress(data)
        elif self.config.compression == CompressionType.BZIP2:
            import bz2
            return bz2.compress(data)
        elif self.config.compression == CompressionType.LZMA:
            import lzma
            return lzma.compress(data)
        else:
            return data
    
    def decompress_data(self, data: bytes) -> bytes:
        """Decompress data using specified compression type"""
        if self.config.compression == CompressionType.GZIP:
            return gzip.decompress(data)
        elif self.config.compression == CompressionType.BZIP2:
            import bz2
            return bz2.decompress(data)
        elif self.config.compression == CompressionType.LZMA:
            import lzma
            return lzma.decompress(data)
        else:
            return data
    
    def convert_to_format(self, data: Any, output_format: DataFormat) -> Union[str, bytes]:
        """Convert data to specified format"""
        if output_format == DataFormat.JSON:
            return json.dumps(data, indent=2 if self.config.pretty_print else None, default=str)
        
        elif output_format == DataFormat.YAML:
            return yaml.dump(data, default_flow_style=False, indent=2 if self.config.pretty_print else None)
        
        elif output_format == DataFormat.XML:
            return self._convert_to_xml(data)
        
        elif output_format == DataFormat.CSV:
            return self._convert_to_csv(data)
        
        elif output_format == DataFormat.HTML:
            return self._convert_to_html(data)
        
        elif output_format == DataFormat.PICKLE:
            return pickle.dumps(data)
        
        elif output_format == DataFormat.COMPRESSED_JSON:
            json_data = json.dumps(data, default=str).encode()
            return self.compress_data(json_data)
        
        elif output_format == DataFormat.COMPRESSED_YAML:
            yaml_data = yaml.dump(data).encode()
            return self.compress_data(yaml_data)
        
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _convert_to_xml(self, data: Any, root_name: str = "data") -> str:
        """Convert data to XML format"""
        def dict_to_xml(d, parent):
            for key, value in d.items():
                if isinstance(value, dict):
                    child = ET.SubElement(parent, str(key))
                    dict_to_xml(value, child)
                elif isinstance(value, list):
                    for item in value:
                        child = ET.SubElement(parent, str(key))
                        if isinstance(item, dict):
                            dict_to_xml(item, child)
                        else:
                            child.text = str(item)
                else:
                    child = ET.SubElement(parent, str(key))
                    child.text = str(value)
        
        root = ET.Element(root_name)
        if isinstance(data, dict):
            dict_to_xml(data, root)
        else:
            root.text = str(data)
        
        return ET.tostring(root, encoding='unicode')
    
    def _convert_to_csv(self, data: Any) -> str:
        """Convert data to CSV format"""
        if not isinstance(data, list):
            data = [data]
        
        if not data:
            return ""
        
        # Flatten nested dictionaries
        flattened_data = []
        for item in data:
            if isinstance(item, dict):
                flattened_item = self._flatten_dict(item)
                flattened_data.append(flattened_item)
            else:
                flattened_data.append({"value": str(item)})
        
        if not flattened_data:
            return ""
        
        # Get all unique keys
        all_keys = set()
        for item in flattened_data:
            all_keys.update(item.keys())
        
        # Create CSV
        import io
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=sorted(all_keys))
        writer.writeheader()
        writer.writerows(flattened_data)
        
        return output.getvalue()
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self._flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
                    else:
                        items.append((f"{new_key}[{i}]", str(item)))
            else:
                items.append((new_key, str(v)))
        return dict(items)
    
    def _convert_to_html(self, data: Any) -> str:
        """Convert data to HTML format"""
        def dict_to_html(d, level=0):
            html = "<ul>\n" if level > 0 else "<div class='data-structure'>\n"
            for key, value in d.items():
                if isinstance(value, dict):
                    html += f"<li><strong>{key}:</strong>\n{dict_to_html(value, level + 1)}</li>\n"
                elif isinstance(value, list):
                    html += f"<li><strong>{key}:</strong>\n<ul>\n"
                    for item in value:
                        if isinstance(item, dict):
                            html += f"<li>{dict_to_html(item, level + 2)}</li>\n"
                        else:
                            html += f"<li>{str(item)}</li>\n"
                    html += "</ul></li>\n"
                else:
                    html += f"<li><strong>{key}:</strong> {str(value)}</li>\n"
            html += "</ul>\n" if level > 0 else "</div>\n"
            return html
        
        css = """
        <style>
        .data-structure {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .data-structure ul {
            list-style-type: none;
            padding-left: 20px;
        }
        .data-structure li {
            margin: 5px 0;
        }
        .data-structure strong {
            color: #333;
        }
        </style>
        """
        
        if isinstance(data, dict):
            body = dict_to_html(data)
        else:
            body = f"<div class='data-structure'>{str(data)}</div>"
        
        return f"<!DOCTYPE html>\n<html>\n<head>\n{css}\n</head>\n<body>\n{body}\n</body>\n</html>"
    
    def optimize_data_structure(self, data: Any, data_type: Optional[str] = None) -> Dict[str, Any]:
        """Main method to optimize data structure"""
        try:
            # Validate data if type is specified
            if data_type and self.config.validation_level != ValidationLevel.BASIC:
                is_valid, errors = self.validate_data(data, data_type)
                if not is_valid and self.config.validation_level == ValidationLevel.STRICT:
                    raise ValueError(f"Data validation failed: {', '.join(errors)}")
                elif not is_valid:
                    logger.warning(f"Data validation warnings: {', '.join(errors)}")
            
            # Normalize data structure
            normalized_data = self.normalize_data(data)
            
            # Add metadata
            if isinstance(normalized_data, dict):
                normalized_data = self.add_metadata(normalized_data)
            else:
                normalized_data = {
                    "data": normalized_data,
                    "_metadata": {}
                }
                normalized_data = self.add_metadata(normalized_data)
            
            return {
                "success": True,
                "data": normalized_data,
                "optimization_info": {
                    "original_type": type(data).__name__,
                    "normalized": True,
                    "metadata_added": self.config.include_metadata,
                    "validation_performed": data_type is not None,
                    "processing_timestamp": datetime.datetime.utcnow().isoformat()
                }
            }
        
        except Exception as e:
            logger.error(f"Data structure optimization failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": data,
                "optimization_info": {
                    "original_type": type(data).__name__,
                    "error_timestamp": datetime.datetime.utcnow().isoformat()
                }
            }
    
    def save_optimized_data(self, data: Any, file_path: Union[str, Path], 
                           output_format: Optional[DataFormat] = None) -> bool:
        """Save optimized data to file"""
        try:
            output_format = output_format or self.config.output_format
            file_path = Path(file_path)
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert data to specified format
            converted_data = self.convert_to_format(data, output_format)
            
            # Write to file
            if isinstance(converted_data, bytes):
                with open(file_path, 'wb') as f:
                    f.write(converted_data)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(converted_data)
            
            logger.info(f"Data saved successfully to {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save data to {file_path}: {str(e)}")
            return False
    
    def load_and_optimize_data(self, file_path: Union[str, Path], 
                              data_type: Optional[str] = None) -> Dict[str, Any]:
        """Load data from file and optimize it"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Determine file format from extension
            file_extension = file_path.suffix.lower()
            
            if file_extension == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif file_extension in ['.yml', '.yaml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            elif file_extension == '.pickle':
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
            else:
                # Try to load as text
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()
            
            # Optimize the loaded data
            return self.optimize_data_structure(data, data_type)
        
        except Exception as e:
            logger.error(f"Failed to load and optimize data from {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

# Utility functions for Ansible integration
def create_vmware_resource_data(resource_id: str, resource_type: str, 
                               resource_name: str, resource_state: str,
                               properties: Dict[str, Any], 
                               metadata: Optional[Dict[str, Any]] = None) -> VMwareResourceData:
    """Create standardized VMware resource data"""
    return VMwareResourceData(
        resource_id=resource_id,
        resource_type=resource_type,
        resource_name=resource_name,
        resource_state=resource_state,
        properties=properties,
        metadata=metadata or {},
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )

def create_operation_result(operation_id: str, operation_type: str,
                           operation_name: str, status: str,
                           start_time: datetime.datetime, success: bool,
                           **kwargs) -> OperationResult:
    """Create standardized operation result"""
    return OperationResult(
        operation_id=operation_id,
        operation_type=operation_type,
        operation_name=operation_name,
        status=status,
        start_time=start_time,
        success=success,
        **kwargs
    )

def create_session_data(session_id: str, session_type: str,
                       session_name: str, start_time: datetime.datetime,
                       operations: List[OperationResult],
                       **kwargs) -> SessionData:
    """Create standardized session data"""
    successful_ops = sum(1 for op in operations if op.success)
    failed_ops = len(operations) - successful_ops
    
    return SessionData(
        session_id=session_id,
        session_type=session_type,
        session_name=session_name,
        start_time=start_time,
        operations=operations,
        total_operations=len(operations),
        successful_operations=successful_ops,
        failed_operations=failed_ops,
        **kwargs
    )

# Main execution for testing
if __name__ == "__main__":
    # Example usage
    config = DataStructureConfig(
        output_format=DataFormat.JSON,
        validation_level=ValidationLevel.STANDARD,
        include_metadata=True,
        pretty_print=True
    )
    
    optimizer = DataStructureOptimizer(config)
    
    # Example data
    sample_data = {
        "vmName": "test-vm-01",
        "vmState": "running",
        "resourcePool": "production",
        "hardware": {
            "memoryMB": 4096,
            "numCPUs": 2
        },
        "networks": [
            {"name": "VM Network", "connected": True},
            {"name": "Storage Network", "connected": False}
        ]
    }
    
    # Optimize data structure
    result = optimizer.optimize_data_structure(sample_data, "vmware_resource")
    
    if result["success"]:
        print("Data optimization successful:")
        print(json.dumps(result["data"], indent=2, default=str))
    else:
        print(f"Data optimization failed: {result['error']}")