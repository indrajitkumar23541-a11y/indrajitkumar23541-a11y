import urllib.request

mirrors = [
    "https://github-readme-stats-eight-theta.vercel.app/api?username=indrajitkumar23541-a11y",
    "https://readme-stats.vercel.app/api?username=indrajitkumar23541-a11y",
    "https://github-readme-stats-bice-pi.vercel.app/api?username=indrajitkumar23541-a11y",
    "https://github-readme-stats-sigma-five.vercel.app/api?username=indrajitkumar23541-a11y",
    "https://github-readme-stats-taupe-two.vercel.app/api?username=indrajitkumar23541-a11y"
]

for url in mirrors:
    try:
        req = urllib.request.Request(url, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=5)
        if resp.status == 200:
            print(f"Working mirror: {url}")
            break
    except Exception as e:
        print(f"Failed: {url} - {e}")
