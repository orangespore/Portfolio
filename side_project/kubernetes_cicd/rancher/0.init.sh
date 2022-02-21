#!/bin/bash

# cat ./server-info.yml | yq e ". | keys" - | read message
# echo $message

# echo " "
# 도커 설치 net tools 는 필요없으면 설치 안해도 됨
# https://docs.docker.com/engine/install/ubuntu/
sudo apt-get install docker.io net-tools -y

# kubectl 설치
# kubectl 을 사용하기 위해서는 ~/.kube/config 에 클러스터 정보를 등록 하거나
# 옵션으로 파일 경로를 지정, 또는 환경 변수로 KUBECONFIG에 파일 경로를 등록
# https://kubernetes.io/docs/tasks/tools/
# https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
sudo snap install kubectl --classic --edge

# helm 설치, kubectl 을 사용 할 수 있어야 helm 도 사용 할 수 있음
# https://helm.sh/docs/intro/install/
sudo snap install helm --classic

# rancher cli 설치
# download 경로 https://github.com/rancher/rke/releases/
# 다운로드 후 실행 권한을 주고 프로그램에 등록
wget https://github.com/rancher/rke/releases/download/v1.3.4/rke_linux-amd64
chmod +x rke*
sudo cp rke* /usr/local/bin/rke 
rke --help
