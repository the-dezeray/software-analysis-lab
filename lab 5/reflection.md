# Lab 5 - reflection

Question: what kinds of UI changes would I expect self-healing to handle well,
and what would still need a human fix?

## Handles well (I saw this in my run)

Renamed ids or classes where the meaning stays the same. I renamed `add-btn`
to `add-btn-v2` and I healed 6/6 at 0.95 because the button still says "Add"
and still has role=button. So if I rename an id, shuffle classes, or move an
XPath, my first fallback catches it as long as the text or role survives.
And because I put my locators in the POM, my one heal fixed all five tests
at once.

## Still needs me

Anything where the meaning itself changed. If I relabel "Add" to "Create",
split it into two buttons, or move it behind a dialog, my chain cannot know
which one I meant and it could click the wrong "Add". I got 0 wrong heals
here but only because my page is simple.

Timing and logic changes too. Healing only fixes *where* I click, not *when*
or *what*. My `?flaky=1` delay and any new validation rule still fail the
assert even if my locator heals.

And I still have to update the POM after. My primary `#add-btn` is still
broken and every heal (~1.5 s) is just a warning. If I never copy the healed
locator back, my chain will rot.

My rule: self-healing covers a rename, I have to fix it when the intent moved.
