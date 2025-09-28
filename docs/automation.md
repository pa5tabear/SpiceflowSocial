# Automation Guide for Spiceflow Social

**Owner:** Gemini
**Date:** 2025-09-28

## 1. Overview

This document describes the process for automating the daily execution of the Spiceflow Social event curation pipeline.

The primary tool for this is the `scripts/daily_research.sh` shell script.

## 2. The Daily Research Script

### Purpose

The `daily_research.sh` script is designed to be run once a day to keep your event calendar up-to-date. It performs the following actions:

1.  **Creates Archive:** It creates a new timestamped directory inside `data/archive/` to store the results of the daily run.
2.  **Activates Environment:** It automatically activates the Python virtual environment (`.venv`) if it exists.
3.  **Runs Pipeline:** It executes the main Python script (`src/run_all.py`) in **rolling update mode** (`--rolling-update`). This preserves your existing event selections and intelligently updates the 7-day plan.
4.  **Archives Artifacts:** It copies the key outputs (`winners.ics`, `weekly_review.md`, and `run_summary.json`) into the newly created archive directory for historical tracking.
5.  **Prints Summary:** It displays the contents of `run_summary.json` to the console, providing a quick overview of the run's success, event counts, and any errors.

### How to Run Manually

To execute the script manually, navigate to the root directory of the `SpiceflowSocial` project and run:

```bash
./scripts/daily_research.sh
```

Make sure the script is executable:

```bash
chmod +x ./scripts/daily_research.sh
```

## 3. Scheduling with Cron (for macOS/Linux)

To fully automate the process, you can schedule the script to run automatically at a set time each day using `cron`.

### Example: Run the script every morning at 7:00 AM

1.  **Open your crontab for editing:**

    ```bash
    crontab -e
    ```

2.  **Add the following line to the file:**

    Replace `/path/to/your/SpiceflowSocial` with the absolute path to your project directory.

    ```cron
    # Run Spiceflow Social daily research every morning at 7:00 AM
    0 7 * * * cd /path/to/your/SpiceflowSocial && ./scripts/daily_research.sh >> /tmp/spiceflow_social.log 2>&1
    ```

### Cron Job Breakdown:

- `0 7 * * *`: This specifies the schedule (minute 0, hour 7, every day, every month, every day of the week).
- `cd /path/to/your/SpiceflowSocial`: This is crucial. It changes the directory to your project root before running the script.
- `./scripts/daily_research.sh`: This executes the script.
- `>> /tmp/spiceflow_social.log 2>&1`: This redirects all output (both standard output and errors) to a log file, so you can check the results of the run later.
