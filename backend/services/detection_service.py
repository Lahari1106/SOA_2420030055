import re
from urllib.parse import urlparse

WORDS = {"login","verify","verification","account","update","secure","banking","password","confirm","wallet","signin","bonus","gift","free","urgent","suspended","recover","security"}
SHORTENERS = ("bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly")

def inspect_url(url: str) -> dict:
    value = url.strip()
    if not value:
        raise ValueError("Please enter a URL.")
    parsed = urlparse(value if "://" in value else "http://" + value)
    host = parsed.netloc.lower().split("@")[-1].split(":")[0]
    lower = value.lower()
    signals = {
        "url_length": len(value),
        "uses_https": lower.startswith("https://"),
        "has_ip_address": bool(re.match(r"^(?:https?://)?(?:\d{1,3}\.){3}\d{1,3}(?:[:/]|$)", lower)),
        "has_at_symbol": "@" in value,
        "has_suspicious_words": any(word in lower for word in WORDS),
        "has_many_subdomains": max(0, len(host.split(".")) - 2) >= 3,
        "uses_punycode": "xn--" in host,
        "uses_shortener": any(item in host for item in SHORTENERS),
    }
    reasons = []
    if not signals["uses_https"]: reasons.append("The URL does not use HTTPS.")
    if signals["has_ip_address"]: reasons.append("The URL uses an IP address instead of a typical domain.")
    if signals["has_at_symbol"]: reasons.append("The URL contains an @ symbol that may obscure its destination.")
    if signals["has_suspicious_words"]: reasons.append("The URL contains words often seen in deceptive links.")
    if signals["url_length"] > 100: reasons.append("The URL is unusually long.")
    if signals["has_many_subdomains"]: reasons.append("The domain has several subdomain levels.")
    if signals["uses_punycode"]: reasons.append("The domain contains punycode.")
    if signals["uses_shortener"]: reasons.append("The URL uses a known link-shortening domain.")
    if not reasons: reasons.append("No obvious suspicious patterns were found by these basic checks.")
    return {"url": value, "signals": signals, "reasons": reasons, "service": "Detection Service"}
