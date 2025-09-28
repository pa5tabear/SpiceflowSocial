# Obsidian Integration Plan — Spiceflow Social

## Vault Preparation (Owner: Matt)
- **Create clean folder structure** inside `~/Spiceflow/` vault: `00_Inbox/`, `10_Preferences/`, `20_Sources/`, `30_Runs/`, `40_Journal/`, `99_Archive/`.
- **Set default new-note location** in Obsidian settings to `00_Inbox/` for quick captures.
- **Enable `Daily Notes` core plugin** pointing to `40_Journal/` with filename format `YYYY-MM-DD` to align with current journaling habits.
- **Install community plugin `Templater` (optional)** to speed up creating run logs or source cards.
- **Sync setup**: keep vault on iCloud/Obsidian Sync to guarantee the iPhone sees identical structure; confirm mobile app points to `Spiceflow` vault once created.

## Repo ↔ Vault Bridges (Owner: Codex CLI)
1. **Preferences sync**
   - Source of truth remains `SpiceflowSocial/src/preferences.yaml`.
   - Add script `scripts/export_preferences_to_md.py` that converts YAML to Markdown (`10_Preferences/preferences.md`) with sections for goals, quiet hours, budgets, quotas, weights.
   - Optionally round-trip by re-importing Markdown edits back to YAML via frontmatter blocks if we adopt human editing in Obsidian.
2. **Sources sync**
   - For each entry in `src/sources.yaml`, generate `20_Sources/<slug>.md` with frontmatter (url, type, tags) and human-readable notes (selectors, testing status).
   - Maintain `20_Sources/_index.md` summarizing counts, last export timestamp, and pending onboarding tasks.
3. **Run artifacts**
   - After each CLI run, copy `data/out/run_summary.json` and formatted Markdown digest into `30_Runs/YYYY-MM-DD.md` via `scripts/export_run_summary.py` (include links to ICS artifacts).
   - Keep `30_Runs/_log.md` referencing latest run for quick mobile review.
4. **Brain dump ingestion**
   - Establish `00_Inbox/brain-dumps.md` as landing pad. On desktop, CLI can append quick notes (e.g., from LLM research) using `scripts/append_brain_dump.py`.
   - Later bricks can parse `brain-dumps.md` and attach metadata (topic, next actions) inside the repo.

## On-the-Go Workflow (Owner: Matt)
- **ChatGPT to Obsidian (Shortcuts approach)**
  1. Build iOS Shortcut: Share → Append text to `Spiceflow/00_Inbox/brain-dumps.md` (Obsidian mobile exposes vault via Files app).
  2. Include timestamp and context (e.g., `source=ChatGPT`, tags) so the CLI parser can categorize entries.
- **ChatGPT Actions option** (future): register a custom HTTPS endpoint that writes payloads straight to the vault; requires exposing local automation or using Obsidian Sync API once available.
- **Daily review ritual**: during desktop planning sessions, empty `00_Inbox/` by tagging entries, migrating to `40_Journal/` or creating tasks in `30_Runs/`.

## Hygiene & Automation Suggestions
- Track vault with git (optional) to version control notes; ignore `.obsidian/plugins` if unnecessary.
- Configure Obsidian to auto-update internal links so renaming sources or preferences does not break references.
- Add README in vault root (`README.md`) explaining folder purpose, sync expectations, and scripts to run after CLI jobs.
- Schedule a weekly task to run `scripts/export_*` utilities so Obsidian mirrors the latest repo state.

## Next Steps Checklist
1. Matt: finalize vault folder structure and sync to iPhone.
2. Codex: implement `scripts/export_preferences_to_md.py` + `scripts/export_sources_to_md.py` (planned bricks).
3. Matt: build and test iOS Shortcut for ChatGPT brain dumps.
4. Codex: add brick to sprint roadmap covering Obsidian export/import workflow.
5. Joint: review first synced run artifacts to confirm formatting meets mobile consumption needs.

This setup keeps the MacBook-based development workflow in sync with mobile-first consumption through Obsidian, while allowing the Codex CLI to remain the single execution engine.
