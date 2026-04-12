# APPROACHES.md

This document captures the key design decisions, edge cases, and reasoning behind the **re:imagined** language.

---

# Core Philosophy

- Meaning must be visible, not implied
- No positional shorthand
- No dead information
- Explicit refinement
- State-based model
- Visible normalization

---

# Key Decisions

## Shorthand
- ❌ `padding: 10 20`
- ✔ `padding: v 10 h 20`

## Order
- Order does not matter when labels exist

## Overlap
- ❌ `padding: h 16 l 20` → error

## Refinement
- `^` used for updates
- Can initialize in new unit context

## Normalization
- Always visible
- Removes dead values

## Units
- Declared with `unit:`
- Persist until changed
- Reset state on change
- Cannot mix

## Initialization after unit change
- ✔ `^ padding: v 1 h 2`
- ❌ `^ padding: 1 2` (unlabeled)

## Completeness
- All properties must resolve fully
- ❌ partial definitions

---

# Final Model

- label-driven
- context-aware
- state-based
- self-normalizing
- explicit
- non-positional
