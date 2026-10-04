# Reflection / Discussion — Lab 5 Self-Healing Locators

*What kinds of UI changes would you expect self-healing locators to handle well, and what kinds
would still require a human fix?*

## Handles well (seen in this lab)

- **Renamed ids / classes with stable semantics.** Our drift (`add-btn` → `add-btn-v2`) healed at
  confidence 0.95 because the button's accessible role+name ("Add") never changed. Any cosmetic
  re-identification — renamed id, reshuffled CSS classes, moved XPath position — heals as long as
  *some* independent signal (role, text, test-id, neighbouring label) survives. Our chain only
  needed its first fallback in all 6/6 heals.
- **Duplicate-signal drift.** Because the POM centralises locators, one healed fallback repairs all
  five tests at once — healing scales with POM discipline and degrades without it.

## Still requires a human

- **Semantic changes.** If "Add" is relabelled "Create", split into two buttons, or moved behind a
  dialog/permission gate, no fallback chain can know which element the test *meant* — the role+name
  fallback would miss and the text fallback could latch onto the wrong "Add" (e.g. "Add tag").
  That is the wrong-element risk the healing table monitors (0 observed here, but the column exists
  for exactly this reason); only a human can re-anchor intent, usually by adding a `data-testid`.
- **Behavioural / timing changes.** Healing fixes *where*, not *when* or *what*: a new async delay,
  a reordered workflow, or a changed validation rule (e.g. empty titles now accepted) passes the
  locator but fails the assertion. Our `?flaky=1` hook shows the counterpart — web-first
  auto-waiting covers timing, but changed app semantics always need a test update.
- **Healing debt.** Every heal (~1.5 s here) is a warning, not a fix: the primary `#add-btn` is
  still broken in the POM. If heals are never promoted back into the page object, chains rot and
  confidence decays down to brittle XPath. Treat the healing log as a maintenance backlog.

**Rule of thumb:** self-healing covers *re-identification* of an unchanged intent; humans are
required whenever the intent itself moved, multiplied, or disappeared.
