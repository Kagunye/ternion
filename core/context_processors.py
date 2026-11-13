from . import content, seo


def site(request):
    match = getattr(request, "resolver_match", None)
    url_name = match.url_name if match else ""
    return {
        **seo.context(request, url_name),
        "company": content.COMPANY,
        "nav": content.NAV,
        "menu": content.MENU,
        "current": match.url_name if match else "",
    }
