def title_key(s:str)->str:
    return ' '.join((s or '').lower().split())

def dedupe(events:list)->list:
    seen, out = set(), []
    for e in events:
        k = (title_key(e.get("title","")), e.get("start_local","")[:16], (e.get("location") or e.get("url") or "").lower())
        if k in seen: 
            continue
        seen.add(k); out.append(e)
    return out
