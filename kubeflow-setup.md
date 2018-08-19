# Kubeflow Setup

[Kubeflow](https://github.com/kubeflow/kubeflow) is an open-source Cloud Native platform for machine learning. 

The Kubeflow project is dedicated to making deployments of machine learning workflows on Kubernetes simple, portable and scalable, providing a straightforward way to deploy systems for ML to diverse infrastructures. Kubeflow comes with several useful components, including JupyterHub, and has support for GPU-accelerated compute. Check out the official documentation at [kubeflow.org](http://kubeflow.org/).

## Installing Kubenetes

Prerequisites:

* `nvidia-docker` 2.0 is installed and properly configured
* User is added to the Docker group (allow Docker to run without sudo)

```
TODO

extract relevant portion from:
https://docs.nvidia.com/datacenter/kubernetes-intall-guide/index.html

commands for:
set docker default runtime to 'nvidia'
```

## Installing Minikube

[Minikube](https://github.com/kubernetes/minikube) is a tool that makes it easy to run Kubernetes locally. Minikube runs a single-node Kubernetes cluster inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day.

### Install Minikube

Run the following commands:

```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin/ && rm minikube
export MINIKUBE_WANTREPORTERRORPROMPT=false
export MINIKUBE_HOME=$HOME
export CHANGE_MINIKUBE_NONE_USER=true
export KUBECONFIG=$HOME/.kube/config
sudo -E minikube start --vm-driver=none --feature-gates=DevicePlugins=true
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.10/nvidia-device-plugin.yml
```

If all went well, you should see the following outout:

```
Starting local Kubernetes v1.10.0 cluster...
Starting VM...
Getting VM IP address...
Moving files into cluster...
Setting up certs...
Connecting to cluster...
Setting up kubeconfig...
Starting cluster components...
Kubectl is now configured to use the cluster.
===================
WARNING: IT IS RECOMMENDED NOT TO RUN THE NONE DRIVER ON PERSONAL WORKSTATIONS
	The 'none' driver will run an insecure kubernetes apiserver as root that may leave the host vulnerable to CSRF attacks

daemonset "nvidia-device-plugin-daemonset" created
```

Check if the GPUs on your node can be accessed from Minikube:

`kubectl get nodes -o=custom-columns=NAME:.metadata.name,GPUs:.status.capacity.'nvidia\.com/gpu'`

```
NAME       GPUs
minikube   4
```

### Install ksonnet

```
TODO:
https://ksonnet.io/
need ks install in /usr/bin
```

### Install Kubeflow using ksonnet

```
# Create a namespace for kubeflow deployment
NAMESPACE=kubeflow
kubectl create namespace ${NAMESPACE}

# Which version of Kubeflow to use
# For a list of releases refer to:
# https://github.com/kubeflow/kubeflow/releases
VERSION=v0.2.3

# Initialize a ksonnet app. Set the namespace for it's default environment.
APP_NAME=my-kubeflow
ks init ${APP_NAME}
cd ${APP_NAME}
ks env set default --namespace ${NAMESPACE}

# Add a reference to Kubeflow's ksonnet manifests
ks registry add kubeflow github.com/kubeflow/kubeflow/tree/${VERSION}/kubeflow

# Install Kubeflow components
ks pkg install kubeflow/core@${VERSION}
ks pkg install kubeflow/tf-serving@${VERSION}
ks pkg install kubeflow/tf-job@${VERSION} # TODO: update this command

# Create templates for core components
ks generate kubeflow-core kubeflow-core

# Enable collection of anonymous usage metrics
# Skip this step if you don't want to enable collection.
ks param set kubeflow-core reportUsage true
ks param set kubeflow-core usageId $(uuidgen)
ks param set kubeflow-core jupyterHubServiceType NodePort

# Deploy Kubeflow
ks apply default -c kubeflow-core

# Expose JupyterHub
PODNAME=`kubectl get pods --namespace=${NAMESPACE} --selector="app=tf-hub" --output=template --template="{{with index .items 0}}{{.metadata.name}}{{end}}"`
kubectl expose pod $PODNAME --type=NodePort --name tf-service --namespace kubeflow
```


## Common Issues

**Rate Limit from GitHub**

```
TODO: full instructions
prepend a github token to the command
GITHUB_TOKEN=xxxXXXxxx ks <command>
```

**Kubernetes Dashboard**

```
minikube dashboard &
```

**Internet access from Jupyter Notebooks**

Apply the following config. You can do so via GUI (Kubernetes Dashboard)

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-dns
  namespace: kube-system
data:
  upstreamNameservers: |
    ["8.8.8.8"]
```

### Outstanding Issues

**JupyterHub Config**

* https://github.com/kubeflow/kubeflow/tree/master/components/jupyterhub
* https://github.com/kubeflow/kubeflow/issues/56


