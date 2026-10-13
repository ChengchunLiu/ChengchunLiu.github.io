#!/usr/bin/env python3
"""Build the multilingual static portfolio without third-party dependencies.

The source of truth lives in ``src/``.  This script renders three localized
homepages, five research notes in each language, and a multilingual sitemap.
Run ``python3 scripts/build_site.py --check`` in CI to verify that committed
generated files still match their sources.
"""

from __future__ import annotations

import argparse
import difflib
import html
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Mapping
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HOME_TEMPLATE_PATH = SRC / "home.template.html"
RESEARCH_TEMPLATE_PATH = SRC / "research.template.html"
PAPERS_PATH = SRC / "papers.json"
GOOGLE_VERIFICATION_PATH = SRC / "google-site-verification.txt"
BASE_URL = "https://chengchunliu.github.io"
DEFAULT_LASTMOD = "2026-10-13"

LANGUAGES: dict[str, dict[str, str]] = {
    "en": {
        "html_lang": "en",
        "directory": "",
        "home_path": "/",
        "short_label": "EN",
    },
    "zh-Hans": {
        "html_lang": "zh-Hans",
        "directory": "zh-hans",
        "home_path": "/zh-hans/",
        "short_label": "简",
    },
    "zh-Hant": {
        "html_lang": "zh-Hant",
        "directory": "zh-hant",
        "home_path": "/zh-hant/",
        "short_label": "繁",
    },
}

LOCALE_PATHS = {
    language: SRC / "locales" / f"{language}.json" for language in LANGUAGES
}

HOME_RESEARCH_TOKENS = {
    "spectromol-multimodal-structure-elucidation": "RESEARCH_SPECTROMOL_URL",
    "geoopt-net": "RESEARCH_GEOOPT_URL",
    "uhsr-symbolic-regression": "RESEARCH_UHSR_URL",
    "ai-chromatography": "RESEARCH_CHROMATOGRAPHY_URL",
    "infrared-spectrum-prediction": "RESEARCH_INFRARED_URL",
}

HOME_REQUIRED_TOKENS = {
    "HTML_LANG",
    "CANONICAL_URL",
    "HREFLANG_LINKS",
    "GOOGLE_SITE_VERIFICATION",
    "ASSET_PREFIX",
    "JSON_LD",
    "LANG_EN_URL",
    "LANG_ZH_HANS_URL",
    "LANG_ZH_HANT_URL",
    "LANG_EN_CURRENT",
    "LANG_ZH_HANS_CURRENT",
    "LANG_ZH_HANT_CURRENT",
    *HOME_RESEARCH_TOKENS.values(),
}

RESEARCH_REQUIRED_TOKENS = {
    "HTML_LANG",
    "PAGE_TITLE",
    "META_DESCRIPTION",
    "CANONICAL_URL",
    "HREFLANG_LINKS",
    "OPEN_GRAPH_TAGS",
    "TWITTER_TAGS",
    "CITATION_META",
    "JSON_LD",
    "ASSET_PREFIX",
    "HOME_URL",
    "BACK_LABEL",
    "SKIP_LABEL",
    "PAGE_LABEL",
    "JOURNAL",
    "YEAR",
    "PAPER_TITLE",
    "AUTHORS_HTML",
    "SUMMARY",
    "DOI_URL",
    "DOI",
    "CODE_LINK_HTML",
    "CONCEPT_ART_HTML",
    "PROBLEM_LABEL",
    "PROBLEM",
    "APPROACH_LABEL",
    "APPROACH",
    "WHY_LABEL",
    "WHY",
    "PUBLICATION_DETAILS_LABEL",
    "AUTHORS_LABEL",
    "JOURNAL_LABEL",
    "YEAR_LABEL",
    "DOI_LABEL",
    "BIBTEX",
    "RELATED_LABEL",
    "RELATED_RESEARCH_HTML",
    "LANGUAGE_LINKS",
    "FOOTER_TEXT",
    "BACK_TOP",
}

TOKEN_RE = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
I18N_MARKER_RE = re.compile(
    r"\bdata-i18n(?:-content|-alt|-aria-label)?\s*=\s*([\"'])([^\"']+)\1"
)


class BuildError(RuntimeError):
    """A source or template error that should stop the build."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise BuildError(f"Required source file is missing: {path}") from exc


def read_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise BuildError(
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def validate_sources(
    locales: Mapping[str, Mapping[str, str]], papers: list[Mapping[str, Any]]
) -> None:
    if set(locales) != set(LANGUAGES):
        raise BuildError("Locale files do not match the configured language set.")

    reference_keys = set(locales["en"])
    for language, locale in locales.items():
        if not all(isinstance(key, str) and isinstance(value, str) for key, value in locale.items()):
            raise BuildError(f"Every key and value in {LOCALE_PATHS[language]} must be a string.")
        missing = reference_keys - set(locale)
        extra = set(locale) - reference_keys
        if missing or extra:
            details = []
            if missing:
                details.append(f"missing {sorted(missing)}")
            if extra:
                details.append(f"extra {sorted(extra)}")
            raise BuildError(f"Locale key mismatch in {LOCALE_PATHS[language]}: {'; '.join(details)}")

    required_locale_keys = {
        "pageTitle",
        "metaDescription",
        "socialDescription",
        "socialImageAlt",
        "displayName",
        "ogLocale",
        "researchBack",
        "researchPageLabel",
        "researchQuestion",
        "researchApproach",
        "researchWhy",
        "publicationDetails",
        "authorsLabel",
        "journalLabel",
        "yearLabel",
        "doiLabel",
        "codeLink",
        "relatedResearch",
        "researchFooter",
        "backTop",
    }
    for language, locale in locales.items():
        missing = required_locale_keys - set(locale)
        if missing:
            raise BuildError(
                f"{LOCALE_PATHS[language]} is missing research UI keys: {sorted(missing)}"
            )

    if len(papers) != 5:
        raise BuildError(f"Expected exactly five selected papers in {PAPERS_PATH}; found {len(papers)}.")

    required_paper_fields = {
        "slug",
        "shortName",
        "title",
        "journal",
        "year",
        "doi",
        "datePublished",
        "authors",
        "equalContributors",
        "keywords",
        "locales",
    }
    required_paper_locale_fields = {
        "seoTitle",
        "description",
        "summary",
        "problem",
        "approach",
        "why",
    }
    slugs: set[str] = set()
    dois: set[str] = set()
    for index, paper in enumerate(papers, start=1):
        missing = required_paper_fields - set(paper)
        if missing:
            raise BuildError(f"Paper {index} is missing fields: {sorted(missing)}")
        slug = paper["slug"]
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise BuildError(f"Paper {index} has an unsafe slug: {slug!r}")
        if slug in slugs:
            raise BuildError(f"Duplicate paper slug: {slug}")
        slugs.add(slug)
        doi = paper["doi"]
        if not isinstance(doi, str) or not doi.startswith("10.") or doi in dois:
            raise BuildError(f"Paper {slug} has an invalid or duplicate DOI: {doi!r}")
        dois.add(doi)
        if not isinstance(paper["datePublished"], str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", paper["datePublished"]
        ):
            raise BuildError(
                f"Paper {slug} has an invalid datePublished value: {paper['datePublished']!r}"
            )
        if not paper.get("pages") and not paper.get("articleNumber"):
            raise BuildError(f"Paper {slug} needs pages or articleNumber metadata.")
        authors = paper["authors"]
        if not isinstance(authors, list) or not authors or not all(isinstance(author, str) for author in authors):
            raise BuildError(f"Paper {slug} must have a non-empty string author list.")
        equal_contributors = paper["equalContributors"]
        if not isinstance(equal_contributors, list) or not set(equal_contributors).issubset(authors):
            raise BuildError(f"Paper {slug} has invalid equalContributors entries.")
        if set(paper["locales"]) != set(LANGUAGES):
            raise BuildError(f"Paper {slug} must contain all three language records.")
        for language, localized in paper["locales"].items():
            missing_localized = required_paper_locale_fields - set(localized)
            if missing_localized:
                raise BuildError(
                    f"Paper {slug} locale {language} is missing: {sorted(missing_localized)}"
                )

    missing_home_routes = set(HOME_RESEARCH_TOKENS) - slugs
    if missing_home_routes:
        raise BuildError(f"Homepage route mapping refers to unknown papers: {sorted(missing_home_routes)}")


def validate_template(
    template: str, template_path: Path, required_tokens: set[str], available_tokens: Iterable[str]
) -> None:
    found = set(TOKEN_RE.findall(template))
    missing_placeholders = required_tokens - found
    if missing_placeholders:
        raise BuildError(
            f"{template_path} is missing required placeholders: "
            + ", ".join(f"{{{{{token}}}}}" for token in sorted(missing_placeholders))
        )
    unknown = found - set(available_tokens)
    if unknown:
        raise BuildError(
            f"{template_path} contains placeholders that the builder cannot provide: "
            + ", ".join(f"{{{{{token}}}}}" for token in sorted(unknown))
        )


def render_template(template: str, context: Mapping[str, str], template_path: Path) -> str:
    found = set(TOKEN_RE.findall(template))
    missing_values = found - set(context)
    if missing_values:
        raise BuildError(
            f"No value was provided for placeholders in {template_path}: "
            + ", ".join(f"{{{{{token}}}}}" for token in sorted(missing_values))
        )

    rendered = TOKEN_RE.sub(lambda match: context[match.group(1)], template)
    unresolved = sorted(set(TOKEN_RE.findall(rendered)))
    if unresolved:
        raise BuildError(
            f"Unresolved placeholders remain after rendering {template_path}: {unresolved}"
        )
    return rendered


def _localize_tag_attribute(
    document: str,
    locale: Mapping[str, str],
    marker: str,
    target_attribute: str,
    source_name: str,
) -> str:
    marker_pattern = re.compile(
        rf"<[A-Za-z][^<>]*\b{re.escape(marker)}\s*=\s*([\"'])(?P<key>[^\"']+)\1[^<>]*>",
        re.DOTALL,
    )
    target_pattern = re.compile(
        rf"(?P<prefix>\s{re.escape(target_attribute)}\s*=\s*)(?P<quote>[\"'])(?P<value>.*?)(?P=quote)",
        re.DOTALL | re.IGNORECASE,
    )

    def replace_tag(match: re.Match[str]) -> str:
        tag = match.group(0)
        key = match.group("key")
        if key not in locale:
            raise BuildError(f"{source_name} refers to missing locale key {key!r}.")
        escaped_value = html.escape(locale[key], quote=True)
        if not target_pattern.search(tag):
            raise BuildError(
                f"Tag marked with {marker}={key!r} in {source_name} has no {target_attribute} attribute."
            )
        return target_pattern.sub(
            lambda attr: f"{attr.group('prefix')}{attr.group('quote')}{escaped_value}{attr.group('quote')}",
            tag,
            count=1,
        )

    return marker_pattern.sub(replace_tag, document)


def localize_home(document: str, locale: Mapping[str, str], source_name: str) -> str:
    """Resolve the existing data-i18n markers into crawlable static HTML."""

    for marker_match in I18N_MARKER_RE.finditer(document):
        key = marker_match.group(2)
        if key not in locale:
            raise BuildError(f"{source_name} refers to missing locale key {key!r}.")

    document = _localize_tag_attribute(
        document, locale, "data-i18n-content", "content", source_name
    )
    document = _localize_tag_attribute(document, locale, "data-i18n-alt", "alt", source_name)
    document = _localize_tag_attribute(
        document, locale, "data-i18n-aria-label", "aria-label", source_name
    )

    element_pattern = re.compile(
        r"(?P<open><(?P<tag>[A-Za-z][\w:-]*)\b"
        r"(?=[^<>]*\sdata-i18n\s*=\s*([\"'])(?P<key>[^\"']+)\3)[^<>]*>)"
        r"(?P<body>.*?)"
        r"(?P<close></(?P=tag)\s*>)",
        re.DOTALL,
    )

    def replace_element(match: re.Match[str]) -> str:
        key = match.group("key")
        if key not in locale:
            raise BuildError(f"{source_name} refers to missing locale key {key!r}.")
        value = html.escape(locale[key], quote=False)
        return f"{match.group('open')}{value}{match.group('close')}"

    document = element_pattern.sub(replace_element, document)
    return document


def home_output_path(language: str) -> Path:
    directory = LANGUAGES[language]["directory"]
    return Path(directory) / "index.html" if directory else Path("index.html")


def research_output_path(language: str, slug: str) -> Path:
    directory = LANGUAGES[language]["directory"]
    if directory:
        return Path(directory) / "research" / slug / "index.html"
    return Path("research") / slug / "index.html"


def home_path(language: str) -> str:
    return LANGUAGES[language]["home_path"]


def research_path(language: str, slug: str) -> str:
    directory = LANGUAGES[language]["directory"]
    prefix = f"/{directory}" if directory else ""
    return f"{prefix}/research/{slug}/"


def absolute_url(path: str) -> str:
    return f"{BASE_URL}{path}"


def asset_prefix(output_path: Path) -> str:
    depth = len(output_path.parent.parts)
    return "../" * depth


def hreflang_links(paths: Mapping[str, str]) -> str:
    lines = [
        f'<link rel="alternate" hreflang="{LANGUAGES[language]["html_lang"]}" href="{html.escape(absolute_url(paths[language]), quote=True)}" />'
        for language in LANGUAGES
    ]
    lines.append(
        f'<link rel="alternate" hreflang="x-default" href="{html.escape(absolute_url(paths["en"]), quote=True)}" />'
    )
    return "\n    ".join(lines)


def language_links(paths: Mapping[str, str], current_language: str) -> str:
    links = []
    for language, config in LANGUAGES.items():
        current = ' aria-current="page"' if language == current_language else ""
        links.append(
            f'<a href="{html.escape(paths[language], quote=True)}" lang="{config["html_lang"]}" '
            f'hreflang="{config["html_lang"]}"{current}>{config["short_label"]}</a>'
        )
    return "\n        ".join(links)


def home_json_ld(language: str, locale: Mapping[str, str], canonical: str) -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{BASE_URL}/#website",
                "url": f"{BASE_URL}/",
                "name": "Chengchun Liu Research Portfolio",
                "alternateName": ["刘丞军学术主页", "劉丞軍學術網站"],
                "inLanguage": ["en", "zh-Hans", "zh-Hant"],
            },
            {
                "@type": "ProfilePage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": locale["pageTitle"],
                "description": locale["metaDescription"],
                "inLanguage": language,
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
                "about": {"@id": f"{BASE_URL}/#person"},
                "mainEntity": {"@id": f"{BASE_URL}/#person"},
                "primaryImageOfPage": {"@id": f"{BASE_URL}/#portrait"},
            },
            {
                "@type": "ImageObject",
                "@id": f"{BASE_URL}/#portrait",
                "url": f"{BASE_URL}/assets/chengchun-liu-360.jpg",
                "contentUrl": f"{BASE_URL}/assets/chengchun-liu-360.jpg",
                "caption": locale["portraitAlt"],
            },
            {
                "@type": "Person",
                "@id": f"{BASE_URL}/#person",
                "name": "Chengchun Liu",
                "alternateName": ["刘丞军", "劉丞軍"],
                "url": f"{BASE_URL}/",
                "image": {"@id": f"{BASE_URL}/#portrait"},
                "jobTitle": "Ph.D. candidate",
                "email": "liuchengchun@stu.pku.edu.cn",
                "affiliation": {
                    "@type": "CollegeOrUniversity",
                    "name": "Peking University",
                    "url": "https://www.pku.edu.cn/",
                },
                "alumniOf": {
                    "@type": "CollegeOrUniversity",
                    "name": "Nankai University",
                    "url": "https://en.nankai.edu.cn/",
                },
                "identifier": {
                    "@type": "PropertyValue",
                    "propertyID": "ORCID",
                    "value": "0009-0002-5550-4145",
                    "url": "https://orcid.org/0009-0002-5550-4145",
                },
                "sameAs": [
                    "https://scholar.google.com/citations?user=iRoA5jUAAAAJ",
                    "https://github.com/ChengchunLiu",
                    "https://orcid.org/0009-0002-5550-4145",
                    "https://www.linkedin.com/in/chengchun-liu-9a93bb243/",
                    "https://www.instagram.com/liuchengchun/",
                ],
                "knowsAbout": [
                    "Artificial intelligence for chemistry",
                    "Molecular spectroscopy",
                    "Molecular geometry refinement",
                    "Scientific agents",
                    "Chromatography",
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=2)


def homepage_context(
    language: str,
    output_path: Path,
    locale: Mapping[str, str],
    google_verification: str,
) -> dict[str, str]:
    paths = {candidate: home_path(candidate) for candidate in LANGUAGES}
    context = {
        "HTML_LANG": LANGUAGES[language]["html_lang"],
        "CANONICAL_URL": absolute_url(paths[language]),
        "HREFLANG_LINKS": hreflang_links(paths),
        "GOOGLE_SITE_VERIFICATION": (
            f'<meta name="google-site-verification" content="{html.escape(google_verification, quote=True)}" />'
            if google_verification
            else ""
        ),
        "ASSET_PREFIX": asset_prefix(output_path),
        "JSON_LD": home_json_ld(language, locale, absolute_url(paths[language])),
        "LANG_EN_URL": paths["en"],
        "LANG_ZH_HANS_URL": paths["zh-Hans"],
        "LANG_ZH_HANT_URL": paths["zh-Hant"],
        "LANG_EN_CURRENT": 'aria-current="page"' if language == "en" else "",
        "LANG_ZH_HANS_CURRENT": 'aria-current="page"' if language == "zh-Hans" else "",
        "LANG_ZH_HANT_CURRENT": 'aria-current="page"' if language == "zh-Hant" else "",
    }
    for slug, token in HOME_RESEARCH_TOKENS.items():
        context[token] = research_path(language, slug)
    return context


def formatted_authors(paper: Mapping[str, Any]) -> str:
    equal = set(paper["equalContributors"])
    authors = []
    for author in paper["authors"]:
        author_html = html.escape(author)
        if author in equal:
            author_html += '<sup aria-label="equal contributor">†</sup>'
        authors.append(author_html)
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    return f"{', '.join(authors[:-1])}, and {authors[-1]}"


def bibtex_for(paper: Mapping[str, Any]) -> str:
    surname = re.sub(r"[^A-Za-z0-9]", "", paper["authors"][0].split()[-1]).lower()
    short_name = re.sub(r"[^A-Za-z0-9]", "", paper["shortName"]).lower()
    citation_key = f"{surname}{paper['year']}{short_name}"
    author_line = " and ".join(paper["authors"])
    # A mapping makes duplicate BibTeX field names impossible while preserving
    # insertion order on every supported Python version.
    fields = {
        "title": paper["title"],
        "author": author_line,
        "journal": paper["journal"],
        "year": paper["year"],
        "date": paper["datePublished"],
    }
    if paper.get("volume"):
        fields["volume"] = paper["volume"]
    if paper.get("issue"):
        fields["number"] = paper["issue"]
    if paper.get("pages"):
        fields["pages"] = paper["pages"].replace("–", "--")
    if paper.get("articleNumber"):
        fields["eid"] = paper["articleNumber"]
    fields["doi"] = paper["doi"]
    fields["url"] = f"https://doi.org/{paper['doi']}"
    field_lines = [
        f"  {name:<7} = {{{value}}}{',' if index < len(fields) - 1 else ''}"
        for index, (name, value) in enumerate(fields.items())
    ]
    return f"@article{{{citation_key},\n" + "\n".join(field_lines) + "\n}"


def research_open_graph(
    paper: Mapping[str, Any], localized: Mapping[str, str], language: str, canonical: str
) -> str:
    values = {
        "title": html.escape(localized["seoTitle"], quote=True),
        "description": html.escape(localized["description"], quote=True),
        "canonical": html.escape(canonical, quote=True),
        "site": html.escape("Chengchun Liu", quote=True),
        "locale": html.escape(
            {"en": "en_US", "zh-Hans": "zh_CN", "zh-Hant": "zh_TW"}[language],
            quote=True,
        ),
        "image": f"{BASE_URL}/assets/og-preview.png",
        "image_alt": html.escape(f"{paper['shortName']} — Chengchun Liu", quote=True),
    }
    return "\n    ".join(
        [
            '<meta property="og:type" content="article" />',
            f'<meta property="og:title" content="{values["title"]}" />',
            f'<meta property="og:description" content="{values["description"]}" />',
            f'<meta property="og:url" content="{values["canonical"]}" />',
            f'<meta property="og:site_name" content="{values["site"]}" />',
            f'<meta property="og:locale" content="{values["locale"]}" />',
            f'<meta property="og:image" content="{values["image"]}" />',
            '<meta property="og:image:width" content="1200" />',
            '<meta property="og:image:height" content="630" />',
            f'<meta property="og:image:alt" content="{values["image_alt"]}" />',
        ]
    )


def research_twitter(paper: Mapping[str, Any], localized: Mapping[str, str]) -> str:
    title = html.escape(localized["seoTitle"], quote=True)
    description = html.escape(localized["description"], quote=True)
    image_alt = html.escape(f"{paper['shortName']} — Chengchun Liu", quote=True)
    return "\n    ".join(
        [
            '<meta name="twitter:card" content="summary_large_image" />',
            f'<meta name="twitter:title" content="{title}" />',
            f'<meta name="twitter:description" content="{description}" />',
            f'<meta name="twitter:image" content="{BASE_URL}/assets/og-preview.png" />',
            f'<meta name="twitter:image:alt" content="{image_alt}" />',
        ]
    )


def citation_meta(paper: Mapping[str, Any], canonical: str) -> str:
    tags = [
        f'<meta name="citation_title" content="{html.escape(paper["title"], quote=True)}" />'
    ]
    tags.extend(
        f'<meta name="citation_author" content="{html.escape(author, quote=True)}" />'
        for author in paper["authors"]
    )
    tags.extend(
        [
            f'<meta name="citation_journal_title" content="{html.escape(paper["journal"], quote=True)}" />',
            f'<meta name="citation_publication_date" content="{html.escape(paper["datePublished"], quote=True)}" />',
            f'<meta name="citation_doi" content="{html.escape(paper["doi"], quote=True)}" />',
            f'<meta name="citation_abstract_html_url" content="{html.escape(canonical, quote=True)}" />',
        ]
    )
    return "\n    ".join(tags)


def research_json_ld(
    paper: Mapping[str, Any],
    localized: Mapping[str, str],
    language: str,
    canonical: str,
    home_url: str,
) -> str:
    authors = []
    for author in paper["authors"]:
        person: dict[str, Any] = {"@type": "Person", "name": author}
        if author == "Chengchun Liu":
            person["@id"] = f"{BASE_URL}/#person"
            person["alternateName"] = ["刘丞军", "劉丞軍"]
        authors.append(person)

    publication_container: dict[str, Any] = {
        "@type": "Periodical",
        "name": paper["journal"],
    }
    if paper.get("volume"):
        publication_container = {
            "@type": "PublicationVolume",
            "volumeNumber": paper["volume"],
            "isPartOf": publication_container,
        }
    if paper.get("issue"):
        publication_container = {
            "@type": "PublicationIssue",
            "issueNumber": paper["issue"],
            "isPartOf": publication_container,
        }

    article: dict[str, Any] = {
        "@type": "ScholarlyArticle",
        "@id": f"https://doi.org/{paper['doi']}",
        "url": canonical,
        "sameAs": f"https://doi.org/{paper['doi']}",
        "headline": paper["title"],
        "name": paper["title"],
        "abstract": localized["summary"],
        "inLanguage": language,
        "datePublished": paper["datePublished"],
        "author": authors,
        "isPartOf": publication_container,
        "pagination": paper.get("pages") or paper.get("articleNumber"),
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "DOI",
            "value": paper["doi"],
            "url": f"https://doi.org/{paper['doi']}",
        },
        "keywords": paper["keywords"],
        "mainEntityOfPage": {"@id": f"{canonical}#webpage"},
    }
    if paper.get("code"):
        article["hasPart"] = {
            "@type": "SoftwareSourceCode",
            "name": f"Source code for {paper['shortName']}",
            "codeRepository": paper["code"],
            "url": paper["code"],
        }

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": localized["seoTitle"],
                "description": localized["description"],
                "inLanguage": language,
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
                "mainEntity": {"@id": f"https://doi.org/{paper['doi']}"},
                "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
            },
            article,
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Chengchun Liu",
                        "item": home_url,
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": paper["shortName"],
                        "item": canonical,
                    },
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=2)


CONCEPTS = {
    "spectromol-multimodal-structure-elucidation": (
        "spectromol",
        ("NMR + IR + MS", "Hypothesis", "Refinement"),
    ),
    "geoopt-net": ("geoopt", ("Force field", "SE(3)", "DFT geometry")),
    "uhsr-symbolic-regression": ("uhsr", ("x₁ · x₂ · xₙ", "Φ", "ŷ = f(Φ)")),
    "ai-chromatography": ("chromatography", ("Molecule", "Column", "Closed loop")),
    "infrared-spectrum-prediction": (
        "infrared",
        ("Structure", "Neighborhood", "IR response"),
    ),
}


def concept_art(paper: Mapping[str, Any], index: int) -> str:
    variant, steps = CONCEPTS.get(
        paper["slug"], ("generic", ("Evidence", "Model", "Insight"))
    )
    escaped_steps = [html.escape(step) for step in steps]
    return (
        f'<div class="concept-art concept-{variant}">\n'
        '  <span class="concept-orbit"></span>\n'
        f'  <span class="concept-chip">{index:02d} · {html.escape(paper["shortName"])}</span>\n'
        '  <div class="concept-grid">\n'
        f'    <span class="concept-node">{escaped_steps[0]}</span>\n'
        f'    <span class="concept-node is-primary">{escaped_steps[1]}</span>\n'
        f'    <span class="concept-node">{escaped_steps[2]}</span>\n'
        "  </div>\n"
        '  <span class="concept-line"></span>\n'
        '  <div class="concept-spectrum"></div>\n'
        "</div>"
    )


def code_link(paper: Mapping[str, Any], locale: Mapping[str, str]) -> str:
    if not paper.get("code"):
        return ""
    return (
        f'<a class="button button-text research-code-link" href="{html.escape(paper["code"], quote=True)}" '
        'target="_blank" rel="noopener noreferrer">'
        f'<span>{html.escape(locale["codeLink"])}</span><span aria-hidden="true">↗</span></a>'
    )


def related_research(
    paper: Mapping[str, Any],
    papers: list[Mapping[str, Any]],
    language: str,
) -> str:
    index = papers.index(paper)
    related = [papers[(index + offset) % len(papers)] for offset in (1, 2)]
    cards = []
    for candidate in related:
        cards.append(
            f'<a class="related-research-card" href="{html.escape(research_path(language, candidate["slug"]), quote=True)}">\n'
            f'  <span class="related-research-meta">{html.escape(candidate["journal"])} · {html.escape(candidate["year"])}</span>\n'
            f'  <strong class="related-research-title" lang="en">{html.escape(candidate["title"])}</strong>\n'
            '  <span class="related-research-arrow" aria-hidden="true">→</span>\n'
            "</a>"
        )
    return "\n              ".join(cards)


def research_context(
    paper: Mapping[str, Any],
    paper_index: int,
    papers: list[Mapping[str, Any]],
    language: str,
    output_path: Path,
    locale: Mapping[str, str],
) -> dict[str, str]:
    localized = paper["locales"][language]
    paths = {candidate: research_path(candidate, paper["slug"]) for candidate in LANGUAGES}
    canonical = absolute_url(paths[language])
    language_home = absolute_url(home_path(language))
    return {
        "HTML_LANG": LANGUAGES[language]["html_lang"],
        "PAGE_TITLE": html.escape(localized["seoTitle"]),
        "META_DESCRIPTION": html.escape(localized["description"], quote=True),
        "CANONICAL_URL": html.escape(canonical, quote=True),
        "HREFLANG_LINKS": hreflang_links(paths),
        "OPEN_GRAPH_TAGS": research_open_graph(paper, localized, language, canonical),
        "TWITTER_TAGS": research_twitter(paper, localized),
        "CITATION_META": citation_meta(paper, canonical),
        "JSON_LD": research_json_ld(
            paper, localized, language, canonical, language_home
        ),
        "ASSET_PREFIX": asset_prefix(output_path),
        "HOME_URL": html.escape(home_path(language), quote=True),
        "BACK_LABEL": html.escape(locale["researchBack"]),
        "SKIP_LABEL": html.escape(locale["skip"]),
        "PAGE_LABEL": html.escape(locale["researchPageLabel"]),
        "JOURNAL": html.escape(paper["journal"]),
        "YEAR": html.escape(paper["year"]),
        "PAPER_TITLE": html.escape(paper["title"]),
        "AUTHORS_HTML": formatted_authors(paper),
        "SUMMARY": html.escape(localized["summary"]),
        "DOI_URL": html.escape(f"https://doi.org/{paper['doi']}", quote=True),
        "DOI": html.escape(paper["doi"]),
        "CODE_LINK_HTML": code_link(paper, locale),
        "CONCEPT_ART_HTML": concept_art(paper, paper_index),
        "PROBLEM_LABEL": html.escape(locale["researchQuestion"]),
        "PROBLEM": html.escape(localized["problem"]),
        "APPROACH_LABEL": html.escape(locale["researchApproach"]),
        "APPROACH": html.escape(localized["approach"]),
        "WHY_LABEL": html.escape(locale["researchWhy"]),
        "WHY": html.escape(localized["why"]),
        "PUBLICATION_DETAILS_LABEL": html.escape(locale["publicationDetails"]),
        "AUTHORS_LABEL": html.escape(locale["authorsLabel"]),
        "JOURNAL_LABEL": html.escape(locale["journalLabel"]),
        "YEAR_LABEL": html.escape(locale["yearLabel"]),
        "DOI_LABEL": html.escape(locale["doiLabel"]),
        "BIBTEX": html.escape(bibtex_for(paper)),
        "RELATED_LABEL": html.escape(locale["relatedResearch"]),
        "RELATED_RESEARCH_HTML": related_research(paper, papers, language),
        "LANGUAGE_LINKS": language_links(paths, language),
        "FOOTER_TEXT": html.escape(locale["researchFooter"]),
        "BACK_TOP": html.escape(locale["backTop"]),
    }


def extract_json_ld(document: str, page_name: str) -> list[Any]:
    scripts = re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        document,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not scripts:
        raise BuildError(f"Generated page {page_name} has no JSON-LD block.")
    parsed = []
    for script in scripts:
        try:
            parsed.append(json.loads(script))
        except json.JSONDecodeError as exc:
            raise BuildError(f"Generated page {page_name} has invalid JSON-LD: {exc}") from exc
    return parsed


def validate_rendered_page(
    document: str,
    page_name: str,
    language: str,
    canonical: str,
    paper: Mapping[str, Any] | None = None,
) -> None:
    if TOKEN_RE.search(document):
        raise BuildError(f"Generated page {page_name} still contains an unresolved template token.")
    expected_lang = LANGUAGES[language]["html_lang"]
    if not re.search(rf'<html\b[^>]*\blang="{re.escape(expected_lang)}"', document):
        raise BuildError(f"Generated page {page_name} does not declare lang={expected_lang!r}.")
    if f'<link rel="canonical" href="{html.escape(canonical, quote=True)}"' not in document:
        raise BuildError(f"Generated page {page_name} has the wrong canonical URL.")
    for hreflang in ("en", "zh-Hans", "zh-Hant", "x-default"):
        if f'hreflang="{hreflang}"' not in document:
            raise BuildError(f"Generated page {page_name} is missing hreflang={hreflang!r}.")
    extract_json_ld(document, page_name)

    if paper is None:
        for slug in HOME_RESEARCH_TOKENS:
            if research_path(language, slug) not in document:
                raise BuildError(f"Generated homepage {page_name} does not link to research/{slug}.")
    else:
        author_meta_count = len(re.findall(r'name="citation_author"', document))
        if author_meta_count != len(paper["authors"]):
            raise BuildError(
                f"Generated research page {page_name} has {author_meta_count} citation authors; "
                f"expected {len(paper['authors'])}."
            )
        required_citation_fields = (
            "citation_title",
            "citation_journal_title",
            "citation_publication_date",
            "citation_doi",
        )
        for field in required_citation_fields:
            if f'name="{field}"' not in document:
                raise BuildError(f"Generated research page {page_name} is missing {field}.")
        if "citation_pdf_url" in document:
            raise BuildError(f"Generated research page {page_name} must not claim a PDF URL.")
        if document.count('class="related-research-card"') < 2:
            raise BuildError(f"Generated research page {page_name} needs at least two related links.")


def sitemap_xml(papers: list[Mapping[str, Any]], lastmod: str) -> str:
    route_groups: list[dict[str, str]] = [
        {language: home_path(language) for language in LANGUAGES}
    ]
    route_groups.extend(
        {
            language: research_path(language, paper["slug"])
            for language in LANGUAGES
        }
        for paper in papers
    )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for group_index, routes in enumerate(route_groups):
        for language, path in routes.items():
            lines.append("  <url>")
            lines.append(f"    <loc>{xml_escape(absolute_url(path))}</loc>")
            lines.append(f"    <lastmod>{xml_escape(lastmod)}</lastmod>")
            lines.append("    <changefreq>monthly</changefreq>")
            lines.append(f"    <priority>{'1.0' if group_index == 0 else '0.8'}</priority>")
            for alternate_language, alternate_path in routes.items():
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="{LANGUAGES[alternate_language]["html_lang"]}" '
                    f'href="{xml_escape(absolute_url(alternate_path))}" />'
                )
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" '
                f'href="{xml_escape(absolute_url(routes["en"]))}" />'
            )
            lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build_outputs(google_verification: str, lastmod: str) -> dict[Path, str]:
    home_template = read_text(HOME_TEMPLATE_PATH)
    research_template = read_text(RESEARCH_TEMPLATE_PATH)
    locales = {language: read_json(path) for language, path in LOCALE_PATHS.items()}
    papers = read_json(PAPERS_PATH)
    if not isinstance(papers, list):
        raise BuildError(f"{PAPERS_PATH} must contain a JSON array.")
    validate_sources(locales, papers)

    home_available_tokens = set(HOME_REQUIRED_TOKENS)
    research_available_tokens = set(RESEARCH_REQUIRED_TOKENS)
    validate_template(
        home_template, HOME_TEMPLATE_PATH, HOME_REQUIRED_TOKENS, home_available_tokens
    )
    validate_template(
        research_template,
        RESEARCH_TEMPLATE_PATH,
        RESEARCH_REQUIRED_TOKENS,
        research_available_tokens,
    )

    outputs: dict[Path, str] = {}
    for language, locale in locales.items():
        output_path = home_output_path(language)
        context = homepage_context(
            language, output_path, locale, google_verification.strip()
        )
        rendered = render_template(home_template, context, HOME_TEMPLATE_PATH)
        rendered = localize_home(rendered, locale, str(HOME_TEMPLATE_PATH))
        if not rendered.endswith("\n"):
            rendered += "\n"
        canonical = absolute_url(home_path(language))
        validate_rendered_page(rendered, str(output_path), language, canonical)
        outputs[output_path] = rendered

        for paper_index, paper in enumerate(papers, start=1):
            output_path = research_output_path(language, paper["slug"])
            context = research_context(
                paper, paper_index, papers, language, output_path, locale
            )
            rendered = render_template(
                research_template, context, RESEARCH_TEMPLATE_PATH
            )
            if not rendered.endswith("\n"):
                rendered += "\n"
            canonical = absolute_url(research_path(language, paper["slug"]))
            validate_rendered_page(
                rendered, str(output_path), language, canonical, paper=paper
            )
            outputs[output_path] = rendered

    outputs[Path("sitemap.xml")] = sitemap_xml(papers, lastmod)
    return outputs


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)
    temporary_path.replace(path)


def write_outputs(outputs: Mapping[Path, str]) -> int:
    changed = 0
    for relative_path, content in outputs.items():
        destination = ROOT / relative_path
        current = destination.read_text(encoding="utf-8") if destination.exists() else None
        if current == content:
            continue
        write_atomic(destination, content)
        changed += 1
        print(f"built {relative_path}")
    if changed == 0:
        print("generated site is already up to date")
    else:
        print(f"built {changed} generated file{'s' if changed != 1 else ''}")
    return 0


def check_outputs(outputs: Mapping[Path, str]) -> int:
    differences = 0
    for relative_path, expected in outputs.items():
        destination = ROOT / relative_path
        if not destination.exists():
            print(f"missing generated file: {relative_path}", file=sys.stderr)
            differences += 1
            continue
        actual = destination.read_text(encoding="utf-8")
        if actual == expected:
            continue
        differences += 1
        print(f"out-of-date generated file: {relative_path}", file=sys.stderr)
        diff = difflib.unified_diff(
            actual.splitlines(),
            expected.splitlines(),
            fromfile=f"current/{relative_path}",
            tofile=f"expected/{relative_path}",
            lineterm="",
            n=2,
        )
        for line_index, line in enumerate(diff):
            if line_index >= 80:
                print("... diff truncated ...", file=sys.stderr)
                break
            print(line, file=sys.stderr)
    if differences:
        print(
            f"{differences} generated file{'s are' if differences != 1 else ' is'} stale; "
            "run python3 scripts/build_site.py",
            file=sys.stderr,
        )
        return 1
    print(f"checked {len(outputs)} generated files; all are up to date")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare generated output with committed files without writing",
    )
    parser.add_argument(
        "--google-site-verification",
        default=(
            os.environ.get("GOOGLE_SITE_VERIFICATION", "")
            or (
                GOOGLE_VERIFICATION_PATH.read_text(encoding="utf-8").strip()
                if GOOGLE_VERIFICATION_PATH.exists()
                else ""
            )
        ),
        metavar="TOKEN",
        help=(
            "optional Google Search Console HTML meta verification token; "
            "defaults to GOOGLE_SITE_VERIFICATION or src/google-site-verification.txt"
        ),
    )
    parser.add_argument(
        "--lastmod",
        default=os.environ.get("SITE_LASTMOD", DEFAULT_LASTMOD),
        metavar="YYYY-MM-DD",
        help=f"sitemap last-modified date (default: {DEFAULT_LASTMOD})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.lastmod):
        print("build error: --lastmod must use YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        outputs = build_outputs(args.google_site_verification, args.lastmod)
        return check_outputs(outputs) if args.check else write_outputs(outputs)
    except BuildError as exc:
        print(f"build error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
