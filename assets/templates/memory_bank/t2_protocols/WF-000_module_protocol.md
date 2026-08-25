# WF-000 Module Protocol

## Inputs

- Approved change scope.
- Current T0, T1, and support-map state.

## Procedure

1. Validate governing inputs.
2. Perform the bounded change.
3. Re-run the module validation.
4. Record historical evidence under the module archive root.

## Stop Conditions

Stop when an identity, validation, or directly consumed safety result fails.

## Evidence

Store the result under `memory_bank/t3_archives/example-module/`.
