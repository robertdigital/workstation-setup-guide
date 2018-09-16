import json
import os
import logging
from kubespawner.spawner import KubeSpawner

class KubeFormSpawner(KubeSpawner):

    def _options_form_default(self):
        global registry, repoName
        return '''
    <script defer src='https://use.fontawesome.com/releases/v5.3.1/js/solid.js' integrity='sha384-GJiigN/ef2B3HMj0haY+eMmG4EIIrhWgGJ2Rv0IaWnNdWdbWPr1sRLkGz7xfjOFw' crossorigin='anonymous'></script>
    <script defer src='https://use.fontawesome.com/releases/v5.3.1/js/brands.js' integrity='sha384-2vdvXGQdnt+ze3ylY5ESeZ9TOxwxlOsldUzQBwtjvRpen1FwDT767SqyVbYrltjb' crossorigin='anonymous'></script>
    <script defer src='https://use.fontawesome.com/releases/v5.3.1/js/fontawesome.js' integrity='sha384-2OfHGv4zQZxcNK+oL8TR9pA+ADXtUODqGpIRy1zOgioC4X3+2vbOAp5Qv7uHM4Z8' crossorigin='anonymous'></script>
    <div class='card' style='width: 100%;'>
    <div class='card-body'>
        <h3 class='card-title'>Welcome to Demo JupyterHub</h3>
        <h4 class='card-subtitle mb-2 text-muted'>Easy Jupyter-based GPU Compute</h4>
        <p class='card-text'>
        <ul>
            <li>Hello world!</li>
        </ul>
        </p>
        <a target='_blank' class='btn btn-primary' href='#'>Random Button</a> 
    </div>
    </div>
    <br>
    <div class='form-group'>
    <label for='inputDockerImage'><i class='fab fa-docker'></i> Docker Image</label>
    <input type='text' class='form-control' id='inputDockerImage' aria-describedby='imgHelp' placeholder='tlkh/deeplearning-lab:0.2' value='tlkh/deeplearning-lab:0.2'>
    <p><small id='imgHelp' class='form-text text-muted'>You can use any JupyterHub compatible Docker image from Docker Hub.<br>
    The default image is <code>tlkh/deeplearning-lab:0.2</code>, which includes most typical packages required for deep learning: TensorFlow, Keras, PyTorch and OpenCV.</small></p>
    </div>
    <div class='form-group'>
    <label for='cpu_guarantee'><i class='fas fa-microchip'></i> vCPU Threads</label>
    <input type='text' class='form-control' id='cpu_guarantee' aria-describedby='cpuHelp' placeholder='1.0'>
    <p><small id='cpuHelp' class='form-text text-muted'>If your work is not CPU-intensive, you can choose less than 1 CPU (e.g. <code>0.5</code>)</small></p>
    </div>
    <div class='form-group'>
    <label for='mem_guarantee'><i class='fas fa-memory'></i> Reserved Memory</label>
    <input type='text' class='form-control' id='mem_guarantee' aria-describedby='memHelp' placeholder='1.0Gi'>
    <p><small id='memHelp' class='form-text text-muted'>Total amount of reserved RAM (e.g. <code>7.5Gi</code>). Your Notebook may consume more if system resources allow.</small></p>
    </div>
    <div class='form-group'>
    <label for='extra_resource_limits'><i class='fas fa-ticket-alt'></i> GPU</label>
    <input class='form-control' list=\"extra_resource_limits\" name=\"extra_resource_limits\" placeholder=''>
    <datalist id=\"extra_resource_limits\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 0}}\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 1}}\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 2}}\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 3}}\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 4}}\">
    </datalist>
    <p><small id='memHelp'>Example: to reserve 2 GPUs: <code>{{&quot;nvidia.com/gpu&quot;: 2}}</code><br>
    To reserve no GPU, please use <code>{{&quot;nvidia.com/gpu&quot;: 0}}</code>.</small></p>
    </div>
    <br>
    <div class='alert alert-warning' role='alert'>
    <p>If your Notebook is unable to start, it is likely that the GPU you requested for is not available.<br>
    Try starting a Notebook <b>without a GPU</b> before reporting a server problem!</p>
    <div>
    <br>
    '''.format(registry, repoName)

    def options_from_form(self, formdata):
        options = {}
        options['image'] = formdata.get('inputDockerImage', [''])[0].strip()
        options['cpu_guarantee'] = formdata.get(
            'cpu_guarantee', [''])[0].strip()
        options['mem_guarantee'] = formdata.get(
            'mem_guarantee', [''])[0].strip()
        options['extra_resource_limits'] = formdata.get(
            'extra_resource_limits', [''])[0].strip()
        logging.info(options)
        return options

    @property
    def singleuser_image_spec(self):
        if self.user_options.get('image'):
            image = self.user_options['image']
        else:
            image = 'tlkh/deeplearning-lab:0.2'
        return image

    @property
    def cpu_guarantee(self):
        cpu = '1.0'
        if self.user_options.get('cpu_guarantee'):
            cpu = self.user_options['cpu_guarantee']
        return cpu

    @property
    def mem_guarantee(self):
        mem = '1Gi'
        if self.user_options.get('mem_guarantee'):
            mem = self.user_options['mem_guarantee']
        return mem

    @property
    def extra_resource_limits(self):
        extra = ''
        if self.user_options.get('extra_resource_limits'):
            extra = json.loads(self.user_options['extra_resource_limits'])
        return extra



###################################################
# JupyterHub Options
###################################################
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'
# Don't try to cleanup servers on exit - since in general for k8s, we want
# the hub to be able to restart without losing user containers
c.JupyterHub.cleanup_servers = False
###################################################

c.JupyterHub.services = [
    {
        'name': 'wget-cull-idle',
        'admin': True,
        'command': ['wget', 'https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/examples/cull-idle/cull_idle_servers.py', '-N']
    },

    {
        'name': 'cull-idle',
        'admin': True,
        'command': ['python', 'cull_idle_servers.py', '--timeout=3600']
    }
]

###################################################
# Spawner Options
###################################################
cloud = os.environ.get('CLOUD_NAME')
registry = os.environ.get('REGISTRY')
repoName = os.environ.get('REPO_NAME')
c.JupyterHub.spawner_class = KubeFormSpawner
c.KubeSpawner.singleuser_image_spec = '{0}/{1}/tensorflow-notebook'.format(
    registry, repoName)

c.KubeSpawner.cmd = 'start-singleuser.sh'
c.KubeSpawner.args = ['--allow-root']
# gpu images are very large ~15GB. need a large timeout.
c.KubeSpawner.start_timeout = 60 * 30
# Increase timeout to 5 minutes to avoid HTTP 500 errors on JupyterHub
c.KubeSpawner.http_timeout = 60 * 5

# Volume setup
c.KubeSpawner.singleuser_uid = 1000
c.KubeSpawner.singleuser_fs_gid = 100
c.KubeSpawner.singleuser_working_dir = '/home/jovyan'
volumes = []
volume_mounts = []
###################################################
# Persistent volume options
###################################################
# Using persistent storage requires a default storage class.
# TODO(jlewi): Verify this works on minikube.
# see https://github.com/kubeflow/kubeflow/pull/22#issuecomment-350500944
pvc_mount = os.environ.get('NOTEBOOK_PVC_MOUNT')
if pvc_mount and pvc_mount != 'null':
    c.KubeSpawner.user_storage_pvc_ensure = True
    # How much disk space do we want?
    c.KubeSpawner.user_storage_capacity = '50Gi'
    c.KubeSpawner.user_storage_class = 'standard'
    c.KubeSpawner.user_storage_access_modes = ['ReadWriteMany']
    c.KubeSpawner.pvc_name_template = 'claim-{username}{servername}'

    # user volume
    volumes.append(
        {
            'name': 'volume-{username}{servername}',
            'persistentVolumeClaim': {
                    'claimName': 'claim-{username}{servername}'
            }
        }
    )
    volume_mounts.append(
        {
            'mountPath': pvc_mount,
            'name': 'volume-{username}{servername}'
        }
    )

    # dataset volume
    volumes.append(
        {
            'name': 'volume-datasets',
            'persistentVolumeClaim': {
                    'claimName': 'claim-datasets'
            }
        }
    )
    volume_mounts.append(
        {
            'mountPath': pvc_mount+'/datasets',
            'name': 'volume-datasets'
        }
    )

# ###################################################
# ### Extra volumes for NVIDIA drivers (Azure)
# ###################################################
# # Temporary fix:
# # AKS / acs-engine doesn't yet use device plugin so we have to mount the drivers to use GPU
# # TODO(wbuchwalter): Remove once device plugin is merged
if cloud == 'aks' or cloud == 'acsengine':
    volumes.append({
        'name': 'nvidia',
        'hostPath': {
            'path': '/usr/local/nvidia'
        }
    })
    volume_mounts.append({
        'name': 'nvidia',
        'mountPath': '/usr/local/nvidia'
    })

c.KubeSpawner.volumes = volumes
c.KubeSpawner.volume_mounts = volume_mounts

######## Authenticator ######
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
