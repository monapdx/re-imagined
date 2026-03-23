from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import re


class ReImaginedError(Exception):
    pass


PROPERTY_TARGETS = {
    "padding": {
        "groups": {
            "v": {"t", "b"},
            "h": {"l", "r"},
        },
        "specific": {"t", "r", "b", "l"},
    },
    "corner-radius": {
        "groups": {
            "t": {"tl", "tr"},
            "b": {"bl", "br"},
            "l": {"tl", "bl"},
            "r": {"tr", "br"},
        },
        "specific": {"tl", "tr", "br", "bl"},
    },
}


@dataclass
class ParsedLine:
    refine: bool
    property_name: str
    raw_value: str


class ReImaginedParser:
    def __init__(self) -> None:
        self.state: Dict[str, Dict[str, int]] = {}

    def run(self, text: str) -> Dict[str, str]:
        outputs: Dict[str, str] = {}
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parsed = self.parse_line(line)
            canonical = self.apply(parsed)
            outputs[parsed.property_name] = canonical

        return outputs

    def parse_line(self, line: str) -> ParsedLine:
        refine = False
        if line.startswith("^"):
            refine = True
            line = line[1:].strip()

        match = re.fullmatch(r"([a-z\-]+)\s*:\s*(.+)", line)
        if not match:
            raise ReImaginedError(f"Invalid syntax: {line}")

        property_name, raw_value = match.groups()

        if property_name not in PROPERTY_TARGETS:
            raise ReImaginedError(f"Unknown property '{property_name}'.")

        return ParsedLine(refine, property_name, raw_value)

    def apply(self, parsed: ParsedLine) -> str:
        config = PROPERTY_TARGETS[parsed.property_name]
        specific_targets = config["specific"]

        assignments = self.parse_value(parsed.property_name, parsed.raw_value)

        if parsed.refine:
            if parsed.property_name not in self.state:
                raise ReImaginedError(
                    f"Cannot refine '{parsed.property_name}' before declaration."
                )
            current = dict(self.state[parsed.property_name])
            current.update(assignments)
            resolved = current
        else:
            resolved = assignments

        if set(resolved.keys()) != specific_targets:
            missing = specific_targets - set(resolved.keys())
            raise ReImaginedError(
                f"Incomplete '{parsed.property_name}', missing: {missing}"
            )

        self.state[parsed.property_name] = resolved
        return self.to_canonical(parsed.property_name, resolved)

    def parse_value(self, property_name: str, raw_value: str) -> Dict[str, int]:
        config = PROPERTY_TARGETS[property_name]
        groups = config["groups"]
        specific = config["specific"]

        tokens = raw_value.split()

        if len(tokens) == 1:
            value = int(tokens[0])
            return {t: value for t in specific}

        if all(token.isdigit() for token in tokens):
            raise ReImaginedError("Unlabeled multi-value shorthand not allowed.")

        assignments: Dict[str, int] = {}

        i = 0
        while i < len(tokens):
            label = tokens[i]
            value = int(tokens[i + 1])

            if label in groups:
                targets = groups[label]
            elif label in specific:
                targets = {label}
            else:
                raise ReImaginedError(f"Unknown label '{label}'")

            overlap = set(assignments.keys()) & targets
            if overlap:
                raise ReImaginedError(f"Overlap detected: {overlap}")

            for t in targets:
                assignments[t] = value

            i += 2

        return assignments

    def to_canonical(self, property_name: str, resolved: Dict[str, int]) -> str:
        if property_name == "padding":
            return self.canonical_padding(resolved)
        if property_name == "corner-radius":
            return self.canonical_corner(resolved)

        raise ReImaginedError("No canonical form.")

    def canonical_padding(self, r: Dict[str, int]) -> str:
        t, rgt, b, l = r["t"], r["r"], r["b"], r["l"]

        if t == rgt == b == l:
            return f"padding: {t}"

        if t == b and l == rgt:
            return f"padding: v {t} h {l}"

        parts = []

        if t == b:
            parts += ["v", str(t)]
        else:
            parts += ["t", str(t), "b", str(b)]

        if l == rgt:
            parts += ["h", str(l)]
        else:
            parts += ["l", str(l), "r", str(rgt)]

        return "padding: " + " ".join(parts)

    def canonical_corner(self, r: Dict[str, int]) -> str:
        tl, tr, br, bl = r["tl"], r["tr"], r["br"], r["bl"]

        if tl == tr == br == bl:
            return f"corner-radius: {tl}"

        if tl == tr and bl == br:
            return f"corner-radius: t {tl} b {bl}"

        if tl == bl and tr == br:
            return f"corner-radius: l {tl} r {tr}"

        return f"corner-radius: tl {tl} tr {tr} br {br} bl {bl}"


# --- demo ---
if __name__ == "__main__":
    parser = ReImaginedParser()

    code = """
    padding: v 10 h 16
    ^ padding: l 20
    ^ padding: r 25

    corner-radius: t 15 b 10
    ^ corner-radius: tl 20 tr 20
    """

    result = parser.run(code)

    print("\n--- OUTPUT ---\n")
    for line in result.values():
        print(line)
