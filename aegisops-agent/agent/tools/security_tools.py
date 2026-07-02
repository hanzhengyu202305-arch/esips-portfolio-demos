from __future__ import annotations


def has_non_root_security_context(text: str) -> bool:
    return "runAsNonRoot: true" in text and "allowPrivilegeEscalation: false" in text
