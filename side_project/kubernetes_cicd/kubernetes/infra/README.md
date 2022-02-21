

# Jenkins Gitlab 설치
각 인프라의 kubectl apply -f <filename> -n namespace 로 실행

&nbsp;  
## GITLAB  
### 설치 후 /etc/gitlab/initial_root_password.rb 파일에서 패스워드 확인
### 설치 후 개발된 소스를 푸시, 파이프라인을 위한 repository 생성  
설명 생략

&nbsp;
## JENKINS  
### 처음 실행시 나오는 메시지에 따라 admin을 세팅  
  
&nbsp;  
### pipeline 구성

> #### 1. blueocean에 들어가서 새 배포 파이프라인 생성을 누른다.  
> #### 2. 소스를 선택할때 git source를 선택한다.  
> #### 3. 주소 입력에 source의 주소 및 접속 정보를 입력한다.  
> #### 4. 테스트 및 확인  
> #### 5. 인식할 수 있는 Jenkins 파일이 있을 경우, 파이프라인 완료  
    : 없을경우 파이프라인 생성 화면으로 이동

  
&nbsp;
*파이프라인의 세부 내용은 demo source 참조*