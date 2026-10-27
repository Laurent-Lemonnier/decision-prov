# decision-prov

Reading the records of the Decision Provenance Standard as W3C PROV: a JSON-LD 1.1 context, an exporter, a worked
example and three SPARQL queries. Version 0.1.0, 27 October 2026. Author: Laurent Lemonnier.

**This is one reader's reading.** It is not part of the Decision Provenance Standard, does not change it, and is not
endorsed by its Steward. The Standard and its extensions are the source; where this reading and the Standard's text
differ, the Standard's text governs. Its vocabulary lives under a namespace the author controls,
`https://w3id.org/decision-prov#` (prefix `dprov:`), and not under the Standard's.

"Decision Provenance Standard" is a trademark of Etsion Brands Ltd., used here to identify the Standard. Attribution:
The Decision Provenance Standard, Yohay Etsion, 2026, CC-BY 4.0, https://decisionprovenancestandard.org.

## Why

People who come from the provenance world ask whether W3C PROV, applied to decisions, does not already do what the
Standard does. It does not, and the two do not compete. PROV-O gives Entity, Activity and Agent, and relations such as
`used`, `wasGeneratedBy`, `wasAssociatedWith`, `wasAttributedTo` and `actedOnBehalfOf`: it describes where something
came from. It has no canonical bytes to digest, no signature semantics, no verifier, no report dimensions, and no
content for a decision: options, rationale, authority. Anyone can state the triple "this person approved this"; nothing
binds it. The Standard's records, action binding and signatures are what PROV leaves out. So PROV is a vocabulary in
which the Standard's records can be read, once they are verified, and this repository makes that reading checkable
rather than asserted.

## What it maps

Three documents, read as they are written, without changing a member:

- a decision record (the record schema 5.2.0 of the Standard's reference files);
- an action-binding attachment (action binding 0.3.0);
- a signatures attachment carrying a `person_approval` (signatures 0.2.0).

| In the records | In the graph |
|---|---|
| the decision record | a `dprov:DecisionRecord`, a `prov:Entity` |
| `accountable_owner` | `prov:wasAttributedTo` a `prov:Person`, who `prov:actedOnBehalfOf` a `prov:Organization` (the employer) |
| `drafting_authority` | `dprov:draftedBy` a `prov:SoftwareAgent` |
| `affirmation_record` | a `prov:Activity`, `prov:wasAssociatedWith` the actor, `prov:endedAtTime` its timestamp |
| `created_at`, `signed_at` | `prov:generatedAtTime` |
| `supersedes` | `prov:wasRevisionOf` |
| the attachment, each action specification | a `prov:Entity` (the specification by its digest; its bytes stay in the export) |
| each stage | a `prov:Activity`, typed by its kind (`dprov:ProposalStage` … `dprov:ResultStage`), `prov:wasAssociatedWith` its actor |
| each `*_ref` from one stage to another | `prov:wasInformedBy`, so the chain proposal, review, outcome, request, recheck, attempt, result is a path |
| a `person_approval` | a `dprov:PersonApproval`, a `prov:Entity`, `prov:wasAttributedTo` the person who signed, carrying the approved digest |
| what the Standard's checks reported on it | `dprov:verification`, repeated from `verification-summary.json`, never computed here |

The members the context leaves under `dprov:` are listed in [vocab.md](vocab.md), each with the member it names.

## What the exporter adds, and what it does not decide

PROV links nodes; the Standard's identifiers are strings (`decision_id`, `stage_id`, an `actor_ref` such as
`person:billing-lead`). The Standard states no IRI convention, on purpose, and no check of its reads an IRI. So the
exporter takes a base IRI from whoever runs it (`--base`), and the worked example uses `urn:example:`. A reference the
records already write as an IRI (a URN, an http(s) IRI) is kept as it is. No URN namespace is invented: `urn:dps:` is
not registered (RFC 8141) and is not used.

The accountable owner named in the record and the actor of a stage are two agents in the graph. The records do not say
they are one person; only an exporter's own data could link them, and this exporter does not.

## What the queries show, and what they do not

On the worked example ([examples/invoice-approval](examples/invoice-approval): a decision to issue an invoice, drafted
by a system, reviewed and approved by a person, requested, rechecked, attempted and observed, with the person's
signature verified by the Standard's reference check), the three documents read through the context give a graph of
178 triples, and the queries in [queries](queries) answer:

- `chain.rq`: the whole stage chain from proposal to result is found as a path of `prov:wasInformedBy`;
- `tracing.rq`: for every attempt there is a `person_approval` whose approved digest is the attempt's digest, which the
  reference check reported verified, attributed to a `prov:Person`;
- the negative control, the same graph with the attribution dropped, finds no one.

The graph proves nothing by itself: the export and its signatures prove, and `dprov:verification` only repeats what
the Standard's checks reported. A query finds what the records state and what the verifier reported; it does not show
that any condition is met, "meaningful human control" included. What it gives is a way to ask the question of a set
of verified records in a vocabulary other tools already read.

## Run

```
pip install rdflib
python3 src/dps_to_prov.py examples/invoice-approval              # --base <IRI> to choose the base
python3 tests/check.py                                            # the example is what the exporter writes
```

`dps_to_prov.py` writes `provenance.jsonld`, `provenance.ttl` and `summary.json` beside the inputs. It needs the three
documents and a `verification-summary.json` saying what the Standard's reference checks reported; it runs none of them.
To verify the documents, use the Standard's own runners (`extensions/*/tests/run_checks.py` in its repository).

## Versions

Written against the Standard's repository at commit bcbe8a6 (27 October 2026): record schema 5.2.0 of the reference
files, action binding 0.3.0, signatures 0.2.0. The context names members of those versions; a later version of an
extension may add members the context does not know, which then stay out of the graph.

## Licence

Code (`src`, `tests`, `queries`): Apache-2.0 ([LICENSE](LICENSE)). Text, the context and the vocabulary (`README.md`,
`vocab.md`, `context/`): CC-BY 4.0 ([LICENSE-CC-BY-4.0](LICENSE-CC-BY-4.0)). The example documents follow the Standard's
formats under their own licences; the data in them is invented. Cite as in [CITATION.cff](CITATION.cff).
