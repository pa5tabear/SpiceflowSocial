import hashlib

def norm_uid(title:str, start_iso:str, url_or_venue:str)->str:
    key = f"{(title or '').strip().lower()}|{(start_iso or '').strip()}|{(url_or_venue or '').strip().lower()}"
    return hashlib.md5(key.encode()).hexdigest() + "@spiceflow"
