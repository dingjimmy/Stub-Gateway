---
mode: agent
description: Create or amend a Gherkin .spec file for a single capability area, following Specification by Example. Each rule is one piece of business logic; each example is a concrete scenario that illustrates it. Companion to /create-requirements in the Agent-First workflow.
---

# Create Spec

You are helping the user produce a **`specs/<slug>.spec`** file — the second artefact in the Agent-First / Agent-Enhanced development workflow. Each spec captures one capability area from `docs/requirements.md` as executable Gherkin: a `Feature`, a set of `Rule`s, and concrete `Example`s that demonstrate each rule.

This file is the canonical source of acceptance behaviour. Tests, implementation, and review all derive from it.

## Inputs you need from the user

Before generating the file, make sure you have:

1. **The capability area** — a name and slug, ideally one already listed in `docs/requirements.md`. If `docs/requirements.md` exists, prefer reading the capability summary directly from there.
2. **Behavioural details** — the rules of business logic for this capability and concrete examples of each. These can come from the user, from the requirements document, or from a discussion you facilitate.
3. **Domain vocabulary** — the nouns and verbs used by the user/product/test stakeholders. Reuse terms already established in `docs/requirements.md` if it exists.

If any of these are missing or ambiguous, **ask the user before writing the file**. Prefer one focused question at a time. Keep asking until you can write each rule and example faithfully — do not guess to fill gaps.

### When to ask clarifying questions

Ask the user (do not assume) whenever any of the following is true:

- A rule is stated abstractly with no concrete example — ask for one.
- Two rules overlap, contradict, or are really the same rule restated.
- A rule mixes multiple pieces of business logic — ask which to split out.
- An example does not clearly demonstrate exactly one rule.
- An example's expected outcome is ambiguous, conditional, or non-deterministic.
- A requirement names a specific technology, data shape, or transport — confirm the underlying *behavioural* need before restating it.
- An edge case is implied (empty input, boundary value, repeated action, failure path) but no example is given.
- The user requests "comprehensive coverage" — confirm which edge cases matter; do not invent them.

If you proceed despite remaining uncertainty, surface every such decision back to the user after writing the file (see *Process*, step 5).

## Hard rules for the output

The generated `.spec` file **must**:

- Be valid Gherkin: a single `Feature:` line, one or more `Rule:` blocks, and one or more `Example:` blocks under each rule. (Use `Example:` rather than `Scenario:` to align with Gherkin 6+ Rule/Example syntax.)
- Use **domain language** shared with the user, product, and test stakeholders. Reuse terminology from `docs/requirements.md` verbatim where it applies.
- Describe **observable behaviour** — Given/When/Then must reference what an external observer (a user, a client, an operator, a test) can see or do. Never reference internal state, classes, modules, or implementation steps.
- Be **technology-agnostic** in wording wherever the requirement is. Concrete protocol details (HTTP status codes, JSON bodies, URLs, header names) are acceptable *only* when they are themselves the externally observable contract — not as an implementation hint. If unsure, prefer domain wording (e.g. "the order is rejected" rather than "returns 400").
- Treat each `Rule:` as **one** piece of business logic. If a rule needs the word "and" to describe two distinct behaviours, split it into two rules.
- Give each rule **at least one concrete `Example:`** (Specification by Example). Prefer two or three when the rule has meaningful variation, boundary conditions, or both positive and negative cases.
- Make every example **self-contained and concrete**: real names, real values, real timestamps, real quantities. Avoid placeholders like `<value>` or "some input".
- Use **Scenario Outlines or Examples tables** only when the variation is genuinely tabular and each row exercises the same behaviour with different data. Otherwise prefer separate `Example:` blocks for clarity.
- Match the `Feature` line to the capability's row in the `docs/requirements.md` Spec file index (the *Feature* column phrasing).

The generated `.spec` file **must not**:

- Contain multiple `Feature:` declarations.
- Mix rules from different capability areas — one capability per spec file.
- Include rules without examples, or examples that don't tie to a stated rule.
- Reference internal implementation: function names, database tables, class hierarchies, frameworks, file paths, design patterns, etc.
- Invent rules or examples the user did not state, imply, or confirm. If you spot a missing case, **ask** rather than fabricate.
- Include task lists, acceptance-criteria checkboxes, owners, or status. The file is pure Gherkin.

## Required structure

Produce the file at `specs/<slug>.spec` with this shape:

```gherkin
Feature: <one-line user-facing phrasing of the capability>

  Rule: <one piece of business logic, stated as an invariant or behaviour>

    Example: <short, distinguishing title>
      Given <observable starting context>
      And <additional context if needed>
      When <observable action by an external actor>
      Then <observable outcome>
      And <additional outcome if needed>

    Example: <another title illustrating the same rule with different data or a boundary>
      Given ...
      When ...
      Then ...

  Rule: <next piece of business logic>

    Example: ...
```

Conventions:

- **Two-space indentation** at each nesting level (`Rule:` indented two spaces under `Feature:`, `Example:` indented two spaces under `Rule:`, steps indented two spaces under `Example:`).
- **Blank line** between rules and between examples.
- **No trailing whitespace** and end the file with a single newline.
- **Background**: only use a `Background:` block (placed once, before the first rule) if every rule genuinely shares the same setup. When in doubt, repeat setup in each example — duplication is better than coupling unrelated rules.

## Slug and Feature line rules

- The file lives at `specs/<slug>.spec`. The slug is **kebab-case**, must match the slug used in `docs/requirements.md`, and must not be re-slugged without explicit user request (specs are referenced by slug from the requirements document).
- The `Feature:` line should read as a one-line, user-facing phrasing of what this capability lets someone do — typically the same wording as the `Feature` column in the Spec file index of `docs/requirements.md`.

## Reference template

Use the template below as the structural and tonal model. It is illustrative only — replace every placeholder with content derived from the user's input. Do **not** copy its domain (a fictional "Order Tracker" service) into the user's document.

````gherkin
Feature: Move orders through fulfilment statuses

  Rule: Orders progress through a fixed sequence of statuses

    Example: A new order starts as received
      Given an operator records an order for customer "Alice Brown" with one line item
      Then the order's status is "received"

    Example: An order advances one step at a time
      Given an order in status "received"
      When the operator marks it as "picked"
      Then the order's status is "picked"
      When the operator marks it as "packed"
      Then the order's status is "packed"

  Rule: Only forward transitions between adjacent statuses are allowed

    Example: Skipping a status is rejected
      Given an order in status "received"
      When the operator tries to mark it as "shipped"
      Then the change is rejected
      And the operator sees a message that the order must be picked and packed first
      And the order's status is still "received"

    Example: Going backwards is rejected
      Given an order in status "packed"
      When the operator tries to mark it as "received"
      Then the change is rejected
      And the order's status is still "packed"

  Rule: Each status change records the time it happened

    Example: The last-updated time advances on each transition
      Given an order in status "received" last updated at 10:00
      When the operator marks it as "picked" at 10:05
      Then the order's status is "picked"
      And the order's last-updated time is 10:05

  Rule: Shipped orders are final

    Example: A shipped order cannot be advanced further
      Given an order in status "shipped"
      When the operator tries to mark it as any other status
      Then the change is rejected
      And the order's status is still "shipped"
````

Notice:

- Each `Rule:` is a single, atomic invariant.
- Every rule has at least one `Example:` with concrete, named data ("Alice Brown", "10:05", real status names).
- Outcomes are stated in domain terms ("the change is rejected", "the order's status is …"), not in protocol or framework terms.
- Negative paths get their own examples rather than being bolted onto a positive example.

## Amendment mode

If `specs/<slug>.spec` already exists, you are **amending**, not authoring from scratch. Treat the existing file as the source of truth and make the smallest faithful change.

### Detect the user's intent

Determine which of these the user wants (ask if unclear):

- **Add a rule** — a new piece of business logic (with at least one example).
- **Add an example** — illustrate an existing rule with another concrete case (e.g. a new edge case or boundary).
- **Change** wording or data of an existing rule or example.
- **Split** a rule that has grown to cover more than one piece of logic.
- **Merge** two rules that turn out to be the same logic.
- **Deprecate** a rule that is going away but is still relevant context.
- **Remove** a rule or example outright (only when the user is explicit).
- **Rename** the Feature line (rare — only if the underlying capability was renamed in `docs/requirements.md`).

Multiple intents in one request are fine; handle each.

### Rules for amendments

- **Read the existing file first.** Reuse its tone, vocabulary, indentation, ordering, and naming conventions for examples.
- **Adding a rule:** place it in the most natural position relative to existing rules (group related rules), not strictly at the end. Give it at least one concrete example.
- **Adding an example:** place it under the rule it illustrates. Prefer examples that exercise behaviour the existing examples do not — boundary, negative path, alternative input. Do not duplicate existing examples with cosmetic changes.
- **Changing an example:** edit in place. Preserve the example title unless the title no longer describes the behaviour.
- **Splitting a rule:** create the new rules, distribute existing examples between them, and add fresh examples if any of the new rules ends up with none.
- **Merging rules:** combine the rule statement faithfully (the merged rule must still be a single piece of business logic — if it isn't, do not merge). Keep the union of their examples; remove only true duplicates.
- **Deprecating a rule:** prefix the rule line with `(Deprecated)` and add a leading example titled `Example: (Deprecated) …` whose body is a one-line Gherkin comment block (`# Deprecated in <version-or-date>: replaced by …`). Keep the original examples beneath, so historical behaviour stays readable. Do **not** silently delete deprecated rules.
- **Removing a rule or example:** only when the user is explicit. Confirm before doing so.
- **Renaming the Feature line:** only when `docs/requirements.md` has changed the capability's wording. Do not change the slug as a side effect.
- **Quality bar is unchanged.** All output rules in *Hard rules for the output* still apply.

### Confirm before destructive changes

Before any of the following, confirm with the user:

- Removing a rule or example outright (vs deprecating it).
- Renaming the Feature line or changing the slug.
- Replacing the file wholesale.
- Merging rules where the combined statement risks bundling more than one piece of logic.

## Process

1. **Identify the target spec.**
   - Confirm the capability name and slug. If `docs/requirements.md` exists, read the matching capability summary and Feature-column phrasing from it and reuse them.
   - If the slug is not listed in `docs/requirements.md`, ask the user whether to add it there first (via the `/create-requirements` skill) before writing the spec.
2. **Check whether `specs/<slug>.spec` already exists.**
   - If it does **not** exist, you are authoring from scratch — continue with step 3.
   - If it **does** exist, switch to *Amendment mode* (see above): read the file, identify the user's intent, apply the smallest faithful change, then jump to step 6.
3. **Elicit rules.** With the user, list the pieces of business logic this capability must satisfy. Each rule must be a single invariant — challenge any rule that contains "and" linking two distinct behaviours.
4. **Elicit examples per rule.** For each rule, gather at least one concrete example with named data. Probe for boundaries, negative paths, and edge cases the user has not yet supplied — but ask, do not fabricate.
5. **Draft and write the file.** Compose the Gherkin in memory following the *Required structure* and *Reference template*, then write to `specs/<slug>.spec`.
6. **Summarise back to the user.** Report:
   - what changed (added rules, added examples, deprecated, removed, renamed) — or, for a fresh file, the rules and examples you created;
   - any wording you reshaped to remove implementation detail or to fit domain language;
   - **assumptions** you had to make to complete the file (rule grouping decisions, edge cases you inferred, defaults you chose). Invite the user to correct any of them. Spec files do not contain an Assumptions section themselves — surface assumptions in the chat response so the user can review and request changes.
7. **Point at the next step.** Remind the user that:
   - the matching capability area in `docs/requirements.md` should reference this spec via the Spec file index;
   - the next workflow step is to drive implementation and acceptance tests from this spec.

## Self-check before finalising

Before writing the file, verify:

- [ ] Exactly one `Feature:` declaration; the wording matches the capability in `docs/requirements.md` if that file exists.
- [ ] Every `Rule:` is a single piece of business logic — no "and" linking two distinct behaviours.
- [ ] Every rule has at least one concrete `Example:`. No rule is left abstract.
- [ ] Every example uses real, named data — no placeholders like `<value>` or "some input".
- [ ] Every Given/When/Then references something externally observable; no internal implementation leaks.
- [ ] Domain language is consistent with `docs/requirements.md` and across rules.
- [ ] Indentation and blank-line conventions match the *Required structure*.
- [ ] If amending: existing slugs and Feature line preserved unless the user asked otherwise; deprecated rules are marked, not silently deleted; destructive changes were confirmed.
- [ ] You asked the user about every material ambiguity you could not resolve from their input.
- [ ] Assumptions you made are surfaced back to the user in the chat response.
- [ ] Nothing in the file tells the reader **how** the capability is implemented.
