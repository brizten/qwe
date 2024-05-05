CREATE OR REPLACE FUNCTION random_data()
RETURNS void AS
$$
BEGIN
    DECLARE
        random_password TEXT;
    BEGIN
        random_password := substr(md5(random()::text), 0, 10);
        
        update admin_passwords
        set password = random_password
        where id = (select id from admin_passwords);
    END;
END;
$$
LANGUAGE plpgsql;


SELECT random_data();

select *
from admin_passwords

delete from admin_passwords


CREATE OR REPLACE FUNCTION update_prev_password()
RETURNS TRIGGER AS
$$
BEGIN
    IF OLD.password IS NOT NULL THEN
        NEW.prev_password := OLD.password;
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER before_password_update
BEFORE UPDATE ON admin_passwords
FOR EACH ROW
EXECUTE FUNCTION update_prev_password();


DROP TRIGGER IF EXISTS before_password_update ON admin_passwords;



Executing "step_script" stage of the job script
00:01
$ Invoke-WebRequest -Uri 'http://github.com/allure-framework/allurectl/releases/latest/download/allurectl_windows_amd64.exe' -OutFile 'allurectl.exe'
Invoke-WebRequest : The request was aborted: Could not create SSL/TLS secure 
channel.
At line:270 char:1
+ Invoke-WebRequest -Uri 
'http://github.com/allure-framework/allurectl/releases/la ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~
    + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:Htt 
   pWebRequest) [Invoke-WebRequest], WebException
    + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShe 
   ll.Commands.InvokeWebRequestCommand



build-job:
  stage: test
  image: gradle
  variables:
    ALLURE_ENDPOINT: https://allure-testops.halykbank.nb
    ALLURE_PROJECT_ID: 6
    ALLURE_RESULTS: build/allure-results
  before_script:
    - Invoke-WebRequest -Uri 'http://github.com/allure-framework/allurectl/releases/latest/download/allurectl_windows_amd64.exe' -OutFile 'allurectl.exe'
    - Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force

  script: 
    - ./allurectl watch -- gradle clean test

test-job1:
  stage: test 
  
  script:
    - ./allurectl watch -- gradle clean test
  
deply-prod:
  stage: deploy
 
  script:
    - ./allurectl watch -- gradle clean test



[global]
index = https://nexus.halykbank.nb/repository/Pypi/pypi
index-url = https://nexus.halykbank.nb/repository/Pypi/simple
extra-index-url = https://nexus.halykbank.nb/repository/pypi-hosted/simple
trusted-host = nexus.halykbank.nb


 pip install psycopg2
Looking in indexes: https://nexus.halykbank.nb/repository/Pypi/simple, https://nexus.halykbank.nb/repository/pypi-hosted/simple
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/Pypi/simple/psycopg2/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/Pypi/simple/psycopg2/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/Pypi/simple/psycopg2/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/Pypi/simple/psycopg2/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/Pypi/simple/psycopg2/
Could not fetch URL https://nexus.halykbank.nb/repository/Pypi/simple/psycopg2/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='nexus.halykbank.nb', port=443): Max retries exceeded with url: /repository/Pypi/simple/psycopg2/ (Caused by SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))) - skipping
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/pypi-hosted/simple/psycopg2/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/pypi-hosted/simple/psycopg2/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/pypi-hosted/simple/psycopg2/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/pypi-hosted/simple/psycopg2/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))': /repository/pypi-hosted/simple/psycopg2/
Could not fetch URL https://nexus.halykbank.nb/repository/pypi-hosted/simple/psycopg2/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='nexus.halykbank.nb', port=443): Max retries exceeded with url: /repository/pypi-hosted/simple/psycopg2/ (Caused by SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)'))) - skipping
ERROR: Could not find a version that satisfies the requirement psycopg2 (from versions: none)
ERROR: No matching distribution found for psycopg2

 

