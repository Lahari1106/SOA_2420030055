def calculate_risk(detection: dict) -> dict:
    signals = detection["signals"]
    score = 0
    if not signals["uses_https"]: score += 12
    if signals["has_ip_address"]: score += 25
    if signals["has_at_symbol"]: score += 20
    if signals["has_suspicious_words"]: score += 20
    if signals["url_length"] > 100: score += 10
    if signals["has_many_subdomains"]: score += 10
    if signals["uses_punycode"]: score += 15
    if signals["uses_shortener"]: score += 10
    score = min(score, 100)
    level = "High" if score >= 60 else "Medium" if score >= 30 else "Low"
    prediction = "Potentially phishing" if score >= 30 else "No strong warning signs found"
    return {"risk_score": score, "risk_level": level, "prediction": prediction, "service": "Risk Analysis Service"}
