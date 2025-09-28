# Spiceflow Social Source Registry

Add each future event source as a Markdown bullet using the format below. The
pipeline will parse these lines directly, so copy the template and swap in your
values when you are ready.

```
- [Display Name](https://example.com/feed) | slug=example_slug | type=ics | city="Ann Arbor, MI" | category=Arts
```

Supported `type` values map to the available scrapers:

- `ics` – download an iCalendar feed
- `jsonld` – fetch page metadata with JSON-LD blocks
- `html` – scrape HTML with CSS selectors
- `js` – render the page with Playwright (requires `--include-js`)

You can add optional attributes as `key=value` pairs separated by `|`. Nested
keys use dot-notation:

```
- [Example HTML Source](https://example.com/events) \
  | slug=example_html \
  | type=html \
  | city="Ann Arbor, MI" \
  | category=Lecture \
  | html.item="div.event-card" \
  | html.title="h3.event-title" \
  | html.datetime="time.event-date" \
  | html.location="div.event-location" \
  | html.url="a::attr(href)"
```

Additional tips:

- Wrap multi-word values in quotes.
- Lists can be provided with JSON/YAML syntax, e.g. `tags=["outdoors","social"]`.
- Lines starting with `#` are ignored. Keep examples inside code fences (as
  above) so they are not parsed.
- Leave this file empty (no bullet lines) if you do not have sources yet.

This documentation block stays at the top so the assistant can convert your
upcoming source list into the optimized structure the scraper expects.
