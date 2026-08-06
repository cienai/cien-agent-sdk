# AGENTS.md

## Purpose

This repository contains Python and PySpark code for data science, analytics, and data engineering workflows.

The goal is to produce:

* correct results
* maintainable code
* debuggable pipelines
* minimal, safe changes
* reproducible behavior

Prefer clarity and correctness over cleverness.

---

# Core Engineering Principles

## Fix root causes, not symptoms

Do not patch around issues just to make code run.

Always identify:

* why the failure happened
* whether the data contract changed
* whether assumptions became invalid
* whether the bug indicates a broader logic issue

A small root-cause fix is preferred over layered defensive hacks.

Bad:

* adding random `.fillna("")`
* wrapping failures in `try/except`
* silently dropping rows
* adding special cases until tests pass

Good:

* identifying schema mismatch
* fixing join keys
* correcting partition logic
* enforcing expected data types
* fixing invalid assumptions

---

## Prefer minimal fixes

Make the smallest change that correctly solves the problem.

Do not:

* rewrite working modules
* refactor unrelated code
* introduce frameworks
* add abstraction unless clearly needed
* “improve” architecture during bug fixes

Keep diffs focused and reviewable.

---

## Do not over-engineer edge cases

Handle realistic failure modes, not hypothetical ones.

Avoid:

* excessive fallback logic
* deeply nested conditionals
* speculative abstractions
* premature generalization

Prefer:

* explicit assumptions
* simple validation
* failing loudly on impossible states

---

## Make failures obvious

Silent corruption is worse than failure.

Prefer:

* explicit validation
* assertions for invariants
* informative exceptions
* schema checks
* row count sanity checks

Avoid:

* swallowing exceptions
* returning partial results silently
* automatic coercion without logging

---

# PySpark-Specific Guidance

## Prefer DataFrame APIs over UDFs

Use built-in Spark functions whenever possible.

Avoid Python UDFs unless absolutely necessary because they:

* break optimization
* reduce performance
* complicate serialization
* make lineage/debugging harder

Prefer:

* `pyspark.sql.functions`
* SQL expressions
* window functions
* native aggregations

---

## Be intentional about shuffles

Shuffles are expensive.

Before joins/groupBys/window operations:

* think about partitioning
* check cardinality
* avoid accidental cross joins
* filter early when possible

Do not add repartitions blindly.

---

## Avoid unnecessary actions

Actions trigger computation.

Avoid repeated:

* `.count()`
* `.collect()`
* `.show()`
* `.toPandas()`

Especially inside loops or helper functions.

---

## Never use `collect()` on large datasets

Use:

* sampling
* limited queries
* aggregates
* targeted debugging

Assume datasets may become large in production.

---

## Be explicit about schemas

Avoid schema inference in production paths when practical.

Prefer:

* explicit types
* deterministic parsing
* validated contracts

Especially for:

* JSON
* CSV
* nested structures
* ingestion pipelines

---

## Preserve determinism

Avoid nondeterministic behavior unless intentional.

Be careful with:

* unordered aggregations
* `first()` without ordering
* random sampling without seeds
* unstable deduplication logic

---

# Data Science Workflow Expectations

## Reproducibility matters

Code should produce the same result given the same inputs.

Always:

* set random seeds where relevant
* avoid hidden notebook state assumptions
* make transformations explicit

---

## Validate data assumptions

Check:

* row counts
* null rates
* uniqueness assumptions
* join explosion risk
* unexpected cardinality changes

Small validation steps prevent major downstream corruption.

---

## Prefer transparent transformations

A slightly longer but understandable pipeline is better than a compressed “smart” one.

Optimize for future maintainers reading the code at 2 AM.

---

# Code Style

## Write straightforward Python

Prefer:

* simple functions
* explicit variable names
* linear control flow

Avoid:

* deeply nested comprehensions
* metaprogramming
* hidden side effects
* magic behavior

---

## Keep functions focused

Functions should generally:

* do one thing
* have clear inputs/outputs
* avoid hidden state

Large functions should usually be split logically.

---

## Comments should explain why

Do not comment obvious code.

Good comments explain:

* business logic
* non-obvious assumptions
* Spark-specific behavior
* performance tradeoffs

---

# Testing and Validation

## Verify behavior, not implementation details

Tests should validate:

* outputs
* schema
* row-level correctness
* aggregation correctness

Avoid brittle tests tied to implementation internals.

---

## Prefer targeted tests

For bug fixes:

* reproduce the failing case
* add the smallest meaningful test
* confirm the root cause is fixed

Do not build massive synthetic test scaffolding unnecessarily.

---

# Performance Philosophy

## First make it correct, then make it fast

But avoid obviously bad Spark patterns.

Do not prematurely optimize, but also do not:

* collect huge datasets locally
* repeatedly scan tables unnecessarily
* use Python loops over Spark operations

---

## Optimize based on evidence

Use:

* explain plans
* stage/task analysis
* skew detection
* actual bottlenecks

Not guesses.

---

# Notebook Guidance

## Notebooks are for exploration

Production logic should eventually move into:

* modules
* reusable functions
* pipelines

Avoid giant stateful notebooks with hidden dependencies.

---

# Agent Behavior Expectations

When modifying code:

1. Understand the existing logic first
2. Identify root cause
3. Make the minimal correct fix
4. Preserve existing behavior unless intentionally changing it
5. Avoid unrelated cleanup
6. Explain reasoning clearly
7. Call out assumptions explicitly
8. Flag risky data-quality issues instead of masking them

When uncertain:

* ask for clarification
* surface assumptions
* do not invent business logic

---

# Preferred Mindset

Think like a careful senior engineer maintaining a critical data platform:

* pragmatic
* skeptical
* precise
* minimal
* evidence-driven
* focused on correctness over cleverness


## Additional Workspace and Data-Engineering Guidance

The workspace is the engineering context. Before changing shared behavior, identify its producers, consumers, schemas, utilities, and tests across relevant repositories. Trace defects to the layer that owns the behavior, and coordinate changes across affected repositories when a shared contract requires it. Do not modify unrelated repositories.

Treat schemas and data contracts as APIs. Check producers and consumers when changing names, types, nullability, semantics, keys, partitions, serialization, paths, or event shapes. Preserve units, timezones, identity, and aggregation level; make schema evolution explicit and keep join keys canonical.

For storage-backed files, use established centralized access, path resolution, and serialization helpers. Consider compatibility with already-written data when changing persisted or shared data.

Remember that Spark is distributed and lazy. Prefer Spark-native expressions, avoid unnecessary driver materialization, shuffles, repartitions, global sorts, cross joins, and repeated actions. Make joins intentional by checking keys, cardinality, duplicates, nulls, and broadcast size. Use explicit schemas, handle nulls and timestamps deliberately, and design rerunnable pipelines to be deterministic and idempotent.

Follow each repository's Python and dependency conventions. Prefer pure, testable functions, reuse existing utilities and domain models, preserve useful types, and do not catch broad exceptions merely to keep pipelines running.

Validate important invariants at their boundary, distinguish data-quality failures from infrastructure failures and code defects, and do not silently drop records. For aggregation or deduplication changes, establish the intended grain and test duplicates, null keys, and multiple events for the same entity.

Run targeted tests and broader established checks when feasible. Test normal and edge cases, exercise real Spark expressions, verify both sides of cross-repository contracts, and never report unrun checks as successful.

Before introducing fallbacks, compatibility shims, duplicated resolvers, or special-case data paths, establish why the source-layer fix is not viable. If evidence is insufficient for a material decision, ask rather than guess. Keep durable instructions focused on recurring constraints.

## Cross-Repository API Contracts

- Before changing an SDK method or adding a field, identify the backend source of truth and trace the value through the SDK request, backend persistence, downstream job/orchestrator code, and response consumer.
- Do not add SDK parameters for values that are derived from authenticated backend context, such as the triggering owner, unless the backend contract explicitly requires the client to supply them.
- Keep semantically distinct fields distinct. In particular, `job_type`/Run Type and `processing_mode` are separate values; never make one a fallback for the other.
- If a requested display value is stored in a separate Jobengine log record, fix the consumer/backend join rather than forcing the SDK to manufacture or duplicate that value.
- Add contract tests for both the serialized request shape and the backend-visible result, including manual, scheduled/system, and absent-optional-field cases.
