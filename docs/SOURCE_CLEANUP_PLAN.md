# Source Cleanup Plan

The legacy GOLD-BOT repository is being reduced before migration.

## Preserve

- deterministic KFOO evidence/rules
- verified MTF candle pipeline
- verified H&S logic
- perception-only vision components
- regression tests
- risk/reward (R:R) calculation and validation

## Do not migrate into Core

- broker/exchange execution
- duplicate web servers
- duplicate launchers
- duplicate CI workflows
- auto-supervisor/self-modifying runtime
- Telegram device control
- multi-symbol opportunity scanner as a core dependency
- experimental deployment tooling

## Core risk model

R:R is a first-class, market-agnostic output of the signal pipeline:

- entry price
- stop-loss price
- target price
- stop distance
- reward distance
- R:R ratio

The system must fail closed when the stop distance is missing, zero, negative, or otherwise invalid. R:R must never be fabricated from a default value.

## Principle

One source of truth per responsibility. KFOO evidence is never silently replaced by a proxy. Execution stays OFF.
