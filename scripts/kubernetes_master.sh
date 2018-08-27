./kubernetes_install.sh

kubeadm init --ignore-preflight-errors=all --config /etc/kubeadm/config.yml

mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.9.1/Documentation/kube-flannel.yml

kubectl get pods --all-namespaces

kubectl taint nodes --all node-role.kubernetes.io/master-

kubectl get pods --all-namespaces


