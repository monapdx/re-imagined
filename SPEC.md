# re:imagined — SPEC v1

A formal specification for the **re:imagined** styling language.

---

## 1. Scope

**This specification defines:**

* syntax
* value model
* labeling system
* refinement behavior
* normalization rules
* simplification rules
* error handling

---

## 2. Syntax

### 2.1 Declaration

A **declaration** assigns a value to a **property**.

```
<property>: <value>
```

**Example:**

```
padding: v 10 h 16
```

---

### 2.2 Refinement

A **refinement** modifies the most recent declaration of the same property.

```
^ <property>: <value>
```

**Example:**

```
padding: v 10 h 16
^ padding: l 20
```

---

## 3. Value Model

A **value** consists of **labeled** or unlabeled components.

### 3.1 Labeled values

```
<label> <number>
```

**Example:**

```
v 10
h 16
l 20
```

---

### 3.2 Unlabeled values

Allowed only when meaning is unambiguous and does not rely on positional conventions.

**Example:**

```
padding: 10
```

---

## 4. Labels

### 4.1 Axes

* v → vertical (top + bottom)
* h → horizontal (left + right)

### 4.2 Sides

* t → top
* r → right
* b → bottom
* l → left

### 4.3 Corners

* tl → top-left
* tr → top-right
* br → bottom-right
* bl → bottom-left

---

## 5. Order Independence

When labels are present, order **MUST NOT** affect meaning.

```
padding: h 16 v 10
```

**is equivalent to:**

```
padding: v 10 h 16
```

---

## 6. Overlap Rules

### 6.1 Within a single declaration

A declaration **MUST NOT** define overlapping targets.

**Invalid:**

```
padding: h 16 l 20
```

**because `h` includes `l`.**

---

### 6.2 Across refinement

Overlap is allowed only when using **refinement (`^`)**, and MUST be resolved through **normalization**.

---

## 7. Refinement Semantics

### 7.1 Target

A refinement applies to the most recent declaration of the same property.

### 7.2 Validity

Refinement **MUST** reference a previously declared property.

**Invalid:**

```
^ padding: l 20
```

---

## 8. Normalization

### 8.1 Definition

Normalization is the process of resolving declarations and refinements into a single canonical form.

### 8.2 Requirements

Normalization **MUST:**

* eliminate overridden values
* remove redundant groupings
* preserve all active meaning
* produce a non-conflicting representation

---

### 8.3 Example

**Input:**

```
padding: v 10 h 16
^ padding: l 20
```

**Normalized output:**

```
padding: v 10 l 20 r 16
```

---

### 8.4 Dead Information

Values that no longer contribute meaning **MUST** be removed.

---

## 9. Simplification

### 9.1 Definition

Simplification reduces a normalized declaration to a shorter equivalent form when clarity is preserved.

---

### 9.2 Allowed Simplifications

```
padding: t 10 r 10 b 10 l 10
→ padding: 10
```

```
padding: t 10 r 16 b 10 l 16
→ padding: v 10 h 16
```

---

### 9.3 Disallowed Simplifications

Simplification **MUST NOT** introduce positional ambiguity.

```
corner-radius: t 12 b 6
```

**MUST NOT become:**

```
corner-radius: 12 6
```

---

## 10. Natural Groupings

The language **SHOULD** support groupings that reflect common usage patterns.

**Examples:**

```
padding: v 10 h 16
corner-radius: t 12 b 6
```

Multiple valid groupings **MAY** exist for a property.

---

## 11. Error Handling

### 11.1 Minor Errors

**SHOULD** produce helpful suggestions.

### 11.2 Conflicts

**MUST** produce errors.

**Example:**

```
padding: h 16 l 20
```

---

### 11.3 Nonsense

**MUST** be rejected.

---

## 12. Evaluation Model

The language is **state-based**.

Only the final normalized form represents meaning.

Intermediate states and refinements are not preserved.

---

## 13. Canonical Representation

The canonical form of a property:

* contains no overlap
* contains no dead values
* uses the shortest clear representation

---

## 14. Summary of Guarantees

**re:imagined guarantees:**

* no hidden overrides
* no positional ambiguity
* no dead information
* consistent interpretation regardless of order
* explicit refinement behavior

---

## 15. Future Extensions (Non-Normative)

Possible areas for extension:

* layout systems
* alignment and positioning
* color and typography rules
* unit handling (px, %, etc.)

---

End of SPEC v1
