from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
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
        "aliases": {},
    },
    "corner-radius": {
        "groups": {
            "t": {"tl", "tr"},
            "b": {"bl", "br"},
            "l": {"tl", "bl"},
            "r": {"tr", "br"},
        },
        "specific": {"tl", "tr", "br", "bl"},
        "aliases": {},
    },
}


@dataclass
class ParsedLine:
    refine: bool
    property_name: str
    raw_value: str


class ReImaginedParser:
    """Tiny prototype for the re:imagined styling language.

    Supported features:
    - declarations: property: value
    - refinements: ^ property: value
    - visible normalization to a canonical string
    - simplification when clarity is preserved

    Supported properties in this prototype:
    - padding
    - corner-radius
    """

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
            suggestions = self.suggest_property(property_name)
            if suggestions:
                raise ReImaginedError(
                    f"Unknown property '{property_name}'. Did you mean '{suggestions[0]}'?"
                )
            raise ReImaginedError(f"Unknown property '{property_name}'.")

        return ParsedLine(refine=refine, property_name=property_name, raw_value=raw_value)

    def apply(self, parsed: ParsedLine) -> str:
        config = PROPERTY_TARGETS[parsed.property_name]
        specific_targets = set(config["specific"])
        groups = config["groups"]

        parsed_assignments = self.parse_value(parsed.property_name, parsed.raw_value)

        if parsed.refine:
            if parsed.property_name not in self.state:
                raise ReImaginedError(
                    f"Cannot refine '{parsed.property_name}' before it has been declared."
                )
            current = dict(self.state[parsed.property_name])
            current.update(parsed_assignments)
            resolved = current
        else:
            resolved = parsed_assignments

        # Ensure complete property state
        if set(resolved.keys()) != specific_targets:
            missing = sorted(specific_targets - set(resolved.keys()))
            raise ReImaginedError(
                f"Property '{parsed.property_name}' is incomplete. Missing: {', '.join(missing)}."
            )

        self.state[parsed.property_name] = resolved
        return self.to_canonical(parsed.property_name, resolved)

    def parse_value(self, property_name: str, raw_value: str) -> Dict[str, int]:
        config = PROPERTY_TARGETS[property_name]
        groups = config["groups"]
        specific = set(config["specific"])

        tokens = raw_value.split()
        if not tokens:
            raise ReImaginedError(f"Missing value for '{property_name}'.")

        # Single-value shorthand only when unambiguous.
        if len(tokens) == 1:
            value = self.parse_int(tokens[0])
            return {target: value for target in specific}

        # Reject unlabeled positional shorthand in this prototype.
        if self.looks_like_all_numbers(tokens):
            raise ReImaginedError(
                f"Unlabeled multi-value shorthand is not allowed for '{property_name}' in this prototype. Use labels."
            )

        assignments: Dict[str, int] = {}
        i = 0
        while i < len(tokens):
            label = tokens[i]
            if i + 1 >= len(tokens):
                raise ReImaginedError(f"Missing numeric value after label '{label}'.")
            value = self.parse_int(tokens[i + 1])

            if label in groups:
                expanded = groups[label]
            elif label in specific:
                expanded = {label}
            else:
                raise ReImaginedError(
                    f"Unknown label '{label}' for property '{property_name}'."
                )

            overlap = expanded & set(assignments.keys())
            if overlap:
                raise ReImaginedError(
                    f"Overlapping definition in '{property_name}': label '{label}' conflicts with {', '.join(sorted(overlap))}."
                )

            for target in expanded:
                assignments[target] = value
            i += 2

        return assignments

    def to_canonical(self, property_name: str, resolved: Dict[str, int]) -> str:
        if property_name == "padding":
            return self.canonical_padding(resolved)
        if property_name == "corner-radius":
            return self.canonical_corner_radius(resolved)
        raise ReImaginedError(f"No canonicalizer for '{property_name}'.")

    def canonical_padding(self, resolved: Dict[str, int]) -> str:
        t, r, b, l = resolved["t"], resolved["r"], resolved["b"], resolved["l"]

        if t == r == b == l:
            return f"padding: {t}"

        if t == b and l == r:
            return f"padding: v {t} h {l}"

        parts: List[str] = []
        if t == b:
            parts.extend(["v", str(t)])
        else:
            parts.extend(["t", str(t), "b", str(b)])

        if l == r:
            parts.extend(["h", str(l)])
        else:
            parts.extend(["l", str(l), "r", str(r)])

        return "padding: " + " ".join(parts)

    def canonical_corner_radius(self, resolved: Dict[str, int]) -> str:
        tl, tr, br, bl = resolved["tl"], resolved["tr"], resolved["br"], resolved["bl"]

        if tl == tr == br == bl:
            return f"corner-radius: {tl}"

        if tl == tr and bl == br:
            return f"corner-radius: t {tl} b {bl}"

        if tl == bl and tr == br:
            return f"corner-radius: l {tl} r {tr}"

        parts = [
            "tl", str(tl),
            "tr", str(tr),
            "br", str(br),
            "bl", str(bl),
        ]
        return "corner-radius: " + " ".join(parts)

    @staticmethod
    def parse_int(token: str) -> int:
        if not re.fullmatch(r"-?\d+", token):
            raise ReImaginedError(f"Expected integer value, got '{token}'.")
        return int(token)

    @staticmethod
    def looks_like_all_numbers(tokens: List[str]) -> bool:
        return all(re.fullmatch(r"-?\d+", token) for token in tokens)

    @staticmethod
    def suggest_property(name: str) -> List[str]:
        possibilities = list(PROPERTY_TARGETS.keys())
        return [p for p in possibilities if p.startswith(name[:3])][:1]


def demo() -> None:
    parser = ReImaginedParser()

    source = """
    padding: v 10 h 16
    ^ padding: l 20
    ^ padding: r 25

    corner-radius: t 15 b 10
    ^ corner-radius: tl 20 tr 20
    """

    print("SOURCE:\n")
    print(source.strip())
    print("\nNORMALIZED OUTPUT:\n")

    outputs = parser.run(source)
    for property_name, canonical in outputs.items():
        print(canonical)


if __name__ == "__main__":
    demo()
