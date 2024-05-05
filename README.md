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


ERROR: Could not install packages due to an OSError.
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/pip/_internal/commands/install.py", line 339, in run
    requirement_set = resolver.resolve(
  File "/usr/lib/python3/dist-packages/pip/_internal/resolution/resolvelib/resolver.py", line 94, in resolve
    result = self._result = resolver.resolve(
  File "/usr/lib/python3/dist-packages/pip/_vendor/resolvelib/resolvers.py", line 481, in resolve
    state = resolution.resolve(requirements, max_rounds=max_rounds)
  File "/usr/lib/python3/dist-packages/pip/_vendor/resolvelib/resolvers.py", line 348, in resolve
    self._add_to_criteria(self.state.criteria, r, parent=None)
  File "/usr/lib/python3/dist-packages/pip/_vendor/resolvelib/resolvers.py", line 172, in _add_to_criteria
    if not criterion.candidates:
  File "/usr/lib/python3/dist-packages/pip/_vendor/resolvelib/structs.py", line 151, in __bool__
    return bool(self._sequence)
  File "/usr/lib/python3/dist-packages/pip/_internal/resolution/resolvelib/found_candidates.py", line 155, in __bool__
    return any(self)
  File "/usr/lib/python3/dist-packages/pip/_internal/resolution/resolvelib/found_candidates.py", line 143, in <genexpr>
    return (c for c in iterator if id(c) not in self._incompatible_ids)
  File "/usr/lib/python3/dist-packages/pip/_internal/resolution/resolvelib/found_candidates.py", line 44, in _iter_built
    for version, func in infos:
  File "/usr/lib/python3/dist-packages/pip/_internal/resolution/resolvelib/factory.py", line 294, in iter_index_candidate_infos
    result = self._finder.find_best_candidate(
  File "/usr/lib/python3/dist-packages/pip/_internal/index/package_finder.py", line 868, in find_best_candidate
    candidates = self.find_all_candidates(project_name)
  File "/usr/lib/python3/dist-packages/pip/_internal/index/package_finder.py", line 809, in find_all_candidates
    page_candidates = list(page_candidates_it)
  File "/usr/lib/python3/dist-packages/pip/_internal/index/sources.py", line 134, in page_candidates
    yield from self._candidates_from_page(self._link)
  File "/usr/lib/python3/dist-packages/pip/_internal/index/package_finder.py", line 769, in process_project_url
    html_page = self._link_collector.fetch_page(project_url)
  File "/usr/lib/python3/dist-packages/pip/_internal/index/collector.py", line 604, in fetch_page
    return _get_html_page(location, session=self.session)
  File "/usr/lib/python3/dist-packages/pip/_internal/index/collector.py", line 509, in _get_html_page
    resp = _get_html_response(url, session=session)
  File "/usr/lib/python3/dist-packages/pip/_internal/index/collector.py", line 125, in _get_html_response
    resp = session.get(
  File "/usr/lib/python3/dist-packages/pip/_vendor/requests/sessions.py", line 542, in get
    return self.request('GET', url, **kwargs)
  File "/usr/lib/python3/dist-packages/pip/_internal/network/session.py", line 454, in request
    return super().request(method, url, *args, **kwargs)
  File "/usr/lib/python3/dist-packages/pip/_vendor/requests/sessions.py", line 529, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python3/dist-packages/pip/_vendor/requests/sessions.py", line 645, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python3/dist-packages/pip/_vendor/cachecontrol/adapter.py", line 57, in send
    resp = super(CacheControlAdapter, self).send(request, **kw)
  File "/usr/lib/python3/dist-packages/pip/_vendor/requests/adapters.py", line 417, in send
    self.cert_verify(conn, request.url, verify, cert)
  File "/usr/lib/python3/dist-packages/pip/_vendor/requests/adapters.py", line 228, in cert_verify
    raise IOError("Could not find a suitable TLS CA certificate bundle, "
OSError: Could not find a suitable TLS CA certificate bundle, invalid path: False

 

