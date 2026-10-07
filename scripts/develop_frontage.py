#!/usr/bin/env python3
"""Develop the existing frontage in place; preserve Site identity and owner sources."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1] / 'frontage'
SOURCE = 'https://github.com/Keddeh1/KEDDEH-SOVEREIGN-NAMESPACE-RUNTIME/blob/8317dbc'  # resolved below
import subprocess
REF = subprocess.check_output(['git', '-C', '/workspace/KEDDEH-SOVEREIGN-NAMESPACE-RUNTIME', 'rev-parse', '8317dbc'], text=True).strip()
SOURCE = SOURCE.rsplit('/', 1)[0] + '/' + REF + '/'

# Customer needs are evaluation invitations, not claims of market share or outcomes.
PROFILES = {
 '/': ('Runtime evaluation', 'Choose an evaluation that fits your operation', 'For teams investigating state continuity, runtime control or reproducible execution evidence.', 'Describe one workload, its current environment and the failure you need to recover from.', 'An evaluation brief can connect your required outcome to a named runtime, measured result and acceptance boundary.', 'docs/architecture/SYSTEM_ARCHITECTURE.md', ['Q-01','Q-02','Q-03','Q-16']),
 '/platform': ('Runtime evaluation', 'Match a responsibility to a component', 'For architects choosing where execution, semantic context, observation and retained artifacts belong.', 'Identify which component owns an action, its state, its returned evidence and its access boundary.', 'Use a responsibility map to evaluate BRAINK execution, KEX routing and IL-LLM context separately, then inspect their integration.', 'docs/architecture/SYSTEM_ARCHITECTURE.md', ['Q-01','Q-14','Q-16']),
 '/architecture': ('Enterprise deployment', 'Evaluate continuity across a lost anchor', 'For operations teams assessing services that retain state while a parent network anchor changes.', 'Provide the expected recovery interval, downstream responsibilities and failure-domain assumptions.', 'Compare pre-failure state, flywheel continuity and reanchor readbacks against your acceptance criteria.', 'docs/architecture/SYSTEM_ARCHITECTURE.md', ['Q-02','Q-03','Q-04','Q-13']),
 '/products/braink': ('Runtime evaluation', 'Make a runtime action reviewable', 'For operators who need to see what an admitted action changed and how an interrupted action recovered.', 'Bring one action, its authority boundary and the receipt or state transition you need to inspect.', 'Evaluate an action-to-receipt journey with original actuator output, observer readback and retained evidence.', 'docs/package/actions/commit/README.md', ['Q-01','Q-02','Q-18']),
 '/products/kex': ('Runtime evaluation', 'Evaluate a recursive service boundary', 'For engineers investigating lineage, routing and state across nested execution domains.', 'Specify the child service, its upstream dependency and the state that must remain after reanchoring.', 'Inspect actual namespace membership, epochs and retained downstream identity against the intended service topology.', 'docs/package/actions/domains/README.md', ['Q-03','Q-04','Q-06','Q-13']),
 '/products/illlm': ('Developer integration', 'Frame a contextual language workflow', 'For teams exploring source-attributed definitions and semantic interfaces within the supplied estate.', 'Describe your permitted data, the semantic task and the source context that should accompany an output.', 'Agree a bounded interface and evidence requirement before selecting or extending the admitted semantic tools.', 'docs/package/actions/estate/README.md', ['Q-16','Q-20']),
 '/research': ('Research collaboration', 'Investigate a reproducible propagation question', 'For researchers comparing graph topology, delays, activation and continuity under explicit assumptions.', 'Bring the graph, noise process, resource budget, units and result you want compared.', 'Retain methods, seeded trials and uncertainty alongside the result so the comparison can be rerun.', 'docs/research/claims/noise-study-summary.json', ['Q-06','Q-07','Q-08','Q-09','Q-10']),
 '/evidence': ('Research collaboration', 'Trace an assertion to its record', 'For technical reviewers evaluating the scope, origin and reproducibility of a result.', 'Identify the claim reference and the result or source revision you want to examine.', 'Separate execution, readback, qualification and external assessment, and resolve the next evidence test explicitly.', 'docs/research/claims/CLAIM_REVIEW.md', ['Q-18','Q-21','Q-22']),
 '/developers': ('Developer integration', 'Build an integration with an acceptance contract', 'For developers connecting a bounded function to the owner estate without crossing customer and operator authority.', 'Describe the interface, input/output shape, state ownership and retry requirements.', 'Use the process, action and configuration contracts to specify a testable integration and release identity.', 'docs/package/README.md', ['Q-01','Q-14','Q-17','Q-20']),
 '/enterprise': ('Enterprise deployment', 'Scope a pilot before a production commitment', 'For teams assessing deployment ownership, data custody, recovery and operational control.', 'Provide your workload, environment, data classification, operators and recovery expectations.', 'Define an evaluation scope and acceptance record, then determine the infrastructure and agreement needed for promotion.', 'docs/architecture/STANDARDIZATION_AUDIT.md', ['Q-12','Q-13','Q-17','Q-20']),
 '/contact': ('General enquiry', 'Send a focused enquiry', 'For questions about an evaluation, a prior registration or an attributed technical result.', 'Include the relevant page or registration reference and the question you want reviewed. Keep secrets out of the form.', 'A successful submission returns a durable reference for the private enquiry record; follow-up remains an owner review action.', 'src/keddeh_namespace/frontage_service.py', ['Q-20']),
 '/interest': ('Runtime evaluation', 'Prepare a useful evaluation brief', 'For runtime, enterprise, research and developer enquiries.', 'Describe the intended outcome, current environment, constraints and evidence you would use to judge success. Keep credentials and sensitive datasets out of the form.', 'Your selected topic and consented enquiry are recorded privately. Registration does not create service access or an operational agreement.', 'src/keddeh_namespace/frontage_service.py', ['Q-20']),
 '/privacy': ('General enquiry', 'Understand the enquiry boundary', 'For visitors deciding what to share and how an enquiry will be handled.', 'Share only the contact information and context needed for owner review. Use your registration reference when asking about an earlier enquiry.', 'The versioned consent applies to enquiry handling. Retention maintenance removes stored enquiries older than 90 days.', 'src/keddeh_namespace/frontage_service.py', ['Q-20']),
 '/research/claim-review': ('Research collaboration', 'Turn a qualification into a defined experiment', 'For reviewers comparing an architectural assertion with retained implementation or trial evidence.', 'Include the Q-reference, intended interpretation and the measurement that would resolve the question.', 'Map existing owner evidence first; then specify a reproducible test with units, resources, acceptance criteria and retained outputs.', 'docs/research/claims/DERIVATION_WORKLIST.md', ['Q-01','Q-08','Q-09','Q-10','Q-15','Q-19']),
}

SECTION_SOURCES = {
 ('/architecture', 'Bilateral execution'): 'src/keddeh_namespace/bilateral_runtime.py',
 ('/architecture', 'State and recovery'): 'scripts/verify_owner_domains.py',
 ('/products/kex', 'Hardware bindings'): 'docs/OWNER_SOURCE_MANIFEST.json',
 ('/research', '0.297 software oscillator'): 'src/keddeh_namespace/bilateral_runtime.py',
 ('/research', 'Propagation abstraction'): 'src/keddeh_namespace/universal_propagation.py',
 ('/evidence', 'Live family readback'): 'src/keddeh_namespace/frontage_service.py',
 ('/evidence', 'Independent assessment'): 'docs/architecture/STANDARDIZATION_AUDIT.md',
}

def section(match, source, route, index):
    body = match.group(1)
    if 'data-page-development=' in body:
        return match.group(0)
    label = re.search(r'<h2[^>]*>(.*?)</h2>', body, re.S)
    title = re.sub('<[^>]*>', '', label.group(1)) if label else 'Page content'
    if (route, title) in SECTION_SOURCES:
        source = SOURCE + SECTION_SOURCES[(route, title)]
    return '<section id="section-' + str(index) + '">' + body + '<details class="section-source"><summary>Sources and interpretation: ' + html.escape(title) + '</summary><p>This section is attributed to the owner implementation or contract below. Evaluation invitations describe a proposed use; measured claims retain their scope in the claim review.</p><a href="' + source + '">Inspect the pinned source</a> · <a href="/research/claim-review">Review claim scope and next tests</a></details></section>'

def main():
    manifest = json.loads((ROOT / 'route-manifest.json').read_text())
    contracts = []
    for page in manifest['routes']:
        route = page['path']; topic, title, fit, inputs, outcome, source_path, claims = PROFILES[route]
        assert (Path('/workspace/KEDDEH-SOVEREIGN-NAMESPACE-RUNTIME') / source_path).exists(), source_path
        source = SOURCE + source_path
        path = ROOT / page['file']; document = path.read_text()
        document = re.sub(r'<!-- page-development:start -->.*?<!-- page-development:end -->', '', document, flags=re.S)
        document = re.sub(r'<details class="section-source">.*?</details>', '', document, flags=re.S)
        # Preserve authored sections and add traceable source disclosure to each.
        counter = [0]
        def annotate(m):
            counter[0] += 1
            return section(m, source, route, counter[0])
        document = re.sub(r'<section(?: id="section-\d+")?>(.*?)</section>', annotate, document, flags=re.S)
        query = urlencode({'topic': topic, 'context': route})
        panel = '<!-- page-development:start --><section class="evaluation-brief" data-page-development="1" aria-labelledby="evaluation-title"><p class="eyebrow">Evaluation fit</p><h2 id="evaluation-title">' + html.escape(title) + '</h2><dl><dt>Who this helps</dt><dd>' + html.escape(fit) + '</dd><dt>What to bring</dt><dd>' + html.escape(inputs) + '</dd><dt>What to evaluate</dt><dd>' + html.escape(outcome) + '</dd></dl>'
        if route not in ['/contact','/interest','/privacy']:
            panel += '<a class="button" href="/interest?' + html.escape(query, quote=True) + '">Discuss this ' + ('research question' if topic == 'Research collaboration' else 'evaluation') + '</a>'
        panel += '<p class="caption">Owner-designed technology · <a href="' + source + '">Pinned implementation and attribution</a> · <a href="/privacy">Enquiry handling and consent</a></p></section><!-- page-development:end -->'
        document = document.replace('</main>', panel + '</main>')
        document = document.replace('Claims about severe-noise resilience or AI-controlled spawn reductions require their original experimental datasets and methods before they can be presented as measured customer outcomes.', 'The retained 16,000-trial SI study compares chain and mesh under both equal rounds and equal transmission budgets. Its results are attributed to that software experiment; other empirical claims retain their own methods and evidence requirements.')
        if route in ['/contact','/interest'] and 'id="enquiry-context"' not in document:
            document = document.replace('<form id="interest-form" aria-describedby="form-guidance">', '<noscript><p class="error">This enquiry needs JavaScript to obtain a durable registration receipt. Your details have not been submitted. Enable JavaScript and reload to use this form.</p></noscript><form method="post" action="/api/interest" id="interest-form" aria-describedby="form-guidance"><p id="enquiry-context" class="caption" hidden></p>')
            document = document.replace('<p id="form-result" role="status" aria-live="polite">', '<p id="form-result" role="status" aria-live="polite" tabindex="-1">')
            document = document.replace('<select name="interest">', '<select name="interest" required>')
            document = document.replace('<button class="button" type="submit">', '<p id="message-guidance" class="caption">Describe your use case in 10–3000 characters. Please do not include credentials or confidential datasets.</p><button class="button" type="submit">')
            document = document.replace('name="message" required', 'name="message" aria-describedby="message-guidance" required')
        path.write_text(document)
        contracts.append({'route': route, 'topic': topic, 'fit': fit, 'inputs': inputs, 'evaluation': outcome, 'source_revision': REF, 'source': source, 'claim_references': claims, 'source_disclosures': counter[0], 'customer_boundary': 'Interest enquiry only; no owner token or automatic service access', 'acceptance': ['named navigation destination','source disclosure expands','topic/context survives enquiry journey','consent remains explicit','keyboard and mobile usable','server failure preserves entered data']})
    (ROOT / 'page-contracts.json').write_text(json.dumps({'schema':'keddeh.customer-page-contracts.v1','owner_attribution':'KEDDEH Systems owner-supplied concepts and runtimes; integration and UX changes recorded by Git revision','source_revision':REF,'pages':contracts}, indent=2) + '\n')
    print(json.dumps({'developed_routes':len(contracts),'source_disclosures':sum(c['source_disclosures'] for c in contracts)}))

if __name__ == '__main__':
    main()
