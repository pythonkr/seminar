# 파이썬 세미나, Python Seminar [![Build Status](https://travis-ci.org/pythonkr/seminar.svg?branch=master)](https://travis-ci.org/pythonkr/seminar)

파이콘 한국 준비위원회가 주관하는 파이썬 세미나를 위한 참가 신청, 티켓 결제, 참석자 관리 등 기능이 포함된 웹사이트 저장소입니다.  
This website repository is for that the seminar by "PyCon Korea Committee" which has below features, Attend request, Purchase ticket, Attendee management, etc.... 


## 로컬에서 환경 설정하는 방법, How to set the local environment

`export DJANGO_SETTINGS_MODULE=seminar.settings.local`

위와 같이 `DJANGO_SETTINGS_MODULE` 을 운영체제 환경변수로 잡거나  
Set the `DJANGO_SETTINGS_MODULE` as OS environment variable, or

`./manage.py COMMAND --settings=seminar.settings.local`

처럼 모든 `manage.py` 명령어마다 `--settings` 설정을 추가해야 한다.  
make sure the `--settings` value on every `manage.py` commands.


## 결제 테스트를 위하여, How to test feature of payment

서버를 가동한 후 관리자 페이지에 들어가서 `constance` 설정에서 아임포트 관련 설정값을 채워 넣어 저장하세요. 관련 설정값은 내부 문서에 기록돼있습니다.  
After run the server, enter the admin site and store the Iamport settings into `constance`. There are the Iamport settings in internal document. 


## 로컬에서 테스트 하는 방법, How to run the tests on your computer

`pytest.ini` 파일을 보면 `test` 로 시작하는 모든 파일은 pytest 목록에 자동으로 추가된다.  
As you see the `pytest.ini` file, The files start with `test` will be automatically added into pytest list.

그리고 나서 아래와 같이 `requirements-dev.txt` 에 있는 의존성을 설치하고 로컬 환경을 잡고 `pytest` 실행  
After then, Install dependencies with `requirements-dev.txt` and set the local environment, run `pytest`.

```
pip install -r requirements-dev.txt
pytest (seminar.settings.local 설정 필수, required the setting)
```
