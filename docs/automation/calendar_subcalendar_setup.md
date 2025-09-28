# AI Calendar Sandbox Setup

This guide keeps the AI pipeline compartmentalised so it **never touches your
primary calendar directly**. The workflow is: export availability from the
systems you already use, let the pipeline plan against that data, and import
winners back into a dedicated sub-calendar that the AI owns.

## 1. Create the sub-calendar

### Apple Calendar (entry point)
1. Open Apple Calendar.
2. In the sidebar, under *On My Mac* or your Google account, create a new
   calendar named **“Ann Arbor Events & Activities”**.
3. Ensure Google sync is enabled (System Settings → Internet Accounts → your
   Google account → enable *Calendars*).

### Google Calendar (optional cross-check)
1. Visit [calendar.google.com](https://calendar.google.com).
2. Under *Other calendars*, create a calendar with the same name.
3. Confirm it appears in Apple Calendar; this is the sole write target for AI
   suggestions.

## 2. Export availability for planning

1. Select the calendars you want the AI to honour (work, personal, shared,
   etc.).
2. In Apple Calendar choose *File → Export → Export…* and save the `.ics` to
   `data/availability/calendar.ics`.
3. The pipeline reads this file automatically when you pass
   `--availability-ics data/availability/calendar.ics` (default path). Refresh
   it whenever your schedule changes.

## 3. Import winners into the sandbox calendar

Each run writes:
- `data/out/winners.ics`
- `data/out/winners-REMOVE.ics` (rollback that cancels every event)

To keep writes compartmentalised:
1. In Apple Calendar, highlight **Ann Arbor Events & Activities** only.
2. Use *File → Import…* and select `winners.ics`.
3. In the dialog, choose the sandbox calendar as the destination.
4. To roll back, import `winners-REMOVE.ics` into the same calendar.

## 4. Optional automation via AppleScript

Save the script below as `automation/import_to_spiceflow_calendar.applescript`
and run with `osascript` to automate imports.

```applescript
set calendarName to "Ann Arbor Events & Activities"
set icsPath to POSIX file "~/SpiceflowSocial/data/out/winners.ics"

tell application "Calendar"
  activate
  set targetCalendar to calendar calendarName
  if targetCalendar is missing value then
    error "Calendar '" & calendarName & "' not found."
  end if
  import icsPath to targetCalendar
end tell
```

Adjust `icsPath` to match your repo. You can wrap this in a `launchd` plist or
run it manually after the pipeline completes.

## 5. Pipeline configuration

- `src/preferences.yaml` now includes:
  ```yaml
  calendar:
    target_name: "Ann Arbor Events & Activities"
    import_notes: "Import winners.ics into this calendar only."
  ```
  Update these values if you rename the calendar; `run_all.py` reads them when
  stamping ICS files with `X-WR-CALNAME`.
- The run report and shortlist respect this sandbox, while availability parsing
  still reads every calendar represented in your exported `.ics`.

Following these steps ensures the AI **reads broadly** but **writes narrowly** to
its sandbox, keeping human-owned calendars safe.

## 6. Daily automation (optional)

Run the helper script to automate the full loop (export → plan → import):

```bash
chmod +x automation/spiceflow_daily.sh
./automation/spiceflow_daily.sh
```

Schedule it with `launchd` by creating a plist like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.matt.spiceflow.daily</string>
    <key>ProgramArguments</key>
    <array>
      <string>/bin/zsh</string>
      <string>-lc</string>
      <string>cd /Users/mattkirsch/SpiceflowSocial && ./automation/spiceflow_daily.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>86400</integer>
    <key>StandardOutPath</key>
    <string>/tmp/spiceflow_daily.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/spiceflow_daily.log</string>
  </dict>
</plist>
```

Load it with:

```bash
launchctl load ~/Library/LaunchAgents/com.matt.spiceflow.daily.plist
```

The script calls the export AppleScript to read all calendars (excluding the sandbox), runs the planner, and re-imports the winners into the sandbox calendar automatically.
