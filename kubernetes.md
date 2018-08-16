Installing Kubenetes on GPU Workstation

https://docs.nvidia.com/datacenter/kubernetes-install-guide/index.html

install nvidia-docker2

set docker default runtime to 'nvidia'

install minikube

sudo minikube start --vm-driver=none --feature-gates=DevicePlugins=true

sudo kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.10/nvidia-device-plugin.yml

sudo kubectl get nodes -o=custom-columns=NAME:.metadata.name,GPUs:.status.capacity.'nvidia\.com/gpu'

need ks install in /usr/bin