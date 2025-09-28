from datetime import datetime

def overlaps(a,b,c,d): return max(a,c) < min(b,d)

def choose_portfolio(scored:list, cfg:dict, busy:list)->list:
    # greedy by score; enforce weekly caps & no-overlap
    chosen, weeks = [], {}
    for ev in sorted(scored, key=lambda e: e["score"], reverse=True):
        s = datetime.fromisoformat(ev["start_local"])
        e = datetime.fromisoformat(ev["end_local"])
        if cfg["hard_rules"].get("no_overlap", True) and any(overlaps(s,e, bs,be) for (bs,be,_) in busy):
            continue
        wk = s.isocalendar().week
        if weeks.get(wk,0) >= cfg["hard_rules"]["max_events_per_week"]:
            continue
        chosen.append(ev); weeks[wk]=weeks.get(wk,0)+1; busy.append((s,e,ev["title"]))
    return chosen
