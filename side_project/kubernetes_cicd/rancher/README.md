# RANCHER 쿠버네티스 설치  
## 하드웨어 최소 사양  
### 2core 8gb 20gb hard disk  
  
### 구조  
설치 스크립트를 실행하는 node 에서 각 node에 접근하여 rancher(kubernetes)를 설치  
rke cli에서 각 node에 ssh를 위해 접근할 수 있도록 미리 세팅 하여야함  
*node0는 node1, node2, node3과 같을 수 있음*
```
script 실행 node0
    |
    |---------------ssh---------- node1
    |
    |---------------ssh---------- node2
    |
    |---------------ssh---------- node3
    .
    .
```
  
&nbsp;
## 전제조건  
### 1. 모든 node에 docker가 설치 되어 있으며 sudo 필요 없이 실행 가능 할것  
### 2. 모든 node에 ssh로 password 없이 접근 가능 할 것  
  
&nbsp;
## 설치 프로그램
### - docker: 기본
### - rancher cli(rke): rancher 설치용 cli 툴
### - kubectl: rancher cluster 설치 후 쿠버네티스 클러스터 컨트롤
### - helm: 쿠버네티스 앱 패키지 관리
  
&nbsp;
## 설치 순서  
### 0. 기본 프로그램 설치(controll)  
### 1. ssh 키 생성  
### 2. ssh 키 각 노드에 등록  
### 3. rancher cluster 생성 및 kubernetes 키등록  
### 4. rancher ui 설치  
  
&nbsp;
## 0. 기본 프로그램  
### 기본 프로그램: docker, kubectl, helm, rke cli  
### *0.init.sh*
```

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

```

&nbsp;
## 1. 키생성
### rancher(쿠버네티스)를 자동으로 설정하기 위해서는 cli에서 각 노드에 ssh로 자유롭게 접근이 가능하도록 해야함
### 먼저 cli를 실행할 노드의 키를 만들고 등록 해야함
### *1.ssh-keygen.sh*
```
# 접속 키 생성
ssh-keygen

# 접속 키 등록 script node가 쿠버네티스 노드 중 하나일 경우
# 자기 자신에도 ssh로 키없이 접근 할 수 있어야함
cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
```
  
&nbsp;
## 2. 각 노드에 키등록 및 도커 세팅
### script 실행 노드의 키를 각 노드에 등록하여 script 노드에서 맘대로 접근 할 수 있도록 함
### docker image를 기본으로 사용하기 때문에 docker 를 설치 해야함(sudo 권한없이 실행 가능 해야함)
```
# scp -r ~/.ssh/ <user>@<host> -p <port>
# 접속 후 docker 설치

# 서버에 접속
# 1. ssh <user>@<server-n> -p <port>

# docker 설치
# 2. sudo apt-get install docker.io -y

# sudo 없이 docker 실행하기
# 3. sudo usermod -aG docker $USER

# check - 아래 명령어를 script노드에서 실행시 패스워드 없이 실행하면 통과
# ssh -p <port> <user>@<server> docker images
```
  
&nbsp;
## 3. rancher(쿠버네티스) 설치
### ssh 로 각 노드에 접근 가능한지 확인 후
### cluster 정보를 cluster.yml 파일에 세팅함
### *cluster.yml*
```
nodes:
    # 주소
  - address: x.x.x.x
    # 내부 주소(optional)
    internal_address: x.x.x.x
    # ssh 접속 id
    user: ubuntu
    # 설치 롤
    role: [controlplane,etcd,worker]
    # 나중에 표시될 서버 이름, 미입력시 현재 서버 이름 사용
    hostname_override: server1
    # 접속할 ssh 키 (~/.ssh/id_rsa 일경우 생략 가능)
    ssh_key_path: ${server1 key path}

  - address: x.x.x.x
    internal_address: x.x.x.x
    user: ubuntu
    role: [controlplane,worker,etcd]
    hostname_override: server2
    ssh_key_path: ${server1 key path}

  - address: x.x.x.x
    internal_address: x.x.x.x
    user: ubuntu
    role: [controlplane,worker,etcd]
    hostname_override: server3
    ssh_key_path: ${server1 key path}
```
  
&nbsp;
### *3.create-rancher.sh*
```
# 실행전에 cluster.yml 파일 편집 필요
rke up --config=cluster.yml && \

# kubectl 을 사용할 수 있도록 config file 등록
mkdir ~/.kube && \
cp kube_config_cluster.yml ~/.kube/config
```
  

## 4. rancher ui 설치
### 쿠버네티스관리 ui 툴 설치
### helm을 사용하여 설치
### *4.rancher-ui.sh*
```
# 쿠버네티스에 namespace를 만듬
kubectl create ns cattle-system

# helm repository를 추가
helm repo add rancher-latest https://releases.rancher.com/server-charts/latest

# rancher ui 설치
# tls(https)는 external를 사용, lets encrypt를 사용 할 수 있음
# https://rancher.com/docs/rancher/v2.5/en/installation/install-rancher-on-k8s/
helm upgrade --install rancher rancher-latest/rancher \
  --namespace cattle-system \
  --set tls="external"

# lets encrypt사용시
# helm upgrade --install rancher rancher-latest/rancher \
#   --namespace cattle-system \
#   --set hostname=${hostname} \
#   --set ingress.tls.source=letsEncrypt \
#   --set letsEncrypt.environment="production" \
#   --set letsEncrypt.email=${email} \
#   --set letsEncrypt.ingress.class=nginx

# helm 배포 상태를 모니터링
kubectl rollout status deploy/rancher -n cattle-system
```
  
&nbsp;
HOST에 접속할 수 있으면 완료  
  
&nbsp;
### rancher 기본 앱 설치  
#### cluster tools: 좌측 상단 햄버거 메뉴 > 하단 Cluster tools  
- longhorn: local disk provisioning(추천)  
- monitoring: server resouece 등 모니터링(추천)  
- altering driver: slack 등 연동  
- rancher backups: 쿠버네티스 클러스터 backup(추천)  
- logging: cluster log 수집 파이프 라인