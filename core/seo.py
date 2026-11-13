"""SEO helpers: canonical URLs, social tags and JSON-LD structured data."""
import json

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from . import content


def absolute(path):
    return settings.SITE_URL.rstrip("/") + path


def page_label(name):
    if name == "contact":
        return "Contact"
    data = content.PAGES.get(name)
    return data["label"] if data else name.title()


def organization():
    c = content.COMPANY
    return {
        "@type": ["Organization", "LocalBusiness"],
        "@id": absolute("/#organization"),
        "name": c["name"],
        "alternateName": "Ternion",
        "url": absolute("/"),
        "logo": absolute(static("img/logo.webp")),
        "image": absolute(static("img/og-image.jpg")),
        "description": content.SEO["home"][1],
        "slogan": "Never chase a truck again. We call you first.",
        "foundingDate": "2022-09",
        "telephone": c["phone"],
        "email": c["email"],
        "priceRange": "Quoted per shipment",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Mombasa Road",
            "addressLocality": "Nairobi",
            "addressCountry": "KE",
        },
        "areaServed": [{"@type": "City", "name": n} for n in
                       [*content.ROUTE["core"], *content.ROUTE["onward"]]],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "sales",
            "telephone": c["phone"],
            "email": c["email"],
            "areaServed": "KE",
            "availableLanguage": ["en"],
        },
        "knowsAbout": ["Road freight", "Inland distribution", "Container haulage", "Freight coordination"],
    }


def jsonld(url_name):
    graph = [
        organization(),
        {
            "@type": "WebSite",
            "@id": absolute("/#website"),
            "url": absolute("/"),
            "name": content.COMPANY["name"],
            "publisher": {"@id": absolute("/#organization")},
            "inLanguage": "en-KE",
        },
    ]
    if url_name in content.SEO and url_name != "home":
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": absolute("/")},
                {"@type": "ListItem", "position": 2, "name": page_label(url_name),
                 "item": absolute(reverse(url_name))},
            ],
        })
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return data.replace("</", "<\\/")     # safe inside <script>


def context(request, url_name):
    title, description = content.SEO.get(url_name, content.SEO["home"])
    return {
        "seo": {
            "title": title,
            "description": description,
            "canonical": absolute(request.path),
            "image": absolute(static("img/og-image.jpg")),
            "jsonld": jsonld(url_name),
        },
        "site_url": settings.SITE_URL.rstrip("/"),
    }
