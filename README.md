DISCONTINUATION OF PROJECT

This project will no longer be maintained by Intel.

Intel has ceased development and contributions including, but not limited to, maintenance, bug fixes, new releases, or updates, to this project.  

Intel no longer accepts patches to this project.

If you have an ongoing need to use this project, are interested in independently developing it, or would like to maintain patches for the open source software community, please create your own fork of this project.  

Contact: webadmin@linux.intel.com
This feature is no longer supported by Intel

ansible-rsd-provisioning
=========

This repository hosts “Intel® Rack Scale Design (RSD) Provisioning for Ansible*” . The code herein available allows a data center administrator or higher-level 
orchestration tool to make use of Ansible* for provisioning Intel® RSD clusters managed by an Intel® RSD compliant POD Manager.

This role provisions a user-defined amount of nodes and saves their actual hardware details resulting from the composition to a file for subsequent reuse. An additional inventory file is also created grouping the IP address of each composed node under a user-defined group name. Multiple runs of the the role will keep appending to this inventory file.

Composition and booting of composed nodes is possible thanks two modules, `rsd_compose` and `rsd_power`, bundled with the role, which support respectively:

- Allocation, assembly and deletion of composed nodes; the specifications and values here allow to enumerate hardware selection, ranging from RAM and CPU, to NVME or FPGA devices over Fabric (see the [Intel® PODM API specification](https://www.intel.com/content/www/us/en/architecture-and-technology/rack-scale-design/podm-api-spec-v2-4.html) for a detailed list).
- Changing the power state of composed nodes, from power on to reboot.

Once the role is installed and executed at least once, the above two modules can be used in any subsequent task or role, granting access to the full range of their functionality.

Composition requirements of the nodes for this role are controlled through a number of predefined variables detailed below. Interaction with PODM requires endpoint and authentication values, also detailed below.

Please note that this role isn't idempotent.

This role supports Intel® RSD 2.3.x and 2.4.0 versions.


“*Other names and brands may be claimed as the property of others”.

Requirements
------------

- `rsd-lib >= 1.0.0`
- an Intel® RSD compliant POD Manager
- Intel® RSD compliant composable hardware

At least [rsd-lib](https://github.com/openstack/rsd-lib) version of 1.0.0 is required:
```
$ sudo pip install git+https://github.com/openstack/rsd-lib.git
```

Role Variables
--------------

Variables needed to run and control this role can be divided into three main categories:
- PODM related; There are two variable groups, one for connection related information and a second one for the credentials. They are read via environment variables, as follows:
    - `PODM_HOST`: specify PODM IP address.
    - `PODM_PORT`: specify port to connect to.
    - `PODM_USERNAME`: specify username for PODM authentication.
    - `PODM_PASSWORD`: specify password for PODM authentication.

An additional variable is available in the role at [defaults/main/podm.yml](defaults/main/podm.yml), `podm_validate_cert`, to control whether to perform the SSL certificate validation (default False).

- output related, to control file generation for the resulting output; default values can be found in [defaults/main/output.yml](defaults/main/output.yml).
    - `rsd_output_path`: base directory for storing output files, by default in the same location as the playbook.
    - `rsd_inventory_group`: group name used in the inventory file to group IPs of the composed (default "rsd_nodes").
    - `rsd_write_to_file`: control variable to enable output and inventory file creation (default: True); node details are still be available as a fact under `rsd_node_info`.


- nodes related, mostly to define composition requirements; default values can be found in [defaults/main/composition.yml](defaults/main/composition.yml). A similar file ([files/requirements_example.yml](files/requirements_example.yml)) containing the same variables with documentation and sample values, can be copied, edited and easily included in your playbook through the `include_vars` directive. Following is a table of the variables defined for node composition:


  | Variable | Default value | Description |
  |----------|:-------------:|-------------|
  |`number_of_nodes_to_provision`| 10 | Number of nodes to be created by the role |
  |`rsd_node_name`| node | Name assigned to the composed node |
  |`rsd_node_description`| "Composed Node" | A short text description associated to node |
  |`rsd_node_cores`| 0 | The composed node will have at lest the amount CPU cores here specified, potentially accross multiple CPUs. |
  |`rsd_node_memory`| 0 | Minimum amount of memory for the whole system, in MiB unit |
  |`rsd_node_memory_spec`| empty | List of Processors (CPUs or FPGAs) and their specification (e.g. Frequency) |
  |`rsd_node_local_drives`| empty | List of local drives to assigned to the node and their specifications, such as capacity, type and interface |
  |`rsd_node_remote_drives`| empty | List of remote drives to assigned to the node and their specifications, such as capacity, type and interface |
  |`rsd_node_eth_interfaces`| empty | List of interfaces and their desired specifications, such as their desired link speed |
  |`rsd_node_state`| assembled | Final state for the composed node. Alternative values are: 'absent', 'allocated' |

For more details on the available resource specification please refer to the [Intel® RSD PODM API specification](https://www.intel.com/content/www/us/en/architecture-and-technology/rack-scale-design/podm-api-spec-v2-4.html). 


Dependencies
------------

None


Example Playbook
----------------

to learn more about modules and how they could be used please see the documentation and examples included with the modules. See `library/rsd_compose.py` to learn more about `rsd_compose` module and `library/rsd_power.py` to learn more about `rsd_power` module. Before running playbook make sure to export PODM authentication variables.

Example export of PODM authentication variables:

    export PODM_HOST=127.0.0.1
    export PODM_PORT=8443
    export PODM_USERNAME=admin
    export PODM_PASSWORD=password

Example playbook using this role:

    - hosts: localhost
      connection: local
      roles:
        - intel.ansible_rsd_provisioning

Example playbook for the rsd_compose module specifying requirements inline:

    - hosts: localhost
      connection: local
      gather_facts: no
      tasks:
        - name: Assemble a node from the specified info/requirements
          rsd_compose:
            spec:
              name: Test node
              description: Node for testing assemble
              total_mem: 8000
              processors:
              - ProcessorType: CPU
                AchievableSpeedMHz: 3000
            state: assembled
            podm:
              validate_cert: True

Example playbook for the rsd_compose module using a spec file with requirements:

    - hosts: localhost
      connection: local
      gather_facts: no
      tasks:
        - name: Assemble a node from a PODM compliant JSON info/requirements file
          rsd_compose:
            specfile: files/simple_specfile.json
            power_on: false
            state: assembled

Example playbook for the rsd_power module:

    - hosts: localhost
      connection: local
      gather_facts: no
      tasks:
      - name: Trigger node reboot
        rsd_power:
          id:
            value: 1
            type: identity
          state: restarted
          force: false

Example playbook for rsd_boot module:

    - hosts: localhost
      connection: local
      gather_facts: no
      tasks:
      - name: Override Boot options to boot once from remote drive in legacy mode.
       rsd_boot:
         id:
           value: 1
         boot_target: remote_drive
         boot_enable: once
         boot_mode: legacy

More examples can be found in the [examples](examples) directory of the role.

License
-------

The role is provided under the Apache 2.0 license. The included modules and
related code (doc fragments and module utils) are released under GPLv3+.

Author Information
------------------

- Marco Chiappero - <marco.chiappero@intel.com>
- Radoslaw Kuschel - <radoslaw.kuschel@intel.com>
- Igor D.C. - <igor.duarte.cardoso@intel.com>
