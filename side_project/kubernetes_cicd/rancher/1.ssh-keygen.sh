#!/bin/bash
# 접속 키 생성
ssh-keygen
# 접속 키 등록
cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys

echo "please copy keys to other nodes and install docker.
cmd
1. copy keys: ssh-copy-id -i ~/.ssh/id_rsa.pub <user>@<host> -p <port>
2. install docker on every nodes: sudo apt-get install docker.io && sudo usermod -aG docker $USER

warning: make sure you can connect each nodes without password and run docker"