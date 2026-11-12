from . import content


def site(request):
    match = getattr(request, "resolver_match", None)
    return {
        "company": content.COMPANY,
        "nav": content.NAV,
        "current": match.url_name if match else "",
    }
