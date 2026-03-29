import requests
from urllib.parse import urljoin
from typing import List, Dict, Tuple, Optional

# * Auditor Keamanan API (REST, GraphQL, Dokumentasi Terbuka)
class ApiAuditor:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/5.0 (API Scanner)'}
        self.commonEndpoints = [
            # Base REST
            "api", "api/v1", "api/v2", "api/v3", "rest", "graphql", "v1/api", "v2/api", "v3/api",
            # Docs
            "api-docs", "swagger", "swagger-ui", "swagger-ui.html", "docs", "v2/docs", "v1/docs", 
            "doc", "apidoc", "redoc", "openapi", "openapi.json", "swagger.json",
            # Auth & Core
            "auth", "login", "signup", "register", "token", "oauth", "jwt", 
            "callback", "webhooks", "ping", "health", "status", "metrics",
            # User & Data
            "user", "users", "admin/api", "user/api", "config", "settings", "profile",
            "account", "me", "data", "search", "upload", "download", "export",
            "import", "graphql/v1", "graphiql", "api/graphql"
        ]

    def fuzzEndpoints(self, baseUrl: str) -> List[str]:
        """Pencarian paksa keberadaan endpoint API tersembunyi.
        
        Args:
            baseUrl: URL dasar target (misal: https://api.target.com)
            
        Returns:
            Daftar endpoint API yang bereaksi aktif (status valid).
        """
        found = []
        base = baseUrl.rstrip('/')
        for e in self.commonEndpoints:
            target = f"{base}/{e}"
            try:
                # Menggunakan GET tanpa mengikuti pengalihan (untuk menghindari misdireksi false positive)
                res = self.session.get(target, timeout=3, allow_redirects=False)
                if res.status_code in [200, 401, 403, 405, 500]:
                    found.append(e)
            except Exception:
                pass
        return found

    def checkAllowedMethods(self, url: str) -> List[str]:
        """Periksa berbagai metode HTTP yang diizinkan untuk melihat kemungkinan celah Bypass.
        
        Args:
            url: URL akhir target (endpoint spesifik).
            
        Returns:
            Daftar metode HTTP yang terbuka layanannya di URL tersebut.
        """
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE"]
        allowed = []
        for m in methods:
            try:
                res = self.session.request(m, url, timeout=3)
                if res.status_code != 405 and res.status_code != 501:
                    allowed.append(m)
            except Exception:
                pass
        return allowed

    def checkGraphqlIntrospection(self, graphqlUrl: str) -> bool:
        """Cari tahu apakah target membiarkan skema GraphQL mereka diintip publik.
        
        Args:
            graphqlUrl: URL khusus entri GraphQL.
            
        Returns:
            True jika GraphQL Introspection diizinkan.
        """
        query = {
            "query": "{ __schema { types { name } } }"
        }
        try:
            res = self.session.post(graphqlUrl, json=query, headers=self.headers, timeout=5)
            if res.status_code == 200 and "__schema" in res.text:
                return True
            return False
        except Exception:
            return False

    def detectExposedDocs(self, baseUrl: str) -> List[str]:
        """Pendeteksi keberadaan modul API Documentation seperti Swagger UI/Redoc.
        
        Args:
            baseUrl: URL dasar yang diekplorasi.
            
        Returns:
            Daftar endpoint yang merujuk pada dokumentasi rawan.
        """
        docs_endpoints = ["swagger-ui.html", "openapi.json", "swagger.json", "api-docs", "redoc", "graphiql"]
        found = []
        base = baseUrl.rstrip('/')
        for d in docs_endpoints:
            target = f"{base}/{d}"
            try:
                res = self.session.get(target, timeout=4)
                if res.status_code == 200 and ("swagger" in res.text.lower() or "openapi" in res.text.lower() or "graphql" in res.text.lower()):
                    found.append(target)
            except Exception:
                pass
        return found
        
    def testBasicIdor(self, authUrl: str, testId1: int = 1, testId2: int = 2) -> Dict[str, str]:
        """Uji dasar Insecure Direct Object Reference berdasarkan tebakan ID sederhana.
        
        Args:
            authUrl: URL API target (berisikan fiks ID, contohnya "user/1" disubstitusi id)
            testId1: Angka pertama pengetesan
            testId2: Angka kedua pengetesan
            
        Returns:
            Dictionary reaktan respon IDOR check.
        """
        results = {}
        try:
            base = authUrl.rstrip('/')
            
            # Request ID 1
            res1 = self.session.get(f"{base}/{testId1}", timeout=4)
            len1 = len(res1.content)
            
            # Request ID 2
            res2 = self.session.get(f"{base}/{testId2}", timeout=4)
            len2 = len(res2.content)
            
            if res1.status_code == 200 and res2.status_code == 200 and len1 != len2:
                results["status"] = "Potential IDOR found (Different Responses Validated)"
            elif res1.status_code == 403 or res1.status_code == 401:
                results["status"] = f"Protected (Status: {res1.status_code})"
            else:
                results["status"] = "No clear IDOR detected"
                
            results["id1_code"] = str(res1.status_code)
            results["id2_code"] = str(res2.status_code)
            
            return results
        except Exception as e:
            return {"status": f"Error testing IDOR: {str(e)}"}
