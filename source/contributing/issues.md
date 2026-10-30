# Report and find issues

## Find a good first issue

1. Open the
   [org-wide issue search](https://github.com/search?q=org%3ASideQuest-Guild+label%3A%22good+first+issue%22+is%3Aopen&type=issues).
2. Pick one that isn't already assigned.
3. Comment on it to say you're picking it up.

:::{note}
See the [contributing guide](guide.md) for how to set up a repo and open a pull request once you
have a fix.
:::

## Write a good bug report

A good bug report lets anyone reproduce the problem without asking you questions first.

1. Open an issue in the repo where the problem happens.
2. State what you expected and what happened instead, each in one sentence.
3. List the exact steps to reproduce it, numbered, starting from a clean state.
4. Add the repo's version or commit, and your OS or browser if it's relevant.
5. Attach a screenshot or error message if you have one.

:::{dropdown} Example
**Bad:** "The events page is broken."

**Good:**

> **Expected:** Selecting a kind tab (e.g. Raids) shows only raid events.
> **Actual:** Selecting Raids shows every event kind.
>
> **Steps:**
> 1. Go to <https://sidequest-guild.com/events/>.
> 2. Select the Raids tab.
> 3. The list still shows dungeons and leveling events.
>
> Chrome 130 on macOS.
:::

## Suggest a feature

1. Open an issue before writing code.
2. Describe the problem it solves, not just the feature itself.
3. Wait for an officer to agree on the approach.

## Security problems

Don't open a public issue for a security problem. Follow the repo's `SECURITY.md` instead.
