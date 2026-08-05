# Newsletter Publication Boundary Contract v0

Status: inactive contract draft; documentation only; not implemented, accepted, or runtime-active

Contract family: `newsletter-publication-boundary/v0`

Consumer identifier: `newsletter-renderer`

## A. Purpose and non-goals

This contract defines the future boundary between canonical activity evidence and an authorized participant-facing newsletter artifact. It separates record approval, newsletter-scoped eligibility, publication selection, projection, rendering, actual inclusion, and generation evidence so that no earlier state silently grants a later authority.

The contract is normative for a future implementation proposal only. It does not activate a schema, artifact, resolver, renderer, publication process, real-data flow, or consumer. It does not modify the current newsletter prototype or the temporary CLI batch guard.

This slice does not define DOCX, PDF, images, visual layout, a generic template or policy engine, deployment, web publication, multi-project abstraction, agent execution, CI, or real centre data.

## B. Normative terminology

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, and **MAY** are normative.

- **Canonical activity record**: one record that validates against the exact supported version of `schemas/activity.schema.json` and has a deterministic content digest.
- **Record approval**: the upstream evidence-review state represented by `qa_status: "approved"`. It is necessary but grants no consumer permission or publication authority.
- **Unresolved uncertainty**: any non-empty `uncertain_fields` value or any unresolved evidence finding applicable to the record revision.
- **Newsletter eligibility**: an immutable, newsletter-scoped decision permitting an exact record identity and an exact field set to be considered by `newsletter-renderer`.
- **Publication selection**: an immutable artifact stating the explicit ordered publication intent for one run context and publication profile.
- **Publication profile**: an immutable, versioned participant-facing field policy defining allowed, required, optional, excluded, and prohibited fields plus projection and rendering rules.
- **Projection**: the deterministic participant-facing data derived from one selected, admitted, eligible record under one exact profile. A projection grants no authority.
- **Actual inclusion**: successful inclusion of one complete projection in the final rendered output. Eligibility and selection do not prove inclusion.
- **Record-level exclusion**: omission of an entire selected record after all run-integrity gates pass, accompanied by a structured stable reason code. It is never a partial rendering of that record.
- **Whole-run integrity failure**: an outcome that produces no replacement participant-facing artifact because the run cannot establish authoritative input, selection, binding, or safe complete output.
- **Generation evidence**: a machine-readable result binding inputs, decisions, findings, included and excluded identities, output digest, and run identity. It is not participant-facing content.
- **Exact record identity**: `run_id`, `activity_id`, canonical schema identity/version, and canonical record digest taken together. `activity_id` alone is insufficient.

## C. Input artifacts

A future publication invocation MUST receive a closed, explicitly enumerated input bundle. Directory presence, filename order, timestamps, input array order, and previously generated output MUST NOT establish authority, membership, or precedence.

Eligibility, selection, and profile artifacts MUST be authenticated through an accepted owner-authority mechanism before production use. Content hashes prove integrity and binding only; they do not self-authenticate an owner decision. This draft neither selects nor activates an operational authority-delivery mechanism.

### Canonical activity records

Each candidate record MUST identify its evidence `run_id`, validate independently against the supported canonical activity schema, and have a lowercase SHA-256 digest over RFC 8785 canonical UTF-8 JSON bytes. The bundle MUST identify the exact schema artifact or immutable schema version used for admission.

The canonical records remain evidence. Their `qa_status` and `uncertain_fields` values are admission facts, not newsletter authority.

### Newsletter eligibility artifact

Each eligibility artifact MUST bind one exact record identity, `consumer_id: "newsletter-renderer"`, an exact publication-profile identity or explicitly compatible profile-family constraint, an exact allowed source-field set, a decision (`eligible` or `denied`), a positive version, and a predecessor identity or `null`.

Eligibility artifacts MUST be immutable, append-only, and versioned. Correction, denial, or revocation MUST create a successor; mutation in place is prohibited. Resolution MUST produce one unique effective same-scope tip. Eligibility for any other consumer MUST NOT transfer to newsletters.

### Ordered publication selection artifact

The selection artifact MUST bind one run context, one exact publication profile, and an ordered `entries` array. Every entry MUST contain an explicit zero-based `position`, `activity_id`, and exact record digest. Positions MUST be contiguous from zero, unique, and equal to array position. This redundant binding makes order explicit and verifiable.

Input record order, eligibility order, filesystem enumeration, and projection generation order MUST NOT become publication order. An intentionally empty publication requires a valid selection with `entries: []`.

Selections MUST be immutable, append-only, and versioned, with a unique same-scope effective tip resolved through an explicit predecessor chain. A successor replaces the complete ordered intent; it does not patch an earlier array in place.

### Publication profile

The publication profile MUST be a versioned, immutable artifact. It MUST define its identity, contract version, consumer, allowed source fields, participant-facing mappings, required and optional fields, omission rules, structural rendering rules, and prohibited fields. Profiles MUST NOT be selected from user-controlled record text.

### Run identity and context

The invocation MUST bind an explicit `publication_run_id`, evidence `run_id`, programme month, consumer, locale, profile identity, selection identity, and expected destination class. Programme month MUST come from authoritative run context and MUST NOT be inferred solely by parsing `run_id`.

## D. Artifact identity and binding requirements

All JSON artifact digests in this contract MUST use lowercase hexadecimal SHA-256 over RFC 8785 canonical UTF-8 bytes. Rendered output digest MUST use SHA-256 over the exact final output bytes. Identity inputs MUST exclude their own derived identity fields to avoid circular construction.

- **Record identity** binds evidence `run_id`, `activity_id`, canonical schema identity/version, and `record_sha256`.
- **Eligibility identity** binds contract version, decision ID and version, predecessor, consumer, exact record identity, profile constraint, decision, and exact allowed fields.
- **Selection identity** binds contract version, selection ID and version, predecessor, run context, consumer, exact profile identity, and every ordered entry including position and record digest.
- **Publication profile identity** binds contract version and the complete canonical profile policy. A human-readable name without a digest is insufficient.
- **Input digest** binds the ordered canonical digest list for the complete invocation bundle: run context, schema, records, effective eligibility chain artifacts, effective selection, and publication profile.
- **Output digest** binds the exact final participant-facing bytes, including their encoding and newline policy.
- **Run identity** binds `publication_run_id` to the evidence run, programme month, consumer, selection, profile, input digest, and outcome evidence.

Every reference MUST resolve to exactly one artifact with a matching recomputed digest. Missing artifacts, stale digests, duplicate logical identities with different content, conflicting exact identities, or cross-run/cross-consumer references fail closed.

Artifact identity and digest correctness MUST NOT be treated as independent proof of publication authority. Required external authority and lifecycle resolution remain separate gates.

## E. State model

The four states are independent and ordered only as gates:

1. **Approval**: source evidence review is complete; `qa_status` is `approved`; unresolved uncertainty is absent.
2. **Eligibility**: one effective newsletter decision permits the exact approved record revision and exact profile fields.
3. **Selection**: one effective artifact explicitly orders the exact eligible record revision for intended publication.
4. **Inclusion**: the complete profile projection passes fidelity and rendering-safety checks and is present in the successfully written output.

Approval MUST NOT imply eligibility. Eligibility MUST NOT imply selection. Selection MUST NOT imply inclusion. Inclusion MUST be recorded in generation evidence and MUST NOT be inferred from eligibility, selection, output text search, or file existence.

## F. Canonical admission requirements

After the candidate effective selection has been structurally resolved, but before eligibility resolution, projection, or rendering, every record referenced by that selection MUST:

1. be uniquely located in the closed input bundle;
2. validate against the exact supported canonical `schemas/activity.schema.json` artifact;
3. have a recomputed digest equal to its bound record digest;
4. have `qa_status: "approved"`;
5. have `uncertain_fields: []`; and
6. have no unresolved provenance or evidence finding that invalidates approval.

Unknown or unsupported record fields MUST fail canonical validation. A selected record that fails canonical admission causes a whole-run canonical validation failure; it MUST NOT be excluded to salvage output. Unselected invalid candidates MAY be reported as record-level findings but MUST NOT affect selection membership unless the declared closed-bundle contract requires all candidates to be canonical.

Schema validity proves shape only. It does not prove source accuracy, eligibility, selection, projection completeness, or publication safety.

## G. Newsletter-scoped eligibility requirements

The resolver MUST establish exactly one effective eligibility decision for every selected exact record identity. It MUST verify the complete immutable predecessor chain, monotonic versions, exact consumer, record, run, profile constraint, allowed fields, and any future externally authorized envelope required by an accepted authority contract.

Missing, malformed, stale, denied, revoked, ambiguous, cross-consumer, cross-record, cross-run, or profile-incompatible eligibility causes a whole-run eligibility resolution failure. An eligibility grant MUST NOT broaden the publication profile. The effective allowed-field set and profile allowlist MUST agree exactly under the future artifact schema; intersection-by-guessing is prohibited.

Eligibility decisions are append-only, versioned, immutable, and bound to exact record identities. Filename, timestamp, directory order, and `qa_status` do not establish eligibility precedence or authority.

## H. Selection integrity requirements

Selection resolution MUST complete before any record projection or rendering. Any selection integrity failure aborts the whole run and preserves the existing destination.

The resolver MUST reject:

- duplicate selected `activity_id` or exact record identities;
- duplicate, negative, non-integer, non-contiguous, missing, or array-position-mismatched order entries;
- unknown IDs;
- missing selected records;
- record digests that do not match the selected canonical records;
- selected records without uniquely effective compatible eligibility;
- eligibility that binds a different record revision, run, consumer, or profile;
- stale selection, eligibility, profile, schema, or run-context bindings;
- conflicting logical identities or one logical identity bound to multiple contents;
- broken, missing, cyclic, cross-scope, or ambiguous selection predecessor chains;
- implicit membership or order derived from an input array, filename, directory, timestamp, or generated artifact; and
- selected entries omitted from integrity accounting.

Selection integrity MUST be evaluated over the complete ordered selection. It MUST NOT silently remove a bad entry and continue.

## I. Publication profile

Only fields explicitly allowed by the exact publication profile MAY enter participant-facing projection data. Unknown profile fields, unsupported mappings, duplicate mappings, and fields present in a projection without an explicit profile rule fail closed.

The v0 candidate field vocabulary is:

| Source field | Default policy |
| --- | --- |
| `activity_title` | includable; normally required |
| `description` | includable; profile determines required/optional |
| `dates` | includable as the complete ordered structure; normally required |
| `dates[*].recurrence` | includable with its owning date entry; MUST NOT be silently dropped |
| `time` | includable; normally required |
| `venue` | includable; profile determines required/optional |
| `target_participants` | includable; preserves participant eligibility/audience meaning |
| `fee` | includable only as the complete ordered fee structure |
| `fee[*].fee_type` | includable with its owning fee; preserves fee audience/category |
| `quota` | includable; profile determines required/optional |
| `registration_method` | includable; profile determines required/optional |
| `registration_period` | includable; profile determines required/optional |
| `notes` | includable; profile determines required/optional |
| `category` | upstream grouping/editorial key only by default; not participant-facing unless a future profile explicitly permits it |
| `staff_in_charge` | excluded by default; MAY be enabled only by explicit profile policy |
| `source_reference` | prohibited from participant-facing output in every profile |

Required publication fields are determined only by the exact immutable profile, subject to mandatory contract prohibitions and fidelity rules. A profile MUST distinguish a safely omittable optional value from an invalid, empty, placeholder, ambiguous, or incomplete required value. Optional fields MAY be omitted only when the profile explicitly defines omission as safe and the entire field unit is omitted. Absence MUST NOT acquire inferred participant-facing meaning.

Profile versions are immutable. Additive or corrective changes create a new profile identity and digest; mutation under an existing version is prohibited.

## J. Projection fidelity requirements

Projection MUST be deterministic and field-allowlisted. It MUST preserve source-supported participant meaning and MUST NOT infer missing facts.

- The complete ordered `dates` array MUST be projected without reordering, truncation, or ambiguous flattening.
- `recurrence` MUST remain associated with its owning date entry and MUST NOT be dropped when present and allowed.
- Multiple sessions or date/time relationships MUST remain unambiguous. A profile incapable of expressing them causes whole-record projection exclusion, not lossy flattening.
- The complete ordered fee array MUST preserve each `fee_type`, amount wording, conditions, and audience/category relationship. Fee audiences MUST NOT be collapsed into an unlabeled aggregate.
- Participant eligibility in `target_participants` MUST remain distinct from `fee_type`; neither may be substituted for the other.
- A required field that is empty, placeholder, ambiguous, incomplete, or unsupported makes the whole record publication-incomplete.
- A publication-incomplete record MUST NOT be partially rendered. If partial generation is permitted, the entire record is excluded with a structured reason.
- Projections MUST contain no field outside the exact profile allowlist and MUST NOT contain `source_reference`.

## K. Failure taxonomy

The future result contract MUST distinguish at least these failure classes:

| Failure class | Boundary | Required effect |
| --- | --- | --- |
| `record_exclusion` | one otherwise admitted selected record is publication-incomplete or has a record-local safe-projection/rendering defect | exclude the whole record only after all run-integrity gates pass; emit finding |
| `selection_integrity_failure` | membership, order, completeness, identity, or selection-chain integrity | abort whole run |
| `canonical_validation_failure` | a selected record is not canonical or digest-bound | abort whole run |
| `eligibility_resolution_failure` | effective newsletter eligibility is absent, invalid, stale, ambiguous, denied, or mismatched | abort whole run |
| `publication_profile_failure` | profile identity, schema, allowlist, mapping, version, or binding is invalid or unsupported | abort whole run |
| `projection_failure` | deterministic faithful projection cannot be produced | record exclusion only when record-local and profile-authorized; otherwise abort whole run |
| `rendering_safety_failure` | content cannot be safely normalized/escaped or renderer invariants fail | record exclusion only when demonstrably record-local; systemic failure aborts whole run |
| `provenance_evidence_failure` | source, record, run, artifact, identity, or digest binding is missing or invalid | abort whole run |

Failures MUST be assigned to their primary boundary. One generic error string MUST NOT replace enumerable structured findings.

## L. Outcome taxonomy

Exactly one outcome is required:

- **`complete_generation`**: selection integrity and every other run gate pass; every selected record is included; `excluded_count` is zero; output is atomically installed.
- **`partial_generation`**: every run-integrity gate passes, at least one selected record is included, and one or more entire records are excluded only for permitted record-level projection/completeness or record-local rendering-safety reasons. Every exclusion is structured and output is atomically installed.
- **`integrity_failure`**: a canonical, eligibility, selection, provenance, systemic projection/rendering, evidence, or output-installation gate fails. No new participant-facing artifact replaces the destination.

Partial generation is allowed only for record-level exclusions after selection integrity, canonical admission, eligibility resolution, identity binding, and run provenance have all passed. Selection integrity failure always aborts the whole run. An explicit empty selection may produce `complete_generation` with zero included records; it is not partial generation.

Silent exclusion is prohibited in every outcome.

## M. Structured findings and generation evidence contract

A future implementation MUST emit one versioned machine-readable generation-evidence artifact. Its schema and storage path are deferred to implementation-contract work. At minimum it MUST contain:

- contract version and status/outcome;
- `input_count`, `selected_count`, `included_count`, and `excluded_count`;
- ordered included IDs and ordered excluded IDs;
- findings with stable machine-readable `reason_code`, failure class, record/selection position when applicable, artifact identity, field/path when applicable, and a human-readable message;
- canonical schema identity and digest;
- record, effective eligibility, selection, and publication-profile identities and digests;
- input digest and output digest, with output digest absent on integrity failure before a complete output exists;
- `publication_run_id`, evidence `run_id`, programme month, and consumer identity; and
- destination class and write outcome without embedding untrusted participant text as provenance.

Counts MUST reconcile:

- `input_count` is the number of candidate activity records explicitly enumerated by the closed input bundle;
- `selected_count` is the number of entries in the uniquely effective ordered selection;
- `included_count` is the number of selected entries actually rendered; and
- `excluded_count` is the number of selected entries wholly excluded under permitted partial-generation rules;
- `selected_count == included_count + excluded_count` for complete or partial generation;
- ordered included and excluded identities MUST partition the ordered selection without duplicates;
- `complete_generation` requires `excluded_count == 0`; and
- an integrity failure MUST NOT claim successful inclusion or destination replacement.

Reason codes are stable API values within a contract major version. A code MUST NOT be reused with different semantics. Additive codes require a compatible contract revision; removal, reassignment, or semantic broadening requires a new major contract version. Unknown reason codes fail closed for consumers that make publication decisions; evidence-only readers MAY preserve and display them as unsupported.

## N. Rendering safety requirements

Participant-controlled or source-controlled text MUST be treated as data, never trusted Markdown structure or provenance.

- Markdown-significant characters and line structure MUST be deterministically escaped or normalized under the exact profile.
- Values MUST NOT forge headings, lists, block quotes, links, fenced code blocks, or raw HTML structures.
- Activity identifiers or text MUST NOT forge or close comments, front matter, metadata, or provenance blocks.
- Trusted provenance MUST remain outside user-controlled participant text and be bound in the generation-evidence artifact.
- Raw HTML comments MUST NOT be the sole provenance mechanism.
- Unsupported control characters, encodings, normalization cases, or structures MUST fail closed at the narrowest proven boundary without partial record rendering.

## O. Output write requirements

The complete output bytes and generation evidence MUST be constructed and validated before destination mutation. A future writer MUST:

1. render to a temporary file on the destination filesystem;
2. flush language/runtime buffers;
3. `fsync` file data where the platform and filesystem support it;
4. validate the exact temporary bytes and compute their output digest;
5. atomically replace the destination;
6. `fsync` the containing directory where applicable; and
7. report any durability limitation explicitly.

Admission, projection, rendering, temporary write, validation, or replacement failure MUST preserve the existing destination. Direct truncating writes to the destination are prohibited. Cross-device replacement and fallback copy-overwrite MUST fail closed unless a future contract explicitly defines equivalent recoverability.

## P. Golden artifact and regression policy

Future implementation acceptance MUST include wholly fictional fixtures under:

- `examples/contract-fixtures/newsletter-publication-boundary/v0/input/`
- `examples/contract-fixtures/newsletter-publication-boundary/v0/golden/fictional-newsletter.md`
- `examples/contract-fixtures/newsletter-publication-boundary/v0/golden/generation-evidence.json`

At least one automated test MUST regenerate the participant-facing artifact and compare exact bytes, including encoding and newline policy, with the tracked golden newsletter. A separate semantic test MUST validate the structured evidence and all digests. Any byte drift requires explicit fixture review; substring assertions alone are insufficient.

A force-added artifact from an ignored runtime output directory MUST NOT be the only golden evidence. Goldens belong in the explicit fictional fixture paths and MUST contain no real centre data.

## Q. Compatibility with the precursor guard

The precursor `Newsletter CLI Batch Admission Guard v0` at commit `c6680f6128ec99443bcb348d99d37873785faef5` rejects non-list, empty, mixed-status, and uncertain CLI batches before rendering. It is necessary but insufficient defense in depth.

That temporary guard:

- is not canonical schema admission;
- is not newsletter-scoped or consumer-scoped eligibility;
- is not publication selection or publication authority;
- does not establish profile fidelity, safe rendering, provenance, structured findings, atomic replacement, or golden assurance; and
- MUST NOT be treated as satisfying any later gate solely because `qa_status == "approved"` and `uncertain_fields == []`.

A future implementation MAY retain the guard as an early diagnostic check, but all contract gates in this document remain independently mandatory.

## R. Deferred work

This contract explicitly defers:

- DOCX generation;
- PDF generation;
- images and other media;
- visual layout and pagination;
- generic template engines;
- generic policy engines;
- deployment and packaging for production;
- web publishing;
- multi-project abstraction;
- agent-executor changes;
- GitHub Actions or other CI changes;
- real centre data, real eligibility, real selection, and real publication; and
- implementation or activation of any runtime publication behavior.

## S. Acceptance criteria for future implementation

A future implementation is not accepted until all of the following are demonstrated on one exact reviewed head:

1. executable schemas or equivalent strict validators exist for eligibility, ordered selection, publication profile, and generation evidence;
2. every selected record is canonically validated and digest-bound before publication;
3. approval, uncertainty, eligibility, selection, and inclusion remain separate tested states;
4. eligibility is uniquely resolved for the exact record, run, consumer, and profile;
5. selection order is explicit and every integrity failure in Section H aborts the run;
6. publication profile allowlists, required/optional rules, and prohibited fields fail closed for unknown values;
7. projections preserve recurrence, multi-session meaning, fee types/audiences, and all required participant-facing facts;
8. incomplete records are wholly excluded only under permitted partial-generation rules and never partially rendered;
9. every exclusion and failure produces stable structured evidence, with all counts, identities, and digests reconciling;
10. Markdown injection and forged provenance negative cases pass;
11. temporary-write, failed-render, failed-fsync where simulatable, and atomic-replacement tests prove destination preservation;
12. fictional golden artifacts pass byte-for-byte regeneration and digest checks;
13. no test relies on real centre data;
14. documentation and implementation make no claim that approval alone grants publication authority;
15. full repository validation and required independent architecture/security review pass; and
16. the Owner separately accepts the implementation and any schema or runtime activation.

This draft grants no implementation authorization. Newsletter Publication Boundary v0 remains unimplemented until those criteria and repository governance are satisfied.
