## Python 설치

[python 3.7.3 설치](https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe)

제어판 > 시스템 > 고급 시스템 설정 > 고급 > 환경변수 이동

다음 2개의 경로를 Path 항목에 추가한다.

C:\Python\Python37;
C:\Python\Python37\Scripts

## 라이브러리 설치 (WINDOWS)

### konlpy 설치

[JDK 설치](https://www.oracle.com/java/technologies/downloads/#jdk17-windows)

제어판 > 시스템 > 고급 시스템 설정 > 고급 > 환경변수 이동

시스템 변수 편집
-> 변수 이름 : JAVA_HOME
-> 변수 값 : 본인이 설치한 jdk 경로 입력 (ex : C:\Program Files\Java\jdk1.8.0_241)

사용자 환경 변수 편집 - 새로 만들기에서
-> %JAVA_HOME%bin
을 추가한다

다시 터미널로 이동하여 

pip install --upgrade pip

를 진행해 주고, 올라와 있는 JPype1.whl 파일을 설치해 준다.

pip install "whl 파일 이름"

이후

pip install konlpy 

를 통해 konlpy를 설치한다

### 이외 필수 라이브러리 설치(tqdm, scikitlearn, selenium, pandas)

pip install tqdm

pip install scikit-learn

pip install scipy 

pip install selenium

pip install pandas

## 사용법

3개의 폴더를 생성한다

"검수" / "결과" / "샘플"

"검수" 폴더의 하위 폴더로 자신이 원하는 키워드 폴더를 만들고 검수할 파일 원고(.txt 확장자)를 저장한다.

이후 "start_inspector.bat" 파일을 실행하여 "키워드" "조회 블로그 페이지 수" 를 입력한다.

"키워드"(문장) : 블로그 검색창에 조회할 단어 혹은 문장(키워드)

"페이지"(숫자) : 노출 빈도 상위 글 기준 페이지 1당 7개의 글이 조회된다. (1~3 사이 권장)

프로그램의 동작이 완료되면 "결과" 폴더 아래의 "키워드.csv" 파일을 확인해서 유사도가 높은 문서를 확인한다.