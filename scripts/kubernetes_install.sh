apt update

apt-get remove docker docker-engine docker.io

apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

add-apt-repository ppa:graphics-drivers/ppa

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
curl -s -L https://nvidia.github.io/kubernetes/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/kubernetes/ubuntu16.04/nvidia-kubernetes.list |\
           sudo tee /etc/apt/sources.list.d/nvidia-kubernetes.list

curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

apt update && apt-upgrade -y

apt install nvidia-396 -y

apt-get install docker-ce

docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo apt-get purge nvidia-docker

sudo apt-get install nvidia-docker2
sudo pkill -SIGHUP dockerd

docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi

apt install -y kubectl=1.9.7+nvidia kubelet=1.9.7+nvidia kubeadm=1.9.7+nvidia
systemctl start kubelet
systemctl status kubelet

sudo reboot
