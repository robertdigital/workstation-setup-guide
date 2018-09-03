import json
import os
from kubespawner.spawner import KubeSpawner


class KubeFormSpawner(KubeSpawner):

    def _options_form_default(self):
        global registry, repoName
        return '''
    <h2>Kubeflow Demo</h2>
    <p>Please allocate resources responsibly<br>
    If your server is unable to start, it is likely that the GPU you requested for is not available.<br>
    Try starting a server <b>without a GPU</b> before reporting a server problem.</p>
    <hr>
    <label for='image'>Image</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input list=\"image\" name=\"image\" placeholder='repo/image:tag'>
    <datalist id=\"image\">
      <option value=\"jupyter/minimal-notebook:latest\">
      <option value=\"jupyter/datascience-notebook:latest\">
      <option value=\"stepankuzmin/pytorch-notebook:latest\">
      <option value=\"{0}/{1}/tensorflow-1.7.0-notebook-cpu:v0.2.1\">
      <option value=\"{0}/{1}/tensorflow-1.7.0-notebook-gpu:v0.2.1\">
      <option value=\"{0}/{1}/tensorflow-1.8.0-notebook-cpu:v0.2.1\">
      <option value=\"{0}/{1}/tensorflow-1.8.0-notebook-gpu:v0.2.1\">
    </datalist>
    <p>If image is not present, it will be pulled from Docker Hub.<br>This may take a long time to complete.</p>
    <br/>
    <label for='cpu_guarantee'>CPU</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input name='cpu_guarantee' placeholder='1.0'></input>
    <p>If your work is not CPU-intensive, you can choose less than 1 CPU (e.g. <code>0.5</code>)</p>
    <br/>
    <label for='mem_guarantee'>Memory</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input name='mem_guarantee' placeholder='1.0Gi'></input>
    <br/>
    <label for='extra_resource_limits'>GPU</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input list=\"extra_resource_limits\" name=\"extra_resource_limits\" placeholder=''>
    <datalist id=\"extra_resource_limits\">
      <option value=\"\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 1}}\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 2}}\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 3}}\">
      <option value=\"{{&quot;nvidia.com/gpu&quot;: 4}}\">
    </datalist>
    <p>Example: to request 2 GPUs: <code>{{&quot;nvidia.com/gpu&quot;: 2}}</code><br>Please leave this field blank for none.</p>
    <br/>
    <label for='node_selector'>Resource Criteria</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input list=\"node_selector\" name=\"node_selector\" placeholder=''>
    <datalist id=\"node_selector\">
      <option value=\"\">
      <option value=\"{{&quot;accelerator&quot;: &quot;k80&quot;}}\">
      <option value=\"{{&quot;accelerator&quot;: &quot;p100&quot;}}\">
    </datalist>
    <p>To request specifically for P100: <code>{{&quot;accelerator&quot;: &quot;p100&quot;}}</code><br>Options: p100, k80, or leave it blank</p>
    <br/>
    '''.format(registry, repoName)

    def options_from_form(self, formdata):
        options = {}
        options['image'] = formdata.get('image', [''])[0].strip()
        options['cpu_guarantee'] = formdata.get(
            'cpu_guarantee', [''])[0].strip()
        options['mem_guarantee'] = formdata.get(
            'mem_guarantee', [''])[0].strip()
        options['extra_resource_limits'] = formdata.get(
            'extra_resource_limits', [''])[0].strip()
        options['node_selector'] = formdata.get(
            'node_selector', [''])[0].strip()
        return options

    @property
    def singleuser_image_spec(self):
        global cloud
        if cloud == 'ack':
            image = 'registry.aliyuncs.com/kubeflow-images-public/tensorflow-notebook-cpu'
        else:
            image = 'gcr.io/kubeflow-images-public/tensorflow-1.8.0-notebook-cpu:v0.2.1'
        if self.user_options.get('image'):
            image = self.user_options['image']
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

    @property
    def node_selector(self):
        extra = ''
        if self.user_options.get('node_selector'):
            extra = json.loads(self.user_options['node_selector'])
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
    c.KubeSpawner.user_storage_capacity = '1Gi'
    c.KubeSpawner.user_storage_class = 'standard'
    c.KubeSpawner.pvc_name_template = 'claim-{username}{servername}'
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
