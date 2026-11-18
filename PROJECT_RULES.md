# AuraFIT Project Rules

These rules must be followed throughout the development lifecycle:

1. Never modify unrelated files.
2. Never rewrite working modules unnecessarily.
3. Keep frontend and backend responsibilities separate.
4. Never place business logic inside React components.
5. Never expose API keys or secrets in the frontend.
6. Nutrition calculations must remain deterministic backend logic.
7. Never allow the LLM to invent authoritative nutrition values.
8. All backend input must be validated.
9. AI outputs must be structurally validated.
10. Every feature must have appropriate tests.
11. Preserve existing functionality when adding features.
12. Avoid unnecessary dependencies.
13. Avoid duplicate business logic.
14. Mobile responsiveness is mandatory.
15. Never use fake functionality as if it were implemented.
16. Do not implement features outside the current phase without explicit instruction.
