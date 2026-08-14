# Source Assets

These files are retained for future editing and are not copied into the public site by Hugo.

- `brand/` contains the original emblem source used for Forge & Verse identity work.
- `work/` contains original work imagery before web compression.
- `prototypes/` contains exact-size and production-oriented PDF proofs used for physical testing and preflight.

Public, web-optimized assets live under `static/`.

## Current v20 prototype sources

- `prototypes/bench-status-pad-prototype-4x6.pdf` - exact-size Bench Status field proof 0.3
- `prototypes/bench-status-pad-prototype-letter-2up.pdf` - ordinary office-printer test
- `prototypes/examination-notebook-interior-prototype.pdf` - 32-page, 5.5 x 8.5 Examination Notebook dummy 0.3
- `prototypes/believe-in-the-badge-composition-study.pdf` - screen-scale composition history
- `prototypes/believe-in-the-badge-production-preflight-v0.1.pdf` - target-size and master-resolution production gate
- `prototypes/preserved-until-it-matters-composition-study.pdf` - retired first composition retained as design history
- `prototypes/preserved-until-it-matters-direction-study.pdf` - current custody-centered v20 direction

## Rebuilding public field-proof packs

The public Bench Status and Examination Notebook field-proof packages can be rebuilt deterministically with:

```powershell
python -m pip install -r .\scripts\requirements-studio.txt
python .\scripts\build_studio_proof_packs.py
```

The exact source PDFs are tracked separately so rebuilding a package does not rewrite the design masters.
