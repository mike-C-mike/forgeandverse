# Forge & Verse v19 Validation

The v19.3 validator hotfix was prepared against GitHub `main` at:

```text
84fb5d93e57a556cd58c2bc4a44b00b65e5800a0
```

## What the v19.2 CI run proved

The repository hygiene audit passed, the release ledger rebuilt, source and release validation passed, and Hugo Extended 0.164.0 completed the production build successfully. The workflow reached the final rendered-site validator for the first time.

That final validator reported 112 errors in two categories:

- 100 alleged missing `alt` attributes
- 12 alleged unresolved `}}` template markers

Both categories were validator false positives. Hugo's HTML minifier may serialize an explicit empty `alt=""` as the valid HTML5 minimized form `alt`, which Python's `HTMLParser` reports with a `None` value even though the attribute is present. Separately, valid JSON-LD can contain adjacent closing braces `}}`, so a bare closing pair is not sufficient evidence of an unresolved Hugo template.

## Corrected by v19.3

- tracks `alt` attribute presence independently from its parsed value
- still fails when an image genuinely has no `alt` attribute
- removes bare `}}` from the unresolved-template marker set
- continues to fail on `{{`, `ZgotmplZ`, `<no value>`, and `<nil>`
- adds regression tests for minified empty alt text, genuinely missing alt text, JSON-LD closing braces, and actual Hugo failure markers
- runs the regression test in both `scripts/build.ps1` and GitHub Actions

## Local verification

```powershell
python .\scripts\test_validate_public.py
.\scripts\clean.ps1
.\scripts\build.ps1
```

Expected result:

1. six validator regression tests pass
2. repository hygiene passes
3. release ledger rebuilds
4. source validation passes
5. Hugo production build succeeds
6. rendered-site validation passes

The GitHub Actions push should then reach the final ledger-diff check.
