# AegisOps Environment Doctor

- project: `aegisops-agent`
- python_version: `3.13.9`
- platform: `macOS-26.5.2-arm64-arm-64bit-Mach-O`

| check | ok | detail |
| --- | ---: | --- |
| project_root | true | /Users/hanzhengyu/Documents/industry/aegisops-agent |
| pytest | true | importable |
| fastapi | false | not importable: No module named 'fastapi' |
| docker | true | /opt/homebrew/bin/docker |
| kind | false | missing; optional dry-run fallback is available |
| kubectl | false | missing; optional dry-run fallback is available |
