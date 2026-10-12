# Chengchun Liu — Personal Portfolio

A lightweight bilingual research portfolio designed for the personal GitHub Pages address `https://chengchunliu.github.io/`.

## Preview locally

From this folder, start any static file server. For example:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

## Publishing

The site has no build step. The included GitHub Actions workflow deploys the repository to GitHub Pages whenever `main` is updated.

Recommended repository:

```text
ChengchunLiu/ChengchunLiu.github.io
```

Before publishing, confirm:

- the final GitHub account or hosting provider;
- whether to add a downloadable public CV;
- whether to add GitHub, ORCID, or other profile links;
- the final personal domain, if any.

Only first- and co-first-author papers are featured on the homepage. The complete record is linked through Google Scholar.

Publisher figures without a confirmed reuse license are represented by original website diagrams. The Advanced Science figure is used with an on-page CC BY 4.0 attribution.

The social sharing image can be regenerated with:

```bash
python3 scripts/generate_og.py
```
