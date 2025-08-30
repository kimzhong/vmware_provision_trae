# VMware VM Provisioning Flow Diagrams

This document provides detailed workflow diagrams for the virtual machine automation deployment system based on Ansible AAP 2.4 and VMware vCenter 8.0. The system adopts a fully decoupled architecture design, supporting call chain tracking, standardized output, retry mechanism, idempotency guarantee, and state management.

## Core Architecture Components

- **Call Stack Management** - Track execution paths and dependencies
- **Standardized Output with set_stats** - Unified output format to AAP Artifacts
- **Retry Mechanism** - Automatic retry of failed operations
- **Idempotency Guarantee** - Ensure operations can be executed repeatedly
- **State Tracking in AAP Inventory** - Real-time state management
- **Decoupled Operations** - Independent configuration of VM/Network/Storage

## Version 2 Core Components Integration

The Version 2 implementation introduces five core management components that integrate seamlessly with the existing workflow:

### Core Component Roles

1. **call_stack_manager** - Initializes and maintains call chain tracking throughout deployment
2. **output_manager** - Standardizes output format and manages artifacts collection
3. **retry_manager** - Provides centralized retry logic with intelligent backoff strategies
4. **idempotency_checker** - Validates resource state and ensures safe re-execution
5. **aap_state_manager** - Manages synchronization with AAP inventory and job state

### Component Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    Version 2 Core Components Integration                       │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Deployment  │
    │   Start     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Call Stack  │ ◄─── Initialize session tracking
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ AAP State   │ ◄─── Sync with AAP inventory
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Idempotency │ ◄─── Check existing resources
    │ Checker     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Main        │ ◄─── Execute with retry support
    │ Deployment  │
    │ Logic       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Retry       │ ◄─── Handle failures intelligently
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Output      │ ◄─── Standardize and collect outputs
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Deployment  │
    │ Complete    │
    └─────────────┘
```

## Workflow Categories

1. **Main Deployment Flow** - Complete VM deployment workflow
2. **Decoupled Component Flow** - Independent configuration flow for VM/Network/Storage
3. **State Management Flow** - State tracking and recovery mechanism
4. **Call Chain Management Flow** - Call chain tracking and management
5. **Error Handling Flow** - Error detection, retry and recovery
6. **AAP Integration Flow** - Integration workflow with Ansible AAP

## 1. Main Deployment Flow

Complete VM deployment workflow based on decoupled architecture, supporting call chain tracking and state management:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Main VM Deployment Flow                              │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   START     │
    │ Deployment  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Initialize  │
    │ Call Chain  │
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Environment │
    │ Validation  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ Environment │ FAIL │ Deployment  │
    │ Check OK?   ├─────▶│   Failed    │
    └──────┬──────┘      └─────────────┘
           │ PASS
           ▼
    ┌─────────────┐
    │ Idempotency │
    │   Checker   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ Resource    │ YES  │ Skip VM     │
    │ Exists?     ├─────▶│ Creation    │
    └──────┬──────┘      └──────┬──────┘
           │ NO                  │
           ▼                     │
    ┌─────────────┐              │
    │ VM Creation │              │
    │ Component   │              │
    └──────┬──────┘              │
           │                     │
           ▼                     │
    ┌─────────────┐              │
    │ Update AAP  │◄─────────────┘
    │   Status    │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Network     │
    │ Config      │
    │ Component   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Storage     │
    │ Config      │
    │ Component   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Inventory   │
    │   Update    │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Standardized│
    │ Output      │
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Deployment  │
    │ Successful  │
    └─────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Error Handling                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ VM Creation │
    │   Failed    │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Network     │
    │ Config      │
    │ Failed      │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Storage     │
    │ Config      │
    │ Failed      │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Retry       │
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ Retry Count │ YES  │ Deployment  │
    │ Exceeded?   ├─────▶│   Failed    │
    └──────┬──────┘      └─────────────┘
           │ NO
           ▼
    ┌─────────────┐
    │ Delay Wait  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Failure     │
    │ Type Check  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ VM Creation │      │ Network     │      │ Storage     │
    │ Retry       │      │ Config      │      │ Config      │
    │             │      │ Retry       │      │ Retry       │
    └─────────────┘      └─────────────┘      └─────────────┘
```

## 2. Decoupled Component Flow

### 2.1 VM Creation Component Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           VM Creation Component                                │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ VM Creation │
    │   Start     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Register    │
    │ Call Chain  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Idempotency │
    │ Check       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ VM Exists?  │ YES  │ Skip VM     │
    └──────┬──────┘ ────▶│ Creation    │
           │ NO          └──────┬──────┘
           ▼                    │
    ┌─────────────┐             │
    │ Select OS   │             │
    │ Template    │             │
    └──────┬──────┘             │
           │                    │
           ▼                    │
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ OS Type?    │ WIN  │ Windows     │      │ Linux       │
    └──────┬──────┘ ────▶│ 2019/2022   │      │ SUSE/RHEL   │
           │ LINUX       └──────┬──────┘      └──────┬──────┘
           └─────────────────────┼─────────────────────┘
                                 ▼
                          ┌─────────────┐
                          │ Apply OS    │
                          │ Config      │
                          └──────┬──────┘
                                 │
                                 ▼
                          ┌─────────────┐
                          │ Create VM   │
                          └──────┬──────┘
                                 │
                                 ▼
                          ┌─────────────┐      ┌─────────────┐
                          │ Creation    │ FAIL │ Trigger     │
                          │ Success?    ├─────▶│ Retry       │
                          └──────┬──────┘      └──────┬──────┘
                                 │ SUCCESS            │
                                 ▼                    ▼
                          ┌─────────────┐      ┌─────────────┐
                          │ Update AAP  │      │ Retry       │
                          │ Status      │      │ Check       │
                          └──────┬──────┘      └──────┬──────┘
                                 │                    │
                                 ▼                    ▼
                          ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                          │ Standardized│      │ Continue?   │ NO   │ VM Creation │
                          │ Output      │◄─────┤             ├─────▶│ Failed      │
                          └──────┬──────┘      └──────┬──────┘      └─────────────┘
                                 │                    │ YES
                                 ▼                    ▼
                          ┌─────────────┐      ┌─────────────┐
                          │ VM Component│      │ Return to   │
                          │ Complete    │      │ OS Template │
                          └─────────────┘      │ Selection   │
                                               └─────────────┘
```

### 2.2 Network Configuration Component Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Network Configuration Component                         │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Network     │
    │ Config      │
    │ Start       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Register    │
    │ Call Chain  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Get VM      │
    │ Status      │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ VM Ready?   │ NO   │ Network     │
    └──────┬──────┘ ────▶│ Config      │
           │ YES         │ Failed      │
           ▼             └─────────────┘
    ┌─────────────┐
    │ Network     │
    │ Idempotency │
    │ Check       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ Network     │ YES  │ Skip Network│
    │ Adapter     ├─────▶│ Config      │
    │ Exists?     │      └──────┬──────┘
    └──────┬──────┘             │
           │ NO                 │
           ▼                    │
    ┌─────────────┐             │
    │ Environment │             │
    │ Selection   │             │
    └──────┬──────┘             │
           │                    │
           ▼                    │
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Deploy Env? │ DEV  │ Dev Network │ SIT  │ Test Network│ UAT  │ UAT Network │
    └──────┬──────┘ ────▶└──────┬──────┘ ────▶└──────┬──────┘ ────▶└──────┬──────┘
           │ PROD              │               │               │
           ▼                   │               │               │
    ┌─────────────┐             │               │               │
    │ Prod Network│             │               │               │
    └──────┬──────┘             │               │               │
           │                    │               │               │
           └────────────────────┼───────────────┼───────────────┘
                                ▼
                         ┌─────────────┐
                         │ Configure   │
                         │ Network     │
                         │ Isolation   │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Add Network │
                         │ Adapter     │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐      ┌─────────────┐
                         │ Config      │ FAIL │ Trigger     │
                         │ Success?    ├─────▶│ Retry       │
                         └──────┬──────┘      └──────┬──────┘
                                │ SUCCESS            │
                                ▼                    ▼
                         ┌─────────────┐      ┌─────────────┐
                         │ Update AAP  │      │ Retry       │
                         │ Status      │      │ Check       │
                         └──────┬──────┘      └──────┬──────┘
                                │                    │
                                ▼                    ▼
                         ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                         │ Standardized│      │ Continue?   │ NO   │ Network     │
                         │ Output      │◄─────┤             ├─────▶│ Component   │
                         └──────┬──────┘      └──────┬──────┘      │ Failed      │
                                │                    │ YES         └─────────────┘
                                ▼                    ▼
                         ┌─────────────┐      ┌─────────────┐
                         │ Network     │      │ Return to   │
                         │ Component   │      │ Environment │
                         │ Complete    │      │ Selection   │
                         └─────────────┘      └─────────────┘
```

### 2.3 Storage Configuration Component Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Storage Configuration Component                         │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Storage     │
    │ Config      │
    │ Start       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Register    │
    │ Call Chain  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Get VM      │
    │ Status      │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ VM Ready?   │ NO   │ Storage     │
    └──────┬──────┘ ────▶│ Config      │
           │ YES         │ Failed      │
           ▼             └─────────────┘
    ┌─────────────┐
    │ Storage     │
    │ Idempotency │
    │ Check       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐
    │ Disk        │ YES  │ Skip Storage│
    │ Exists?     ├─────▶│ Config      │
    └──────┬──────┘      └──────┬──────┘
           │ NO                 │
           ▼                    │
    ┌─────────────┐             │
    │ Disk Spec   │             │
    │ Definition  │             │
    └──────┬──────┘             │
           │                    │
           ▼                    │
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Storage     │ SYS  │ System Disk │ DATA │ Data Disk   │
    │ Type?       ├─────▶│ Config      ├─────▶│ Config      │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │ LOG               │               │
           ▼                   │               │
    ┌─────────────┐             │               │
    │ Log Disk    │             │               │
    │ Config      │             │               │
    └──────┬──────┘             │               │
           │                    │               │
           └────────────────────┼───────────────┘
                                ▼
                         ┌─────────────┐
                         │ Select      │
                         │ Datastore   │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Add Disk    │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐      ┌─────────────┐
                         │ Config      │ FAIL │ Trigger     │
                         │ Success?    ├─────▶│ Retry       │
                         └──────┬──────┘      └──────┬──────┘
                                │ SUCCESS            │
                                ▼                    ▼
                         ┌─────────────┐      ┌─────────────┐
                         │ Update AAP  │      │ Retry       │
                         │ Status      │      │ Check       │
                         └──────┬──────┘      └──────┬──────┘
                                │                    │
                                ▼                    ▼
                         ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                         │ Standardized│      │ Continue?   │ NO   │ Storage     │
                         │ Output      │◄─────┤             ├─────▶│ Component   │
                         └──────┬──────┘      └──────┬──────┘      │ Failed      │
                                │                    │ YES         └─────────────┘
                                ▼                    ▼
                         ┌─────────────┐      ┌─────────────┐
                         │ Storage     │      │ Return to   │
                         │ Component   │      │ Disk Spec   │
                         │ Complete    │      │ Definition  │
                         └─────────────┘      └─────────────┘
```

## 3. State Management Flow

### 3.1 AAP State Tracking Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            AAP State Tracking                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ State       │
    │ Management  │
    │ Start       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Check       │
    │ Existing    │
    │ State       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ AAP         │ NEW  │ Create      │ EXIST│ Load        │
    │ Inventory   ├─────▶│ State File  ├─────▶│ Existing    │
    │ Status?     │      └──────┬──────┘      │ State       │
    └─────────────┘             │             └──────┬──────┘
                                ▼                    │
                         ┌─────────────┐             ▼
                         │ Initialize  │      ┌─────────────┐      ┌─────────────┐
                         │ State       │      │ State       │ VALID│ State       │
                         │ Variables   │      │ Validation  ├─────▶│ Ready       │
                         └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
                                │                    │ INVALID            │
                                ▼                    ▼                    │
                         ┌─────────────┐      ┌─────────────┐             │
                         │ Set Initial │      │ State       │             │
                         │ State       │      │ Recovery    │             │
                         └──────┬──────┘      └──────┬──────┘             │
                                │                    │                    │
                                │                    ▼                    │
                                │             ┌─────────────┐             │
                                │             │ Repair State│             │
                                │             │ Data        │             │
                                │             └──────┬──────┘             │
                                │                    │                    │
                                └────────────────────┼────────────────────┘
                                                     ▼
                                              ┌─────────────┐
                                              │ Execute     │
                                              │ Operation   │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ Update      │
                                              │ State       │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ Save to AAP │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐      ┌─────────────┐
                                              │ Continue?   │ YES  │ Next Step   │
                                              └──────┬──────┘ ────▶└──────┬──────┘
                                                     │ NO                 │
                                                     ▼                    │
                                              ┌─────────────┐             │
                                              │ State       │◄────────────┘
                                              │ Management  │
                                              │ Complete    │
                                              └─────────────┘
```

### 3.2 State Recovery and Re-run Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         State Recovery and Re-run                              │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Re-run      │
    │ Detection   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Read AAP    │
    │ State       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Last        │ VM   │ Continue    │ NET  │ Continue    │ STOR │ Continue    │ FAIL │ Error       │
    │ Execution   ├─────▶│ from VM     ├─────▶│ from Network├─────▶│ from Storage├─────▶│ Analysis    │
    │ Status?     │      │ Creation    │      │ Config      │      │ Config      │      └──────┬──────┘
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘             │
           │ COMPLETE           │                    │                    │                    ▼
           ▼                    ▼                    ▼                    ▼             ┌─────────────┐
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      │ Error Type  │
    │ Skip        │      │ VM State    │      │ Network     │      │ Storage     │      │ Analysis    │
    │ Duplicate   │      │ Validation  │      │ State       │      │ State       │      └──────┬──────┘
    │ Execution   │      └──────┬──────┘      │ Validation  │      │ Validation  │             │
    └─────────────┘             │             └──────┬──────┘      └──────┬──────┘             ▼
                                ▼                    │                    │             ┌─────────────┐
                         ┌─────────────┐             ▼                    ▼             │ Recoverable?│
                         │ VM          │      ┌─────────────┐      ┌─────────────┐      └──────┬──────┘
                         │ Complete?   │      │ Network     │      │ Storage     │             │
                         └──────┬──────┘      │ Normal?     │      │ Ready?      │             ▼
                                │             └──────┬──────┘      └──────┬──────┘      ┌─────────────┐
                                ▼                    │                    │             │ Auto Repair │
                         ┌─────────────┐             ▼                    ▼             └──────┬──────┘
                         │ Continue    │ YES  ┌─────────────┐      ┌─────────────┐             │
                         │ Network     ├─────▶│ Continue    │ YES  │ Complete    │ YES         ▼
                         │ Config      │      │ Storage     ├─────▶│ Deployment  ├─────▶┌─────────────┐
                         └──────┬──────┘      │ Config      │      └─────────────┘      │ Re-execute  │
                                │ NO          └──────┬──────┘                          └─────────────┘
                                ▼                    │ NO
                         ┌─────────────┐             ▼
                         │ Recreate VM │      ┌─────────────┐
                         └─────────────┘      │ Reconfigure │
                                              │ Network     │
                                              └─────────────┘
                                                     │ NO
                                                     ▼
                                              ┌─────────────┐
                                              │ Reconfigure │
                                              │ Storage     │
                                              └─────────────┘

                                       ┌─────────────┐      ┌─────────────┐
                                       │ Manual      │ NO   │ Pause and   │
                                       │ Intervention├─────▶│ Wait        │
                                       │ Required?   │      └─────────────┘
                                       └─────────────┘
```

## 4. Call Stack Management Flow

### 4.1 Call Stack Tracking Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Call Stack Tracking                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Call Stack  │
    │ Start       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Initialize  │
    │ Call Stack  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Register    │
    │ Caller Info │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Generate    │
    │ Call Stack  │
    │ ID          │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Update Call │
    │ Depth       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Execution   │ VM   │ VM          │ NET  │ Network     │ STOR │ Storage     │
    │ Type?       ├─────▶│ Component   ├─────▶│ Component   ├─────▶│ Component   │
    └─────────────┘      │ Call        │      │ Call        │      │ Call        │
           ▲             └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                    │                    │
           │                    ▼                    ▼                    ▼
           │             ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
           │             │ Record VM   │      │ Record      │      │ Record      │
           │             │ Call        │      │ Network Call│      │ Storage Call│
           │             └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                    │                    │
           │                    └────────────────────┼────────────────────┘
           │                                         ▼
           │                                  ┌─────────────┐
           │                                  │ Establish   │
           │                                  │ Dependencies│
           │                                  └──────┬──────┘
           │                                         │
           │                                         ▼
           │                                  ┌─────────────┐
           │                                  │ Update AAP  │
           │                                  │ State       │
           │                                  └──────┬──────┘
           │                                         │
           │                                         ▼
           │                                  ┌─────────────┐
           │                                  │ Standardized│
           │                                  │ Output      │
           │                                  └──────┬──────┘
           │                                         │
           │                                         ▼
           │                                  ┌─────────────┐      ┌─────────────┐
           │                                  │ Sub-calls?  │ YES  │ Recursive   │
           │                                  └──────┬──────┘ ────▶│ Call        │
           │                                         │ NO          └──────┬──────┘
           │                                         ▼                    │
           │                                  ┌─────────────┐             ▼
           │                                  │ Return to   │      ┌─────────────┐
           │                                  │ Parent      │      │ Increase    │
           │                                  └──────┬──────┘      │ Call Depth  │
           │                                         │             └──────┬──────┘
           │                                         ▼                    │
           │                                  ┌─────────────┐             │
           │                                  │ Decrease    │◄────────────┘
           │                                  │ Call Depth  │
           │                                  └──────┬──────┘
           │                                         │
           │                                         ▼
           │                                  ┌─────────────┐      ┌─────────────┐
           │                                  │ Root Call?  │ YES  │ Call Stack  │
           │                                  └──────┬──────┘ ────▶│ Complete    │
           │                                         │ NO          └─────────────┘
           │                                         ▼
           │                                  ┌─────────────┐
           │                                  │ Continue    │
           │                                  │ Return      │
           │                                  └──────┬──────┘
           │                                         │
           └─────────────────────────────────────────┘
```

### 4.2 Call Stack Output Format

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         Call Stack Output Format                               │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Call Stack  ├─────▶│ Call Stack  ├─────▶│ Call Depth  ├─────▶│ Timestamp   │
    │ Data        │      │ ID          │      │             │      │             │
    └─────────────┘      └─────────────┘      └─────────────┘      └──────┬──────┘
                                                                           │
                                                                           ▼
                                                                    ┌─────────────┐
                                                                    │ Dependencies│
                                                                    └──────┬──────┘
                                                                           │
                                                                           ▼
                                                                    ┌─────────────┐
                                                                    │ Format      │
                                                                    │ Output      │
                                                                    └──────┬──────┘
                                                                           │
                                                                           ▼
                                                                    ┌─────────────┐
                                                                    │ Save to AAP │
                                                                    └──────┬──────┘
                                                                           │
                                                                           ▼
                                                                    ┌─────────────┐
                                                                    │ set_stats   │
                                                                    │ Output      │
                                                                    └──────┬──────┘
                                                                           │
                                                                           ▼
                                                                    ┌─────────────┐
                                                                    │ Call Stack  │
                                                                    │ Example:    │
                                                                    │ playbook_   │
                                                                    │ main →      │
                                                                    │ vm_provision│
                                                                    │ → network_  │
                                                                    │ config →    │
                                                                    │ storage_    │
                                                                    │ config      │
                                                                    └─────────────┘
```

## 5. Error Handling Flow

### 5.1 Error Detection and Classification Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       Error Detection and Classification                       │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Error       │
    │ Detection   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Error       │
    │ Analysis    │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Error       │ VM   │ VM Related  │ NET  │ Network     │ STOR │ Storage     │ SYS  │ System      │
    │ Type?       ├─────▶│ Errors      ├─────▶│ Related     ├─────▶│ Related     ├─────▶│ Related     │
    └─────────────┘      └──────┬──────┘      │ Errors      │      │ Errors      │      │ Errors      │
                                │             └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
                                ▼                    │                    │                    │
                         ┌─────────────┐             ▼                    ▼                    ▼
                         │ VM Error    │      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                         │ Subclass?   │      │ Network     │      │ Storage     │      │ System      │
                         └──────┬──────┘      │ Error       │      │ Error       │      │ Error       │
                                │             │ Subclass?   │      │ Subclass?   │      │ Subclass?   │
                                ▼             └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
                         ┌─────────────┐             │                    │                    │
                         │ Template    │ TMPL        ▼                    ▼                    ▼
                         │ Missing/    ├──────┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                         │ Corrupted   │      │ Network     │ DISK │ Disk Space  │ CONN │ vCenter     │
                         └──────┬──────┘      │ Missing/    ├─────▶│ Insufficient├─────▶│ Connection  │
                                │ RSRC        │ VLAN        │      └──────┬──────┘      │ Timeout     │
                                ▼             └──────┬──────┘             │             └──────┬──────┘
                         ┌─────────────┐             │ IP                 ▼                    │
                         │ CPU/Memory  │             ▼             ┌─────────────┐             ▼
                         │ Insufficient│      ┌─────────────┐      │ Storage     │      ┌─────────────┐
                         └──────┬──────┘      │ IP Address  │      │ Unavailable │      │ Auth        │
                                │ PERM        │ Conflict    │      └──────┬──────┘      │ Failure     │
                                ▼             └──────┬──────┘             │ PERM        └──────┬──────┘
                         ┌─────────────┐             │ DNS                ▼                    │ API
                         │ vCenter     │             ▼             ┌─────────────┐             ▼
                         │ Permission  │      ┌─────────────┐      │ Storage     │      ┌─────────────┐
                         └──────┬──────┘      │ DNS         │      │ Permission  │      │ API Call    │
                                │             │ Resolution  │      └──────┬──────┘      │ Error       │
                                │             └──────┬──────┘             │             └──────┬──────┘
                                │                    │                    │                    │
                                └────────────────────┼────────────────────┼────────────────────┘
                                                     ▼                    │
                                              ┌─────────────┐             │
                                              │ Record      │◄────────────┘
                                              │ Error       │
                                              │ Details     │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ Update AAP  │
                                              │ State       │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ Enter Retry │
                                              │ Flow        │
                                              └─────────────┘
```

### 5.2 Retry Mechanism Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            Retry Mechanism                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Retry       │
    │ Manager     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Check Retry │
    │ Count       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Retry       │ NOT  │ Calculate   │ OVER │ Retry       │
    │ Count?      ├─────▶│ Delay Time  ├─────▶│ Failed      │
    └─────────────┘      └──────┬──────┘      └──────┬──────┘
           ▲                    │                    │
           │                    ▼                    ▼
           │             ┌─────────────┐      ┌─────────────┐
           │             │ Error       │      │ Record      │
           │             │ Severity?   │      │ Final       │
           │             └──────┬──────┘      │ Failure     │
           │                    │             └──────┬──────┘
           │                    ▼                    │
           │             ┌─────────────┐             ▼
           │             │ Minor:      │ MINOR┌─────────────┐
           │             │ Short Delay ├─────▶│ Update AAP  │
           │             │ (10s)       │      │ State       │
           │             └──────┬──────┘      └──────┬──────┘
           │                    │ MODERATE           │
           │                    ▼                    ▼
           │             ┌─────────────┐      ┌─────────────┐
           │             │ Moderate:   │      │ Send Alert  │
           │             │ Medium Delay│      └─────────────┘
           │             │ (30s)       │
           │             └──────┬──────┘
           │                    │ SEVERE
           │                    ▼
           │             ┌─────────────┐
           │             │ Severe:     │
           │             │ Long Delay  │
           │             │ (60s)       │
           │             └──────┬──────┘
           │                    │
           │                    ▼
           │             ┌─────────────┐
           │             │ Execute     │
           │             │ Retry       │
           │             └──────┬──────┘
           │                    │
           │                    ▼
           │             ┌─────────────┐      ┌─────────────┐
           │             │ Retry       │ SUCC │ Retry       │
           │             │ Result?     ├─────▶│ Success     │
           │             └──────┬──────┘      └─────────────┘
           │                    │ FAIL
           │                    ▼
           │             ┌─────────────┐
           │             │ Increase    │
           │             │ Retry Count │
           │             └──────┬──────┘
           │                    │
           │                    ▼
           │             ┌─────────────┐
           │             │ Record      │
           │             │ Retry       │
           │             │ Failure     │
           │             └──────┬──────┘
           │                    │
           │                    ▼
           │             ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
           │             │ Error       │ SAME │ Continue    │ NEW  │ Re-analyze  │
           │             │ Changed?    ├─────▶│ Retry       ├─────▶│ Error       │
           │             └─────────────┘      └──────┬──────┘      └──────┬──────┘
           │                                         │                    │
           └─────────────────────────────────────────┘                    ▼
                                                                    ┌─────────────┐
                                                                    │ Error       │
                                                                    │ Re-classify │
                                                                    └──────┬──────┘
                                                                           │
                                                                           ▼
                                                                    ┌─────────────┐
                                                                    │ Reset Retry │
                                                                    │ Count       │
                                                                    └──────┬──────┘
                                                                           │
                                                                           │
                                                                           └──────────────────────┐
                                                                                                  │
                                                                                                  │
                                                                           ┌──────────────────────┘
                                                                           │
                                                                           ▼
                                                                    ┌─────────────┐
                                                                    │ Back to     │
                                                                    │ Check Retry │
                                                                    │ Count       │
                                                                    └─────────────┘
```

## 6. State Management Flow

### 6.1 State Initialization and Validation Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      State Initialization and Validation                      │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ State       │
    │ Management  │
    │ Start       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Check AAP   │
    │ State       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ State       │ EXIST│ Verify      │ NONE │ Initialize  │
    │ Exists?     ├─────▶│ State       ├─────▶│ New State   │
    └─────────────┘      │ Integrity   │      └──────┬──────┘
                         └──────┬──────┘             │
                                │                    ▼
                                ▼             ┌─────────────┐
                         ┌─────────────┐      │ Create      │
                         │ State       │      │ State       │
                         │ Valid?      │      │ Structure   │
                         └──────┬──────┘      └──────┬──────┘
                                │ VALID              │
                                ▼                    ▼
                         ┌─────────────┐      ┌─────────────┐
                         │ Load        │      │ Set Initial │
                         │ Historical  │      │ Parameters  │
                         │ State       │      └──────┬──────┘
                         └──────┬──────┘             │
                                │ INVALID            ▼
                                ▼             ┌─────────────┐
                         ┌─────────────┐      │ Save        │
                         │ State       │      │ Initial     │
                         │ Repair      │      │ State       │
                         └──────┬──────┘      └──────┬──────┘
                                │                    │
                                ▼                    │
                         ┌─────────────┐             │
                         │ Repair      │ SUCC        │
                         │ Success?    ├─────────────┼─────────────┐
                         └──────┬──────┘             │             │
                                │ FAIL               │             │
                                └────────────────────┘             │
                                                                   │
                                ┌──────────────────────────────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Analyze     │
                         │ Execution   │
                         │ History     │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                         │ Is Re-run?  │ YES  │ Determine   │ NO   │ Normal      │
                         └──────┬──────┘      │ Recovery    ├─────▶│ Execution   │
                                │             │ Point       │      └──────┬──────┘
                                │             └──────┬──────┘             │
                                │                    │                    │
                                │                    ▼                    │
                                │             ┌─────────────┐             │
                                │             │ Recovery    │             │
                                │             │ Point Type? │             │
                                │             └──────┬──────┘             │
                                │                    │                    │
                                │                    ▼                    │
                                │             ┌─────────────┐             │
                                │             │ VM Creation │ VM          │
                                │             │ Recovery    ├─────────────┼─────┐
                                │             └──────┬──────┘             │     │
                                │                    │ NET                │     │
                                │                    ▼                    │     │
                                │             ┌─────────────┐             │     │
                                │             │ Network     │             │     │
                                │             │ Config      ├─────────────┼─────┤
                                │             │ Recovery    │             │     │
                                │             └──────┬──────┘             │     │
                                │                    │ STOR               │     │
                                │                    ▼                    │     │
                                │             ┌─────────────┐             │     │
                                │             │ Storage     │             │     │
                                │             │ Config      ├─────────────┼─────┤
                                │             │ Recovery    │             │     │
                                │             └──────┬──────┘             │     │
                                │                    │ FULL               │     │
                                │                    └────────────────────┘     │
                                │                                               │
                                └───────────────────────────────────────────────┼─────┐
                                                                                │     │
                                                                                │     │
                                                                         ┌──────┴─────┴──┐
                                                                         │ State Ready   │
                                                                         └───────────────┘
```

### 6.2 State Update and Synchronization Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      State Update and Synchronization                          │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ State       │
    │ Update      │
    │ Triggered   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Get Current │
    │ State       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Prepare     │
    │ Update Data │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Update      │ TASK │ Update Task │ RSRC │ Update      │ ERR  │ Update      │ DONE │ Update      │
    │ Type?       ├─────▶│ Progress    ├─────▶│ Resource    ├─────▶│ Error       ├─────▶│ Completion  │
    └─────────────┘      └──────┬──────┘      │ Info        │      │ Info        │      │ Info        │
                                │             └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
                                ▼                    │                    │                    │
                         ┌─────────────┐             ▼                    ▼                    ▼
                         │ Calculate   │      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                         │ Progress    │      │ Verify      │      │ Record      │      │ Mark Task   │
                         │ Percentage  │      │ Resource    │      │ Error       │      │ Complete    │
                         └──────┬──────┘      │ State       │      │ Details     │      └──────┬──────┘
                                │             └──────┬──────┘      └──────┬──────┘             │
                                │                    │                    │                    │
                                └────────────────────┼────────────────────┼────────────────────┘
                                                     ▼                    │
                                              ┌─────────────┐             │
                                              │ Local State │◄────────────┘
                                              │ Update      │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ AAP State   │
                                              │ Sync        │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                                              │ Sync        │ SUCC │ State Sync  │ FAIL │ Sync        │
                                              │ Success?    ├─────▶│ Complete    ├─────▶│ Failure     │
                                              └─────────────┘      └─────────────┘      │ Handling    │
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌─────────────┐
                                                                                        │ Record      │
                                                                                        │ Sync Error  │
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌─────────────┐
                                                                                        │ Delay       │
                                                                                        │ Retry Sync  │
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌─────────────┐
                                                                                        │ Retry Count │
                                                                                        │ Check       │
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌─────────────┐      ┌─────────────┐
                                                                                        │ Retry       │ OVER │ Sync Final  │
                                                                                        │ Limit?      ├─────▶│ Failure     │
                                                                                        └──────┬──────┘      └──────┬──────┘
                                                                                               │ NOT                │
                                                                                               │                    ▼
                                                                                               │             ┌─────────────┐
                                                                                               │             │ Offline     │
                                                                                               │             │ Mode        │
                                                                                               │             │ Operation   │
                                                                                               │             └──────┬──────┘
                                                                                               │                    │
                                                                                               └────────────────────┼─────────────┐
                                                                                                                    │             │
                                                                                                                    │             │
                                                                                                             ┌──────┴─────────────┴──┐
                                                                                                             │ State Update Complete │
                                                                                                             └───────────────────────┘
```

## 7. AAP Integration Flow

### 7.1 AAP Task Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            AAP Task Execution                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ AAP         │
    │ Integration │
    │ Start       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Get Job     │
    │ Template    │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Verify      │
    │ Template    │
    │ Permission  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Permission  │ PASS │ Launch Job  │ FAIL │ Permission  │
    │ Check?      ├─────▶│             ├─────▶│ Error       │
    └─────────────┘      └──────┬──────┘      └──────┬──────┘
                                │                    │
                                ▼                    │
                         ┌─────────────┐             │
                         │ Get Job ID  │             │
                         └──────┬──────┘             │
                                │                    │
                                ▼                    │
                         ┌─────────────┐             │
                         │ Monitor     │             │
                         │ Execution   │             │
                         │ Status      │             │
                         └──────┬──────┘             │
                                │                    │
                                ▼                    │
                         ┌─────────────┐             │
                         │ Job Status? │             │
                         └──────┬──────┘             │
                                │                    │
                                ▼                    │
                         ┌─────────────┐             │
                         │ RUNNING     │ RUN         │
                         │ Wait        ├─────┐       │
                         │ Execution   │     │       │
                         └──────┬──────┘     │       │
                                │ SUCC       │       │
                                ▼            │       │
                         ┌─────────────┐     │       │
                         │ Execution   │     │       │
                         │ Success     │     │       │
                         └──────┬──────┘     │       │
                                │ FAIL       │       │
                                ▼            │       │
                         ┌─────────────┐     │       │
                         │ Execution   │     │       │
                         │ Failed      │     │       │
                         └──────┬──────┘     │       │
                                │ CANCEL     │       │
                                ▼            │       │
                         ┌─────────────┐     │       │
                         │ Task        │     │       │
                         │ Cancelled   │     │       │
                         └──────┬──────┘     │       │
                                │            │       │
                                │            ▼       │
                                │     ┌─────────────┐ │
                                │     │ Get         │ │
                                │     │ Execution   │ │
                                │     │ Progress    │ │
                                │     └──────┬──────┘ │
                                │            │       │
                                │            ▼       │
                                │     ┌─────────────┐ │
                                │     │ Update      │ │
                                │     │ Status Info │ │
                                │     └──────┬──────┘ │
                                │            │       │
                                │            ▼       │
                                │     ┌─────────────┐ │
                                │     │ Delay Wait  │ │
                                │     └──────┬──────┘ │
                                │            │       │
                                │            └───────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Get         │
                         │ Execution   │
                         │ Result      │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Parse       │
                         │ Output Data │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Update      │
                         │ Inventory   │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Set         │
                         │ set_stats   │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Archive     │
                         │ Execution   │
                         │ Result      │
                         └──────┬──────┘
                                │
                                │
                                └─────────────────────────────────────────────────────┐
                                                                                      │
                                                                                      │
                                                                               ┌──────┴──────┐
                                                                               │ AAP         │
                                                                               │ Integration │
                                                                               │ Complete    │
                                                                               └─────────────┘
```

### 7.2 AAP Data Output and Archive Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AAP Data Output and Archive                             │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ Data Output │
    │ Start       │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Collect     │
    │ Execution   │
    │ Data        │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Format      │
    │ Output Data │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Output      │ STAT │ Status Info │ RSLT │ Execution   │ ERR  │ Error Info  │ CALL │ Call Chain  │
    │ Type?       ├─────▶│ Output      ├─────▶│ Result      ├─────▶│ Output      ├─────▶│ Output      │
    └─────────────┘      └──────┬──────┘      │ Output      │      └──────┬──────┘      └──────┬──────┘
                                │             └──────┬──────┘             │                    │
                                │                    │                    │                    │
                                └────────────────────┼────────────────────┼────────────────────┘
                                                     ▼                    │
                                              ┌─────────────┐             │
                                              │ Use         │◄────────────┘
                                              │ set_stats   │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ Save to AAP │
                                              │ Artifacts   │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ Create      │
                                              │ Archive     │
                                              │ File        │
                                              └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                                              │ Archive     │ JSON │ JSON Format │ YAML │ YAML Format │ LOG  │ Log Format  │
                                              │ Type?       ├─────▶│             ├─────▶│             ├─────▶│             │
                                              └─────────────┘      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
                                                                          │                    │                    │
                                                                          ▼                    ▼                    ▼
                                                                   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                                                                   │ Save JSON   │      │ Save YAML   │      │ Save Log    │
                                                                   │ File        │      │ File        │      │ File        │
                                                                   └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
                                                                          │                    │                    │
                                                                          └────────────────────┼────────────────────┘
                                                                                               ▼
                                                                                        ┌─────────────┐
                                                                                        │ Generate    │
                                                                                        │ Download    │
                                                                                        │ Link        │
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌─────────────┐
                                                                                        │ Send        │
                                                                                        │ Notification│
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌─────────────┐
                                                                                        │ Update      │
                                                                                        │ Execution   │
                                                                                        │ Statistics  │
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌─────────────┐
                                                                                        │ Output      │
                                                                                        │ Archive     │
                                                                                        │ Complete    │
                                                                                        └─────────────┘
```

## 8. Architecture Features Summary

### 8.1 Core Architecture Features Implementation

This workflow diagram system fully embodies all core features of the Enhanced VMware Virtual Machine Decoupled Deployment Solution defined in `context.md`:

#### 🔗 Call Chain Management
- **Call Chain Tracking Flow** implements complete call chain management mechanism
- Achieves call chain identification and depth tracking through `ansible_call_stack` and `ansible_call_depth`
- Supports recursive calls and dependency relationship establishment
- Provides complete call chain output format

#### 📊 Standardized Output Management
- **AAP Data Output and Archive Flow** implements standardized output management
- Contains complete structure including metadata, context, task information, data and infrastructure information
- Supports multiple output formats (JSON, YAML, LOG)
- Implements output recording to files and AAP Artifacts

#### 🔄 Retry Mechanism
- **Retry Mechanism Flow** implements intelligent retry management
- Supports dynamic delay strategy based on error severity
- Includes retry count management and error change detection
- Provides alert mechanism for retry failures

#### ✅ Idempotency Guarantee
- **Main Deployment Flow** and **Decoupled Component Flows** integrate idempotency checks
- Existence checks for VM, network adapter and disk resources
- Implemented through `vmware_guest_info`, `vmware_vm_vnic_info` and `vmware_vm_disk_info` modules
- Ensures safety of repeated executions

#### 📊 State Tracking
- **State Management Flow** implements complete state tracking mechanism
- Supports state initialization, validation, update and synchronization
- Contains dual mechanism of AAP state management and local state management
- Provides state recovery and re-run functionality

#### 🔧 Decoupled Operations
- **Decoupled Component Flows** implement complete decoupling of VM, network and storage
- Each component has independent flow and state management
- Supports component-level retry and error handling
- Implements loose coupling design between components

### 8.2 Workflow Usage Guide

#### 📋 Development Team Usage
- **Main Deployment Flow**: As entry point and overall flow reference for the entire architecture
- **Decoupled Component Flows**: For specific component development and implementation
- **Call Chain Management Flow**: For debugging and issue tracking
- **Error Handling Flow**: For exception handling and recovery

#### 🔍 Operations Team Usage
- **State Management Flow**: For monitoring and state management
- **AAP Integration Flow**: For AAP platform integration and management
- **Retry Mechanism Flow**: For fault recovery and retry strategies

#### 📊 Management Team Usage
- **Architecture Features Summary**: For understanding overall architecture design
- **Workflow Overview**: For project progress and quality assessment

### 8.3 Implementation Recommendations

1. **Implement by Workflow Order**: Recommend development and implementation following the logical order of workflows
2. **Component-based Development**: Utilize decoupling features to develop different components in parallel
3. **Test-driven**: Each workflow should have corresponding test cases
4. **Monitoring Integration**: Ensure all workflows are integrated into monitoring and alert systems
5. **Documentation Synchronization**: Keep workflows synchronized with actual code updates

---

> **Note**: This workflow diagram system strictly follows the architectural requirements defined in `context.md`. All playbook development requires supporting design documents, workflow diagrams, test cases, acceptance criteria and usage documentation.
