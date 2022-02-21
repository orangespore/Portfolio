#!/bin/bash

# 실행전에 cluster.yml 파일 편집 필요
rke up --config=cluster.yml && \

# kubectl 을 사용할 수 있도록 config file 등록
mkdir ~/.kube && \
cp kube_config_cluster.yml ~/.kube/config