def generate_health_alert(hazards):
    if not hazards:
        return "No hazards detected."

    hazards = set(hazards)
    msg = "⚠️ Hazards Identified:\n"

    if "stagnant_water" in hazards:
        msg += "- Stagnant water → High mosquito breeding risk.\n"

    if "waste_dump" in hazards:
        msg += "- Waste hotspot → Risk of cholera & infections.\n"

    if "blocked_drain" in hazards:
        msg += "- Blocked drainage → Potential flooding.\n"

    msg += "\nRecommended Action: Notify local health officers or emergency response team."
    return msg
