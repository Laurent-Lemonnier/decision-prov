# Vocabulary: `https://w3id.org/decision-prov#`

Prefix `dprov:`. Every term below names a member of a document of the Decision Provenance Standard (record schema 5.2.0 of the reference files, action binding 0.3.0, signatures 0.2.0) read as it is written there; the term carries no meaning of its own beyond naming that member in a graph. Members mapped to PROV-O or RDFS terms are not listed here: they are `prov:` and `rdfs:` terms (see the context).

| Term | Member(s) of the Standard's documents |
|---|---|
| `dprov:ActionBindingAttachment` | `ActionBindingAttachment` |
| `dprov:ActionSpecification` | `ActionSpecification` |
| `dprov:DecisionRecord` | `DecisionRecord` |
| `dprov:PersonApproval` | `PersonApproval` |
| `dprov:Stage` | `Stage` |
| `dprov:accountableOwnerSignoff` | `accountable_owner_signoff` |
| `dprov:actionSpecification` | `action_specifications` |
| `dprov:affirmedBy` | `affirmation_record` |
| `dprov:algorithm` | `algorithm` |
| `dprov:altitude` | `altitude` |
| `dprov:approvedSpecDigest` | `approved_spec_digest` |
| `dprov:assertion` | `assertion` |
| `dprov:assumptionDependedOn` | `assumptions_depended_on` |
| `dprov:authority` | `authority` |
| `dprov:authorityRef` | `authority_ref` |
| `dprov:authoritySourceRef` | `authority_source_ref` |
| `dprov:basis` | `basis` |
| `dprov:charterId` | `charter_id` |
| `dprov:closedAt` | `closed_at` |
| `dprov:consentPosture` | `consent_posture` |
| `dprov:contextAtDecision` | `context_at_decision` |
| `dprov:coreRef` | `core_ref` |
| `dprov:decisionClass` | `decision_class` |
| `dprov:decisionId` | `decision_id` |
| `dprov:decisionStatement` | `decision_statement` |
| `dprov:deployerRolePointer` | `deployer_role_pointer` |
| `dprov:dispatchMode` | `dispatch_mode` |
| `dprov:draftedBy` | `drafting_authority` |
| `dprov:evidenceRef` | `evidence_ref` |
| `dprov:forDecision` | `for_decision` |
| `dprov:keyRef` | `key_ref` |
| `dprov:kind` | `kind` |
| `dprov:mediaType` | `media_type` |
| `dprov:method` | `method` |
| `dprov:modeClassificationAttestation` | `mode_classification_attestation` |
| `dprov:observed` | `observed` |
| `dprov:optionConsidered` | `options_considered` |
| `dprov:origin` | `origin` |
| `dprov:outcome` | `outcome` |
| `dprov:personSignature` | `person_signatures` |
| `dprov:postureClass` | `posture_class` |
| `dprov:profile` | `profile` |
| `dprov:profileVersion` | `profile_version` |
| `dprov:rationale` | `rationale` |
| `dprov:reDecisionTrigger` | `re_decision_trigger` |
| `dprov:recheckResult` | `result` |
| `dprov:recordLocation` | `record_location` |
| `dprov:recordState` | `record_state` |
| `dprov:recordType` | `record_type` |
| `dprov:representation` | `representation` |
| `dprov:requestId` | `request_id` |
| `dprov:requiredInputUsed` | `required_inputs_used` |
| `dprov:role` | `role` |
| `dprov:sealAlgorithm` | `seal_algorithm` |
| `dprov:sealHash` | `seal_hash` |
| `dprov:shownSpecDigest` | `shown_spec_digest` |
| `dprov:shownViewDigest` | `shown_view_digest` |
| `dprov:signature` | `signature` |
| `dprov:specDigest` | `spec_digest` |
| `dprov:stage` | `stages` |
| `dprov:stageId` | `stage_id` |
| `dprov:successCriterion` | `success_criteria` |
| `dprov:traceRef` | `trace_refs` |
| `dprov:valueBase64` | `value_b64` |
| `dprov:verification` | `verification` |
| `dprov:version` | `version` |

Classes: `dprov:DecisionRecord`, `dprov:ActionBindingAttachment`, `dprov:ActionSpecification`, `dprov:Stage` and one subclass per stage kind (`dprov:ProposalStage`, `dprov:ReviewStage`, `dprov:OutcomeStage`, `dprov:RequestStage`, `dprov:RecheckStage`, `dprov:AttemptStage`, `dprov:ResultStage`, `dprov:StandingApprovalStage`, `dprov:StandingRevocationStage`, `dprov:ChangeAuthorisationStage`), `dprov:PersonApproval`. Each is also typed `prov:Entity` or `prov:Activity` by the exporter.

This vocabulary is the author's own reading. It is not part of the Decision Provenance Standard and is not endorsed by its Steward; where this reading and the Standard's text differ, the Standard's text governs. The namespace is a w3id.org permanent identifier controlled by the author; until the redirect is registered, this file is the vocabulary's description.
