#!/usr/bin/env python3
"""Read a chain of the Decision Provenance Standard as W3C PROV.

Inputs, in one folder: decision-record.json (record schema 5.2.0 of the reference files), action-binding-attachment.json
(action binding 0.3.0), signatures-attachment.json (signatures 0.2.0) and verification-summary.json, what the Standard's
own reference checks reported on them. Outputs, in the same folder: provenance.jsonld, provenance.ttl and summary.json.

The context (context/decision-prov.context.jsonld) maps the members of those documents to PROV-O terms, or to terms of
this reading's own vocabulary, without changing a member. What this script adds is only what a graph needs: an IRI for
each node, under a base the exporter chooses (--base; the Standard's identifiers are strings and it states no IRI
convention), and the types. The accountable owner of the record and the actor of a stage stay two agents: the records
do not say they are one person, and only an exporter's own data could.

Nothing here verifies anything. dprov:verification repeats what verification-summary.json reports for the
person_approval; the queries find what the records state and what the verifier reported, not that any condition is met.
Standard library plus rdflib.
"""
import argparse
import copy
import json
import pathlib
import sys

from rdflib import Graph

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CONTEXT = json.loads((ROOT / "context" / "decision-prov.context.jsonld").read_text(encoding="utf-8"))["@context"]
QUERIES = {name: (ROOT / "queries" / f"{name}.rq").read_text(encoding="utf-8") for name in ("attempts", "tracing", "chain")}


def stage_class(kind):
    return "dprov:" + "".join(part.capitalize() for part in kind.split("_")) + "Stage"


def as_jsonld(base, record, attachment, signatures, verification, *, with_attribution=True):
    """The three documents as one JSON-LD document under the context, with IRIs under `base`."""
    def iri(kind, value):
        return f"{base}{kind}:{value}"

    def agent(ref):
        # A reference the records already write as an IRI (a URN, an http(s) IRI) is kept as it is.
        return ref if str(ref).startswith(("urn:", "http://", "https://")) else iri("agent", ref)

    decision_iri = iri("decision", record["decision_id"])

    def stage_iri(sid):
        return iri("stage", f"{record['decision_id']}:{sid}")

    rec = copy.deepcopy(record)
    rec["@id"] = decision_iri
    rec["@type"] = ["DecisionRecord", "Entity"]
    owner = rec.get("accountable_owner") or {}
    # The owner is an agent of its own, named by the record's text; the exporter does not link it to any stage actor.
    rec["accountable_owner"] = {"@id": agent("owner:" + str(owner.get("full_name", "")).lower().replace(" ", "-")),
                                "@type": "Person", **{k: v for k, v in owner.items() if k != "employer"},
                                **({"employer": {"@id": agent("org:" + owner["employer"]), "@type": "Organization",
                                                 "rdfs:label": owner["employer"]}} if owner.get("employer") else {})}
    drafting = rec.get("drafting_authority") or {}
    rec["drafting_authority"] = {"@id": agent("system:" + str(drafting.get("system_name", ""))), "@type": "SoftwareAgent",
                                 **drafting}
    affirmation = rec.get("affirmation_record") or {}
    rec["affirmation_record"] = {"@id": iri("affirmation", record["decision_id"]), "@type": "Activity",
                                 **{k: v for k, v in affirmation.items() if k != "actor_identity"},
                                 **({"actor_identity": agent(affirmation["actor_identity"])} if affirmation.get("actor_identity") else {})}
    if rec.get("supersedes"):
        rec["supersedes"] = iri("decision", rec["supersedes"])
    else:
        rec.pop("supersedes", None)

    att = copy.deepcopy(attachment)
    att["@id"] = iri("attachment", record["decision_id"])
    att["@type"] = ["ActionBindingAttachment", "Entity"]
    att["for_decision"] = decision_iri
    att.pop("decision_id", None)
    for spec in att.get("action_specifications", []):
        spec["@id"] = iri("spec", spec["spec_digest"])
        spec["@type"] = ["ActionSpecification", "Entity"]
        spec.pop("content", None)  # the bytes stay in the export; the graph carries the digest
    for stage in att.get("stages", []):
        stage["@id"] = stage_iri(stage["stage_id"])
        stage["@type"] = ["Stage", "Activity", stage_class(stage["kind"])]
        for key in ("proposal_ref", "review_ref", "authorised_by", "request_ref", "recheck_ref", "attempt_ref", "revokes_ref"):
            if key in stage:
                stage[key] = stage_iri(stage[key])
        for key in ("reviewer_ref", "actor_ref", "requested_by", "executor_ref"):
            if key in stage:
                stage[key] = {"@id": agent(stage[key]),
                              "@type": "Person" if str(stage[key]).startswith("person:") else "SoftwareAgent"}
        if isinstance(stage.get("authority"), dict) and stage["authority"].get("authority_ref"):
            stage["authority"] = {"authority_ref": stage["authority"]["authority_ref"]}
        for key in ("rationale", "core_ref", "trace_refs", "bounds"):
            stage.pop(key, None)

    sigs = copy.deepcopy(signatures)
    sigs["@id"] = iri("signatures", record["decision_id"])
    sigs["@type"] = "Entity"
    for index, sig in enumerate(sigs.get("person_signatures", [])):
        sig["@id"] = iri("approval", f"{record['decision_id']}:{sig.get('stage_id')}:{index}")
        sig["@type"] = ["PersonApproval", "Entity"]
        sig["for_decision"] = decision_iri
        sig["stage_id"] = stage_iri(sig["stage_id"])
        sig["verification"] = verification
        if with_attribution:
            actor = next((s.get("actor_ref") for s in attachment["stages"]
                          if s.get("stage_id") == signatures["person_signatures"][index]["stage_id"]), None)
            if actor:
                sig["signed_by"] = agent(actor)
        sig.pop("decision_id", None)
    return {"@context": CONTEXT, "@graph": [rec, att, sigs]}


def export(folder, base):
    folder = pathlib.Path(folder)
    read = lambda name: json.loads((folder / name).read_text(encoding="utf-8"))  # noqa: E731
    record, attachment, signatures = read("decision-record.json"), read("action-binding-attachment.json"), read("signatures-attachment.json")
    checks = read("verification-summary.json")["person_approval"]
    verification = "verified" if all(v == "verified" for v in checks.values()) else "not_verified"

    document = as_jsonld(base, record, attachment, signatures, verification)
    (folder / "provenance.jsonld").write_text(json.dumps(document, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    graph = Graph().parse(data=json.dumps(document), format="json-ld")
    (folder / "provenance.ttl").write_text(graph.serialize(format="turtle"), encoding="utf-8")

    attempts = {str(r.attempt) for r in graph.query(QUERIES["attempts"])}
    traced = {str(r.attempt): str(r.person) for r in graph.query(QUERIES["tracing"])}
    chain = [str(r.result) for r in graph.query(QUERIES["chain"])]
    negative = as_jsonld(base, record, attachment, signatures, verification, with_attribution=False)
    found_without = {str(r.attempt) for r in Graph().parse(data=json.dumps(negative), format="json-ld").query(QUERIES["tracing"])}
    result = {"base": base, "triples": len(graph), "attempts": sorted(attempts), "traced_to": traced,
              "every_attempt_traced": bool(attempts) and set(traced) == attempts,
              "full_stage_chain_found": bool(chain), "negative_control_finds_no_one": not found_without,
              "note": "The graph describes; the export and its signatures prove. The queries find what the records state "
                      "and what the verifier reported, not that any condition is met. dprov:verification repeats "
                      "verification-summary.json."}
    (folder / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", help="folder holding the three documents and verification-summary.json")
    parser.add_argument("--base", default="urn:example:", help="base IRI for the nodes (default urn:example:, for a worked example; "
                        "an exporter uses a base it controls)")
    args = parser.parse_args()
    result = export(args.folder, args.base)
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0 if result["every_attempt_traced"] and result["full_stage_chain_found"] and result["negative_control_finds_no_one"] else 1


if __name__ == "__main__":
    sys.exit(main())
