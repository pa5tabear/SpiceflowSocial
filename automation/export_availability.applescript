-- Export non-sandbox calendars to an ICS snapshot for Spiceflow Social
property sandbox_calendar_name : "Ann Arbor Events & Activities"
property calendars_to_export : {}

tell application "Calendar"
  set repoPath to POSIX path of (do shell script "pwd")
  set exportPath to repoPath & "/data/availability/calendar.ics"
  set exportFile to POSIX file exportPath
  set exportList to {}

  if calendars_to_export is {} then
    repeat with cal in calendars
      if (name of cal) is not sandbox_calendar_name then
        set end of exportList to cal
      end if
    end repeat
  else
    repeat with calName in calendars_to_export
      try
        set theCal to calendar calName
        if (name of theCal) is not sandbox_calendar_name then
          set end of exportList to theCal
        end if
      on error errMsg
        error "Calendar '" & calName & "' not found: " & errMsg
      end try
    end repeat
  end if

  if exportList is {} then
    error "No calendars selected for export. Update calendars_to_export in export_availability.applescript."
  end if

  export exportList to exportFile
end tell
