import requests
from urllib.parse import urljoin

# * Auditor API (REST/GraphQL Fuzzing dan Method Check)
class ApiAuditor:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/4.9 (API Scanner)'}
        self.commonEndpoints = [
            "api", "api/v1", "api/v2", "rest", "graphql", "v1/api", "v2/api", "api-docs",
            "swagger-ui", "docs", "v2/docs", "user/api", "admin/api", "auth", "login",
            "signup", "register", "token", "oauth", "jwt", "callback", "webhooks"
        ]

    # * Cari endpoint API tersembunyi
    def fuzzEndpoints(self, baseUrl):
        found = []
        base = baseUrl.rstrip('/')
        for e in self.commonEndpoints:
            target = f"{base}/{e}"
            try:
                res = self.session.get(target, timeout=3, allow_redirects=False)
                # * Kita cari yang response-nya beneran API (200, 401, 403, 405)
                if res.status_code in [200, 401, 403, 405]:
                    found.append(e)
            except Exception:
                pass
        return found

    # * Cek metode HTTP yang di-support (IDOR/Bypass check)
    def checkAllowedMethods(self, url):
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        allowed = []
        for m in methods:
            try:
                res = self.session.request(m, url, timeout=3)
                if res.status_code != 405:
                    allowed.append(m)
            except Exception:
                pass
        return allowed
