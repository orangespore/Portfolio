# git-flow  
## 서버 3개를 운영
  
![gitflow](./git-model@2x.png =300x400)
  
### - develop: 개발 브랜치 -> 개발 서버 파이프라인 연결
### - release: 테스트 브랜치 -> 테스트 서버 파이프라인 연결
### - master: 운영 브랜치 -> 운영 서버 파이프라인 연결
  
  &nbsp;
## 개발서버  
### - 개발시에 필요한 서버  
### - front와 api backend로 구성시에  
### - backend에서 개발한 api를 프론트 개발에 열어줄 필요가 있어 개발 서버가 필요  
  
  &nbsp;
## 테스트 서버(릴리즈, 스테이징)  
### - 운영서버에 반영하기 전에 QA 또는 발주처 컨펌용으로 사용  
### - 개발 서버에서 어느정도 버그가 잡힌 이후에 반영  
### - 개발자들이 직접 푸시하는 것을 막아야 함  
  
&nbsp;
## 운영 서버  
### - 말그대로 운영서버 리소스가 충분한 것이 좋음  
### - 개발자들이 직접 푸시 하는 것을 막아야 함  

```
개발자1 ----┐
            |
개발자2 ----┤----> dev branch ----> release branch ----> master branch
            |           |                  |                   |
개발자3 ----┘          ∨                 ∨                  ∨
                     개발서버           테스트 서버          운영서버

```
  
  &nbsp;
## HOT FIX  
### 긴급 패치가 필요할 경우 전략은 두가지  
#### 1. 수정 후 master 부터 release dev로 동기화  
#### 2. 수정 후 release에서 테스트 후 master, dev에 푸시  
  
  &nbsp;
## FILE
### 서버를 동일 노드에 구성 할 수도 있고 별도로 구성 할수도 있음  
### 예제는 동일 노드에 구성함  
    
```
kubectl 명령어로 배포 할 수 있음  
option으로 namespace를 지정할 수 있는데,

<filenames>
- deployment-develop.yml: 개발 서버  
- deployment-release.yml: 테스트 서버  
- deployment-master.yml: 운영 서버  
- deployment-template.yml: 세팅 기본값  

1. template에 namespace가 있을 경우: 생략 또는 같은 이름 사용해야함
2. template에 namespace가 없을 경우: 생략하면 default 넣으면 그 namespace에서 만듬

kubectl apply -f <filename> (-n <namespace>)
```
