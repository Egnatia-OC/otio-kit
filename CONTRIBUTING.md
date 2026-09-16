# Contributing

Thanks — the useful contributions for this project are in a specific order:

1. **Fidelity evidence.** A reproducible import test on a Resolve version we
   haven't covered (20.3, 21.0, 21.2+; Windows/macOS Free) is worth more than
   any code change. Follow the method in `docs/matrix-21.1.md` and the open
   items in `docs/fidelity-log.md`; record negative results too.
2. **Spec/safe-set extensions** — only with a fidelity-log row behind them.
   The rule that freezes the scope: nothing is emitted without import
   evidence (`docs/spec-scope-v0.md`, versioning rules).
3. **Code** — emitters (FCPXML/EDL are the next formats), the retry +
   schema-repair pass for messy LLM output, and bug fixes.

## Development

```
git clone https://github.com/Egnatia-OC/otio-kit && cd otio-kit
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e . pytest ruff
.venv/bin/ruff check core tests
.venv/bin/pytest tests/ -q
```

(No `uv`? `python -m venv .venv` and `pip install -e . pytest ruff` work the
same.)

## Rules

- Stock OTIO schemas only in the emitter; custom semantics ride in
  `metadata` (fidelity rule 1 — an unknown schema fatals the import).
- Errors are loud and collected (all missing media in one pass, never
  silent).
- Commit style: `area: summary` (e.g. `fix: …`, `docs: …`, `bench: …`).
- The committed test media are empty stubs on purpose; generate real media
  with `specimen/build_specimen.py` for local fidelity work.
