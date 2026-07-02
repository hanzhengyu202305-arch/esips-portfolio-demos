#!/usr/bin/env python
from __future__ import annotations

from agent.poc import create_scorecard


if __name__ == "__main__":
    result = create_scorecard()
    print(result.scorecard_path)
