def score_event(ev:dict, cfg:dict)->float:
    score = 0.0
    cats = (ev.get("category","") or "").lower()
    if "lecture" in cats or "tech" in cats: score += cfg["weights"]["goals.career_learning"]
    if "wellness" in cats: score += cfg["weights"]["goals.wellbeing_fitness"]
    if "outdoors" in cats: score += cfg["weights"]["goals.outdoors_nature"]
    if "business" in cats: score += cfg["weights"]["goals.career_learning"]*0.6
    return score
