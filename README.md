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

normalizes to:

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

means the same thing as:

```txt
padding: v 10 h 16
```

### 2. No overlapping definitions

A single declaration cannot define the same underlying target twice.

Invalid:

```txt
padding: h 16 l 20
```

because `h` already includes `l`.

### 3. Natural grouping preferred

The language prefers the shortest form that is still clear.

Preferred:

```txt
padding: v 10 h 16
corner-radius: t 15 b 10
```

Valid but less preferred:

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

becomes:

```txt
padding: v 10 l 20 r 25
```

### 7. Simplify only when clarity is preserved

Good simplification:

```txt
padding: t 10 r 10 b 10 l 10
```

becomes:

```txt
padding: 10
```

Good simplification:

```txt
padding: t 10 r 16 b 10 l 16
```

becomes:

```txt
padding: v 10 h 16
```

Bad simplification:

```txt
corner-radius: t 15 b 10
```

should **not** become:

```txt
corner-radius: 15 10
```

because that would hide meaning behind positional convention.

## Example Flow

```txt
padding: v 10 h 16
^ padding: l 20
^ padding: r 25
```

Final visible result:

```txt
padding: v 10 l 20 r 25
```

## Design Principles

* clarity over convention
* visible meaning over positional guessing
* explicit refinement over silent override
* normalization over dead history
* simplification when it helps, not when it obscures


