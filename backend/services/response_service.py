def recommend_response(risk: dict) -> dict:
    score = risk["risk_score"]
    if score >= 60:
        action, message = "BLOCK_AND_ALERT", "High risk. Do not open this link and report it to your security team."
    elif score >= 30:
        action, message = "WARN_USER", "Use caution. Do not enter passwords or personal information."
    else:
        action, message = "ALLOW_WITH_CAUTION", "No strong warning signs were detected. Continue to be cautious."
    return {"action": action, "message": message, "simulated": True, "service": "Response Service"}
