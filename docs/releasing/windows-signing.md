# Windows Authenticode signing

A valid Windows-trusted code-signing identity is required. No signing identity was
configured in this repository at the audit checkpoint. A self-signed certificate does
not meet this requirement, and a signed executable can still receive a SmartScreen
reputation warning. Do not claim a warning-free or signed release from an unsigned build.

For an existing compatible PFX signing identity, configure these GitHub Actions secrets:

- `U1_WINDOWS_SIGNING_CERT_BASE64`: base64-encoded PFX with the signing key.
- `U1_WINDOWS_SIGNING_CERT_PASSWORD`: its password; never place either value in source,
  issues, tool output or chat.

Modern managed/hardware-backed signing services need their own provider integration;
no subscription, identity verification or credential is fabricated or purchased here.

`tools/u1/windows/sign-portable.ps1` imports a supplied identity into the hosted job's
user certificate store, signs the owned application binaries with SHA-256 and an RFC3161
timestamp, and verifies the Windows trust chain and timestamp. Temporary PFX material
and newly imported keys are removed. No certificate is added to a trusted-root store.
A configured but unusable identity fails the job; it never falls back to claiming success.

Without an identity, push-triggered runs can produce explicitly unsigned **test artifacts**.
The signing report says `not_configured`; portable verification independently reads the
actual executable signature. Manual release dispatch defaults `require_signature=true`,
so unsigned artifacts cannot pass that publication gate. Opting out must be a deliberate
operator dispatch, and any such release must remain clearly labeled unsigned/experimental.

The Windows preflight parses both signing and verification scripts. Syntax checks and
the unsigned path do not prove successful signing. A real signed build remains an external
release gate until an authorized identity is supplied and the trust checks pass.

Primary command reference: https://learn.microsoft.com/windows/win32/seccrypto/signtool
