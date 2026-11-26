"""Earned-pride line keeper: hold one quiet moment up to the light."""
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

SPAN = 240
STAGE = "u-mang-one-line-of-earned-pride-a0138557"


@dataclass
class Verdict:
    ok: bool = False
    span: int = 0
    body: str = ""
    trail: list = field(default_factory=list)

    def weigh(self, text):
        self.span = len(text)
        self.body = text
        if not text.strip():
            self.trail.append("hollow")
        elif self.span > SPAN:
            self.trail.append("too-wide")
        else:
            self.ok = True
            self.trail.append("holds-weight")

    def describe(self):
        return {"ok": self.ok, "span": self.span, "trail": self.trail, "stage": STAGE}


def consign(text):
    shelf = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    shelf_path = Path(shelf)
    shelf_path.mkdir(parents=True, exist_ok=True)
    kept = shelf_path / "entry.txt"
    kept.write_text(text + "\n", encoding="utf-8", newline="\n")
    return kept


def keep():
    nest = Path(__file__).resolve().parent
    draft = (nest / "entry.txt").read_text(encoding="utf-8").rstrip("\n")
    verdict = Verdict()
    verdict.weigh(draft)
    if not verdict.ok:
        print(json.dumps(verdict.describe()))
        sys.exit(6)
    consign(draft)
    print("KEPT", verdict.describe())


if __name__ == "__main__":
    keep()
