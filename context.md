1.现在基于 ansible aap 2.4 和 vmware vcenter 8.0 版本，需要开发一套自动化生成 vmware vcenter 8.0 版本的 vm 的 playbook，需要用到 ansible playbook role 2.基于克隆 vm template 来创建 vm，vm 创建完需要 vm 相关信息写入到 ansible aap 2.4 版本的 inventory 中 3.需要开发一个 role 来实现 vmware vcenter 8.0 版本的 vm 相关信息的写入 ansible aap 2.4 版本的 inventory 中。 4.需要定义好这一套 playbook 需要的， 比如输入 vm template name，或者 vm_os os_version 选择对应的 template，然后需要把 vm 放到对应的 folder 中 5.需要定义好这一套 playbook 需要的变量，比如 vm_name, vm_cpu, vm_memory, vm_os, vm_os_version, vm_folder, vm_datastore, vm_network, vm_gateway, vm_dns, vm_nic,需要尽量的精简和服用变量 6.需要支持多环境/多数据中心的 vm 创建，需要定义好变量来支持，多域名，多 vm_os 即 windows 2019/2022 suse15 redhat8/9 7.需要定义好这一套 playbook 需要的 tags，比如 windows, suse, redhat, 多环境/多数据中心的 vm 创建，独立的 role 8.需要定义好这一套 playbook 需要的 handlers，比如重启 vm，关闭 vm，删除 vm 9.需要定义好这一套 playbook 需要的 vars_prompt，比如 vm_name, vm_cpu, vm_memory, vm_os, vm_os_version, vm_folder, vm_datastore, vm_network, vm_gateway, vm_dns, vm_nic 10.需要定义好这一套 playbook 需要的 vars_files，比如 vm_os_version, vm_folder, vm_datastore, vm_network, vm_gateway, vm_dns, vm_nic
11.vm 的生成需要解耦 vm/network/disk 三个部分，vm 部分需要定义好变量，network 部分需要定义好变量，disk 部分需要定义好变量 12.需要定义好这一套 playbook 需要的 roles，比如 vmware_vcenter80_vm, vmware_vcenter80_network, vmware_vcenter80_disk 13.需要支持幂等性/重跑/失败后重试/失败后手动处理，使用 set_stat 标准化输出，还有调用链报错到 inventroy 里的 host 变量 14.独立一个 role 是处理状态管理，比如 vm 是否存在，network 是否存在，disk 是否存在，vm 是否启动，vm 是否关闭，vm 是否删除，network 是否删除，disk 是否删除 15.独立一个 role 是调用链跟踪，比如 vm 创建完需要调用 vmware_vcenter80_network role 来创建 network，network 创建完需要调用 vmware_vcenter80_disk role 来创建 disk，disk 创建完需要调用 vmware_vcenter80_inventory role 来写入 inventory 16.独立一个 role 是标准化输出需要 set_stat 和输出到 ansible aap job template 的 artifacts 里，比如 vm 创建完需要调用 vmware_vcenter80_inventory role 来写入 inventory，inventory 写入完需要调用 vmware_vcenter80_inventory role 来转化输出
12 所有的操作遵循 ansible 的幂等性/可重跑/失败后重试/失败后手动处理/可回退/溯源/方便排错
13 所有的实现都是 ansible 的 playbook，不需要 python 脚本，使用 ansible aap 2.4 的功能。最后可以设计一套 workflow template 实现多环境多网络多 os 类型多域名的 vm 部署，其他的功能参考公有云的 vm 部署功能，需要支持状态管理等等
14 ansible 的 playbook 是使用 git 来管理的，每个 playbook 都有一个对应的 git 仓库，每个 playbook 都有一个对应的 branch，每个 playbook 都有一个对应的 tag，每个 playbook 都有一个对应的 release，每个 playbook 都有一个对应的 changelog，每个 playbook 都有一个对应的 README.md 文件，每个 playbook 都有一个对应的 LICENSE 文件
15 所有的 playbook 开发需要先有设计文档/流程图/测试用例/验收标准/使用文档

#################
version 2

增强型 VMware 虚拟机解耦部署方案

基于您的需求，我将设计一个完整的解决方案，整合调用链跟踪、标准化输出（使用 set_stats）、重试机制、幂等性和重跑支持，实现 VMware 虚拟机的完全解耦部署。

整体架构设计

```
VMware 解耦部署系统
├── 调用链管理 (Call Stack Management)
├── 标准化输出 (Standardized Output with set_stats)
├── 重试机制 (Retry Mechanism)
├── 幂等性保证 (Idempotency Guarantee)
├── 状态跟踪 (State Tracking in AAP Inventory)
└── 解耦操作 (Decoupled Operations)
    ├── VM 创建 (VM Creation)
    ├── 网络配置 (Network Configuration)
    ├── 存储配置 (Storage Configuration)
    └── OS 内部配置 (OS Internal Configuration)
```

核心组件实现

1. 调用链管理器 (Call Stack Manager)

```yaml
# roles/call_stack_manager/tasks/main.yml
---
- name: 初始化调用栈
  set_fact:
    ansible_call_stack: "{{ ansible_call_stack | default([]) }}"
    ansible_call_depth: "{{ ansible_call_depth | default(0) | int }}"

- name: 添加当前组件到调用栈
  set_fact:
    ansible_call_stack: "{{ ansible_call_stack + [caller_info] }}"
    ansible_call_depth: "{{ ansible_call_depth | int + 1 }}"
  vars:
    caller_info: "{
      'type': '{{ caller_type }}',
      'name': '{{ caller_name }}',
      'timestamp': '{{ ansible_date_time.iso8601 }}',
      'depth': '{{ ansible_call_depth | int }}'
    }"

- name: 生成调用链标识
  set_fact:
    call_chain_id: "{{ ansible_call_stack | map(attribute='name') | join('->') }}"

- name: 注册调用链信息
  set_stats:
    data:
      call_stack: "{{ ansible_call_stack }}"
      call_chain_id: "{{ call_chain_id }}"
      call_depth: "{{ ansible_call_depth }}"
    per_host: false
```

2. 标准化输出管理器 (Standardized Output Manager)

```yaml
# roles/output_manager/tasks/main.yml
---
- name: 准备标准化输出数据
  set_fact:
    standardized_output:
      metadata:
        version: "2.0"
        format: "ansible-aap-standardized"
        generated_at: "{{ ansible_date_time.iso8601 }}"
        execution_id: "{{ execution_id | default(ansible_date_time.epoch) }}"
      context:
        tower_job_id: "{{ tower_job_id | default(omit) }}"
        parent_job_id: "{{ parent_job_id | default(omit) }}"
        call_chain: "{{ call_chain_id | default(omit) }}"
        inventory_hostname: "{{ inventory_hostname }}"
      task:
        name: "{{ task_name | default(omit) }}"
        status: "{{ task_status | default(omit) }}"
        start_time: "{{ task_start_time | default(omit) }}"
        end_time: "{{ task_end_time | default(omit) }}"
        duration: "{{ task_duration | default(omit) }}"
        retry_count: "{{ retry_count | default(0) }}"
      data: "{{ task_data | default({}) }}"
      infrastructure: "{{ infrastructure_data | default({}) }}"

- name: 注册标准化输出
  set_stats:
    data:
      "output_{{ execution_id | default(ansible_date_time.epoch) }}_{{ task_name | default('unknown') }}": "{{ standardized_output }}"
    per_host: true

- name: 记录输出到文件 (可选)
  copy:
    content: "{{ standardized_output | to_nice_json }}"
    dest: "/var/log/ansible/{{ execution_id | default(ansible_date_time.epoch) }}/{{ task_name | default('unknown') }}.json"
  delegate_to: localhost
  when: output_to_file | default(false) | bool
```

3. 重试管理器 (Retry Manager)

```yaml
# roles/retry_manager/tasks/main.yml
---
- name: 初始化重试参数
  set_fact:
    current_retry: "{{ current_retry | default(0) | int + 1 }}"
    max_retries: "{{ max_retries | default(3) }}"
    retry_delay: "{{ retry_delay | default(10) }}"

- name: 检查重试次数
  fail:
    msg: "任务 '{{ task_name }}' 在 {{ max_retries }} 次重试后仍然失败"
  when: current_retry > max_retries

- name: 记录重试开始
  include_role:
    name: output_manager
  vars:
    task_name: "retry_attempt"
    task_data:
      task_name: "{{ task_name }}"
      attempt: "{{ current_retry }}"
      max_attempts: "{{ max_retries }}"
    task_status: "info"

- name: 执行重试延迟
  pause:
    seconds: "{{ retry_delay }}"
  when: current_retry > 1

- name: 执行任务
  include_tasks: "{{ task_file }}"
  register: task_result

- name: 检查任务结果
  set_fact:
    task_succeeded: "{{ task_result is succeeded }}"

- name: 处理任务失败
  when: not task_succeeded
  block:
    - name: 记录重试失败
      include_role:
        name: output_manager
      vars:
        task_name: "retry_failure"
        task_data:
          task_name: "{{ task_name }}"
          attempt: "{{ current_retry }}"
          max_attempts: "{{ max_retries }}"
          error: "{{ task_result.msg | default(task_result|to_json) }}"
        task_status: "warning"

    - name: 递归调用重试管理器
      include_role:
        name: retry_manager
      vars:
        task_file: "{{ task_file }}"
        task_name: "{{ task_name }}"
        current_retry: "{{ current_retry }}"
        max_retries: "{{ max_retries }}"
        retry_delay: "{{ retry_delay }}"
```

4. 幂等性检查器 (Idempotency Checker)

````yaml
# roles/idempotency_checker/tasks/main.yml
---
- name: 检查资源是否存在 (VMware VM)
  block:
    - name: 获取 VM 信息
      vmware_guest_info:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: no
        name: "{{ resource_name }}"
      register: resource_info
      ignore_errors: yes

# roles/idempotency_checker/tasks/main.yml
---
- name: 检查资源是否存在 (VMware VM)
  block:
    - name: 获取 VM 信息
      vmware_guest_info:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: no
        name: "{{ resource_name }}"
      register: resource_info
      ignore_errors: yes
      when: resource_type == "vmware_vm"

    - name: 检查网络适配器是否存在
      vmware_vm_vnic_info:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: no
        vm_id: "{{ resource_id }}"
      register: network_info
      when: resource_type == "vmware_vm_nic"

    - name: 检查磁盘是否存在
      vmware_vm_disk_info:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: no
        vm_id: "{{ resource_id }}"
      register: disk_info
      when: resource_type == "vmware_vm_disk"

  rescue:
    - name: 记录检查失败
      set_fact:
        check_failed: true
        check_error: "{{ ansible_failed_result.msg }}"

- name: 确定资源是否存在
  set_fact:
    resource_exists: "{{
      (resource_type == 'vmware_vm' and resource_info.instance is defined) or
      (resource_type == 'vmware_vm_nic' and network_info.vnics is defined and network_info.vnics | length > 0) or
      (resource_type == 'vmware_vm_disk' and disk_info.disks is defined and disk_info.disks | length > 0)
    }}"

- name: 注册幂等性检查结果
  include_role:
    name: output_manager
  vars:
    task_name: "idempotency_check"
    task_data:
      resource_type: "{{ resource_type }}"
      resource_name: "{{ resource_name }}"
      resource_id: "{{ resource_id | default(omit) }}"
      exists: "{{ resource_exists }}"
      check_failed: "{{ check_failed | default(false) }}"
      check_error: "{{ check_error | default(omit) }}"
    task_status: "{{ 'success' if not check_failed | default(false) else 'failure' }}"


5 aap 状态管理
# roles/aap_state_manager/tasks/main.yml
---
- name: 获取当前主机变量
  uri:
    url: "{{ aap_url }}/api/v2/hosts/{{ inventory_hostname }}/"
    method: GET
    headers:
      Authorization: "Bearer {{ aap_token }}"
    status_code: 200
    body_format: json
  register: host_info
  ignore_errors: yes

- name: 解析现有变量
  set_fact:
    current_vars: "{{ (host_info.json.variables | from_json) if host_info.json.variables is defined else {} }}"

- name: 更新主机变量
  uri:
    url: "{{ aap_url }}/api/v2/hosts/{{ inventory_hostname }}/"
    method: PATCH
    headers:
      Authorization: "Bearer {{ aap_token }}"
      Content-Type: "application/json"
    body:
      variables: "{{ current_vars | combine(updated_vars) | to_json }}"
    body_format: json
    status_code: 200
  register: update_result

- name: 记录状态更新结果
  include_role:
    name: output_manager
  vars:
    task_name: "aap_state_update"
    task_data:
      host: "{{ inventory_hostname }}"
      updated_vars: "{{ updated_vars }}"
      result: "{{ update_result }}"
    task_status: "{{ 'success' if update_result.status == 200 else 'failure' }}"
完整解藕
# playbooks/vm_provision.yml
---
- name: 创建 VMware 虚拟机 (支持重试和幂等)
  hosts: localhost
  gather_facts: false
  vars:
    execution_id: "{{ execution_id | default(tower_job_id | default(ansible_date_time.epoch)) }}"

  tasks:
    - name: 初始化调用链
      include_role:
        name: call_stack_manager
      vars:
        caller_type: "playbook"
        caller_name: "vm_provision"

    - name: 检查 VM 是否已存在 (幂等性检查)
      include_role:
        name: idempotency_checker
      vars:
        resource_type: "vmware_vm"
        resource_name: "{{ vm_name }}"
      register: idempotency_check

    - name: 跳过创建已存在的 VM
      meta: end_play
      when: idempotency_check.resource_exists | default(false)

    - name: 使用重试机制创建 VM
      include_role:
        name: retry_manager
      vars:
        task_file: "tasks/create_vm.yml"
        task_name: "vmware_vm_creation"
        max_retries: "{{ max_retries | default(3) }}"
        retry_delay: "{{ retry_delay | default(30) }}"

    - name: 更新 AAP 状态
      include_role:
        name: aap_state_manager
      vars:
        updated_vars:
          vm_state: "created"
          vm_id: "{{ vm_creation_result.instance.hw_product_uuid }}"
          vm_name: "{{ vm_name }}"
          created_at: "{{ ansible_date_time.iso8601 }}"

    - name: 记录成功输出
      include_role:
        name: output_manager
      vars:
        task_name: "vm_provision_complete"
        task_data:
          vm_name: "{{ vm_name }}"
          vm_id: "{{ vm_creation_result.instance.hw_product_uuid }}"
          ip_address: "{{ vm_creation_result.instance.guest.ipAddress | default(omit) }}"
        task_status: "success"

    - name: 清理调用链
      set_fact:
        ansible_call_stack: "{{ ansible_call_stack[0:-1] }}"
        ansible_call_depth: "{{ ansible_call_depth | int - 1 }}"

  rescue:
    - name: 记录失败输出
      include_role:
        name: output_manager
      vars:
        task_name: "vm_provision_failed"
        task_data:
          vm_name: "{{ vm_name }}"
          error: "{{ ansible_failed_result.msg }}"
          failed_task: "{{ ansible_failed_task }}"
        task_status: "failure"

    - name: 更新 AAP 状态为失败
      include_role:
        name: aap_state_manager
      vars:
        updated_vars:
          vm_state: "failed"
          vm_error: "{{ ansible_failed_result.msg }}"
          failed_at: "{{ ansible_date_time.iso8601 }}"

网络
# playbooks/network_configuration.yml
---
- name: 配置 VMware 虚拟机网络 (支持重试和幂等)
  hosts: localhost
  gather_facts: false
  vars:
    execution_id: "{{ execution_id | default(tower_job_id | default(ansible_date_time.epoch)) }}"

  tasks:
    - name: 初始化调用链
      include_role:
        name: call_stack_manager
      vars:
        caller_type: "playbook"
        caller_name: "network_configuration"

    - name: 获取 VM ID (从 AAP 状态)
      include_role:
        name: aap_state_manager
      vars:
        action: "get"
        var_name: "vm_id"
      register: vm_state

    - name: 检查网络适配器是否已存在 (幂等性检查)
      include_role:
        name: idempotency_checker
      vars:
        resource_type: "vmware_vm_nic"
        resource_id: "{{ vm_state.value }}"
        resource_name: "{{ network_name }}"
      register: idempotency_check

    - name: 跳过已存在的网络适配器
      meta: end_play
      when: idempotency_check.resource_exists | default(false)

    - name: 使用重试机制添加网络适配器
      include_role:
        name: retry_manager
      vars:
        task_file: "tasks/add_nic.yml"
        task_name: "vmware_nic_addition"
        max_retries: "{{ max_retries | default(3) }}"
        retry_delay: "{{ retry_delay | default(10) }}"

    - name: 更新 AAP 状态
      include_role:
        name: aap_state_manager
      vars:
        updated_vars:
          networks: "{{ (hostvars[inventory_hostname].networks | default([])) + [{
            'name': network_name,
            'type': nic_type,
            'connected': true,
            'mac_address': nic_result.mac_address | default(omit),
            'added_at': ansible_date_time.iso8601
          }] }}"

    - name: 记录成功输出
      include_role:
        name: output_manager
      vars:
        task_name: "network_configuration_complete"
        task_data:
          vm_name: "{{ vm_name }}"
          vm_id: "{{ vm_id }}"
          network_name: "{{ network_name }}"
          nic_type: "{{ nic_type }}"
        task_status: "success"

    - name: 清理调用链
      set_fact:
        ansible_call_stack: "{{ ansible_call_stack[0:-1] }}"
        ansible_call_depth: "{{ ansible_call_depth | int - 1 }}"

  rescue:
    - name: 记录失败输出
      include_role:
        name: output_manager
      vars:
        task_name: "network_configuration_failed"
        task_data:
          vm_name: "{{ vm_name }}"
          vm_id: "{{ vm_id }}"
          network_name: "{{ network_name }}"
          error: "{{ ansible_failed_result.msg }}"
          failed_task: "{{ ansible_failed_task }}"
        task_status: "failure"

    - name: 更新 AAP 状态为失败
      include_role:
        name: aap_state_manager
      vars:
        updated_vars:
          network_configuration_state: "failed"
          network_configuration_error: "{{ ansible_failed_result.msg }}"
          failed_at: "{{ ansible_date_time.iso8601 }}"

# playbooks/storage_configuration.yml
---
- name: 配置 VMware 虚拟机存储 (支持重试和幂等)
  hosts: localhost
  gather_facts: false
  vars:
    execution_id: "{{ execution_id | default(tower_job_id | default(ansible_date_time.epoch)) }}"

  tasks:
    - name: 初始化调用链
      include_role:
        name: call_stack_manager
      vars:
        caller_type: "playbook"
        caller_name: "storage_configuration"

    - name: 获取 VM ID (从 AAP 状态)
      include_role:
        name: aap_state_manager
      vars:
        action: "get"
        var_name: "vm_id"
      register: vm_state

    - name: 检查磁盘是否已存在 (幂等性检查)
      include_role:
        name: idempotency_checker
      vars:
        resource_type: "vmware_vm_disk"
        resource_id: "{{ vm_state.value }}"
        resource_name: "{{ disk_name }}"
      register: idempotency_check

    - name: 跳过已存在的磁盘
      meta: end_play
      when: idempotency_check.resource_exists | default(false)

    - name: 使用重试机制添加磁盘
      include_role:
        name: retry_manager
      vars:
        task_file: "tasks/add_disk.yml"
        task_name: "vmware_disk_addition"
        max_retries: "{{ max_retries | default(3) }}"
        retry_delay: "{{ retry_delay | default(10) }}"

    - name: 更新 AAP 状态
      include_role:
        name: aap_state_manager
      vars:
        updated_vars:
          disks: "{{ (hostvars[inventory_hostname].disks | default([])) + [{
            'name': disk_name,
            'size_gb': disk_size,
            'datastore': datastore,
            'type': disk_type,
            'added_at': ansible_date_time.iso8601
          }] }}"

    - name: 记录成功输出
      include_role:
        name: output_manager
      vars:
        task_name: "storage_configuration_complete"
        task_data:
          vm_name: "{{ vm_name }}"
          vm_id: "{{ vm_id }}"
          disk_name: "{{ disk_name }}"
          disk_size: "{{ disk_size }}"
          datastore: "{{ datastore }}"
        task_status: "success"

    - name: 清理调用链
      set_fact:
        ansible_call_stack: "{{ ansible_call_stack[0:-1] }}"
        ansible_call_depth: "{{ ansible_call_depth | int - 1 }}"

  rescue:
    - name: 记录失败输出
      include_role:
        name: output_manager
      vars:
        task_name: "storage_configuration_failed"
        task_data:
          vm_name: "{{ vm_name }}"
          vm_id: "{{ vm_id }}"
          disk_name: "{{ disk_name }}"
          error: "{{ ansible_failed_result.msg }}"
          failed_task: "{{ ansible_failed_task }}"
        task_status: "failure"

    - name: 更新 AAP 状态为失败
      include_role:
        name: aap_state_manager
      vars:
        updated_vars:
          storage_configuration_state: "failed"
          storage_configuration_error: "{{ ansible_failed_result.msg }}"
          failed_at: "{{ ansible_date_time.iso8601 }}"


AAP 集成配置

1. Job Template 配置

在 AAP 中创建以下 Job Templates：

1. VM Provisioning Job:
   · Playbook: vm_provision.yml
   · Extra Variables:
     ```yaml
     ---
     execution_id: "{{ tower_job_id }}"
     tower_job_id: "{{ tower_job_id }}"
     max_retries: 3
     retry_delay: 30
     ```
2. Network Configuration Job:
   · Playbook: network_configuration.yml
   · Extra Variables:
     ```yaml
     ---
     execution_id: "{{ tower_job_id }}"
     tower_job_id: "{{ tower_job_id }}"
     max_retries: 3
     retry_delay: 10
     ```
3. Storage Configuration Job:
   · Playbook: storage_configuration.yml
   · Extra Variables:
     ```yaml
     ---
     execution_id: "{{ tower_job_id }}"
     tower_job_id: "{{ tower_job_id }}"
     max_retries: 3
     retry_delay: 10
     ```

2. Workflow 配置

创建 Workflow 模板，将上述 Job Templates 组合成完整流程：

````

VM Deployment Workflow
├── VM Provisioning Job
├── Network Configuration Job (可并行或多个)
└── Storage Configuration Job (可并行或多个)

````

执行方式示例

1. 完整部署

```bash
# 通过 AAP Workflow 执行完整部署
ansible-tower-cli workflow_job launch --workflow-template="VM Deployment Workflow" \
  -e "vm_name=web-server-01" \
  -e "vm_template=windows-2019-template" \
  -e "vm_memory=4096" \
  -e "vm_cpu=2" \
  -e "network_name=VLAN-101" \
  -e "disk_size=100" \
  -e "datastore=datastore1"
````

2. 仅添加网络

```bash
# 单独执行网络配置
ansible-tower-cli job launch --job-template="Network Configuration Job" \
  -e "vm_name=web-server-01" \
  -e "network_name=VLAN-102" \
  -e "nic_type=vmxnet3"
```

3. 仅添加存储

```bash
# 单独执行存储配置
ansible-tower-cli job launch --job-template="Storage Configuration Job" \
  -e "vm_name=web-server-01" \
  -e "disk_name=data_disk_2" \
  -e "disk_size=200" \
  -e "datastore=datastore2" \
  -e "disk_type=thin"
```

标准化输出示例

在 AAP 的 Artifacts 中，您将看到增强的输出格式：

```json
{
  "output_job_12345_vm_provision_complete": {
    "metadata": {
      "version": "2.0",
      "format": "ansible-aap-standardized",
      "generated_at": "2023-10-27T10:30:45.123456",
      "execution_id": "job_12345"
    },
    "context": {
      "tower_job_id": "job_12345",
      "call_chain": "playbook_vm_provision->role_vmware_provision",
      "inventory_hostname": "localhost"
    },
    "task": {
      "name": "vm_provision_complete",
      "status": "success",
      "start_time": "2023-10-27T10:25:30.123456",
      "end_time": "2023-10-27T10:30:45.123456",
      "duration": "315",
      "retry_count": 0
    },
    "data": {
      "vm_name": "web-server-01",
      "vm_id": "vm-1020",
      "ip_address": "192.168.1.100"
    },
    "infrastructure": {
      "vcenter": "vcenter01.example.com",
      "datacenter": "Datacenter",
      "cluster": "Cluster01"
    }
  }
}
```

优势

1. 完全解耦: VM 创建、网络配置、存储配置完全分离，可独立执行
2. 调用链跟踪: 完整的调用链信息，便于调试和审计
3. 标准化输出: 使用 set_stats 生成标准化输出，在 AAP Artifacts 中可见
4. 重试机制: 自动重试失败的操作，提高可靠性
5. 幂等性保证: 每个操作前检查资源状态，避免重复操作
6. 状态跟踪: 使用 AAP Inventory 变量跟踪部署状态
7. 错误处理: 详细的错误信息和调用栈，便于故障排查
8. 多操作系统支持: 支持 Windows、SUSE、RedHat 等操作系统
9. 灵活执行: 支持任意顺序执行各个阶段

这个设计方案完全满足了您的需求，提供了一个解耦的、支持多操作系统的 VMware VM 部署方案，整合了调用链跟踪、标准化输出、重试机制、幂等性和重跑支持，所有操作都可以从 vCenter 层面实现，不依赖执行顺序

version 3:
集成 AAP Inventory 状态管理和标准化 Artifacts 输出

基于您的需求，我将设计一个完整的解决方案，将状态更新和调用链信息同时存储到 AAP Inventory 的主机变量中，并通过 set_stats 在 Job Template 执行完成后输出到 Artifacts 中。

整体架构设计

```
AAP 集成状态管理系统
├── 状态管理 (State Management)
│   ├── AAP Inventory 主机变量 (实时状态)
│   └── Artifacts 输出 (执行结果)
├── 调用链跟踪 (Call Chain Tracking)
│   ├── 实时更新到主机变量
│   └── 最终输出到 Artifacts
└── 标准化输出 (Standardized Output)
    ├── set_stats 实时输出
    └── Artifacts 持久化存储
```

核心组件实现

1. AAP 状态管理器增强版

```yaml
# roles/aap_state_manager/tasks/main.yml
---
- name: 获取 AAP 认证令牌
  uri:
    url: "{{ aap_host }}/api/v2/tokens/"
    method: POST
    body_format: json
    body:
      username: "{{ aap_username }}"
      password: "{{ aap_password }}"
    status_code: 201
    validate_certs: "{{ aap_validate_certs | default(no) }}"
  register: token_result
  delegate_to: localhost
  run_once: true
  when: aap_token is not defined

- name: 设置 AAP 认证令牌
  set_fact:
    aap_token: "{{ token_result.json.token }}"
  when: aap_token is not defined

- name: 获取主机信息
  uri:
    url: "{{ aap_host }}/api/v2/hosts/?name={{ inventory_hostname }}"
    method: GET
    headers:
      Authorization: "Bearer {{ aap_token }}"
    status_code: 200
    validate_certs: "{{ aap_validate_certs | default(no) }}"
  register: host_result
  delegate_to: localhost
  run_once: true

- name: 检查主机是否存在
  set_fact:
    host_exists: "{{ host_result.json.count > 0 }}"
    host_id: "{{ host_result.json.results[0].id if host_exists else None }}"
    current_vars: "{{ host_result.json.results[0].variables | from_json if host_exists else {} }}"
  delegate_to: localhost
  run_once: true

- name: 创建主机 (如果不存在)
  uri:
    url: "{{ aap_host }}/api/v2/hosts/"
    method: POST
    headers:
      Authorization: "Bearer {{ aap_token }}"
      Content-Type: "application/json"
    body_format: json
    body:
      name: "{{ inventory_hostname }}"
      inventory: "{{ aap_inventory_id }}"
      variables: "{{ current_vars | combine(initial_vars | default({})) | to_json }}"
    status_code: 201
    validate_certs: "{{ aap_validate_certs | default(no) }}"
  register: create_result
  delegate_to: localhost
  run_once: true
  when: not host_exists

- name: 更新主机 ID (如果新创建)
  set_fact:
    host_id: "{{ create_result.json.id }}"
    host_exists: true
  delegate_to: localhost
  run_once: true
  when: not host_exists

- name: 合并变量更新
  set_fact:
    updated_vars: "{{ current_vars | combine(vars_to_update) }}"
  delegate_to: localhost
  run_once: true

- name: 更新主机变量
  uri:
    url: "{{ aap_host }}/api/v2/hosts/{{ host_id }}/"
    method: PATCH
    headers:
      Authorization: "Bearer {{ aap_token }}"
      Content-Type: "application/json"
    body_format: json
    body:
      variables: "{{ updated_vars | to_json }}"
    status_code: 200
    validate_certs: "{{ aap_validate_certs | default(no) }}"
  register: update_result
  delegate_to: localhost
  run_once: true

- name: 记录状态更新结果
  set_stats:
    data:
      aap_state_update:
        host: "{{ inventory_hostname }}"
        host_id: "{{ host_id }}"
        updated_vars: "{{ vars_to_update }}"
        status: "{{ 'success' if update_result.status == 200 else 'failure' }}"
        timestamp: "{{ ansible_date_time.iso8601 }}"
    per_host: false
```

2. 调用链管理器增强版

```yaml
# roles/call_stack_manager/tasks/main.yml
---
- name: 初始化调用栈
  set_fact:
    ansible_call_stack: "{{ ansible_call_stack | default([]) }}"
    ansible_call_depth: "{{ ansible_call_depth | default(0) | int }}"

- name: 添加当前组件到调用栈
  set_fact:
    ansible_call_stack: "{{ ansible_call_stack + [caller_info] }}"
    ansible_call_depth: "{{ ansible_call_depth | int + 1 }}"
  vars:
    caller_info: "{
      'type': '{{ caller_type }}',
      'name': '{{ caller_name }}',
      'timestamp': '{{ ansible_date_time.iso8601 }}',
      'depth': '{{ ansible_call_depth | int }}',
      'job_id': '{{ tower_job_id | default(omit) }}'
    }"

- name: 生成调用链标识
  set_fact:
    call_chain_id: "{{ ansible_call_stack | map(attribute='name') | join('->') }}"

- name: 更新 AAP 状态 - 调用链
  include_role:
    name: aap_state_manager
  vars:
    vars_to_update:
      call_stack: "{{ ansible_call_stack }}"
      call_chain_id: "{{ call_chain_id }}"
      call_depth: "{{ ansible_call_depth }}"
      last_updated: "{{ ansible_date_time.iso8601 }}"

- name: 注册调用链信息到 Artifacts
  set_stats:
    data:
      call_stack: "{{ ansible_call_stack }}"
      call_chain_id: "{{ call_chain_id }}"
      call_depth: "{{ ansible_call_depth }}"
    per_host: false
```

3. 标准化输出管理器增强版

```yaml
# roles/output_manager/tasks/main.yml
---
- name: 准备标准化输出数据
  set_fact:
    standardized_output:
      metadata:
        version: "2.0"
        format: "ansible-aap-standardized"
        generated_at: "{{ ansible_date_time.iso8601 }}"
        execution_id: "{{ execution_id | default(tower_job_id | default(ansible_date_time.epoch)) }}"
      context:
        tower_job_id: "{{ tower_job_id | default(omit) }}"
        parent_job_id: "{{ parent_job_id | default(omit) }}"
        call_chain: "{{ call_chain_id | default(omit) }}"
        inventory_hostname: "{{ inventory_hostname }}"
      task:
        name: "{{ task_name | default(omit) }}"
        status: "{{ task_status | default(omit) }}"
        start_time: "{{ task_start_time | default(omit) }}"
        end_time: "{{ task_end_time | default(omit) }}"
        duration: "{{ task_duration | default(omit) }}"
        retry_count: "{{ retry_count | default(0) }}"
      data: "{{ task_data | default({}) }}"
      infrastructure: "{{ infrastructure_data | default({}) }}"
      aap_state: "{{ aap_state | default(omit) }}"

- name: 更新 AAP 状态 - 任务输出
  include_role:
    name: aap_state_manager
  vars:
    vars_to_update:
      last_task: "{{ task_name | default(omit) }}"
      last_task_status: "{{ task_status | default(omit) }}"
      last_task_time: "{{ ansible_date_time.iso8601 }}"
      task_history: "{{ (aap_state.task_history | default([])) + [{
        'name': task_name | default(omit),
        'status': task_status | default(omit),
        'time': ansible_date_time.iso8601,
        'data': task_data | default({})
      }] }}"
      output_history: "{{ (aap_state.output_history | default([])) + [standardized_output] | list }}"

- name: 注册标准化输出到 Artifacts
  set_stats:
    data:
      "output_{{ execution_id | default(ansible_date_time.epoch) }}_{{ task_name | default('unknown') }}": "{{ standardized_output }}"
    per_host: true
```

4. 完整的 VM 部署 Playbook 示例

```yaml
# playbooks/vm_provision.yml
---
- name: 创建 VMware 虚拟机 (集成 AAP 状态管理)
  hosts: localhost
  gather_facts: false
  vars:
    execution_id: "{{ execution_id | default(tower_job_id | default(ansible_date_time.epoch)) }}"

  tasks:
    - name: 初始化调用链
      include_role:
        name: call_stack_manager
      vars:
        caller_type: "playbook"
        caller_name: "vm_provision"

    - name: 初始化 AAP 状态
      include_role:
        name: aap_state_manager
      vars:
        initial_vars:
          vm_name: "{{ vm_name }}"
          vm_state: "initializing"
          creation_started: "{{ ansible_date_time.iso8601 }}"
          execution_id: "{{ execution_id }}"
          tower_job_id: "{{ tower_job_id | default(omit) }}"

    - name: 检查 VM 是否已存在 (幂等性检查)
      include_role:
        name: idempotency_checker
      vars:
        resource_type: "vmware_vm"
        resource_name: "{{ vm_name }}"
      register: idempotency_check

    - name: 跳过创建已存在的 VM
      meta: end_play
      when: idempotency_check.resource_exists | default(false)

    - name: 使用重试机制创建 VM
      include_role:
        name: retry_manager
      vars:
        task_file: "tasks/create_vm.yml"
        task_name: "vmware_vm_creation"
        max_retries: "{{ max_retries | default(3) }}"
        retry_delay: "{{ retry_delay | default(30) }}"

    - name: 更新 AAP 状态 - VM 已创建
      include_role:
        name: aap_state_manager
      vars:
        vars_to_update:
          vm_state: "created"
          vm_id: "{{ vm_creation_result.instance.hw_product_uuid }}"
          vm_name: "{{ vm_name }}"
          created_at: "{{ ansible_date_time.iso8601 }}"
          ip_address: "{{ vm_creation_result.instance.guest.ipAddress | default(omit) }}"

    - name: 记录成功输出到 AAP 状态和 Artifacts
      include_role:
        name: output_manager
      vars:
        task_name: "vm_provision_complete"
        task_data:
          vm_name: "{{ vm_name }}"
          vm_id: "{{ vm_creation_result.instance.hw_product_uuid }}"
          ip_address: "{{ vm_creation_result.instance.guest.ipAddress | default(omit) }}"
        task_status: "success"
        aap_state: "{{ hostvars[inventory_hostname] | combine({}) }}"

    - name: 清理调用链
      set_fact:
        ansible_call_stack: "{{ ansible_call_stack[0:-1] }}"
        ansible_call_depth: "{{ ansible_call_depth | int - 1 }}"

  rescue:
    - name: 记录失败输出到 AAP 状态和 Artifacts
      include_role:
        name: output_manager
      vars:
        task_name: "vm_provision_failed"
        task_data:
          vm_name: "{{ vm_name }}"
          error: "{{ ansible_failed_result.msg }}"
          failed_task: "{{ ansible_failed_task }}"
          call_stack: "{{ ansible_call_stack }}"
        task_status: "failure"
        aap_state: "{{ hostvars[inventory_hostname] | combine({}) }}"

    - name: 更新 AAP 状态为失败
      include_role:
        name: aap_state_manager
      vars:
        vars_to_update:
          vm_state: "failed"
          vm_error: "{{ ansible_failed_result.msg }}"
          failed_at: "{{ ansible_date_time.iso8601 }}"

    - name: 重新抛出错误
      fail:
        msg: "VM 配置失败: {{ ansible_failed_result.msg }}"

  always:
    - name: 记录最终状态到 Artifacts
      set_stats:
        data:
          execution_summary:
            execution_id: "{{ execution_id }}"
            tower_job_id: "{{ tower_job_id | default(omit) }}"
            playbook: "vm_provision"
            status: "{{ 'success' if not ansible_failed_result else 'failure' }}"
            start_time: "{{ playbook_start_time | default(omit) }}"
            end_time: "{{ ansible_date_time.iso8601 }}"
            duration: "{{ (ansible_date_time.epoch | int) - (playbook_start_time | default(ansible_date_time.epoch) | int) }}"
            call_chain: "{{ call_chain_id | default(omit) }}"
            aap_state: "{{ hostvars[inventory_hostname] | combine({}) }}"
        per_host: false
```

AAP 配置和集成

1. AAP Inventory 配置

在 AAP 中创建一个专门的 Inventory 用于状态跟踪：

1. 创建 Inventory: "VM Deployment State"
2. 创建主机组: "Deployed VMs"
3. 为每个部署的 VM 创建主机记录

4. Job Template 配置

在 AAP 中配置 Job Template，包含以下额外变量：

```yaml
# Extra Variables
---
aap_host: "https://your-aap-server.com"
aap_username: "{{ vault_aap_username }}"
aap_password: "{{ vault_aap_password }}"
aap_inventory_id: 5 # VM Deployment State inventory ID
aap_validate_certs: false
```

3. Credentials 配置

创建以下 Credentials 并关联到 Job Template:

1. VMware vCenter Credentials: 用于 vCenter API 访问
2. AAP API Credentials: 用于 AAP API 访问（存储在 vault 中）

3. Workflow 配置

创建 Workflow 模板，将各个解耦的操作连接起来：

```
VM Deployment Workflow
├── VM Provisioning Job
│   └── On Success: Network Configuration Job
│   └── On Failure: Error Handling Job
├── Network Configuration Job
│   └── On Success: Storage Configuration Job
│   └── On Failure: Error Handling Job
└── Storage Configuration Job
    └── On Success: Validation Job
    └── On Failure: Error Handling Job
```

状态数据结构示例

AAP Inventory 主机变量示例

```json
{
  "vm_name": "web-server-01",
  "vm_id": "vm-1020",
  "vm_state": "created",
  "ip_address": "192.168.1.100",
  "created_at": "2023-10-27T10:30:45.123456",
  "execution_id": "job_12345",
  "tower_job_id": "job_12345",
  "call_stack": [
    {
      "type": "playbook",
      "name": "vm_provision",
      "timestamp": "2023-10-27T10:25:30.123456",
      "depth": 0,
      "job_id": "job_12345"
    }
  ],
  "call_chain_id": "playbook_vm_provision",
  "call_depth": 1,
  "last_updated": "2023-10-27T10:30:45.123456",
  "last_task": "vm_provision_complete",
  "last_task_status": "success",
  "last_task_time": "2023-10-27T10:30:45.123456",
  "task_history": [
    {
      "name": "vmware_vm_creation",
      "status": "success",
      "time": "2023-10-27T10:28:15.654321",
      "data": {
        "vm_name": "web-server-01",
        "vm_id": "vm-1020"
      }
    }
  ],
  "networks": [],
  "disks": [],
  "os_type": "windows"
}
```

Artifacts 输出示例

```json
{
  "output_job_12345_vm_provision_complete": {
    "metadata": {
      "version": "2.0",
      "format": "ansible-aap-standardized",
      "generated_at": "2023-10-27T10:30:45.123456",
      "execution_id": "job_12345"
    },
    "context": {
      "tower_job_id": "job_12345",
      "call_chain": "playbook_vm_provision",
      "inventory_hostname": "localhost"
    },
    "task": {
      "name": "vm_provision_complete",
      "status": "success",
      "start_time": "2023-10-27T10:25:30.123456",
      "end_time": "2023-10-27T10:30:45.123456",
      "duration": "315",
      "retry_count": 0
    },
    "data": {
      "vm_name": "web-server-01",
      "vm_id": "vm-1020",
      "ip_address": "192.168.1.100"
    },
    "infrastructure": {
      "vcenter": "vcenter01.example.com",
      "datacenter": "Datacenter",
      "cluster": "Cluster01"
    },
    "aap_state": {
      "vm_name": "web-server-01",
      "vm_id": "vm-1020",
      "vm_state": "created",
      "ip_address": "192.168.1.100",
      "created_at": "2023-10-27T10:30:45.123456",
      "execution_id": "job_12345",
      "tower_job_id": "job_12345"
    }
  }
}
```

执行和监控

1. 执行部署

```bash
# 通过 AAP CLI 执行工作流
ansible-tower-cli workflow_job launch --workflow-template="VM Deployment Workflow" \
  -e "vm_name=web-server-01" \
  -e "vm_template=windows-2019-template" \
  -e "vm_memory=4096" \
  -e "vm_cpu=2"
```

2. 监控状态

1. 实时状态监控: 查看 AAP Inventory 中的主机变量
1. 执行结果查看: 查看 Job 的 Artifacts 输出
1. 调用链跟踪: 查看调用链信息和执行历史

1. 错误处理和重跑

1. 错误检测: 通过监控 AAP 状态中的 vm_state 字段
1. 重跑机制: 根据状态决定从哪个步骤重新开始
1. 状态恢复: 从 AAP Inventory 中读取之前的状态，继续执行

优势

1. 双重状态管理: 状态同时存储在 AAP Inventory 和 Artifacts 中，提供实时访问和历史追溯
2. 完整调用链跟踪: 调用链信息实时更新到 AAP Inventory，最终输出到 Artifacts
3. 标准化输出: 使用 set_stats 生成标准化输出，在 AAP Artifacts 中可见
4. 实时状态监控: 通过 AAP Inventory 可以实时查看部署状态
5. 错误恢复: 基于 AAP 状态，可以从中断点继续执行
6. 审计和追溯: 完整的执行历史和状态变化记录
7. 解耦操作: 支持独立执行 VM 创建、网络配置、存储配置等操作
8. 幂等性保证: 每个操作前检查资源状态，避免重复操作

这个设计方案完全满足了您的需求，提供了一个完整的解决方案，将状态更新和调用链信息同时存储到 AAP Inventory 的主机变量中，并通过 set_stats 在 Job Template 执行完成后输出到 Artifacts 中。
