import requests
from typing import List, Dict, Optional

# * Modul Auditor Layanan Cloud Terbuka (S3, Firebase, Azure, DO, Alibaba)
class CloudAudit:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/5.0 (Cloud Auditor)'}
        self.cloudSuffixes = {
            "AWS S3": ".s3.amazonaws.com",
            "Firebase": ".firebaseio.com",
            "Google Cloud Storage": ".storage.googleapis.com",
            "Azure Blob": ".blob.core.windows.net",
            "DigitalOcean Spaces": ".nyc3.digitaloceanspaces.com", # Default region
            "Alibaba OSS": ".oss-cn-hangzhou.aliyuncs.com" # Default region
        }

    def generateBucketPermutations(self, domain: str) -> List[str]:
        """Kumpulkan pola nama bucket umum.
        
        Args:
            domain: Domain target sumber nama.
            
        Returns:
            List berisi perpaduan string bucket names.
        """
        name = domain.split('.')[0]
        tld = domain.split('.')[-1] if '.' in domain else ''
        
        permutations = [
            name,
            f"{name}-bucket",
            f"{name}-storage",
            f"{name}-assets",
            f"{name}-media",
            f"{name}-public",
            f"{name}-private",
            f"{name}-prod",
            f"{name}-dev",
            f"bucket-{name}",
            f"{name}.{tld}",
            f"{name}-{tld}"
        ]
        return list(set(permutations))

    def checkPermissions(self, url: str) -> str:
        """Cek hak akses direktori/file pada URL target cloud.
        
        Args:
            url: URL lengkap dari cloud storage.
            
        Returns:
            Status permissions (Public, Auth-Required, Private, atau Error).
        """
        try:
            res = self.session.get(url, timeout=4)
            if res.status_code == 200:
                if "ListBucketResult" in res.text or "Error" not in res.text:
                    return "Public (Fully Exposed)"
                return "Public (Accessible but structured)"
            elif res.status_code in [401, 403]:
                return "Private/Auth-Required"
            elif res.status_code == 404:
                return "Not Found"
            return f"Unknown (Status {res.status_code})"
        except Exception:
            return "Connection Error"

    def findCloudBuckets(self, domain: str) -> List[Dict[str, str]]:
        """Mencari eksistensi bucket cloud terbuka dari sebuah target domain.
        
        Args:
            domain: Domain dari target pencarian.
            
        Returns:
            List of dictionary berisi informasi tentang URL dan Status.
        """
        found = []
        names_to_test = self.generateBucketPermutations(domain)
        
        for name in names_to_test:
            for provider, suffix in self.cloudSuffixes.items():
                target = f"https://{name}{suffix}"
                try:
                    res = self.session.head(target, timeout=3, allow_redirects=True)
                    # Hanya log kalau server bereaksi valid terhadap request cloud (200, 403, 401)
                    if res.status_code in [200, 401, 403]:
                        perm = self.checkPermissions(target)
                        found.append({
                            "provider": provider,
                            "url": target,
                            "permission": perm,
                            "status_code": str(res.status_code)
                        })
                except Exception:
                    pass
        return found
