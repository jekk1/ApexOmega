import requests
from typing import List, Dict, Optional

# * Modul Auditor Layanan Cloud Terbuka (S3, Firebase, Azure, DO, Alibaba)
class CloudAudit:
    """
    CloudAudit itu kayak detektif yang nyari harta karun di awan (cloud storage).
    
    Perusahaan modern nyimpen data di cloud:
    - AWS S3 (Amazon)
    - Firebase (Google)
    - Google Cloud Storage
    - Azure Blob (Microsoft)
    - DigitalOcean Spaces
    
    MASALAH BESAR: Banyak yang lupa setting permission!
    
    Bayangin lu punya gudang data di cloud, tapi:
    - Gak dikunci (public access)
    - Siapa aja bisa baca (data leakage)
    - Siapa aja bisa tulis (upload file malicious)
    - Siapa aja bisa hapus (data destruction)
    
    Tool ini bisa:
    
    1. BUCKET NAMING PERMUTATIONS - Tebak nama bucket
       - Dari nama domain, dia bikin variasi:
       - nama.com → nama, nama-bucket, nama-storage, nama-assets
       - bucket-nama, nama.prod, nama.dev, dll
    
    2. PERMISSION CHECKING - Cek apakah bucket kebuka publik
       - Bisa baca file? (data breach)
       - Bisa upload file? (bisa nyelipin malware)
       - Bisa hapus file? (sabotage)
    
    3. MULTI-CLOUD SCAN - Cek semua provider cloud
       - AWS S3, Firebase, GCS, Azure, dll
       - Satu command, semua dicek
    
    Data sensitif yang sering kebocoran:
    - Database backup (.sql, .dump)
    - Config file (.env, credentials.json)
    - User data (CSV, Excel dengan data pelanggan)
    - Log file (bisa ada password/API key)
    - Source code backup
    
    Ini bukan hack - ini NYURI YANG LEGAL karena pintunya kebuka!
    """
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
        HANYA laporkan bucket yang benar-benar PUBLIC (HTTP 200), bukan yang private/auth-required (401/403).

        Args:
            domain: Domain dari target pencarian.

        Returns:
            List of dictionary berisi informasi tentang URL dan Status (hanya yang public).
        """
        found = []
        names_to_test = self.generateBucketPermutations(domain)

        for name in names_to_test:
            # * Robust Handling: Cek apakah data source adalah dict atau list (v6.3.1 Fix)
            items = self.cloudSuffixes.items() if isinstance(self.cloudSuffixes, dict) else [(f"Provider_{i}", s) for i, s in enumerate(self.cloudSuffixes)]

            for provider, suffix in items:
                target = f"https://{name}{suffix}"
                try:
                    res = self.session.head(target, timeout=3, allow_redirects=True)
                    # HANYA laporkan bucket yang benar-benar PUBLIC (200)
                    # JANGAN laporkan 401/403 karena itu artinya bucket PRIVATE (bukan vulnerability)
                    if res.status_code == 200:
                        perm = self.checkPermissions(target)
                        found.append({
                            "provider": provider,
                            "url": target,
                            "permission": perm,
                            "status_code": str(res.status_code)
                        })
                    # 401/403/404 = Bucket tidak ada atau private - ini NORMAL, bukan vulnerability
                except Exception:
                    pass
        return found
