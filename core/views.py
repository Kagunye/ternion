from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from . import content, fleet_svg
from .forms import QuoteRequestForm


def home(request):
    return render(request, "core/home.html", {
        "home": content.HOME,
        "values": content.VALUES,
        "vision": content.VISION,
        "mission": content.MISSION,
        "industries": content.INDUSTRIES,
        "why_us": content.WHY_US,
        "route": content.ROUTE,
        "sizes": fleet_svg.vehicles(),
    })


def page(request, slug):
    data = content.PAGES.get(slug)
    if data is None:
        raise Http404
    ctx = {"page": data, "slug": slug}
    if data.get("values"):
        ctx["values"] = content.VALUES
    if data.get("sizes"):
        ctx["sizes"] = fleet_svg.vehicles()
    if data.get("route"):
        ctx["route"] = content.ROUTE
    return render(request, "core/page.html", ctx)


def contact(request):
    initial = {}
    if request.GET.get("service") in dict(QuoteRequestForm.base_fields["service"].choices):
        initial["service"] = request.GET["service"]

    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you, your freight enquiry is in. Your Ternion contact will call you back.")
            return redirect(reverse("contact") + "#quote")
    else:
        form = QuoteRequestForm(initial=initial)

    return render(request, "core/contact.html", {"page": content.CONTACT, "form": form})
