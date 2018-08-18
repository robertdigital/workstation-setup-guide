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

install minikube

sudo minikube start --vm-driver=none --feature-gates=DevicePlugins=true

fix perms

kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.10/nvidia-device-plugin.yml

kubectl get nodes -o=custom-columns=NAME:.metadata.name,GPUs:.status.capacity.'nvidia\.com/gpu'

NAME       GPUs
minikube   4

need ks install in /usr/bin

https://github.com/Azure/kubeflow-labs/tree/master/4-kubeflow

## Common Issues

For internet access from Jupyter Notebooks:

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

`kubectl apply -f upstreamDNS.yaml`

JupyterHub Config:

* https://github.com/kubeflow/kubeflow/tree/master/components/jupyterhub
* https://github.com/kubeflow/kubeflow/issues/56


