# Owned text input component — implementation77

## Implemented boundary

`newsendmsg_text_input_4115.hpp` now constructs and owns the factory-created input used by the frozen numeric-one route. It accepts injected factory/string-assignment functions and a separately established expected payload vtable. It rejects missing functions/identity, empty inputs, missing ownership, a different vtable, nonzero numeric fields or nonempty initial strings. It copies the original chat_id to payload+0x90 and exact content bytes to payload+0x5c8. Low type+0xe4 becomes1 only after both assignments complete; high type+0xe8 stays0. This last-write policy is an owned-construction choice: the native builder writes type1 before copying strings.

Factory output is retained immediately. A failed check or assignment unwinds the shared owner, including partially modified strings. Exposed shared ownership permits a consumer to retain the input after this wrapper leaves scope. Other constructor defaults are preserved. There is no loader, address binding, scheduler, coroutine, service invocation, protocol rewriting or product connection.

## Current verification

`text-input-owner-qualified-20261018-v2/verification.json` records two real Apple ARM64 builds: strict C++17 with warnings as errors, and UndefinedBehaviorSanitizer with recovery disabled. Both exited0 with no stderr and passed the same21 assertions/scenarios:

- Hidden x8 storage for the nontrivial16-byte shared return.
- Five body inputs: Unicode/newline, long text, brand_account-shaped text, emoticon/CDATA/CRLF/quotes, embedded NUL.
- Three missing-function/identity rejections and two empty-input rejections before allocation.
- Seven failed/stale factory results, two assignment exceptions after mutation, and one retained-owner/caller-mutation scenario.
- Guard regions and created/destroyed counts are asserted across the ownership scenarios. These are host fixture assertions, not observations of target cleanup.

Four frozen exports match1998 instructions. Thirty exact sites and seven independently decoded BLs establish the selected factory/result, constructor, zero initialization and numeric-one assignments. The0x713f8e0 stub is independently decoded to chained bind slot0x9b36500, ordinal1183, exact import `__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_`. Thirty-three source hashes bind the component, fixture, verifier, frozen exports/logs and stop record. Ruff passed.

## Preserved failed sanitizer attempt

The first strict build also passed21 cases in `text-input-owner-20261018/`. The first qualification attempt retained its strict pass and ASan+UBSan build under `text-input-owner-qualified-20261018/`, but the sanitized executable produced no output and timed out after15 seconds. A separate ASan-only minimal executable did not reach its first main write within5 seconds. Both timeout children were terminated and reaped by subprocess.run. The failed verifier source and all diagnostics are preserved. This supports an unavailable host ASan probe, not a passed ASan/leak check or proof of a component defect.

## Remaining requirements

This closes implementation77's owned component and host ABI check only. Target allocator/control-block compatibility is unexecuted. Direct copying without category parsing here does not prove arbitrary text preservation through final record replacement/network serialization. Complete service prerequisites, the actual coroutine and service lifetime, cancellation ordering/final drain, a complete integrated native adapter, real sending and an independent receipt remain open. A7 and11/18/20–24/55/67 stay unchecked. Account safety stop remains authoritative; no WeChat operation, new attachment request, installation, Git or archival occurred.
