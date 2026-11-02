# CareBand3 live job search

A working server-side integration for Adzuna's UK jobs API. It searches real adverts, retains Band 3 care roles, and renders each vacancy with its source-provided application link. Adzuna's redirect URL may first go through Adzuna before reaching the original employer.

## Start
1. Register for credentials at https://developer.adzuna.com/ and check the API licence/attribution terms.
2. Set environment variables `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` (never place them in the HTML).
3. Run `python server.py` and open `http://localhost:8000`.
4. Deploy this folder to a Python-capable host, configure both environment variables, and set start command `python server.py`.

No live listings are available without credentials and a running server. A static HTML file opened locally cannot run this backend. Search coverage depends on the provider, and sponsorship cannot be inferred. NHS-specific official feed integration would require separate implementation and permission/terms review.
