-- Placeholder AppleScript. Do not run now.
-- Later, set calName to the exact Google-backed calendar in Apple Calendar.
set calName to "Matt – Google"

on make_event(tTitle, tLocation, tStartISO, tEndISO, tURL, tNotes)
  set startDate to do shell script "date -j -f \"%Y-%m-%dT%H:%M\" " & quoted form of tStartISO & " \"+%m/%d/%Y %H:%M\""
  set endDate   to do shell script "date -j -f \"%Y-%m-%dT%H:%M\" " & quoted form of tEndISO   & " \"+%m/%d/%Y %H:%M\""
  tell application "Calendar"
    tell calendar calName
      make new event with properties {summary:tTitle, location:tLocation, start date:date startDate, end date:date endDate, description:(tNotes & return & tURL)}
    end tell
  end tell
end make_event
