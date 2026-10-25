# Reflection - visual diff vs accessibility scan

A pixel diff only answers one question: "did this page change compared with
the baseline?" It does not know what the pixels mean.

## Violations a pixel diff would never catch

- **Missing accessible names.** The priority `<select>` had no label. The
  pixel diff was perfectly happy because the control still looked the same.
  A screen-reader user would hear an unnamed combobox.
- **Low contrast.** The `#aaa` helper text and `#888` completed-task text were
  visually present. A pixel diff only notices contrast if the baseline was
  already different; it cannot say whether the current contrast meets WCAG.
- **Landmark and region structure.** The page had no `<main>` landmark. That
  is invisible to a pixel comparison, but it matters for keyboard and
  screen-reader navigation.
- **Semantic roles, focus order, ARIA state, and announcements.** These are
  not represented by pixels at all.

The important point is that a pixel diff compares against the baseline, not
against WCAG. If the baseline is already inaccessible, the visual test passes.
That is why the visual and accessibility scans answer different questions.

## Why both scans are justified

- **Visual regression** catches unintended layout, spacing, font, and styling
  changes. It protects the design contract from accidental edits.
- **Accessibility scanning** catches semantic and conformance problems even
  when the page looks unchanged.

In this lab the deliberate CSS change produced a 3.286% visual diff, while the
accessibility scan found four violations that a screenshot comparison would
not have reported as failures. Running both gives coverage of appearance and
meaning; neither tool can replace the other.
