from pathlib import Path
def write_digest(path:Path, summary:str, proposals:list):
    lines = [summary, ""]
    for p in proposals:
        lines.append(f"• {p['type'].upper()} {p['when']} — {p['title']} @ {p.get('location','')}")
    path.write_text("\n".join(lines))
