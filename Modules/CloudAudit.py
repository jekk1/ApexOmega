import requests

# * Cloud Recon (S3, Firebase, GCP bucket discovery)
class CloudAudit:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/4.9 (CloudHunter)'}
        self.cloudSuffixes = [".s3.amazonaws.com", ".firebaseio.com", ".storage.googleapis.com"]

    # * Cari bucket publik berdasarkan domain
    def findCloudBuckets(self, domain):
        found = []
        name = domain.split('.')[0]
        # * Contoh: target-bucket.s3.amazonaws.com
        for suffix in self.cloudSuffixes:
            target = f"https://{name}{suffix}"
            try:
                res = self.session.get(target, timeout=3)
                # * Kita cari yang 200 (Buka/Public) atau 403 (Ada tapi Private)
                # * Kita anggap yang beneran publicly accessible saja (200)
                if res.status_code == 200:
                    found.append(target)
            except Exception:
                pass
        return found
