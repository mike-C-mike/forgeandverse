# Forge & Verse v20 Validation

v20 was prepared from the green GitHub `main` baseline at:

```text
2f0e237b5d6a1ce569754740b4bf57fb1bad10e3
```

That commit is the v19.4 ledger-portability hotfix and is the first baseline in this cycle where the complete GitHub Actions pipeline passed.

## What this round must prove

v20 changes the studio artifacts more than the framework. Validation therefore focuses on both repository correctness and the honesty of the physical-development state.

### Bench Status Pad v0.3

- exact-size proof remains 4 x 6 inches
- letter two-up proof preserves exact physical size
- v0.3 field-test package is deterministic and checksummed
- three representative desk simulations fit without miniature writing
- the page remains a field proof until real practitioner testing confirms the under-thirty-second re-entry goal

### Examination Notebook v0.3

- exact trim is 5.5 x 8.5 inches
- total length is 32 pages
- 31 interior pages include five structured pages and 26 open working pages
- 26 / 31 = 83.9 percent of the interior remains open working space
- mirrored gutter behavior and four note treatments remain visible for physical testing
- the object remains a production-oriented dummy, not a finished notebook

### Believe in the Badge

- current backdrop master is recorded as 1536 x 1024 pixels
- working large-format target is 36 x 24 inches
- that source is approximately 42.7 ppi at the working target and is therefore not approved for production
- preflight requires at least 5400 x 3600 photographic pixels for a 150 ppi working minimum, with 7200 x 4800 or higher preferred
- no physical-edition state is promoted until a high-resolution master and real sample exist

### Preserved Until It Matters

- new direction study removes the teddy bear from the active hero position
- public study language identifies custody over time as the subject
- previous teddy composition remains only as retired study history
- no real case identifiers or borrowed anecdotal details are introduced

## Required local verification

Install the usual source-validation dependency and the proof-generation dependency when rebuilding proof packs:

```powershell
python -m pip install -r .\scripts\requirements.txt
python -m pip install -r .\scripts\requirements-studio.txt
```

Run:

```powershell
python .\scripts\test_validate_public.py
python .\scripts\test_build_release_ledger.py
python .\scripts\validate_hygiene.py
python .\scripts\build_release_ledger.py
python .\scripts\validate.py
.\scripts\build.ps1
```

Priority browser review after `dev.ps1`:

```text
/
/roadmap/
/roadmap/bench-status-pad/
/roadmap/examination-notebook/
/roadmap/believe-in-the-badge-edition/
/roadmap/preserved-until-it-matters/
/works/believe-in-the-badge/
/releases/
/materials/
```

## GitHub acceptance

The pushed v20 commit should pass the existing workflow all the way through:

1. rendered-site validator regression tests
2. release-ledger portability tests
3. repository hygiene
4. release-ledger generation
5. source and release-artifact validation
6. Hugo Extended 0.164.0 production build
7. rendered-site validation
8. clean deterministic release-ledger diff

A green workflow proves the site build and release records. It does **not** substitute for physical field testing or production sampling of the objects themselves.
