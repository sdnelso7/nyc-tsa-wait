import httpx

# Public API used by the Port Authority airport websites (JFK, LGA, EWR).
# Requires Origin header that matches the airport's website domain.
_API_BASE = "https://avi-prod-mpp-webapp-api.azurewebsites.net/api/v1"
_API_KEY = "A6CE0EE926BC408B1E9D6E9EC14A5D64"

AIRPORTS = {
    "JFK": {
        "name": "John F. Kennedy International",
        "origin": "https://www.jfkairport.com",
    },
    "LGA": {
        "name": "LaGuardia",
        "origin": "https://www.laguardiaairport.com",
    },
    "EWR": {
        "name": "Newark Liberty International",
        "origin": "https://www.newarkairport.com",
    },
}


def fetch_wait_times(code: str) -> list[dict]:
    """Return TSA checkpoint wait times for the given airport code."""
    airport = AIRPORTS[code]
    url = f"{_API_BASE}/SecurityWaitTimesPoints/{code}"
    headers = {
        "Accept": "application/json",
        "api-key": _API_KEY,
        "Origin": airport["origin"],
        "Referer": f"{airport['origin']}/security-wait-times",
    }
    resp = httpx.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()
