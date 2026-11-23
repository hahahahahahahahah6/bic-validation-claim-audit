# Documentation claim audit

This offline tool compares selected documentation prose against static Python source patterns. It does not execute the inspected code or use the network.

## Usage

```sh
python3 -m bic_validation_claim_audit audit .
python3 -m bic_validation_claim_audit audit . --json --verbose --ignore vendor --fail-on medium
python3 -m bic_validation_claim_audit --version
```

A finding at the chosen threshold returns status 2; a clean audit returns 0 and an input or usage error returns 1. The default threshold is high; test-only evidence produces a medium finding. Repeat the ignore option to skip more path prefixes.

Only the root README and Markdown files under a docs directory are read. Fenced code is excluded; inline code is included. Exact phrases are matched after case, whitespace, hyphen, and contraction normalization. Python source is parsed without execution; test files are treated separately. Symlinks, fixtures, examples, and documentation source files are excluded from evidence. Each recognized route must occur in one module.

## Differentiation

This concerns business identifier code strings. It does not cover generic input checks; ISBN or ISSN check digits; IBAN bank accounts; UUIDs; semantic versions; MAC addresses; payment processing; credit card extraction; authentication; password verification, hashing, generation or strength; PDF encryption; email or SMS sending; document extraction; barcode scanning or generation; email, phone, date, credit card, domain, URL, IP address or JSON schema checks. Parsing JSON, matching a regular expression, splitting or fetching a URL, and DNS resolution are separate operations. Reading account numbers, reading identifier components, bank registry lookup, generating or reshaping an identifier, and judging a basic bank account number are separate operations.

Other distinct families cover spreadsheet, word-document and presentation reading and generation; PDF extraction, generation, merging, splitting, rotation, form-filling, watermarking, redaction, compression and annotation; table extraction, OCR, document extraction and e-signature; screen recording and video generation; QR code generation; audio mixing, generation and editing; source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription.

## Limitations

The following wording may refer to a registry or remote lookup, so a human should review the result.

```text
validate bic
```

The following wording may refer to a manual runbook step, so a human should review the result.

```text
check bic
```

The following wording may refer to a roadmap item, so a human should review the result.

```text
bic validation
```

The following wording may refer to a hosted page, so a human should review the result.

```text
bic validator
```

The following wording may refer to reader advice, so a human should review the result.

```text
valid bic
```

The following wording may refer to a successful lookup, so a human should review the result.

```text
bic is valid
```

The following wording may refer to a specification section, so a human should review the result.

```text
bic string validation
```

The following wording may refer to an allow-list lookup, so a human should review the result.

```text
validate bic string
```

The following wording may refer to registry existence, so a human should review the result.

```text
verify bic
```

The following wording may refer to a length-only check, so a human should review the result.

```text
detect invalid bic
```

The following wording may refer to a theoretical discussion, so a human should review the result.

```text
bic well formed
```

The following wording may refer to a generated value, so a human should review the result.

```text
is valid bic
```

The following wording may refer to spacing alone, so a human should review the result.

```text
bic format validation
```

The following wording may refer to Swift source code, so a human should review the result.

```text
validate swift code
```

The following wording may refer to Swift source code, so a human should review the result.

```text
swift code validation
```

The following wording may refer to Swift source code, so a human should review the result.

```text
check swift code
```

The following wording may refer to compiling Swift source, so a human should review the result.

```text
valid swift code
```

The following wording may refer to a manual step, so a human should review the result.

```text
bic check
```

The following wording may refer to a specification section, so a human should review the result.

```text
bic string check
```

The following wording may refer to another business identifier, so a human should review the result.

```text
validate business identifier code
```

The following wording may refer to a Bayesian information criterion score, so a human should review the result.

```text
bic validation
```

The following wording may refer to a nonexistent version field, so a human should review the result.

```text
validate bic version
```

A constructor with the option to allow invalid input does not count by itself; an instance method or property may count separately.

Bank-code lookup constructors do not count.

Component and lookup property reads do not count.

Compacting a value does not count.

Formatting a value does not count.

Account-number constructors do not count.

A regular expression match alone does not count.

An instance produced by another module or an untraced helper is missed.

A bare import does not count.

A roadmap claim still counts as a claim.

A changelog claim still counts as a claim.

A TODO claim still counts as a claim.

Denial paraphrases outside the list are missed.

A claim outside the selected documentation paths is missed.

Evidence split across modules is missed.

Locally shadowed route names do not count.

Dead code counts as evidence.

Subprocess calls do not count.

Generic input checks do not count.

Email checks do not count.

Phone checks do not count.

URL checks do not count.

IP address checks do not count.

Domain checks do not count.

ISBN checks do not count.

ISSN checks do not count.

IBAN checks do not count.

UUID checks do not count.

Semantic version checks do not count.

MAC address checks do not count.

Extraction calls do not count.

Locally defined generic names do not count.

Alias chains beyond direct imports can be missed.

Exact matching cannot infer meaning.

Implementations in other languages are missed.

Dynamically loaded routes are missed.
