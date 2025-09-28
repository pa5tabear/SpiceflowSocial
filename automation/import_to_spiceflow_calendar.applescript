set calendarName to "Spiceflow Social (AI Sandbox)"
set repoPath to POSIX path of (do shell script "pwd")
set winnersPath to repoPath & "/data/out/winners.ics"

tell application "Calendar"
  activate
  set targetCalendar to calendar calendarName
  if targetCalendar is missing value then
    error "Calendar '" & calendarName & "' not found."
  end if
  import POSIX file winnersPath to targetCalendar
end tell
