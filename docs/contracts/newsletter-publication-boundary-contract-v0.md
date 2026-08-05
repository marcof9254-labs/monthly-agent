# Newsletter Publication Boundary Contract v0

Status: inactive contract draft; documentation only; not implemented, accepted, or runtime-active

Contract family: `newsletter-publication-boundary/v0`

Draft revision: 2

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
- **Evidence-findings artifact**: an immutable input that enumerates resolved and unresolved evidence findings for one exact evidence run and exact record revisions, including an affirmative no-unresolved-findings statement where applicable.
- **Partial-generation policy**: the immutable publication-profile rule that authorizes or prohibits whole-record exclusions and defines allowed stable reason codes and any minimum inclusion threshold.
- **Record-local failure**: a failure proven to arise solely from one record's admitted projected values under an explicitly enumerated record-local reason code and authorized exclusion policy.
- **Systemic failure**: any failure of a shared component or invariant, any failure whose locality cannot be proven, or any unknown or unsupported failure. Systemic classification is the default.
- **Destination class**: the immutable run-context classification of the output target. `fixture` permits only a declared non-production fictional-fixture destination; `production` denotes a real participant-facing destination and requires authenticated Owner authority. Unknown classes fail closed.
- **Destination identity**: a system-assigned stable logical ID for one exact output target, resolved independently of participant-controlled record text and bound to its destination class.
- **Prepared state**: durable intent evidence created before destination mutation and binding the proposed output and operation.
- **Finalized state**: durable evidence written after an installation attempt that records its observed result.
- **Unknown state**: durable or reconstructible state used when installation or finalization cannot be determined reliably. It never establishes successful publication.
- **Installation state**: exactly one of `not_attempted` (destination mutation did not begin), `installed` (replacement is known to have completed), `not_replaced` (an attempted operation is known not to have replaced the destination), or `unknown` (neither installed nor not-replaced can be established durably).
- **Durability capability class**: a stable enumeration of the platform/filesystem guarantees actually available to the writer, as defined in Section O.
- **Closed input bundle**: the immutable, explicitly enumerated set of run context, schema, candidate records, evidence-findings, eligibility chains, effective selection chain, and publication profile admitted for one invocation.
- **Authority-resolution snapshot**: the immutable invocation input that enumerates the complete same-scope eligibility and selection chains, their uniquely resolved effective tips, the exact profile reference, and the destination generation/fencing state used for current-state decisions.
- **Stale artifact**: a structurally and cryptographically valid historical artifact presented or referenced as the current effective same-scope artifact after a uniquely resolved later successor has superseded it in the invocation's authority-resolution snapshot.
- **Destination generation/fencing state**: authenticated immutable state for one destination identity containing a non-negative `destination_generation`, either a totally ordered `fencing_token` or single-use compare-and-swap token, and `current_output_sha256` as a lowercase digest or the stable sentinel `absent`. A future mechanism may choose the token form but MUST preserve equivalent current-versus-stale discrimination.
- **Stale invocation**: an invocation whose prepared expected destination generation/fencing state or authenticated authority state is no longer current immediately before replacement.
- **Installation-right precondition**: the fail-closed proof, evaluated immediately before replacement, that the invocation's authenticated expected destination generation/fencing state still equals the current observed state and grants this invocation current installation authority.
- **Same scope**: exact equality of the lifecycle key for the artifact type. Eligibility scope is evidence `run_id` + exact record identity + consumer + exact profile logical ID/digest. Selection scope is evidence `run_id` + programme month + consumer + exact profile logical ID/digest + destination identity/class. Destination scope is destination identity + destination class within the authenticated authority namespace.

## C. Input artifacts

A future publication invocation MUST receive a closed, explicitly enumerated input bundle. Directory presence, filename order, timestamps, input array order, and previously generated output MUST NOT establish authority, membership, or precedence.

Eligibility, selection, and profile artifacts MUST be authenticated through an accepted owner-authority mechanism before production use. Content hashes prove integrity and binding only; they do not self-authenticate an owner decision. This draft neither selects nor activates an operational authority-delivery mechanism.

### Canonical activity records

Each candidate record MUST identify its evidence `run_id`, validate independently against the supported canonical activity schema, and have a lowercase SHA-256 digest over RFC 8785 canonical UTF-8 JSON bytes. The bundle MUST identify the exact schema artifact or immutable schema version used for admission.

The canonical records remain evidence. Their `qa_status` and `uncertain_fields` values are admission facts, not newsletter authority.

### Evidence-findings artifact

The closed bundle MUST contain exactly one immutable evidence-findings artifact for the exact evidence `run_id`. It MUST bind every applicable exact record revision, enumerate unresolved and resolved findings, identify each finding's stable identity and disposition, and affirmatively state when no applicable unresolved findings exist for a bound record and for the run.

The artifact MUST be complete for the candidate record set and digest-bound into the complete input digest. Missing, malformed, run/record-revision-mismatched, ambiguous, incomplete, duplicate, or unresolvable evidence-findings input causes `provenance_evidence_failure` and aborts the whole run. No-unresolved-findings status MUST NOT be inferred from artifact absence, an empty directory, a missing record entry, or a missing findings array.

### Newsletter eligibility artifact

Each eligibility artifact MUST bind one exact record identity, `consumer_id: "newsletter-renderer"`, one exact immutable publication-profile logical ID and digest, an exact allowed source-field set, a decision (`eligible` or `denied`), a positive version, and a predecessor identity or `null`.

Eligibility artifacts MUST be immutable, append-only, and versioned. Correction, denial, or revocation MUST create a successor; mutation in place is prohibited. Resolution MUST produce one unique effective same-scope tip. Eligibility for any other consumer MUST NOT transfer to newsletters.

Any different publication-profile logical ID or digest requires a separate eligibility decision. Profile-family membership, compatibility inheritance, additive-version compatibility, and profile widening are prohibited in v0.

### Ordered publication selection artifact

The selection artifact MUST bind one run context, one exact publication profile, and an ordered `entries` array. Every entry MUST contain an explicit zero-based `position`, `activity_id`, and exact record digest. Positions MUST be contiguous from zero, unique, and equal to array position. This redundant binding makes order explicit and verifiable.

Input record order, eligibility order, filesystem enumeration, and projection generation order MUST NOT become publication order. An intentionally empty publication requires a valid selection with `entries: []`.

Selections MUST be immutable, append-only, and versioned, with a unique same-scope effective tip resolved through an explicit predecessor chain. A successor replaces the complete ordered intent; it does not patch an earlier array in place.

### Publication profile

The publication profile MUST be a versioned, immutable artifact. It MUST define its identity, contract version, consumer, allowed source fields, participant-facing mappings, required and optional fields, omission rules, structural rendering rules, prohibited fields, and `partial_generation_policy`. Profiles MUST NOT be selected from user-controlled record text.

### Run identity and context

The invocation MUST bind an explicit `publication_run_id`, evidence `run_id`, programme month, consumer, locale, profile identity, selection identity, destination identity, destination class, and authority-resolution snapshot. Destination class MUST be exactly `fixture` or `production`; unknown or unsupported classes fail closed. A `fixture` destination MUST be technically isolated from every real or production destination. Programme month MUST come from authoritative run context and MUST NOT be inferred solely by parsing `run_id`.

Destination identity and class MUST be bound through the exact authenticated selection/run-context relationship, digest-protected in the closed input bundle, and included in authenticated authority scope. Participant-controlled record text MUST NOT select, derive, redirect, or alter a destination. In production-capable mode, Owner authority MUST cover the intended destination identity, destination class, and exact destination scope.

## D. Artifact identity and binding requirements

All JSON artifact digests in this contract MUST use lowercase hexadecimal SHA-256 over RFC 8785 canonical UTF-8 bytes. Rendered output digest MUST use SHA-256 over the exact final output bytes. Every artifact MUST distinguish its owner/system-assigned logical ID from its derived canonical content digest. Every versioned artifact MUST contain a positive integer version. Eligibility and selection artifacts MUST contain an explicit predecessor logical-ID reference or `null`; every artifact without a predecessor chain MUST state that predecessor is not applicable or use a future schema's explicit nullable predecessor field. No logical ID or digest may include itself in its derivation.

- **Record artifact** contains an upstream-assigned `activity_id`, its evidence `run_id`, schema version, and positive record revision; `record_sha256` is derived from the complete canonical record content and those identity inputs, excluding `record_sha256` itself.
- **Canonical schema artifact** contains its assigned schema `$id` and supported positive schema version; `schema_sha256` is derived from the exact schema bytes and excludes itself. Schema lineage is referenced by version, so predecessor is not applicable in v0.
- **Run-context artifact** contains a system-assigned `run_context_id`, positive version, evidence `run_id`, programme month, consumer, locale, destination identity, and destination class; `run_context_sha256` is derived from its complete canonical content and excludes itself. Predecessor is not applicable in v0.
- **Authority-resolution snapshot artifact** contains a system-assigned `authority_resolution_snapshot_id`, positive version, complete same-scope chain membership and effective tips, exact profile reference, destination identity/class, and destination generation/fencing state; `authority_resolution_snapshot_sha256` is derived from its complete canonical content and excludes itself. Its eligibility-chain arrays use selection-position then root-to-tip order, and its selection-chain array uses root-to-tip order. Predecessor is not applicable because it is an invocation snapshot, not an authority chain.
- **Eligibility artifact** contains an owner-assigned `eligibility_id`, positive `eligibility_version`, and `predecessor_eligibility_id` or `null`; `eligibility_sha256` is derived from its complete canonical content, excluding `eligibility_sha256` itself.
- **Selection artifact** contains an owner-assigned `selection_id`, positive `selection_version`, and `predecessor_selection_id` or `null`; `selection_sha256` is derived from its complete canonical content including ordered entries, excluding `selection_sha256` itself.
- **Evidence-findings artifact** contains a system-assigned `evidence_findings_id`, positive version, and exact run/record references; `evidence_findings_sha256` is derived from its complete canonical content, excluding that digest itself.
- **Publication profile artifact** contains an owner-assigned `publication_profile_id` and positive `profile_version`; `publication_profile_sha256` is derived from the complete canonical profile policy, excluding that digest itself. A human-readable name is not identity.
- **Closed input-bundle artifact** contains a system-assigned `input_bundle_id`, positive version, and references the run context and every enumerated artifact; `input_sha256` is derived by the exact ordering rules below and excludes `input_sha256` itself. Predecessor is not applicable in v0.
- **Participant-facing output artifact** contains a system-assigned `output_id`, positive `output_version`, and references `publication_run_id`; `output_sha256` is derived from the exact final output bytes, including their encoding and newline policy, and cannot contain itself. Predecessor is not applicable in v0.
- **Publication run** contains a system-assigned `publication_run_id`, positive `publication_run_version`, and references the evidence run, programme month, consumer, destination, selection, and profile. Predecessor is not applicable in v0. The assigned ID is not derived from generation evidence. Prepared and finalized generation-evidence artifacts reference `publication_run_id`; their content digests are derived from their own canonical content while excluding their own digest fields. This one-way relationship prevents circular identity construction.
- **Prepared generation-evidence artifact** contains a system-assigned `prepared_evidence_id`, positive version, and references `publication_run_id`; `prepared_evidence_sha256` is derived from its complete canonical content and excludes itself. Predecessor is not applicable.
- **Finalized generation-evidence artifact** contains a system-assigned `finalized_evidence_id`, positive version, and references the exact prepared logical ID and digest; `finalized_evidence_sha256` is derived from its complete canonical content and excludes itself. Its prepared reference is an association, not a predecessor chain.

Every reference MUST resolve to exactly one artifact with a matching recomputed digest. Missing artifacts, mismatched digests, duplicate logical identities with different content, conflicting exact identities, or cross-run/cross-consumer references fail closed.

Artifact identity and digest correctness MUST NOT be treated as independent proof of publication authority. Required external authority and lifecycle resolution remain separate gates.

### Canonical `input_sha256` ordering

`input_sha256` MUST be derived from RFC 8785 canonical UTF-8 bytes of one identity-input array containing these tagged categories in exactly this order:

1. `run_context`: the exact run-context logical ID, version, and digest;
2. `canonical_schema`: the exact schema logical ID, version, and digest;
3. `candidate_records`: the complete candidate-record identity entries in the order defined below;
4. `evidence_findings`: the evidence-findings logical ID, version, digest, and its ordered record bindings;
5. `effective_eligibility`: the effective eligibility chains in the order defined below;
6. `effective_selection`: the complete selection chain ordered root-to-tip by positive version and verified predecessor relation, followed by the exact effective-tip logical ID, version, digest, and authoritative ordered entries;
7. `publication_profile`: the exact profile logical ID, version, and digest; and
8. `authority_destination_state`: the authority-resolution snapshot logical ID, version, and digest plus the expected destination identity, class, generation/fencing value, and expected destination digest/state.

Candidate activity records MUST be sorted lexicographically by this exact record-identity tuple, comparing Unicode strings by code point and digests by lowercase hexadecimal byte value:

1. evidence `run_id`;
2. `activity_id`;
3. canonical schema logical ID;
4. canonical schema version; and
5. `record_sha256`.

Evidence-findings record bindings MUST be sorted by the same exact record-identity tuple. Their finding arrays MUST use the stable finding identity order defined by the future evidence-findings schema; a schema without that deterministic order cannot satisfy this contract.

Each effective eligibility chain MUST be associated with one exact selected record identity. Chains MUST be ordered by the record's authoritative selection position. Within a chain, artifacts MUST be ordered root-to-tip by positive version and verified predecessor relation; version alone MUST NOT repair a broken predecessor relation. Eligibility artifacts relating only to unselected candidates MUST NOT be admitted to the closed input bundle and MUST NOT contribute to `input_sha256`.

Input array order, filesystem enumeration, filename, timestamp, and map/object iteration order MUST NOT affect category membership or ordering. Physically different enumerations of one identical closed bundle MUST produce one identical `input_sha256`.

### Staleness and effective-state resolution

The authority-resolution snapshot is the sole immutable invocation context for deciding effective eligibility and selection tips and destination generation/fencing state. A valid predecessor retained as root-to-tip chain history is not stale merely because it is older. `stale` applies only when a valid superseded artifact is incorrectly presented or referenced as effective/current.

- A malformed, cyclic, gapped, or predecessor-inconsistent chain uses the applicable `*_chain_invalid` reason.
- Multiple unresolved effective tips use the applicable `*_ambiguous` reason.
- Exact record, profile, or consumer mismatches use their dedicated `*_record_mismatch`, `*_profile_mismatch`, or `*_consumer_mismatch` reason.
- A uniquely superseded eligibility artifact presented as effective uses `eligibility_stale`.
- A uniquely superseded selection artifact presented as effective uses `selection_stale` under `selection_integrity_failure`.
- Publication profiles in v0 have immutable exact identities but no succession or current-tip model. A different profile uses `eligibility_profile_mismatch` or `publication_profile_failure`, not stale.
- Canonical schema and run-context references in v0 have no successor/current-tip model. Invalid or mismatched references use canonical or provenance failure, not stale.

Tests MUST distinguish valid predecessor history, a stale superseded effective artifact, ambiguous tips, broken chains, and exact identity mismatches.

## E. State model

The four states are independent and ordered only as gates:

1. **Approval**: source evidence review is complete; `qa_status` is `approved`; unresolved uncertainty is absent.
2. **Eligibility**: one effective newsletter decision permits the exact approved record revision and exact profile fields.
3. **Selection**: one effective artifact explicitly orders the exact eligible record revision for intended publication.
4. **Inclusion**: the complete profile projection passes fidelity and rendering-safety checks and is present in the successfully written output.

Approval MUST NOT imply eligibility. Eligibility MUST NOT imply selection. Selection MUST NOT imply inclusion. Inclusion MUST be recorded in generation evidence and MUST NOT be inferred from eligibility, selection, output text search, or file existence.

### Normative pipeline order

The future pipeline MUST execute these phases in this order:

1. closed-bundle and artifact structural admission;
2. effective selection structural resolution, including chain, identity, ordered positions, membership references, and digest structure that do not depend on eligibility semantics;
3. canonical admission of every explicitly enumerated candidate record;
4. evidence-findings resolution for the exact run and record revisions;
5. newsletter eligibility resolution;
6. semantic selection and publication-profile compatibility checks;
7. deterministic projection;
8. rendering execution;
9. rendering-safety validation;
10. complete output and prepared-evidence validation;
11. durable prepared/intent-state persistence;
12. installation-right precondition followed immediately by the destination installation attempt; and
13. evidence finalization or explicit unknown-state recording.

No phase may use success from a later phase to repair or authorize an earlier phase. Rendering execution MUST NOT begin before phases 1–7 pass. Rendering-safety validation MUST NOT precede completed rendering execution. Destination mutation MUST NOT begin before phases 1–11 pass, and replacement MUST immediately follow a successful phase 12 installation-right precondition without an intervening operation that can invalidate the observed current state.

## F. Canonical admission requirements

Every candidate record explicitly enumerated by the closed input bundle MUST:

1. be uniquely located in the closed input bundle;
2. validate against the exact supported canonical `schemas/activity.schema.json` artifact;
3. have a recomputed digest equal to its bound record digest;
4. have `qa_status: "approved"`;
5. have `uncertain_fields: []`.

Unknown or unsupported record fields MUST fail canonical validation. Any candidate record that fails canonical admission causes a whole-run canonical validation failure; it MUST NOT be ignored or excluded to salvage output. This rule defines the complete closed-bundle scope and admits no policy-controlled exception for unselected candidates.

Schema validity proves shape only. It does not prove source accuracy, eligibility, selection, projection completeness, or publication safety.

### Evidence-findings resolution

After canonical admission, the resolver MUST validate the evidence-findings artifact and its complete run/record coverage. An **unresolved evidence finding** is an applicable finding whose artifact disposition is explicitly `unresolved`, whose claimed resolution does not bind the admitted exact record revision, or whose resolution evidence cannot be validated. A **resolved evidence finding** has an explicit `resolved` disposition and resolution reference bound to the admitted exact record revision. Unknown dispositions fail closed.

Every selected record and the evidence run MUST have an affirmative, artifact-bound statement that no applicable unresolved findings remain. Any applicable unresolved finding prohibits that record from proceeding and causes `provenance_evidence_failure` for the whole run. The absence of a finding, record entry, resolution reference, or artifact never proves resolution.

## G. Newsletter-scoped eligibility requirements

The resolver MUST establish exactly one effective eligibility decision for every selected exact record identity. It MUST verify the complete immutable predecessor chain, monotonic versions, exact consumer, record, run, exact publication-profile logical ID and digest, allowed fields, and any future externally authorized envelope required by an accepted authority contract.

Missing, malformed, stale, denied, revoked, ambiguous, cross-consumer, cross-record, cross-run, or exact-profile-mismatched eligibility causes a whole-run eligibility resolution failure. `eligibility_profile_mismatch` applies whenever either the profile logical ID or digest differs. An eligibility grant MUST NOT broaden the publication profile. The effective allowed-field set and profile allowlist MUST agree exactly under the future artifact schema; intersection-by-guessing is prohibited.

Eligibility decisions are append-only, versioned, immutable, and bound to exact record identities. Filename, timestamp, directory order, and `qa_status` do not establish eligibility precedence or authority.

Within `eligibility_resolution_failure`, the primary finding MUST use one of these stable reason codes where applicable:

- `eligibility_missing`
- `eligibility_denied`
- `eligibility_revoked`
- `eligibility_stale`
- `eligibility_ambiguous`
- `eligibility_chain_invalid`
- `eligibility_consumer_mismatch`
- `eligibility_record_mismatch`
- `eligibility_profile_mismatch`
- `eligibility_invalid`

A valid Owner denial or revocation MUST remain distinguishable from malformed, incomplete, or corrupted eligibility evidence. `eligibility_invalid` covers malformed, incomplete, corrupted, or otherwise unsupported eligibility evidence and MUST NOT be mislabeled as denial or revocation.

## H. Selection integrity requirements

Selection integrity has two ordered phases. Structural resolution in normative phase 2 establishes the unique chain, artifact identities, ordered positions, and resolvable membership references without assuming eligibility. Semantic checks in normative phase 6 validate the already admitted records, resolved eligibility, and exact profile compatibility. Both MUST complete before projection or rendering. Any selection integrity failure aborts the whole run and preserves the existing destination before installation begins.

The resolver MUST reject:

- duplicate selected `activity_id` or exact record identities;
- duplicate, negative, non-integer, non-contiguous, missing, or array-position-mismatched order entries;
- unknown IDs;
- missing selected records;
- record digests that do not match the selected canonical records;
- selected records without uniquely effective compatible eligibility;
- eligibility that binds a different record revision, run, consumer, or profile;
- stale selection or eligibility effective bindings;
- mismatched profile, schema, or run-context identities/digests;
- conflicting logical identities or one logical identity bound to multiple contents;
- broken, missing, cyclic, cross-scope, or ambiguous selection predecessor chains;
- implicit membership or order derived from an input array, filename, directory, timestamp, or generated artifact; and
- selected entries omitted from integrity accounting.

Selection integrity MUST be evaluated over the complete ordered selection. It MUST NOT silently remove a bad entry and continue.

## I. Publication profile

Only fields explicitly allowed by the exact publication profile MAY enter participant-facing projection data. Unknown profile fields, unsupported mappings, duplicate mappings, and fields present in a projection without an explicit profile rule fail closed.

Every profile MUST contain `partial_generation_policy` with exactly these minimum semantics:

- `allow_partial_generation`: an explicit boolean;
- `allowed_record_local_reason_codes`: a unique array of stable reason codes enumerated by the applicable result contract;
- `minimum_included_count`: a non-negative integer or explicit `null` when no count threshold is required; and
- `minimum_included_ratio`: a number from 0 through 1 inclusive or explicit `null`, calculated as `included_count / selected_count` for a non-empty selection.

Partial generation is authorized only when `allow_partial_generation` is `true`, every excluded record has an allowed proven record-local reason code, and all non-null thresholds are met. A missing, malformed, unsupported, internally inconsistent, or non-authorizing policy prohibits partial generation. Under that default-deny condition, any otherwise excludable record escalates the run to `integrity_failure`; an implementation MUST NOT supply a permissive default. A non-empty selection can never satisfy partial-generation policy with `included_count == 0`.

Every profile MUST also define versioned executable deterministic `incompleteness_predicates` for each allowed field. The predicates MUST classify, using only deterministic operations enumerated by the future accepted profile schema, at least: empty required value, placeholder value, ambiguous value, incomplete value, and unsupported value shape. Each predicate MUST have a stable predicate ID, explicit applicable field paths, deterministic inputs, and a declared result. Unknown predicate IDs, missing required predicates, unsupported operations, or implementation-defined heuristics cause `publication_profile_failure`. Free-form model judgment, probabilistic inference, and unstated semantic guessing MUST NOT determine publication completeness.

The v0 candidate field vocabulary is:

| Source field | Default policy |
| --- | --- |
| `activity_title` | includable; normally required |
| `description` | includable; profile determines required/optional |
| `dates` | includable as the complete ordered structure; normally required; allowing it requires recurrence support |
| `dates[*].recurrence` | MUST be allowed whenever `dates` is allowed and MUST remain with its owning entry |
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

A profile that allows `dates` MUST support and allow `dates[*].recurrence`. A profile that disallows or does not define support for present recurrence is invalid during semantic profile compatibility checks and aborts the run with `publication_profile_failure`. If a valid profile supports recurrence but one admitted record contains a value shape that the profile explicitly classifies as publication-incomplete, the whole record may be excluded only under an authorized stable record-local reason. A projection implementation that fails to honor a valid supported recurrence rule has a systemic `projection_failure`. Recurrence MUST never be silently dropped.

A profile that allows `fee` MUST support and allow the complete ordered fee structure, including `fee[*].fee_type` and every source-supported fee audience/category relationship. If `fee_type` or another audience/category value is present, it MUST remain attached to its owning fee entry. A profile that allows `fee` but omits or cannot represent the required fee type/audience structure is invalid during semantic profile compatibility checks and aborts with `publication_profile_failure`. Fee audience/type MUST never be flattened, detached, merged without labels, or inferred.

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
| `record_exclusion` | one otherwise admitted selected record is publication-incomplete or has a proven record-local value rejection | exclude the whole record only after all run-integrity gates pass and policy authorization; emit finding |
| `selection_integrity_failure` | membership, order, completeness, identity, or selection-chain integrity | abort whole run |
| `canonical_validation_failure` | a selected record is not canonical or digest-bound | abort whole run |
| `eligibility_resolution_failure` | effective newsletter eligibility is absent, invalid, stale, ambiguous, denied, or mismatched | abort whole run |
| `publication_profile_failure` | profile identity, schema, allowlist, mapping, version, or binding is invalid or unsupported | abort whole run |
| `partial_generation_policy_failure` | a valid profile prohibits partial output or its inclusion threshold is not met | abort whole run before prepared intent |
| `projection_failure` | deterministic faithful projection cannot be produced | record exclusion only for an enumerated value-local reason authorized by policy; shared projector defects abort the run |
| `rendering_safety_failure` | admitted content cannot be rendered safely or a renderer/escaping invariant fails | record exclusion only for an enumerated value-local rejection authorized by policy; invariant failures abort the run |
| `provenance_evidence_failure` | source, record, run, artifact, identity, or digest binding is missing or invalid | abort whole run |
| `output_installation_failure` | durable intent, capability, replacement, finalization, or observed installation state fails | abort whole run and report `not_attempted`, `not_replaced`, or `unknown` exactly as observed |

A failure is record-local only when all of these conditions are proven:

1. it maps to an explicitly enumerated stable record-local reason code;
2. it is caused solely by that record's admitted projected values;
3. no renderer, normalizer, escaping, profile, cross-record, environment, durability, or output-installation invariant failed; and
4. excluding the whole record is explicitly authorized by the exact `partial_generation_policy`, including its thresholds.

Unexpected exceptions, renderer or escaping invariant failures, normalization implementation defects, profile interpretation defects, cross-record inconsistency, nondeterminism, environment or installation failures, failures whose locality cannot be proven, and unknown or unsupported failure reasons are systemic and abort the whole run. Multiple occurrences of one reason code do not by themselves prove either record-local or systemic scope. Default classification is systemic.

Primary failure classification is deterministic: the primary class is the class assigned to the earliest normative pipeline phase that detects the defect. Within that phase, the primary class is assigned by the accountable boundary below:

- phase 1 structural bundle, identity, digest, or run-context defects: `provenance_evidence_failure`; structurally malformed profile artifacts: `publication_profile_failure`;
- phase 2 selection chain, reference, membership, or order defects: `selection_integrity_failure`;
- phase 3 schema, candidate-record uniqueness, or record-digest defects: `canonical_validation_failure`;
- phase 4 evidence-findings coverage, disposition, identity, or binding defects: `provenance_evidence_failure`;
- phase 5 eligibility defects: `eligibility_resolution_failure` with the Section G reason code;
- phase 6 selection-to-record/eligibility/profile mismatch: `selection_integrity_failure`; invalid profile semantics or policy: `publication_profile_failure`;
- phase 7 value-local incomplete projection: `record_exclusion` when policy-authorized and `partial_generation_policy_failure` when exclusion is not authorized; projector invariant or systemic fidelity defect: `projection_failure`;
- phase 8 value-local rendering rejection: `record_exclusion` when policy-authorized and `partial_generation_policy_failure` when exclusion is not authorized; renderer execution exception, invariant failure, or nondeterminism: `rendering_safety_failure`;
- phase 9 unsafe rendered structure, escaping, or normalization: `rendering_safety_failure`, except an explicitly enumerated policy-authorized record-local value rejection remains `record_exclusion`;
- phase 10 invalid completed output: `rendering_safety_failure`; invalid prepared-evidence binding: `provenance_evidence_failure`; unmet partial policy after counts are known: `partial_generation_policy_failure`; and
- phases 11–13 durability, intent persistence, installation-right, replacement, finalization, or unknown-state defects: `output_installation_failure`.

A run MUST NOT emit multiple competing primary classes. Later or related defects MAY be recorded as secondary findings, but they MUST NOT change the primary class or permit later processing to continue past an aborting gate. One generic error string MUST NOT replace enumerable structured findings where findings can be constructed.

## L. Outcome taxonomy

Exactly one outcome is required:

- **`complete_generation`**: selection integrity and every other run gate pass; every selected record is included; `excluded_count` is zero; output is atomically installed.
- **`partial_generation`**: every run-integrity gate passes, at least one selected record is included, and one or more entire records are excluded only for permitted record-level projection/completeness or record-local rendering-safety reasons. Every exclusion is structured and output is atomically installed.
- **`integrity_failure`**: a canonical, eligibility, selection, provenance, systemic projection/rendering, evidence, policy, or output-installation gate fails. Destination state is `not_attempted`, `not_replaced`, or `unknown`; it MUST NOT be reported more definitely than durable evidence supports.

Partial generation is allowed only for policy-authorized record-level exclusions after selection integrity, canonical admission, evidence-findings resolution, eligibility resolution, identity binding, and run provenance have all passed. Selection integrity failure always aborts the whole run.

If the effective selection is non-empty and `included_count == 0`, the outcome MUST be `integrity_failure` and the existing destination MUST be preserved. This condition is determined before prepared intent or installation, and no empty participant-facing artifact may replace the destination merely because every selected record was excluded. Only a valid explicitly empty selection may produce `complete_generation` with zero included records. Therefore all mathematically possible valid count states resolve as follows:

- `selected_count == 0`, `included_count == 0`, `excluded_count == 0`: `complete_generation` only for an explicitly empty valid selection;
- `selected_count > 0`, `included_count == selected_count`, `excluded_count == 0`: `complete_generation`;
- `selected_count > 0`, `included_count > 0`, `excluded_count > 0`: `partial_generation` only when exact policy authorization and thresholds pass, otherwise `integrity_failure`; and
- `selected_count > 0`, `included_count == 0`: `integrity_failure` regardless of exclusion reasons or policy thresholds.

Negative or non-integer counts, `selected_count > input_count`, or any successful-generation count set where `selected_count != included_count + excluded_count` is invalid and causes `integrity_failure`.

Silent exclusion is prohibited in every outcome.

## M. Structured findings and generation evidence contract

A future implementation MUST emit versioned machine-readable generation evidence through the prepared and finalized/unknown lifecycle in Section O. Exact schemas and storage paths are deferred to implementation-contract work. Taken together, the constructible evidence MUST contain at minimum:

- contract version and status/outcome;
- `input_count`, `selected_count`, `included_count`, and `excluded_count`;
- ordered included IDs and ordered excluded IDs;
- findings with stable machine-readable `reason_code`, failure class, record/selection position when applicable, artifact identity, field/path when applicable, and a human-readable message;
- canonical schema identity and digest;
- record, effective eligibility, selection, and publication-profile identities and digests;
- authority-resolution snapshot identity/digest and effective-tip identities;
- input digest and output digest, with output digest absent on integrity failure before a complete output exists;
- `publication_run_id`, evidence `run_id`, programme month, and consumer identity; and
- destination identity/class, expected and observed generation/fencing values and destination digests/states, temporary-byte digest verification, and write outcome without embedding untrusted participant text as provenance.

Generation evidence is a lifecycle with prepared, finalized, and unknown states as specified in Section O; it is not one assertion written optimistically before installation. When structural admission permits trustworthy construction, even `integrity_failure` MUST emit minimal failure evidence containing the contract version, `publication_run_id`, observed phase, primary failure class and reason code, known artifact identities/digests, and destination class/state. When trustworthy evidence cannot be constructed, the implementation MUST fail closed and emit a stable out-of-band diagnostic without claiming publication success.

If integrity failure occurs before a count can be established reliably, the affected count MUST be represented explicitly as `null` with a reason code; it MUST NOT be omitted, guessed, or reported as zero. `null` is not a valid count state for complete or partial generation.

Counts MUST reconcile:

- `input_count` is the number of candidate activity records explicitly enumerated by the closed input bundle;
- `selected_count` is the number of entries in the uniquely effective ordered selection;
- `included_count` is the number of selected entries actually rendered; and
- `excluded_count` is the number of selected entries wholly excluded under permitted partial-generation rules;
- `selected_count <= input_count`;
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

For one destination identity, installation authority MUST be exclusive and current: two invocations MUST NOT both retain unconditional authority to replace that destination. A successful installation MUST consume, advance, or otherwise fence its installation right so that an older prepared invocation cannot later overwrite it. The invariant MAY be implemented by single-writer serialization, destination lease, fencing token, compare-and-swap over authenticated destination digest/state, or an equivalent fail-closed mechanism; this contract does not select one mechanism.

The complete output bytes and prepared evidence MUST be constructed and validated before destination mutation. Evidence and output use this durable state protocol:

1. **Temporary output**: render to a temporary file on the destination filesystem under exclusive controlled access that prevents untrusted mutation during validation and installation. Flush runtime buffers, perform required file-data synchronization, and compute `output_sha256` from the final temporary bytes.
2. **Prepared / intent state**: durably persist an immutable prepared-evidence artifact before destination mutation. It MUST bind `publication_run_id`, input and output digests, all artifact logical IDs/versions/digests, proposed outcome, included and excluded IDs, destination identity/class, temporary-output identity, authority-resolution snapshot, expected destination generation/fencing value, expected current destination digest/state, and durability capability class.
3. **Installation-right precondition**: immediately before replacement, prove that the prepared authenticated installation right remains current by comparing its expected destination generation/fencing and digest/state with the freshly observed authenticated current values. File existence, timestamps, process-local memory, or an earlier check alone MUST NOT establish current installation authority.
4. **Installation attempt**: after and immediately adjacent to a successful precondition, recompute or verify `output_sha256` from the final temporary bytes while exclusive controlled access remains in force, then attempt one atomic replacement. No intervening operation may invalidate the observed destination state. Direct truncating writes, cross-device rename fallbacks, and copy-overwrite fallbacks are prohibited.
5. **Finalized state**: after the attempt, durably persist finalized evidence that references the prepared-evidence logical ID and digest and records `installed` or `not_replaced`, the expected and observed destination generation/fencing values and digests/states, the resulting generation/fencing state where installed, and completed durability operations.
6. **Unknown state**: if the system cannot determine whether replacement occurred, or cannot durably finalize the observed result after a potentially successful replacement, the matching operation state is `unknown`. An unfinalized prepared artifact is interpreted as unknown unless reliable reconciliation proves a narrower result.

An installation-right or destination-state precondition failure MUST classify as `output_installation_failure`, MUST preserve the destination, and MUST durably finalize as `not_replaced` with expected and observed destination/fencing evidence. An invocation prepared against an older destination or authority state is stale and MUST NOT replace output installed by a newer valid invocation.

Prepared evidence MUST NOT claim successful destination replacement. Finalized evidence MUST NOT report `installed` until replacement is known to have occurred and the installed destination bytes are corroboratable against `output_sha256`. A destination/temp/output digest mismatch makes the destination unverified and MUST NOT be reported as a verified installed artifact. A destination with missing, non-finalized, mismatched, or unknown matching evidence is unverified and MUST NOT be treated as published. A failure after a potentially successful replace MUST NOT be rewritten as a definite no-mutation failure. Automatic retry after unknown state MUST NOT blindly replace the destination and MUST NOT bypass fresh fencing/current-state checks; retry requires a future reconciliation design that first determines destination/output digest, authority-resolution snapshot, generation/fencing state, and evidence state. Reconciliation mechanics are deferred, but unknown-outcome detection and fail-closed reporting are mandatory.

Every invocation MUST select and record exactly one durability capability class:

- `durability_full`: file-data `fsync` completed, atomic replace is supported and used, and containing-directory `fsync` completed;
- `durability_file_sync_atomic_replace`: file-data `fsync` completed and atomic replace is supported and used, but directory `fsync` is unsupported and recorded as `unsupported`;
- `durability_atomic_replace_only`: atomic replace is supported and used, but file-data and/or directory `fsync` is unsupported and each unsupported operation is recorded; permitted only for `fixture` destinations; or
- `durability_unsupported`: atomic replacement is unavailable or the platform/filesystem capabilities cannot be established; installation MUST NOT be attempted.

The minimum class for a `production` destination is `durability_file_sync_atomic_replace`. The minimum class for a `fixture` destination is `durability_atomic_replace_only`. Evidence MUST separately record platform/filesystem capability class, whether file-data `fsync` was `completed` or `unsupported`, whether directory `fsync` was `completed` or `unsupported`, atomic-replace capability and observed use, and every durability degradation. Unsupported capability is a stable recorded value, not omission. Tests MUST cover every supported class and the `durability_unsupported` rejection path. No result may claim durability stronger than its recorded completed operations.

Admission, projection, rendering, temporary write, validation, or durable-intent failure before installation MUST preserve the existing destination. The zero-inclusion failure in Section L occurs before prepared intent and therefore MUST preserve the existing destination. After installation begins, destination state MUST be reported only as durably observed or `unknown` under this protocol.

## P. Golden artifact and regression policy

Future implementation acceptance MUST include wholly fictional fixtures under:

- `examples/contract-fixtures/newsletter-publication-boundary/v0/input/`
- `examples/contract-fixtures/newsletter-publication-boundary/v0/golden/fictional-newsletter.md`
- `examples/contract-fixtures/newsletter-publication-boundary/v0/golden/generation-evidence.json`

At least one automated test MUST regenerate the participant-facing artifact and compare exact bytes, including encoding and newline policy, with the tracked golden newsletter. A separate semantic test MUST validate the structured evidence and all digests. Any byte drift requires explicit fixture review; substring assertions alone are insufficient.

A force-added artifact from an ignored runtime output directory MUST NOT be the only golden evidence. Goldens belong in the explicit fictional fixture paths and MUST contain no real centre data.

## Q. Compatibility with the precursor guard

`Newsletter CLI Batch Admission Guard v0` exists separately as a diagnostic precursor on a disjoint prototype branch. It rejects certain malformed, empty, mixed-status, and uncertain CLI batches before that prototype renders. That early diagnostic is necessary for its bounded CLI behavior but insufficient for publication. It is not a normative dependency of this contract, and this contract remains complete and valid if the prototype branch is never merged.

That temporary guard:

- is not canonical schema admission;
- is not newsletter-scoped or consumer-scoped eligibility;
- is not publication selection or publication authority;
- does not establish profile fidelity, safe rendering, provenance, structured findings, atomic replacement, or golden assurance; and
- MUST NOT be treated as satisfying any later gate solely because `qa_status == "approved"` and `uncertain_fields == []`.

A future implementation MAY retain equivalent early diagnostics only after independently satisfying every applicable gate in this contract. A precursor CLI input array never establishes publication membership or publication order, even when every record passes that diagnostic guard.

## R. Deferred work

This contract explicitly defers:

- DOCX generation;
- PDF generation;
- images and other media;
- visual layout and pagination;
- generic template engines;
- generic policy engines;
- profile-family eligibility, compatibility inheritance, and profile widening;
- deployment and packaging for production;
- web publishing;
- multi-project abstraction;
- agent-executor changes;
- GitHub Actions or other CI changes;
- real centre data, real eligibility, real selection, and real publication; and
- implementation or activation of any runtime publication behavior.

## S. Acceptance criteria for future implementation

A future implementation is not accepted until all of the following are demonstrated on one exact reviewed head:

1. executable schemas or equivalent strict validators exist for evidence-findings, eligibility, ordered selection, publication profile, and prepared/finalized/unknown generation evidence;
2. every selected record is canonically validated and digest-bound before publication;
3. every explicitly enumerated candidate record is canonical, and evidence-findings completely and affirmatively resolves the exact run and record revisions;
4. approval, uncertainty, eligibility, selection, and inclusion remain separate tested states;
5. eligibility is uniquely resolved for the exact record, run, consumer, and exact profile logical ID/digest, with every reason code in Section G tested and a different profile always requiring a separate decision;
6. staleness tests distinguish valid predecessor history, a superseded artifact incorrectly presented as effective, ambiguous tips, broken chains, and exact record/profile/consumer mismatches;
7. selection order is explicit and every integrity failure in Section H aborts the run;
8. destination identity/class originates only from the authenticated selection/run-context authority scope and cannot originate from or be altered by participant-controlled record text;
9. repeated randomized physical enumeration of one identical closed bundle produces exactly one `input_sha256`, including candidate, evidence-binding, root-to-tip eligibility, root-to-tip selection-chain, and authority-snapshot ordering;
10. publication profile allowlists, required/optional rules, prohibited fields, default-deny partial policy, and executable incompleteness predicates fail closed for missing, malformed, unknown, unsupported, or implementation-defined values;
11. the singular 13-phase normative order and earliest-phase primary classification are tested, including rendering execution, safety validation, complete-output validation, and secondary-finding behavior;
12. zero-inclusion and every valid or invalid count state produce exactly the outcome required by Section L;
13. record-local classification satisfies every condition in Section K, while unexpected, invariant, shared, unproven, and unknown failures are systemic;
14. projections preserve recurrence, multi-session meaning, complete fee structures, fee types/audiences, and all required participant-facing facts; fee audience flattening or inference fails;
15. incomplete records are wholly excluded only under permitted partial-generation rules and never partially rendered;
16. concurrent installation tests prove that:
    1. two overlapping valid invocations cannot both retain unconditional installation authority;
    2. a newer invocation may install before an older invocation resumes;
    3. the stale older invocation then fails closed without replacement;
    4. stale-invocation finalized evidence records `output_installation_failure` and `not_replaced`; and
    5. retry after an unknown outcome cannot bypass fresh fencing/current-state checks;
17. every exclusion and failure produces stable structured evidence, with all counts, logical IDs, versions, predecessors, snapshots, fencing values, and digests reconciling without circular derivation;
18. exclusive temporary-byte access, immediate pre-replacement digest recomputation, installed destination digest corroboration, and temp/destination digest mismatch handling are tested; a mismatch never claims verified installation;
19. Markdown injection and forged provenance negative cases pass;
20. prepared intent, installation, finalization, unknown outcome, no-blind-retry behavior, destination preservation, and every durability capability class are tested;
21. fictional golden artifacts pass byte-for-byte regeneration and digest checks;
22. no test relies on real centre data;
23. documentation and implementation make no claim that approval alone grants publication authority;
24. exactly one authority-acceptance mode is enforced:
    - **Production-capable mode**: eligibility, selection, and publication-profile artifacts are authenticated through a separately accepted Owner-authority contract, with authentication, exact scope, revocation, replay resistance, identity, and failure behavior tested; or
    - **Fixture-only mode**: the implementation is technically prevented from targeting any real or `production` destination, is hard-bound to fictional fixture inputs and a non-production `fixture` destination, and cannot allow any unauthenticated artifact to authorize real publication;
25. digest correctness, unique chain resolution, file ownership, directory location, or local filesystem access is never accepted as a substitute for authenticated Owner authority;
26. full repository validation and required independent architecture/security review pass; and
27. the Owner separately accepts the implementation and any schema or runtime activation.

This draft grants no implementation authorization. Newsletter Publication Boundary v0 remains unimplemented until those criteria and repository governance are satisfied.
