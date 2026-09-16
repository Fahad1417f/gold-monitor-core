# Source Cleanup Plan

The legacy GOLD-BOT repository is being reduced before migration.

## Preserve
- deterministic KFOO evidence/rules
- verified MTF candle pipeline
- verified H&S logic
- perception-only vision components
- regression tests

## Do not migrate into Core
- broker/exchange execution
- duplicate web servers
- duplicate launchers
- duplicate CI workflows
- auto-supervisor/self-healing
- Telegram device control
- multi-symbol opportunity scanner
- experimental deployment tooling

## Principle
One source of truth per responsibility. KFOO evidence is never silently replaced by a proxy. Execution stays OFF.
