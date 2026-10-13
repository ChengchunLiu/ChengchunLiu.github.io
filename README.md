# Chengchun Liu — Research Portfolio

A lightweight multilingual research portfolio for `https://chengchunliu.github.io/`. English, Simplified Chinese, and Traditional Chinese are generated as separate static pages so visitors and search engines receive the correct language without waiting for JavaScript.

## Build the site

The editable sources live in `src/`. Generate the public pages with:

```bash
python3 scripts/build_site.py
```

The build creates three localized homepages, fifteen localized research pages, and a multilingual sitemap. To confirm that committed output matches the sources:

```bash
python3 scripts/build_site.py --check
```

## Preview locally

From this folder, start any static file server. For example:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

Localized routes:

- English: `/`
- Simplified Chinese: `/zh-hans/`
- Traditional Chinese: `/zh-hant/`
- Research pages: `/research/<slug>/` and their localized equivalents

## Publishing

The included GitHub Actions workflow rebuilds and deploys the site to GitHub Pages whenever `main` is updated.

Recommended repository:

```text
ChengchunLiu/ChengchunLiu.github.io
```

Before publishing, confirm:

- the final GitHub account or hosting provider;
- whether to add a downloadable public CV;
- whether to add any additional public profile links;
- the final personal domain, if any.

Only first- and co-first-author papers are featured on the homepage. Each selected paper has a crawlable research page with complete authorship, DOI metadata, original explanatory copy, and structured data. The complete publication record is linked through Google Scholar.

Research concepts are represented by original website diagrams rather than reproduced publisher figures.

SEO support includes canonical URLs, `hreflang`, a multilingual sitemap, academic citation metadata, and `ProfilePage`, `Person`, and `ScholarlyArticle` JSON-LD.

The social sharing image can be regenerated with:

```bash
python3 scripts/generate_og.py
```
