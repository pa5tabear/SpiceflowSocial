from icalendar import Calendar, Event
from datetime import datetime
import pytz, uuid

TZ = pytz.timezone("America/Detroit")

def to_ics(events:list)->Calendar:
    cal = Calendar()
    cal.add('prodid','-//Spiceflow Social//EN'); cal.add('version','2.0')
    for e in events:
        ev = Event()
        ev.add('uid', e.get('uid', str(uuid.uuid4())))
        ev.add('summary', e.get('title',''))
        start = datetime.fromisoformat(e['start_local'])
        end   = datetime.fromisoformat(e['end_local'])
        if start.tzinfo is None: start = TZ.localize(start)
        if end.tzinfo is None:   end   = TZ.localize(end)
        ev.add('dtstart', start); ev.add('dtend', end)
        if e.get('location'): ev.add('location', e['location'])
        if e.get('url'): ev.add('url', e['url'])
        desc = ((e.get('notes','') + ' ' + e.get('url','')).strip())[:350]
        if desc: ev.add('description', desc)
        cal.add_component(ev)
    return cal
