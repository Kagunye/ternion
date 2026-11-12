from django.db import models


class QuoteRequest(models.Model):
    SERVICE_CHOICES = [
        ("road", "Road freight"),
        ("inland", "Inland distribution"),
        ("cargodesk", "CargoDesk enquiry"),
    ]

    name = models.CharField(max_length=120)
    company = models.CharField(max_length=160, blank=True)
    phone = models.CharField("Phone / WhatsApp", max_length=40)
    email = models.EmailField(blank=True)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, default="road")
    origin = models.CharField("Collection point", max_length=160)
    destination = models.CharField(max_length=160)
    cargo_type = models.CharField("Cargo type", max_length=160)
    weight = models.CharField("Approximate weight", max_length=60)
    movement_date = models.DateField("Preferred movement date", null=True, blank=True)
    release_time = models.CharField("Expected release time", max_length=80, blank=True,
                                    help_text="If the goods are awaiting release")
    closing_time = models.CharField("Store closing hour", max_length=80, blank=True,
                                    help_text="If your store closes at a set hour")
    message = models.TextField("Anything else", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.origin} → {self.destination}"
