# KEDDEH HCI / UX research baseline

- WCAG 2.2: visible focus, minimum target sizing, reduced redundant entry and accessible authentication. KEDDEH targets 44px primary controls and explicit focus treatment. https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- Nielsen Norman Group progressive disclosure: show frequent/high-value actions first; disclose advanced options on demand. https://www.nngroup.com/articles/progressive-disclosure/
- Nielsen Norman Group information scent: link label + context + prior expectations should make destinations predictable. https://www.nngroup.com/articles/information-scent/
- Google people-first content: useful, original, satisfying content with clear purpose and demonstrated expertise. https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google page experience: mobile display, Core Web Vitals, secure serving, non-intrusive presentation and distinguishable main content. https://developers.google.com/search/docs/appearance/page-experience

## KEDDEH interaction law
1. Every page names audience, purpose and one dominant next action.
2. Every internal clickable resolves through the same route registry used by build/tests.
3. Deep architecture uses progressive disclosure.
4. Motion is non-essential and respects reduced-motion preference.
5. Forms retain values after failure and announce status through `aria-live`.
6. Learning interest is not silently promoted to a sales-qualified lead.
7. Public claims state their evidence class.
8. Owner/admin capability is server-side authenticated; secrets never appear in client HTML.
