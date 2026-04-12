# APPROACHES.md

This document captures the **exact scenarios, edge cases, and decision points** explored while designing the re:imagined language, along with the chosen responses.

---

# 1. Shorthand vs Explicit Meaning

### Scenario
Should shorthand rely on positional meaning?

Example:
padding: 10 20

### Response
❌ Not allowed

### Reasoning
Values are not attached to directions → ambiguous.

### Accepted
padding: v 10 h 20

---

# 2. Ambiguity vs Clarity

### Scenario
Should ambiguous language be allowed?

Example:
"They saw her duck"

### Response
✔ Allowed, but clarity tools should exist

---

# 3. Grammar Strictness

### Scenario
Should imperfect grammar be allowed?

Example:
"Me go to store yesterday"

### Response
✔ Correct form preferred  
✔ Imperfect form tolerated but discouraged

---

# 4. Word Creation

### Scenario
Can users create new words?

### Response
✔ Allowed with conventions  
❌ Arbitrary combinations discouraged

---

# 5. Context Dependence

### Scenario
Should meaning rely on context?

### Response
✔ Yes, context is valid

---

# 6. Order vs Labels

### Scenario
Does order matter?

Example:
padding: h 16 v 10

### Response
✔ Order does not matter if labels exist

---

# 7. Positional Systems

### Scenario
Use clockwise positional shorthand?

### Response
❌ Rejected

### Reason
Requires memorization

---

# 8. Implicit Pairing

### Scenario
padding: 10 16

### Response
❌ Not allowed

### Reason
Second value has no explicit meaning

---

# 9. Label Redundancy

### Scenario
padding-sides: v 10 h 16

### Response
❌ Redundant

### Preferred
padding: v 10 h 16

---

# 10. Overlapping Definitions

### Scenario
padding: h 16 l 20

### Response
❌ Error

---

# 11. Refinement Operator

### Scenario
How should updates be expressed?

### Response
✔ Use ^

Example:
^ padding: l 20

---

# 12. Refinement Behavior

### Scenario
What does ^ mean?

### Response
✔ Adjust existing state

---

# 13. Dead Information

### Scenario
Original values become unused

### Response
❌ Not allowed

---

# 14. Normalization

### Scenario
How to handle layered updates?

### Response
✔ Normalize to clean final form

---

# 15. Visible vs Hidden Normalization

### Scenario
Should normalization be visible?

### Response
✔ Visible

---

# 16. Simplification

### Scenario
Should output be simplified?

### Response
✔ Yes, when clarity improves  
❌ No if meaning is hidden

---

# 17. Units

### Scenario
How should units work?

### Response
- Defined separately using unit:
- Persist until changed
- Cannot mix

---

# 18. Unit Reset

### Scenario
What happens when unit changes?

### Response
✔ Resets all previous numeric state

---

# 19. Refinement After Unit Change

### Scenario
Can refinement follow a unit change?

### Response
✔ Yes

### Interpretation
Acts within new context, not previous

---

# 20. ^ as Initialization

### Scenario
Can ^ define a property?

Example:
unit: rem
^ padding: v 1 h 2

### Response
✔ Yes

---

# 21. Incomplete Definitions

### Scenario
^ padding: l 2

### Response
❌ Not allowed

---

# 22. Unlabeled Multi-Values

### Scenario
padding: 1 2

### Response
❌ Not allowed

---

# 23. Single Unlabeled Value

### Scenario
padding: 10

### Response
✔ Allowed (uniform only)

---

# Final Model

- Meaning must be explicit
- No positional assumptions
- No dead info
- State-based system
- Context-driven via unit:
- Visible normalization
- Labels define everything
