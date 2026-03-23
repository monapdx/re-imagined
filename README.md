# re:imagined

**A human-centered styling language built around visible meaning, explicit refinement, and self-normalizing structure.**

## Overview

**re:imagined** is a tiny styling language concept that prioritizes readability over memorized positional shorthand.

**Its core ideas are:**

* **labels** define meaning, not **position**
* **shorthand** should match **natural human grouping**
* **refinement** must be **explicit**
* **dead information** should never survive
* the **written form** should always reflect the **current truth**

## Core Syntax

### Declaration

```txt
padding: v 10 h 16
corner-radius: t 12 b 6
```

### Refinement

```txt
padding: v 10 h 16
^ padding: l 20
```

### Visible normalization

```txt
padding: v 10 h 16
^ padding: l 20
```

**normalizes to:**

```txt
padding: v 10 l 20 r 16
```

## Labels

### Axes

* `v` = vertical (`top + bottom`)
* `h` = horizontal (`left + right`)

### Sides

* `t` = top
* `r` = right
* `b` = bottom
* `l` = left

### Corners

* `tl` = top-left
* `tr` = top-right
* `br` = bottom-right
* `bl` = bottom-left

## Rules

### 1. Labels over position

When labels are present, order does not matter.

```txt
padding: h 16 v 10
```

**means the same thing as:**

```txt
padding: v 10 h 16
```

### 2. No overlapping definitions

A single declaration cannot define the same underlying target twice.

**Invalid:**

```txt
padding: h 16 l 20
```

because `h` already includes `l`.

### 3. Natural grouping preferred

The language prefers the shortest form that is still clear.

**Preferred:**

```txt
padding: v 10 h 16
corner-radius: t 15 b 10
```

**Valid but less preferred:**

```txt
padding: t 10 r 16 b 10 l 16
```

### 4. Refinement must be explicit

A refinement uses `^`.

```txt
padding: v 10 h 16
^ padding: l 20
```

### 5. Refinement is visible

The source should update to the normalized result rather than keep stale history.

### 6. No dead information

If a grouped value no longer contributes meaning, it disappears.

```txt
padding: v 10 h 16
^ padding: l 20 r 25
```

**becomes:**

```txt
padding: v 10 l 20 r 25
```

### 7. Simplify only when clarity is preserved

**Good simplification:**

```txt
padding: t 10 r 10 b 10 l 10
```

**becomes:**

```txt
padding: 10
```

**Good simplification:**

```txt
padding: t 10 r 16 b 10 l 16
```

**becomes:**

```txt
padding: v 10 h 16
```

**Bad simplification:**

```txt
corner-radius: t 15 b 10
```

**should **not** become:**

```txt
corner-radius: 15 10
```

because that would hide meaning behind positional convention.

### 8. No mixed units inside values

**So this is invalid:**

```
padding: v 10px h 5%
```
Because a declaration cannot mix unit systems.

### 9. Units are declared separately and persist downward

So units behave like a current measurement context for the lines that follow.

**Example:**

```
unit: px
padding: v 10 h 16
corner-radius: t 12 b 6

unit: %
width: 50
height: 25
```
**This would mean:**

the first group uses px
then unit: % changes the default for everything after it

### 10. Interpretation rule

Every numeric value after that uses the current unit unless and until another unit declaration appears.

So:

```
unit: px
padding: v 10 h 16
^ padding: l 20
```

means all those numbers are in px.

**Then if later:**

```
unit: rem
padding: 2
```

that new padding is in rem.

### 11. Unit Context

A unit declaration establishes the active numeric unit for all following numeric declarations until another unit declaration overrides it.

**Example:**

```
unit: px
padding: v 10 h 16
corner-radius: t 12 b 6
```

```
unit: rem
padding: 2
```
### Unit Rules

- Numeric declarations MUST use the current active unit.
- Mixed units within a declaration are not allowed.
- A new unit declaration replaces the previous unit context for subsequent lines.
- Refinements inherit the active unit context of their position in the document.

- Units are declared separately
- A unit declaration stays in effect until another one appears later
- That means a property and its refinements should stay within one unit context

## Example Flow

```txt
padding: v 10 h 16
^ padding: l 20
^ padding: r 25
```

**Final visible result:**

```txt
padding: v 10 l 20 r 25
```

## Design Principles

* clarity over convention
* visible meaning over positional guessing
* explicit refinement over silent override
* normalization over dead history
* simplification when it helps, not when it obscures


