from django.urls import path

from . import views

PAGE_SLUGS = ["about", "services", "industries", "operations", "cargodesk", "privacy", "terms"]

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
] + [
    path(f"{slug}/", views.page, {"slug": slug}, name=slug) for slug in PAGE_SLUGS
]
