set calendarName to "Ann Arbor Events and Activities"
set repoPath to POSIX path of (do shell script "pwd")
set winnersPath to repoPath & "/data/out/winners.ics"

set timeHorizonDays to 30 -- adjust window for verification

tell application "Calendar"
  activate
  set targetCalendar to calendar calendarName
  if targetCalendar is missing value then
    error "Calendar '" & calendarName & "' not found."
  end if
  import POSIX file winnersPath to targetCalendar

  -- Verification block
  set nowDate to current date
  set cutoffDate to nowDate - (timeHorizonDays * days)
  set recentEvents to (every event of targetCalendar whose start date is greater than cutoffDate)
  set eventCount to count of recentEvents
  display notification "Spiceflow run imported events" with title "Spiceflow Social" subtitle "Sandbox calendar updated" sound name "Glass"
  log "Spiceflow sandbox verification — events in last " & timeHorizonDays & " days: " & eventCount
end tell
