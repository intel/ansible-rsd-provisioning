# Copyright (c) 2019 Intel Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
#   - Marco Chiappero <marco.chiappero@intel.com>
#######################################################

class ModuleDocFragment(object):

    DOCUMENTATION = '''
options:
    podm:
        description:
        - A dictionary containing information for connecting to a remote PODM.
        - A the very least a host has to be provided, but other parameters may
          be optional and/or specified through environment variables.
        required: false
        suboptions:
            host:
                description:
                    - A hostname or IP adress for connecting to PODM.
                    - Alternatively, if not specified, the environment variable
                      C(PODM_HOST) can be used.
                required: true
            port:
                description:
                    - Port for the PODM API service.
                    - The environment variable C(PODM_PORT) can be defined
                      instead.
                default: 8443
                type: int
            protocol:
                description:
                    - Specifies the protocol to be used to connect to PODM
                default: https
                choices:
                    - http
                    - https
            validate_certs:
                description:
                    - Whether or not SSL API requests should be verified.
                default: false
                type: bool
            
    auth:
        description:
            - A dictionary containing PODM access credentials
        suboptions:
            username:
                description:
                    - The username required to interact with PODM API
                    - Especially for security reasons, the environment variable
                      C(PODM_USERNAME) can be provided instead.
                required: true
                aliases:
                    - user
            password:
                description:
                    - The password required to interact with PODM API
                    - Especially for security reasons, the environment variable
                      C(PODM_PASSWORD) can be provided instead.
                required: true
                aliases:
                    - pass

requirements:
  - rsd-lib > 0.2.2
  - RSD PODM API >= 2.1

seealso:
    - name: Rack Scale Design documentation
      description: Reference RSD documentation, including the latest PODM API
                   specification containing detailed information on the
                   supported values and options for composition.
      link: https://www.intel.com/content/www/us/en/architecture-and-technology/rack-scale-design/rack-scale-design-resources.html
'''
