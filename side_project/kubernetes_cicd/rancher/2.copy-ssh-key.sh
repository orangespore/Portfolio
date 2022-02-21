#!/bin/bash
echo "
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
"