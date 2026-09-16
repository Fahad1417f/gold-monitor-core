# Legacy Migration Matrix

| Capability | GOLD-BOT V56 | KFOO Signal Monitor | New Core treatment |
|---|---|---|---|
| TradingView live vision | Legacy/fragile | Limited/indirect | Isolated adapter |
| KFOO table evidence | Dedicated components | Proxy/limited | Evidence adapter |
| Whales evidence | Dedicated logic | Proxy/limited | Evidence adapter |
| Multi-timeframe context | Strong | Good | Core contract |
| 3M entry timing | Strong | Strong | Core contract |
| H&S confirmation | Detailed | More generic | Structure module |
| Market-data proxy | Secondary | Strong | Research-only source |
| Signal outcomes | Good | Strong | Unified outcome store |
| Dashboard | Limited | Strong | Separate UI layer |
| Broker execution | Present in legacy experiments | Not required | Excluded from core |

## Migration rule

Every migrated module must have a bounded responsibility, explicit source contract, tests, and a safety review. Preserve behavior only when it matches the new source-boundary rules.
