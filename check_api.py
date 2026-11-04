"""API Health Checker script.

Validates the availability of remote SVG badge / telemetry services with:
- Standard User-Agent header (prevents 403 Forbidden from Cloudflare/Vercel)
- Safe fallback from HEAD to GET (handles 405 Method Not Allowed)
- Proper resource management (auto-closing response context)
- Deterministic exit codes for CI/CD automation (0 for UP, 1 for DOWN)
"""

import sys
import urllib.error
import urllib.request

DEFAULT_URL = (
    "https://github-profile-trophy.vercel.app/"
    "?username=indrajitkumar23541-a11y&theme=tokyonight&no-frame=true&no-bg=true&margin-w=15"
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def check_endpoint(url: str, timeout: int = 5) -> tuple[bool, str]:
    """Check if the given URL is reachable and returns HTTP 200.

    Attempts a HEAD request first, falling back to a GET request if HEAD is rejected (HTTP 405).

    Returns:
        tuple (is_up: bool, message: str)
    """
    headers = {"User-Agent": USER_AGENT}

    # Attempt HEAD request
    try:
        req = urllib.request.Request(url, headers=headers, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return True, f"UP (HTTP {resp.status} via HEAD)"
    except urllib.error.HTTPError as e:
        if e.code == 405:
            # Fall back to GET if serverless endpoint rejects HEAD
            try:
                req_get = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(req_get, timeout=timeout) as resp:
                    if resp.status == 200:
                        return True, f"UP (HTTP {resp.status} via GET fallback)"
            except Exception as err:
                return False, f"DOWN: {err}"
        return False, f"DOWN (HTTP {e.code}: {e.reason})"
    except Exception as e:
        return False, f"DOWN: {e}"

    return False, "DOWN (Unknown response)"


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python check_api.py [url]")
        print("Probes an API endpoint and checks its availability status.")
        return 0

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    print(f"Checking API: {url}")
    is_up, message = check_endpoint(url)
    if is_up:
        print(f"API Status: {message}")
        return 0
    else:
        print(f"API Status: {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
