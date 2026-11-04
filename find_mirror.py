"""Mirror Discovery Script for GitHub Readme Stats.

Finds a responsive and operational mirror instance for github-readme-stats.
Handles:
- User-Agent headers to prevent Vercel/Cloudflare 403 blocks
- Proper HTTP response closing
- Fallback from HEAD to GET for serverless compatibility
- CLI username parameterization
- Deterministic exit codes
"""

import sys
import urllib.error
import urllib.request

DEFAULT_USERNAME = "indrajitkumar23541-a11y"

MIRROR_HOSTS = [
    "https://github-readme-stats-eight-theta.vercel.app",
    "https://readme-stats.vercel.app",
    "https://github-readme-stats-bice-pi.vercel.app",
    "https://github-readme-stats-sigma-five.vercel.app",
    "https://github-readme-stats-taupe-two.vercel.app",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def probe_url(url: str, timeout: int = 5) -> bool:
    """Probe whether an endpoint returns HTTP 200."""
    headers = {"User-Agent": USER_AGENT}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    return True
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code == 405:
                continue  # Retry with GET
            return False
        except Exception:
            if method == "HEAD":
                continue  # Retry with GET in case HEAD timed out or was rejected
            return False
    return False


def find_working_mirror(username: str) -> str | None:
    """Iterate through mirror candidates and return the first active mirror URL."""
    for host in MIRROR_HOSTS:
        url = f"{host}/api?username={username}"
        print(f"Testing mirror: {url} ...")
        if probe_url(url):
            return url
        print(f"  Mirror failed: {host}")
    return None


def main() -> int:
    username = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USERNAME
    print(f"Searching for responsive github-readme-stats mirror for user: {username}")

    working_mirror = find_working_mirror(username)
    if working_mirror:
        print(f"\n[SUCCESS] Working mirror found: {working_mirror}")
        return 0
    else:
        print(f"\n[ERROR] All mirrors failed for user: {username}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
