---
mode: agent
description: Create or amend a high-level requirements.md from a project summary and a list of high-level requirements, following the Agent-First workflow conventions. Supports adding, changing, and deprecating capabilities in an existing document.
---

# Create Requirements

You are helping the user produce **`docs/requirements.md`** — the first artefact in the Agent-First / Agent-Enhanced development workflow. It is a high-level requirements document that states **what** the system must do. Detailed observable behaviour will later be expressed as Gherkin scenarios in `specs/*.spec`; this document does not contain those scenarios, only the capability map that points to them.

## Inputs you need from the user

Before generating the file, make sure you have:

1. **Project / system name** — used in the document title.
2. **Summary** — one or two paragraphs describing the system's purpose, who uses it, and the problem it solves.
3. **High-level requirements** — a list of needs, capabilities, or constraints the system must satisfy. These can be rough, overlapping, or expressed at different levels of detail; you will shape them into capability areas.

If any of these are missing or ambiguous, **ask the user before writing the file**. Prefer one focused question at a time using the available question tool rather than batching. Keep asking until you are confident you can produce a faithful document — do not guess to fill gaps.

### When to ask clarifying questions

Ask the user (do not assume) whenever any of the following is true:

- A high-level requirement is vague, broad, or could be interpreted multiple ways.
- Two requirements appear to overlap or conflict.
- A requirement names a specific technology — confirm the underlying *behavioural* need before restating it.
- You are unsure whether something is in scope, out of scope, or a non-functional concern.
- You are unsure how to group requirements into capability areas (see next section).
- A non-functional concern (performance, isolation, transparency, security, etc.) is implied but no target or expectation is given.

If you proceed despite remaining uncertainty, capture every such decision in the **Assumptions** section described below.

## Hard rules for the output

The generated document **must**:

- Use **domain language** that the user, product, and test stakeholders share. Avoid jargon from any specific tech stack.
- Describe **observable behaviour** — what an external observer (a test, a user, an operator) can see. Never describe internal implementation.
- Be **technology-agnostic**. Do **not** mention databases, frameworks, languages, libraries, ORMs, message brokers, cloud providers, file formats, classes, modules, design patterns, or any "how". If the user supplies implementation details, restate them as observable behaviour or omit them.
- Group the user's high-level requirements into **capability areas**. The mapping is not necessarily one-to-one: a single high-level requirement may split into several capabilities, and several related requirements may merge into one. Decide groupings deliberately; when the right grouping is not obvious, **ask the user**.
- Each capability area gets a short paragraph and a placeholder link to a `specs/<slug>.spec` file (the spec files do not need to exist yet — they will be created in the next workflow step).
- Be self-consistent: every capability area listed in the body must also appear in the **Spec file index** table at the bottom, and vice versa.
- Stay concise. Each capability area is typically 1–3 sentences.

The generated document **must not**:

- Invent requirements the user did not state or imply. If you think something is missing, ask.
- Specify acceptance criteria as Gherkin or step-by-step rules — those belong in the spec files.
- Include task lists, timelines, owners, or status tracking.

## Required structure

Produce the file at `docs/requirements.md` with these sections, in order:

1. `# <Project Name> — Requirements`
2. A short intro paragraph stating that this document is the **what**, that observable behaviour is in `specs/`, and that implementation choices are intentionally omitted.
3. `## How to use this documentation` — a two-row table mapping `docs/requirements.md` and `specs/*.spec` to their roles, plus a one-line note on the update workflow (update the relevant spec first, then this document only if scope or capabilities change).
4. `## Purpose` — derived from the user's summary. Describe the system, its users, and the problem it solves, in domain terms.
5. `## Core concepts` — a short bulleted glossary of the key domain nouns used throughout the document (typically 2–5 items). Optionally followed by a short **Scope assumptions (behavioural, not implementation)** bullet list capturing observable boundaries (e.g. protocols spoken, channels offered) — only include assumptions the user actually stated or confirmed.
6. `## Capability areas` — one `### <Capability>` subsection per high-level requirement. Each subsection contains a short behavioural description and a `**Spec:** [` `specs/<slug>.spec` `](../specs/<slug>.spec)` line.
7. `## Non-functional requirements` — a table with `Concern | Requirement` columns, covering only NFRs the user mentioned or confirmed (typical concerns: startup time, determinism, transparency of failures, isolation). Frame each requirement as something observable in test or operations.
8. `## Out of scope` — a bulleted list of things explicitly excluded. Prefix with the line `Unless added in a later version:`.
9. `## Assumptions` — a bulleted list of every assumption you made while drafting the document. Include:
   - Capability-area groupings you chose where the user's input was ambiguous.
   - Reinterpretations of implementation-flavoured input as behaviour.
   - Default non-functional expectations you introduced because the user did not state one.
   - Anything in scope/out-of-scope you decided without explicit confirmation.
   If you genuinely made no assumptions, write a single bullet stating so. The user reviews this section to catch misinterpretations early.
10. `## Spec file index` — a final table with `Spec file | Feature` columns, one row per capability area, linking to `specs/<slug>.spec`.

Use `---` horizontal rules between top-level sections, matching the existing example.

## Slug rules for spec files

For each capability area, derive a kebab-case slug from the capability name:

- lowercase, words separated by hyphens
- no articles, no punctuation
- short and stable (e.g. "Define stubs" → `define-stubs`, "CI and parallel test runs" → `ci-and-parallel-runs`)

The `Feature` column in the Spec file index should be a one-line, user-facing phrasing of the capability (not a copy of the heading).

## Reference template

Use the template below as the structural and tonal model. It is illustrative only — replace every placeholder with content derived from the user's input. Do **not** copy its domain (a fictional "Order Tracker" service) into the user's document.

````markdown
# Order Tracker — Requirements

This document states **what** the system must do at a requirements level. **Observable behaviour** is specified in full as executable Gherkin scenarios in [`specs/`](../specs/). Implementation choices (database, in-memory store, framework, UI framework) are intentionally omitted.

---

## How to use this documentation

| Document | Role |
|----------|------|
| This file (`docs/requirements.md`) | High-level requirements, scope, and capability map |
| [`specs/*.spec`](../specs/) | Canonical BDD scenarios (rules and examples) for acceptance tests and implementation |

When adding or changing behaviour, update the relevant `.spec` file first, then adjust this document only if scope, capabilities, or non-functional expectations change.

---

## Purpose

Order Tracker lets small retailers see the live status of every customer order in one place. Staff record orders as they are taken, update progress as items are picked, packed, and shipped, and answer customer queries without phoning the warehouse.

The system replaces a spreadsheet shared by email. It is used in-shop on a tablet and from the back office on a desktop browser.

---

## Core concepts

- **Order** — A customer's request for one or more items, with a status that progresses from *received* through *shipped* or *cancelled*.
- **Line item** — A single product and quantity within an order.
- **Operator** — A staff member who creates and updates orders.

**Scope assumptions (behavioural, not implementation):**

- The system is reached through a web interface over the public internet.
- Operators sign in before making changes; read-only views may be available without sign-in.

---

## Capability areas

### Capture orders

Operators can record a new order with customer details and one or more line items. The system rejects orders with no line items and surfaces the reason. Saved orders are immediately visible to all operators.

**Spec:** [`specs/capture-orders.spec`](../specs/capture-orders.spec)

### Progress orders through fulfilment

Each order moves through a defined sequence of statuses. Operators can advance an order to the next status, and only valid transitions are accepted. The current status and the time of the last change are visible on the order.

**Spec:** [`specs/progress-orders.spec`](../specs/progress-orders.spec)

### Search and filter orders

Operators can find orders by customer name, order reference, or status. Results are ordered with the most recently updated first. An empty result is reported clearly rather than as an error.

**Spec:** [`specs/search-orders.spec`](../specs/search-orders.spec)

### Cancel orders

Operators can cancel an order that has not yet shipped. Cancellation requires a reason, which is recorded against the order. Shipped orders cannot be cancelled.

**Spec:** [`specs/cancel-orders.spec`](../specs/cancel-orders.spec)

---

## Non-functional requirements

| Concern | Requirement |
|---------|-------------|
| Responsiveness | Common operator actions (open, save, search) appear to complete within one second on a typical broadband connection. |
| Determinism | The same sequence of operator actions produces the same order state every time. |
| Transparency | Validation failures and forbidden transitions return explicit, human-readable messages. |

---

## Out of scope

Unless added in a later version:

- Payment capture or refunds.
- Inventory management beyond decrementing on shipment.
- Multi-warehouse routing.
- Customer-facing self-service order tracking.

---

## Assumptions

- "Live" was interpreted as "visible to other operators on their next refresh", not as real-time push updates. Confirm with the user if continuous push is required.
- "Search" was assumed to cover customer name, order reference, and status; other fields can be added later.
- Sign-in is assumed to be required for any change but not for read-only views; this was not explicitly stated.

---

## Spec file index

| Spec file | Feature |
|-----------|---------|
| [`capture-orders.spec`](../specs/capture-orders.spec) | Record new customer orders |
| [`progress-orders.spec`](../specs/progress-orders.spec) | Move orders through fulfilment statuses |
| [`search-orders.spec`](../specs/search-orders.spec) | Find orders by common attributes |
| [`cancel-orders.spec`](../specs/cancel-orders.spec) | Cancel orders that have not yet shipped |
````

## Amendment mode

If `docs/requirements.md` already exists, you are **amending**, not authoring from scratch. Treat the existing file as the source of truth and make the smallest faithful change that satisfies the user's intent.

### Detect the user's intent

Determine which of these the user wants (ask if unclear):

- **Add** a new capability, NFR, or out-of-scope item.
- **Change / clarify** wording or scope of an existing capability or NFR.
- **Deprecate** a capability that is going away (still relevant context, but no longer required).
- **Remove** a capability that was never delivered or is being abandoned outright.
- **Rename / re-group** capabilities (split, merge, or re-slug).
- **Replace** the document wholesale (rare — confirm explicitly before doing this).

Multiple intents in one request are fine; handle each.

### Rules for amendments

- **Read the existing file first.** Reuse its tone, terminology, capability ordering, and slug style. Do not silently rewrite sections you were not asked to change.
- **Preserve slugs.** Never re-slug an existing capability unless the user explicitly asks. Slugs are referenced by `specs/*.spec` files and changing them breaks links.
- **Adding a capability:**
  - Append a new `### <Capability>` subsection in the most natural place (group with related capabilities, not strictly at the end).
  - Add a corresponding row to the **Spec file index**.
  - Note in **Assumptions** that the matching `specs/<slug>.spec` does not yet exist and is the next workflow step.
- **Changing a capability:** edit the paragraph in place. Do not change its slug or its Spec file index row unless the feature description genuinely needs it.
- **Deprecating a capability:**
  - Keep the `### <Capability>` subsection. Prefix the heading with `(Deprecated) ` and add a leading sentence in the form: *"**Deprecated in <version-or-date>.** Replaced by `<other-capability>` / removed because …"*.
  - Keep the Spec file index row but mark the Feature column with a leading `(Deprecated)`.
  - Do **not** delete the spec link — it remains useful history until the spec file itself is retired.
- **Removing a capability:** only if the user is explicit that it never shipped or should be erased. Delete the subsection and its index row, and record the removal in **Assumptions**.
- **Renaming / re-grouping:** prefer additive changes. If a slug must change, list both the old and new slug in **Assumptions** so spec files can be migrated.
- **Out of scope:** when a previously in-scope capability is being permanently dropped (not just deprecated), move a corresponding bullet into **Out of scope**.
- **Non-functional requirements:** add, change, or remove rows the same way; do not reorder unrelated rows.
- **Assumptions section:**
  - Replace stale assumption bullets that the amendment now invalidates.
  - Append new bullets for every fresh assumption made during this amendment.
  - If the existing document had no Assumptions section, add one.
- **Quality bar is unchanged.** All output rules in *Hard rules for the output* still apply: domain language, observable behaviour, no implementation detail.

### Confirm before destructive changes

Before doing any of the following, confirm with the user:

- Removing a capability outright (vs deprecating it).
- Re-slugging an existing capability.
- Replacing the document wholesale.
- Deleting any Out-of-scope or Assumption bullet you did not put there in this session.

## Process

1. **Check whether `docs/requirements.md` already exists.**
   - If it does **not** exist, you are authoring from scratch — continue with step 2.
   - If it **does** exist, switch to *Amendment mode* (see above): read the file, identify the user's intent (add / change / deprecate / remove / rename / replace), and apply the smallest faithful change. Skip step 2's "from-scratch" framing and go straight to the relevant amendment work, then jump to step 5.
2. Confirm you have the project name, summary, and high-level requirements. Ask for anything missing or ambiguous, one question at a time.
3. Decide capability-area groupings. Remember the mapping from high-level requirements to capabilities is not necessarily one-to-one — split, merge, or rename as needed. Where the right grouping is genuinely ambiguous, ask the user; otherwise proceed and record the choice as an assumption.
4. For each capability area, derive its kebab-case slug. Draft the document in memory, then write it to `docs/requirements.md`.
5. After writing, briefly summarise:
   - what changed (new, changed, deprecated, removed, renamed) — or, for a fresh document, the capability areas you created with their slugs,
   - any requirements you reshaped to remove implementation detail, and
   - the assumptions you recorded or updated — invite the user to correct any of them.
6. Remind the user that the next workflow step is to create or update the matching `specs/<slug>.spec` files. Call out specifically any new slugs (need a new spec) and any deprecated slugs (spec may need a deprecation note or removal).

## Self-check before finalising

Before writing the file, verify:

- [ ] No section names a specific technology, framework, or storage mechanism.
- [ ] Every capability area links to a `specs/<slug>.spec` file.
- [ ] The Spec file index lists exactly the same slugs as the capability areas.
- [ ] Out-of-scope items are explicit exclusions, not vague disclaimers.
- [ ] Non-functional requirements are phrased as externally observable expectations.
- [ ] An **Assumptions** section is present and lists every non-obvious choice you made (or explicitly states none were made).
- [ ] You asked the user about every material ambiguity you could not resolve from their input.
- [ ] If amending an existing document: existing slugs were preserved unless the user asked otherwise; deprecated capabilities are marked, not silently deleted; destructive changes were confirmed.
- [ ] Nothing in the document tells the reader **how** the system is built.
