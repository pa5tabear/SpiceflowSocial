import pytz
from datetime import datetime, timedelta
TZ = pytz.timezone("America/Detroit")

def iso_local(dt:datetime)->str:
    if dt.tzinfo is None:
        dt = TZ.localize(dt)
    return dt.astimezone(TZ).replace(second=0, microsecond=0).isoformat(timespec="minutes")

def default_end(start_iso:str, minutes:int)->str:
    from dateutil import parser
    s = parser.isoparse(start_iso)
    return iso_local(s + timedelta(minutes=minutes))
