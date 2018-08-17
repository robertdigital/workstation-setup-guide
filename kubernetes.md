Installing Kubenetes on GPU Workstation

https://docs.nvidia.com/datacenter/kubernetes-install-guide/index.html

install nvidia-docker2

set docker default runtime to 'nvidia'

install minikube

sudo minikube start --vm-driver=none --feature-gates=DevicePlugins=true

fix perms

kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.10/nvidia-device-plugin.yml

kubectl get nodes -o=custom-columns=NAME:.metadata.name,GPUs:.status.capacity.'nvidia\.com/gpu'

NAME       GPUs
minikube   4

need ks install in /usr/bin

https://github.com/Azure/kubeflow-labs/tree/master/4-kubeflow

For internet access:
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

