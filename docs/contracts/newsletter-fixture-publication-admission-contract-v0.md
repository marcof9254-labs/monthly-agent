# Newsletter Fixture Publication Admission Contract v0

**Status:** Draft revision 3 — architecture artifact for bounded closure review
**Parent contract:** `docs/contracts/newsletter-publication-boundary-contract-v0.md`
**Parent exact head:** `cfef8a8fae74cd628f085022287683d597bc38cf`
**Parent status:** Owner-accepted normative architecture boundary through a later append-only acceptance event
**Parent acceptance attestation:** `docs/acceptance/newsletter-publication-boundary-contract-v0-owner-acceptance-attestation.md`
**Parent acceptance attestation SHA-256:** `576d4f80930f3c862129ae6a7d35590d893582fe30858cfea52997e3233e0844`
**Scope class:** contract-only, documentation-only, fixture-first
**Runtime implementation:** not authorized by this document
**Production activation:** prohibited

---

## 1. Purpose

This contract defines the smallest executable publication-admission boundary required for the next fictional, supervised newsletter pilot.

The slice exists to prevent four currently demonstrated failure classes:

1. treating canonical record approval as publication authority;
2. allowing implicit array, filesystem, filename, timestamp, or physical enumeration order to affect publication identity or output order;
3. losing participant-facing semantics such as recurrence, multi-session dates, and fee audience/type relationships during projection;
4. silently excluding invalid or incomplete selected records while still reporting successful generation.

This contract does **not** define a complete production publication engine.

Draft revision 3 preserves the minimal fixture-first scope, retains every parent safety invariant required before destination mutation, and closes the remaining governance-evidence and executable-vocabulary findings from the first bounded closure review.

---

## 2. Governing invariants

The following parent-contract separations remain normative:

```text
record approval
≠ newsletter eligibility
≠ publication selection
≠ actual inclusion
```

Additional v0 invariants:

```text
fixture-only execution
complete-or-fail generation
explicit zero-based ordered selection
exact run / schema / record / profile binding
deterministic closed-bundle identity
prepared intent before destination mutation
explicit installation state
fail-closed single-writer installation right
no production destination reachability
no silent exclusion
```

A narrower fixture capability may omit production features, but it must not weaken a parent safety invariant.

Owner acceptance of the parent contract does not authorize runtime implementation, PR creation, Ready transition, merge, real-data processing, or production activation.

---

## 3. Authorized pilot shape

The only intended pilot is:

```text
fictional canonical candidate records
→ explicit run-level and record-level clean findings state
→ exact newsletter eligibility
→ explicit ordered selection
→ exact publication profile
→ deterministic closed-bundle identity
→ deterministic projection
→ safe Markdown rendering
→ durable prepared intent
→ immediate fixture installation-right validation
→ isolated fixture installation
→ finalized or explicit unknown evidence
```

The pilot must be:

- fictional-data only;
- manually supervised;
- single-writer;
- non-production;
- non-networked as an operational constraint unless separately authorized;
- unable to select or mutate a production destination;
- unable to retry automatically after an unknown installation result.

---

## 4. Closed input bundle

The v0 closed input bundle contains exactly:

1. run context;
2. exact canonical schema artifact identity/version/digest;
3. canonical candidate fixture records;
4. explicit evidence-findings artifact covering the candidate set and the evidence run;
5. effective newsletter eligibility decisions for selected records;
6. ordered publication selection;
7. publication profile;
8. fixture authority/destination state.

The implementation must not derive input identity, authority, or order from:

- filesystem enumeration;
- filename or physical path;
- modification time;
- source array order;
- directory presence;
- prior output existence;
- process-local memory.

Any missing, duplicate, malformed, unsupported, ambiguous, or mismatched required artifact causes whole-run failure.

Unselected candidate eligibility artifacts are outside the v0 closed bundle and therefore outside `input_sha256`.

---

## 5. Minimal executable artifact schemas

### 5.1 Run context

Required fields:

```text
run_id
publication_run_id
programme_month
locale
consumer_id
schema_id
schema_version
schema_sha256
profile_id
profile_sha256
selection_id
destination_class = fixture
destination_id
```

Rules:

- `run_id` identifies the evidence run.
- `publication_run_id` identifies one publication attempt and must not be inferred from `run_id`.
- `programme_month` must be explicit and must not be inferred from identifiers or filenames.
- `locale` must be explicit.
- all identifiers must be non-empty stable identifiers;
- destination identity is part of the run scope;
- expected destination generation and digest are authoritative only in the fixture authority/destination state artifact defined in §5.6.

### 5.2 Canonical fixture candidate record

Each candidate record must include or resolve to:

```text
run_id
schema_id
schema_version
activity_id
record_sha256
qa_status
uncertain_fields
participant-facing activity fields
```

Admission requires:

```text
record.run_id == run_context.run_id
record.schema_id == run_context.schema_id
record.schema_version == run_context.schema_version
qa_status == approved
uncertain_fields == []
valid exact canonical schema
record_sha256 matches canonical record bytes
```

Exact record identity is the tuple:

```text
(run_id, activity_id, schema_id, schema_version, record_sha256)
```

Unknown record fields fail closed unless the exact canonical schema explicitly permits them.

The publication profile in §5.7 is the sole authority for participant-facing field admission.

### 5.3 Evidence-findings artifact

The findings artifact must include a run-level statement and one binding for every candidate record.

Required run-level fields:

```text
run_id
schema_id
schema_version
candidate_count
run_findings_status = clean
unresolved_run_findings = []
```

Required per-record binding:

```text
run_id
schema_id
schema_version
activity_id
record_sha256
findings_status = clean
unresolved_findings = []
```

Rules:

- the artifact must be complete for the candidate record set;
- every candidate record must have exactly one binding;
- each binding must match the exact record identity tuple;
- run-level and record-level clean status must be affirmative;
- absence of a findings artifact must never be interpreted as clean;
- any unresolved run-level or record-level finding fails the whole run.

Historical chains, succession, revocation, and ambiguous-tip resolution remain out of scope.

### 5.4 Newsletter eligibility decision

Required fields:

```text
eligibility_id
run_id
schema_id
schema_version
consumer_id
activity_id
record_sha256
profile_id
profile_sha256
decision = eligible
```

Rules:

- eligibility must bind one exact evidence run;
- eligibility must bind one exact canonical schema identity/version;
- eligibility must bind one exact record digest;
- eligibility must bind one exact consumer;
- eligibility must bind one exact profile logical ID and digest;
- all fields must match the run context, record, and profile exactly.

Cross-run reuse fails closed even when `activity_id` and `record_sha256` are otherwise identical.

No profile-family compatibility, profile inheritance, or additive-version inheritance is permitted.

### 5.5 Ordered publication selection

Required fields:

```text
selection_id
run_id
programme_month
consumer_id
profile_id
profile_sha256
destination_class = fixture
destination_id
entries[]
```

Each entry contains:

```text
position
activity_id
record_sha256
eligibility_id
```

Selection rules:

- positions start at `0`;
- positions are contiguous from `0`;
- positions are unique;
- `position == array index`;
- activity IDs are unique;
- every entry resolves to one exact admitted record;
- every entry resolves to one exact eligible decision;
- selection scope fields must match run context exactly;
- publication order is taken only from the validated explicit position.

An explicit empty selection is represented by:

```text
entries: []
```

### 5.6 Fixture authority/destination state

Required logical fields:

```text
destination_class = fixture
destination_id
expected_destination_generation
expected_destination_sha256_or_null
```

Operational resolution may additionally produce:

```text
configured_fixture_root
resolved_path
```

Rules:

- `destination_class` and `destination_id` must match the run context exactly;
- expected destination generation and digest exist only in this artifact and are the sole authoritative expected-state values;
- logical destination identity enters the closed-bundle digest;
- `resolved_path` is validated operationally but does not enter `input_sha256`;
- destination must resolve under a configured test-controlled fixture root;
- production destination resolution must be technically unreachable;
- arbitrary user-supplied absolute paths are prohibited;
- existing real newsletter paths are prohibited;
- traversal, symlink, junction, reparse-point, or equivalent root escape is prohibited;
- path containment must be revalidated immediately before installation using a fail-closed mechanism appropriate to the platform.

### 5.7 Publication profile

Required fields:

```text
profile_id
profile_sha256
consumer_id
allowed_fields
required_fields
field_mappings
prohibited_fields
predicate_rules
partial_generation_policy
```

Required v0 partial policy shape:

```text
partial_generation_policy:
  allow_partial_generation: false
  allowed_record_local_reason_codes: []
  minimum_included_count: null
  minimum_included_ratio: null
```

`allowed_fields` and `predicate_rules` use the same canonical field-path vocabulary. v0 supports top-level field names and the following schema-aligned array-element paths:

```text
dates[*].recurrence
fee[*].fee_type
```

`predicate_rules` has this executable v0 shape:

```text
canonical_field_path -> ordered list of predicate_name
```

Every `predicate_rules` key must be a member of `allowed_fields` using the exact same canonical field-path spelling.

Example:

```yaml
predicate_rules:
  activity_title:
    - required_non_empty
    - not_placeholder
    - supported_scalar_shape
  dates:
    - required_non_empty
    - supported_date_shape
  dates[*].recurrence:
    - supported_recurrence_shape
  fee:
    - supported_fee_shape
  fee[*].fee_type:
    - supported_scalar_shape
```

v0 predicates do not accept parameters, arbitrary path expressions, or nested boolean expressions.

At minimum, the profile may support:

```text
activity_title
dates
dates[*].recurrence
time
venue
description
target_participants
fee
fee[*].fee_type
quota
registration_method
registration_period
notes
```

Rules:

- if `dates` is allowed, `dates[*].recurrence` must also be supported;
- if `fee` is allowed, the complete fee structure must be supported, including `fee[*].fee_type` and every source-supported fee audience/category relationship;
- `source_reference` is always prohibited from participant-facing output;
- unknown fields, mappings, or predicates fail closed.

### 5.8 Prepared intent artifact

Before any replacement attempt, a prepared intent must be durably persisted.

Required fields:

```text
publication_run_id
run_id
programme_month
consumer_id
input_sha256
proposed_output_sha256
schema_id
schema_version
schema_sha256
selection_id
selection_sha256
profile_id
profile_sha256
destination_class
destination_id
expected_destination_generation
expected_destination_sha256_or_null
proposed_outcome = complete_generation
prepared_at_or_sequence
state = prepared
```

The prepared artifact must be written before destination mutation and must be sufficient to distinguish a later `unknown` result from a definite `not_replaced` result.

### 5.9 Final generation evidence

Required fields:

```text
publication_run_id
run_id
programme_month
consumer_id
input_sha256
output_sha256_or_null
schema_id
schema_version
schema_sha256
selection_id
selection_sha256
profile_id
profile_sha256
destination_class
destination_id
input_count
selected_count
included_count
excluded_count
ordered_included_activity_ids
ordered_excluded_activity_ids
outcome
primary_failure_class_or_null
reason_code_or_null
installation_state
file_sync_completed_or_unsupported
directory_sync_completed_or_unsupported
atomic_replace_capability
```

Allowed `installation_state` values:

```text
not_attempted
installed
not_replaced
unknown
```

Rules:

- `input_count` is the number of canonical candidate activity records explicitly enumerated in the closed input bundle;
- `selected_count` is the number of validated ordered-selection entries;
- `0 <= selected_count <= input_count`;
- `included_count <= selected_count`;
- `excluded_count == selected_count - included_count`;
- `complete_generation` requires `included_count == selected_count` and `excluded_count == 0`;
- ordered included IDs must equal the ordered selection exactly;
- v0 never emits a successful outcome with excluded IDs;
- evidence must not infer inclusion from output text search or file existence;
- an unfinalized prepared artifact is interpreted as `unknown` unless reliable reconciliation proves a narrower result;
- this v0 has no automated reconciliation, so an unfinalized prepared artifact requires manual inspection and prohibits blind retry;
- evidence finalization failure after a possible replacement must never produce an optimistic `installed` or false `not_replaced` claim.

---

## 6. Deterministic input identity

`input_sha256` must be calculated from canonical serialization of the closed bundle in this fixed category order:

1. run context;
2. canonical schema artifact;
3. candidate activity records;
4. evidence-findings artifact;
5. effective eligibility decisions for selected records;
6. ordered publication selection;
7. publication profile;
8. logical fixture authority/destination state.

Canonical ordering rules:

### 6.1 Candidate records

Sort lexicographically by the exact record-identity tuple:

```text
run_id
activity_id
schema_id
schema_version
record_sha256
```

### 6.2 Findings bindings

Sort record bindings by the same exact record-identity tuple.

The run-level findings statement precedes all record bindings.

### 6.3 Eligibility decisions

Order eligibility decisions by the validated selection position of the exact selected record.

### 6.4 Selection

Serialize entries in validated zero-based position order.

### 6.5 Destination state

Include only logical destination and expected-state fields:

```text
destination_class
destination_id
expected_destination_generation
expected_destination_sha256_or_null
```

Do not include:

```text
resolved_path
configured_fixture_root
filename
platform-specific path representation
```

Physical enumeration order must not affect `input_sha256`.

Randomized enumeration of the same logical bundle must produce the same digest and rendered bytes.

This v0 explicitly includes the complete candidate record set in category 3 while including eligibility only for selected records.

---

## 7. Normative phase order

This child contract preserves the parent 13-phase numbering.

1. closed-bundle structural admission;
2. effective selection structural resolution;
3. canonical record admission;
4. evidence-findings resolution;
5. newsletter eligibility resolution;
6. semantic selection/profile compatibility;
7. projection construction;
8. rendering execution;
9. rendering-safety validation;
10. complete-output, partial-generation-policy, and prepared-evidence validation;
11. durable prepared-intent persistence;
12. immediate current installation-right and path-containment validation, followed directly by the installation attempt with no intervening operation capable of invalidating the observed state;
13. installation-result determination plus finalized or explicit unknown evidence persistence.

The primary failure classification is the earliest normative phase that detects the defect.

Secondary findings may be recorded but must not replace the primary failure classification.

---

## 8. Projection fidelity

Projection must preserve:

- all selected dates;
- date order;
- recurrence ownership;
- multi-session meaning;
- fee order;
- fee type/audience relationship;
- participant target meaning;
- registration meaning;
- explicit notes.

The implementation must not:

- infer missing facts;
- flatten fee audiences;
- merge participant audience with fee audience;
- drop recurrence;
- partially render an activity;
- silently repair unsupported shapes.

Unsupported or incomplete projected shapes fail the whole run.

---

## 9. Predicate vocabulary

v0 supports only these deterministic predicates:

```text
required_non_empty
not_placeholder
supported_scalar_shape
supported_list_shape
supported_date_shape
supported_recurrence_shape
supported_fee_shape
```

Predicate evaluation rules:

- predicates execute in the profile-declared order for each field;
- failure of any predicate fails the selected record;
- because partial generation is disabled, any selected-record predicate failure fails the whole run;
- unknown predicate names fail closed;
- predicate parameters, user-defined code, probabilistic judgment, and generic DSL behavior are unsupported.

---

## 10. Rendering safety

The renderer must produce deterministic UTF-8 bytes with a fixed newline policy.

Participant-controlled text must be escaped or normalized so it cannot forge:

- Markdown headings;
- list structure;
- trusted provenance comments;
- run identity;
- publication-run identity;
- profile identity;
- selection identity;
- digest evidence.

Trusted identifiers must come only from admitted artifacts and must not be represented in a form that participant text can imitate as authority.

---

## 11. Outcome model

v0 permits exactly two generation outcomes:

```text
complete_generation
integrity_failure
```

`complete_generation` requires:

```text
every selected record included exactly once
included order equals explicit selection order
included_count == selected_count
excluded_count == 0
installation_state == installed
final evidence successfully established
```

Any exclusion, mismatch, unsupported value, renderer failure, prepared-intent failure, installation-right failure, installation failure, or evidence finalization failure is `integrity_failure`.

Partial generation is disabled by the profile object in §5.7.

Silent exclusion is prohibited.

An explicit empty selection may produce a valid empty fixture output only when:

```text
entries == []
selected_count == 0
included_count == 0
excluded_count == 0
all integrity gates pass
installation_state == installed
```

A non-empty selection with zero inclusion is always `integrity_failure`.

---

## 12. Fixture installation and evidence lifecycle

### 12.1 Temporary output

The implementation must:

1. create the temporary output on the same fixture filesystem as the destination;
2. use controlled exclusive access;
3. fully render before destination mutation;
4. validate the complete temporary bytes;
5. recompute `output_sha256` from final temporary bytes immediately before replacement.

### 12.2 Prepared intent

Before replacement, the implementation must durably persist the prepared intent defined in §5.8.

If prepared intent cannot be persisted, installation is not attempted and the existing fixture destination is preserved.

### 12.3 Immediate installation-right validation

Immediately before replacement, the implementation must revalidate:

```text
single-writer right is current
expected destination generation still matches
expected destination digest still matches when supplied
destination class remains fixture
destination ID remains bound to this run
resolved path remains contained under fixture root
no symlink/junction/reparse-point escape has appeared
```

A stale or failed precondition results in:

```text
outcome = integrity_failure
installation_state = not_replaced
```

### 12.4 Replacement

Fixture minimum capability is:

```text
durability_atomic_replace_only
```

The implementation must not:

- truncate the destination in place;
- use a cross-device copy fallback;
- claim stronger durability than the operations completed.

Where supported, file-data sync may be attempted and honestly recorded.

### 12.5 Finalization

After replacement, the implementation must finalize generation evidence.

Final evidence may report only:

```text
installed
not_replaced
unknown
```

for an attempted installation, or `not_attempted` when no installation was attempted.

If replacement may have succeeded but the system cannot confirm the destination/evidence relationship, the result is:

```text
outcome = integrity_failure
installation_state = unknown
```

The system must not:

- optimistically claim `installed`;
- rewrite a possible mutation as definite `not_replaced`;
- retry blindly;
- infer success from destination existence alone.

Manual reconciliation is required for `unknown`; automated reconciliation remains deferred.

---

## 13. Concurrency boundary

v0 supports one active writer only.

The installation-right mechanism must be fail closed and may be satisfied by isolated single-writer serialization within a test-controlled workspace.

A diagnostic lock may exist only as an additional signal; a non-authoritative lock alone does not satisfy installation authority.

Concurrent publishers, leases, general fencing tokens, distributed compare-and-swap, stale-worker recovery, and unattended retry are not implemented.

The implementation must reject execution when it cannot establish the current exclusive fixture installation right.

This mechanism must not be represented as production fencing.

---

## 14. Required tests

### 14.1 Artifact and binding tests

- missing run-level findings statement fails;
- missing record-level findings binding fails;
- incomplete findings coverage of candidate records fails;
- approved record without eligibility fails;
- eligibility `run_id` mismatch fails;
- cross-run eligibility reuse fails even when activity ID and record digest match;
- eligibility schema ID/version mismatch fails;
- eligibility record-digest mismatch fails;
- eligibility profile-digest mismatch fails;
- eligibility consumer mismatch fails;
- selection record-digest mismatch fails;
- selection consumer/month/destination mismatch fails;
- fixture authority/destination identity mismatch with run context fails;
- duplicate activity ID fails;
- duplicate position fails;
- non-contiguous zero-based position fails;
- `position != array index` fails;
- unknown activity ID fails;
- unknown record field fails unless canonical schema allows it;
- predicate key not present in `allowed_fields` fails;
- non-canonical field-path spelling fails;
- unknown predicate fails.

### 14.2 Destination isolation tests

- production destination class fails;
- arbitrary absolute destination path fails;
- path traversal from fixture root fails;
- symlink/junction/reparse-point escape fails;
- destination path changed between admission and installation fails;
- expected destination generation mismatch fails;
- expected destination digest mismatch fails;
- inability to establish exclusive fixture installation right fails.

### 14.3 Determinism tests

- randomized physical candidate enumeration yields identical `input_sha256`;
- randomized physical findings enumeration yields identical `input_sha256`;
- randomized physical eligibility enumeration yields identical `input_sha256`;
- randomized physical input order yields identical output bytes;
- explicit zero-based selection position controls output order;
- repeated identical logical runs yield identical output bytes and content digests;
- different local fixture paths with the same logical destination identity yield identical `input_sha256`.

Cross-operating-system byte identity is required only where canonical serialization, newline policy, locale, and renderer implementation are identical.

### 14.4 Projection fidelity tests

- all dates preserved;
- date order preserved;
- recurrence preserved;
- multi-session structure preserved;
- fee order preserved;
- fee type/audience relationship preserved;
- target participant meaning preserved;
- registration meaning preserved;
- unsupported shape fails the whole run.

### 14.5 Rendering safety tests

- Markdown heading injection escaped;
- list injection escaped;
- HTML/provenance comment injection escaped;
- trusted identity forgery fails or is neutralized;
- placeholder required value fails whole run;
- renderer exception preserves existing destination;
- temp-byte digest mismatch prevents replacement.

### 14.6 Prepared/finalized/unknown tests

- prepared intent is persisted before replacement;
- prepared-intent write failure preserves destination and yields `not_attempted`;
- installation-right failure after preparation yields `not_replaced`;
- confirmed replacement plus successful evidence finalization yields `installed`;
- crash or finalization failure after possible replacement yields `unknown`;
- unknown result prohibits automatic retry;
- no result path can encode possible mutation as definite `not_replaced`;
- no result path can claim `installed` without matching final evidence.

### 14.7 Evidence reconciliation tests

- evidence `input_count` equals the number of candidate records in the closed bundle;
- `selected_count > input_count` fails;
- evidence `selected_count` equals selection length;
- evidence `included_count` equals ordered included IDs length;
- complete generation included IDs equal selection IDs in order;
- `excluded_count == 0` for complete generation;
- any selected-record omission produces `integrity_failure`;
- evidence-vs-selection mismatch fails;
- evidence must not infer inclusion from Markdown search.

### 14.8 Outcome tests

- all selected records included exactly once and installed produces `complete_generation`;
- any selected-record exclusion produces `integrity_failure`;
- explicit empty selection can produce valid empty output;
- non-empty selection with zero inclusion fails;
- evidence failure after possible replacement produces `integrity_failure` plus `unknown`.

---

## 15. Explicit deferrals

The following remain outside this slice:

- production Owner-authority adapter;
- real-data processing;
- production destination resolution;
- partial generation execution;
- eligibility, findings, profile, or selection succession chains;
- revocation and ambiguous-tip resolution;
- stale historical artifact classification;
- multi-writer or distributed publisher fencing;
- unattended retry;
- automated reconciliation;
- production durability capability matrix;
- generic predicate DSL;
- multi-profile compatibility;
- cross-record editorial invariants;
- pagination, layout, image handling, DOCX/PDF generation, and deployment.

The following are **not** deferred because they are minimum parent safety invariants:

```text
prepared intent before mutation
explicit installation_state
unknown outcome honesty
fail-closed single-writer installation right
exact run/schema/record/profile binding
verifiable inclusion evidence
```

No implementation may quietly introduce a deferred capability.

---

## 16. Evidence required before deferred work

Deferred capabilities may be proposed only when supported by concrete evidence.

### 16.1 Artifact succession and revocation

Required evidence:

- a real need to revoke, replace, or supersede an eligibility, selection, findings, or profile artifact; and
- proof that a single immutable artifact cannot preserve the required audit history.

### 16.2 Partial generation

Required evidence:

- repeated operational delay caused by whole-run failure from a small number of bad records;
- a stable record-local failure taxonomy;
- proof that partial output is operationally preferable and safe.

### 16.3 Production authority and destination activation

Required evidence:

- successful fixture pilot;
- independent implementation review;
- explicit Owner intent for one bounded production step;
- an accepted authenticated Owner-authority mechanism;
- exact binding of that authority to destination class, destination identity/scope, consumer, profile, and bounded operation.

### 16.4 Multi-writer concurrency and fencing

Required evidence:

- more than one possible publisher;
- scheduler/manual overlap;
- retry-worker overlap; or
- an observed stale-invocation risk.

### 16.5 Automated reconciliation

Required evidence:

- an observed `unknown` outcome; or
- a requirement for unattended recovery.

### 16.6 Production durability capability matrix

Required evidence:

- execution across multiple operating systems or filesystems;
- use on NAS/network storage; or
- a formal requirement for crash-durable production publication evidence.

### 16.7 Generic predicate DSL

Required evidence:

- multiple active profiles with materially different predicates;
- repeated hard-coded predicate duplication or conflict.

The governing rule is:

```text
build a deferred capability only when
an observed operational need exists,
the simpler design demonstrably fails,
and the failure cost exceeds the added complexity.
```

---

## 17. Closure mapping for revision 2

Draft revision 2 preserves all technical closures from revision 1 and resolves the remaining first-closure-review findings as follows:

```text
F-M11 external append-only Owner acceptance attestation binds the accepted parent exact head without modifying the accepted parent bytes
N1    expected destination generation/digest exist only in fixture authority/destination state; destination identity must match run context
N2    allowed_fields and predicate_rules use one canonical schema-aligned field-path vocabulary
N3    unfinalized prepared intent is interpreted as unknown unless reliable reconciliation proves a narrower result
N4    phases 10–13 restore the parent validation and immediate-installation semantics
N5    input_count is explicitly defined with count invariants and tests
```

The parent acceptance evidence model is:

```text
immutable parent artifact at exact head
+
later append-only Owner acceptance attestation
```

The attestation does not modify the accepted parent bytes, does not authorize merge, and does not authorize runtime or production activation.

Revision 2 does not reopen or alter the already closed eligibility model, selection model, canonical digest ordering, prepared-before-replace requirement, fixture isolation, partial-generation default deny, or production deferrals.

---

## 18. Acceptance criteria and governance stop state

This contract is ready for bounded closure review only when it:

- remains subordinate to the Owner-accepted parent exact head and binds the append-only acceptance attestation identified in this document;
- prevents approval from being treated as publication authority;
- requires exact run, schema, record, consumer, profile, selection, and destination binding;
- requires explicit zero-based ordered selection;
- defines deterministic parent-aligned closed-bundle identity;
- preserves recurrence and fee-audience semantics;
- prohibits silent omission and partial generation;
- makes production destination technically unreachable;
- requires prepared intent before mutation;
- distinguishes `not_attempted`, `installed`, `not_replaced`, and `unknown` honestly;
- provides evidence sufficient to verify inclusion without parsing rendered output;
- uses fail-closed single-writer installation authority;
- states durability and concurrency limits honestly;
- contains explicit implementation deferrals and evidence gates.

Owner acceptance of this document would authorize only the architecture boundary at its exact accepted head.

It would not authorize:

```text
runtime implementation
schema activation
real-data processing
production publication
PR creation
Ready transition
merge
main changes
production authority activation
automated reconciliation
```

The next permitted governance action after this draft is:

```text
second bounded closure review
```

The second closure review must verify only:

```text
F-M11 governance-evidence closure
N1 destination-state authority closure
N2 canonical field-path closure
N3 unknown-state wording closure
N4 phase-semantics closure
N5 input_count closure
no regression
no production scope expansion
no weakening of the parent contract
```
