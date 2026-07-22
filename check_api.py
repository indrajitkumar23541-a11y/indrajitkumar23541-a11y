import urllib.request
url = "https://github-profile-trophy.vercel.app/?username=indrajitkumar23541-a11y&theme=tokyonight&no-frame=true&no-bg=true&margin-w=15"
try:
    req = urllib.request.Request(url, method="HEAD")
    resp = urllib.request.urlopen(req, timeout=5)
    print("Trophy API is UP:", resp.status)
except Exception as e:
    print("Trophy API is DOWN:", e)
