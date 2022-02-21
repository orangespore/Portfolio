#!/bin/bash

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