# AegisOps Environment Doctor

- project: `aegisops-agent`
- python_version: `3.14.0`
- platform: `macOS-26.5.2-arm64-arm-64bit-Mach-O`

| check | ok | detail |
| --- | ---: | --- |
| project_root | true | repository root contains Makefile and agent/ |
| pytest | true | importable |
| fastapi | true | importable |
| docker | true | /opt/homebrew/bin/docker |
| kind | false | missing; optional dry-run fallback is available |
| kubectl | false | missing; optional dry-run fallback is available |
