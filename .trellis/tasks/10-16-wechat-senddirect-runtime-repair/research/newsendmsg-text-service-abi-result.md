# Text service returned value ABI — implementation78

## Native boundary established

Frozen0x317ded4 accepts x0=service and x1=address of an input shared pair, retains a local input copy, and forwards to0x317df64 with w2=1. The caller's hidden x8 return storage is preserved.0x317df64 saves x8, constructs/queues its context, then passes the context+0x70 shared future to0x3189980 with the original result address in x8.

0x3189980 retains that future pair, calls0x66856fc, and obtains a typed value through0x312bae8. The new read-only pass422 has156 bytes/39 instructions and no script error. Its exact expected RTTI name is `_5678d644\0` at0x88bc000+0xe2; name comparison masks the high pointer bit. It returns the erased holder's value+8 or throws. This name identifies the outer value type, not the meaning of the shared payload inside it.

The returned nontrivial value is **0x30 bytes**, not a16-byte future:

| Offset | Verified representation |
|---|---|
| +0/+4 | Two32-bit words; selected caller requires both zero for its success branch |
| +8 |24-byte libc++ string, short representation copy or0x18d20 heap copy |
| +0x20/+0x28 | Shared pointer/control pair; source control+8 incremented during copy |

The selected caller uses result base sp+0x310, tests words at+0/+4, consumes the pointer at sp+0x330, and finally releases control at sp+0x338 and the heap string indicated by sp+0x32f. This corroborates the owned result layout. `newsendmsg_text_service_abi_4115.hpp` declares that layout, its nontrivial destructor, and the two-argument function pointer. The shared payload stays opaque and the words use positional names; no unproved business schema or receipt meaning is generated.

## Host verification

`text-service-abi-20261018/verification.json` records strict Apple ARM64 C++17 and UBSan builds, each passing7 scenarios with no stderr: exact x0/x1/x8 plus48-byte guard bounds, owned return retaining input, nonzero status with owned data, result copy/move and independent string storage, exception cleanup after allocation, zero status with absent payload, and safe empty destruction. Assembly-backed prvalue construction writes directly into the expected return slot. Fixture input/value objects are owned host tags; they do not impersonate native payloads or invoke WeChat.

Seven frozen exports match1629 instructions;58 sites,10 independently decoded BLs and the exact RTTI literal are checked. The33 source hashes from implementation77 are revalidated before the new checks. ASan remains unavailable based on the prior minimal probe; it was not repeated and is not claimed to pass. Both verification scripts pass Ruff.

## Practical consequence and remaining work

The service wrapper itself waits in0x3189980→0x66856fc→0x6674d5c, whose selected entry reads coroutine TLS descriptor0xa24de80. This confirms that even direct typed input submission still requires a legitimate coroutine context; avoiding the high-level recipient lookup does not make a plain executor callback safe. The async pair passed to the wait helper is still x0; this helper is not a no-argument current-coroutine getter.

This closes the return ABI declaration/host ownership component only. Complete target ABI execution, source/recipient/content preservation through record changes, a proven launch/cancel/shutdown lifecycle, full integrated native adapter, actual send with independent receipt and deployment remain open. No WeChat attachment, loading, invocation, UI operation, sending, installation, Git or archival occurred. Account safety stop and product refusal remain in force; A7 and11/18/20–24/55/67 stay unchecked.
