"""Approved website copy for Ternion Ventures Limited (Nov 2026 content doc)."""

COMPANY = {
    "name": "Ternion Ventures Limited",
    "short": "Ternion",
    "tagline": "Transport · Logistics · Supply Chain Solutions",
    "contact_name": "Alfred Nzinga",
    "phone": "+254 724 388677",
    "phone_href": "+254724388677",
    "whatsapp": "https://wa.me/254724388677",
    "email": "alfrednzinga@gmail.com",
    "office": "Mombasa Road, Nairobi, Kenya",
}

NAV = [
    ("home", "Home"),
    ("about", "About"),
    ("services", "Services"),
    ("industries", "Industries"),
    ("operations", "Operations"),
    ("cargodesk", "CargoDesk"),
    ("contact", "Contact"),
]

HOME = {
    "headline": "Never chase a truck again.",
    "headline_accent": "We call you first.",
    "intro": (
        "Ternion Ventures Limited arranges road freight from Mombasa to Nairobi and onward across Kenya. "
        "We match your cargo to a truck, coordinate collection and follow the load through to signed handover. "
        "One named Ternion contact keeps your team informed along the way."
    ),
    "three_calls": [
        ("Loaded.", "Once the carrier confirms loading, we call with the dispatch details and expected arrival window. "
                    "Your warehouse can plan for a truck that is actually on the road."),
        ("Plans changed.", "A late release in Mombasa can cost you an unloading slot in godown. We call as soon as we learn "
                           "of a change, explain what it affects and agree when you'll hear from us next."),
        ("Delivered.", "We confirm handover and follow up on the signed delivery note. Where agreed, we send a photo to "
                       "your nominated WhatsApp contact so your office can close the job."),
    ],
}

VALUES = [
    ("Accountability", "We Own the Follow-Up",
     "Every shipment deserves someone who takes responsibility. From collection to signed handover, we coordinate the "
     "movement, keep customers informed and follow through until the job is complete."),
    ("Honesty and Communication", "We Call First",
     "We believe customers deserve clear information, not excuses. We communicate when cargo is loaded, alert them when "
     "plans change and confirm delivery. When challenges arise, we explain them early and agree on the next step."),
    ("Care and Commitment", "Every Load Matters",
     "Behind every shipment is a business depending on its arrival. We prioritise cargo safety, suitable carriers, timely "
     "coordination and proper delivery documentation. We treat every load with the care and attention it deserves."),
]

VISION = "A freight industry where cargo moves smoothly, customers stay informed, and nobody has to chase a truck."
MISSION = (
    "We connect cargo with the right trucks, coordinate every movement and keep customers informed before they have to "
    "ask. From collection to signed handover, one accountable Ternion contact takes responsibility for the follow-up, "
    "allowing customers to focus on their business instead of chasing deliveries."
)

INDUSTRIES = [
    ("Importers and clearing agents",
     "We coordinate the road leg around release at the container freight station. Your clearing contact handles the "
     "release arrangements. Your Ternion contact follows up on the truck and confirms when the cargo has loaded."),
    ("Manufacturers",
     "Inbound materials may have to arrive within a stores or production window. We agree the slot with your receiving "
     "team before dispatch and call if the expected arrival changes."),
    ("Wholesalers and distributors",
     "A delivery is still open on your books until the right person signs. We record the branch, receiving contact and "
     "document required, then follow up on the signed note after unloading."),
]

CTA_QUOTE = ("contact", "Request a freight quote")

PAGES = {
    "about": {
        "num": "02", "label": "About us", "title": "About us",
        "image": "img/truck-orange.webp", "sketch": "img/truck-orange-sketch.webp",
        "intro": (
            "Ternion Ventures Limited has coordinated commercial freight through contracted carriers since September 2022. "
            "Our growth plan adds company-owned trucks on repeat routes while retaining our carrier network for additional "
            "loads, different vehicle requirements and onward deliveries."
        ),
        "blocks_title": "What drives us",
        "blocks": [
            ("Our vision", VISION),
            ("Our mission", MISSION),
            ("Why three calls?", "Ternion is a group of three. In our business, three moments matter to the person waiting "
                                 "at the other end: the cargo leaves, the plan changes, the delivery is signed for. We built "
                                 "our customer promise around those moments."),
        ],
        "values": True,
        "cta": ("operations", "Explore our operations"),
    },
    "services": {
        "num": "03", "label": "Services", "title": "Services",
        "image": "img/truck-container.webp", "sketch": "img/truck-container-sketch.webp",
        "intro": (
            "We arrange road freight for individual consignments and repeat deliveries. The quotation sets out the journey, "
            "the agreed work, the price and the time the offer expires."
        ),
        "blocks_title": "What we arrange",
        "blocks": [
            ("Road freight", "We match the truck to the cargo weight, dimensions, loading method and access at destination. "
                             "For a coastal collection, the release time matters as much as the distance."),
            ("Inland distribution", "We check the full route, unloading access and receiving hours before quoting. Standard "
                                    "bookings include dispatch updates and delivery confirmation. For customers managing "
                                    "several parties or sites, CargoDesk is being developed as a separately priced "
                                    "coordination service."),
        ],
        "note": (
            "Each firm quote states what the price covers and how long it holds. If the destination, load or scope changes, "
            "we set out any revised price for approval before proceeding with the change."
        ),
        "sizes": True,
        "cta": CTA_QUOTE,
    },
    "industries": {
        "num": "04", "label": "Industries", "title": "Industries",
        "image": "img/container-hook.webp", "sketch": "img/container-hook-sketch.webp",
        "intro": (
            "An importer needs to know when cargo clears the collection point. A factory needs an unloading slot it can staff. "
            "A distributor needs a signed note its accounts team can use. We plan each booking around the people who depend on it."
        ),
        "blocks_title": "Who we plan for",
        "blocks": INDUSTRIES,
        "cta": CTA_QUOTE,
    },
    "operations": {
        "num": "05", "label": "Operations", "title": "Operations",
        "image": "img/truck-orange.webp", "sketch": "img/truck-orange-sketch.webp",
        "intro": (
            "Our core route connects collection points in Mombasa with Nairobi. We also arrange onward movements to Nakuru, "
            "Eldoret, Kisumu and Kitui, subject to customer request."
        ),
        "route": True,
        "blocks_title": "How a movement runs",
        "blocks": [
            ("Capacity on repeat routes", "As bookings support expansion, owned trucks will serve repeat movements alongside "
                                          "contracted vehicles."),
            ("Before dispatch", "We confirm the collection point, cargo details and receiving contact. We agree a delivery "
                                "window with the receiving team before the truck leaves. A site with restricted access or an "
                                "early closing time is planned into the booking."),
            ("On the road", "Your shipment contact follows up with the carrier. If a delay puts the agreed slot at risk, we "
                            "alert the nominated contacts, check the next receiving window and confirm the revised plan."),
            ("At handover", "The designated receiver checks the delivery and signs the agreed document. We confirm receipt "
                            "or flag any discrepancy, then follow up on the signed record."),
        ],
        "cta": CTA_QUOTE,
    },
    "cargodesk": {
        "num": "06", "label": "Ternion CargoDesk", "title": "Ternion CargoDesk",
        "image": "img/container-hook.webp", "sketch": "img/container-hook-sketch.webp",
        "intro": (
            "CargoDesk is our developing paid service for importers, clearing agents, wholesalers and distributors who want "
            "Ternion to take on more of the work around a delivery. A freight booking already includes the Three Calls and "
            "delivery confirmation. CargoDesk adds coordination across the businesses involved."
        ),
        "badge": "In development",
        "blocks_title": "What CargoDesk adds",
        "blocks": [
            ("From CFS release to the receiving door", "For an import collected at a Mombasa container freight station, "
             "CargoDesk brings the release contact, contracted carrier and receiving warehouse into one collection and "
             "delivery plan. When release slips, the coordinator follows up on the next receiving slot."),
            ("Recurring loads and multiple sites", "For distributors and clearing agents managing repeated movements, the "
             "proposed service keeps branch instructions, booking references and receiving contacts together. The "
             "coordinator follows up on exceptions and brings outstanding delivery records back to the account contact."),
            ("How the service is priced", "Managed-shipment work is quoted by assignment. Recurring customers can also agree "
             "a monthly account-management fee. Each quotation sets out the account work, any per-shipment charges and the "
             "freight price. Scope and availability are confirmed before booking."),
        ],
        "cta": ("contact", "Enquire about CargoDesk"),
    },
    "privacy": {
        "num": "08", "label": "Privacy notice", "title": "Privacy notice",
        "subtitle": "Your enquiry and shipment records.",
        "intro": (
            "Ternion Ventures Limited uses the details supplied with an enquiry to assess the movement, prepare a quotation "
            "and respond. For a confirmed booking, contact and delivery details also support collection, updates and handover."
        ),
        "blocks_title": "How we handle your details",
        "blocks": [
            ("Information we use", "This may include your name, company, phone, email, route, cargo description, timing and "
             "the receiving contact you nominate. Provide only the details needed to quote or carry out the movement."),
            ("Forms, calls and WhatsApp", "The website form uses FormSubmit to forward enquiries to Ternion's inbox. The "
             "provider may apply spam checks and describes a temporary 30-day submission archive. Email, telephone and "
             "WhatsApp communications also pass through the provider you choose."),
            ("Delivery notes and access", "Where photo proof is agreed, the signed note is shared with the contact nominated "
             "for that shipment. Please use an authorised number and tell us if the recipient changes before delivery."),
            ("Retention and enquiries", "We keep correspondence and shipment records as needed for the enquiry, the booking, "
             "business records and applicable obligations. This website version has no advertising trackers or analytics "
             "scripts. Hosting may generate technical logs. For access, correction or deletion requests, email "
             "alfrednzinga@gmail.com."),
        ],
        "legal": True,
    },
    "terms": {
        "num": "09", "label": "Terms of use", "title": "Terms of use",
        "subtitle": "Freight quotations and booking terms.",
        "intro": (
            "This website describes the freight services of Ternion Ventures Limited. Each shipment is governed by its agreed "
            "quotation and booking terms."
        ),
        "blocks_title": "Booking terms",
        "blocks": [
            ("Quote validity", "A firm quotation identifies the route, cargo, agreed work, price and expiry time. Booking "
             "requires agreement on the price, scope and timing. A change in load, route or handling requirements may "
             "require a revised quotation."),
            ("Collection and delivery windows", "Vehicle availability, release arrangements and receiving slots are confirmed "
             "per shipment. Arrival windows are estimates. Customers should disclose material access, handling and timing "
             "restrictions before booking."),
            ("Updates and proof of delivery", "The booking identifies the customer contact, agreed communication channels and "
             "required handover record. A photo of the signed note is sent by WhatsApp where agreed. Original-document "
             "arrangements are confirmed separately."),
            ("CargoDesk and website materials", "CargoDesk is in development. Confirm the available scope when enquiring. "
             "Website illustrations depict freight operations and do not identify company-owned vehicles. Enquiries may be "
             "directed to alfrednzinga@gmail.com."),
        ],
        "legal": True,
    },
}

CONTACT = {
    "num": "07", "label": "Contact",
    "title": "Request a freight quote.",
    "intro": (
        "Send the collection point, destination, cargo type, approximate weight and preferred movement date. If the goods "
        "are awaiting release, include the expected release time. If your store closes at a set hour, include that too."
    ),
}

ROUTE = {
    "core": ("Mombasa", "Nairobi"),
    "onward": ["Nakuru", "Eldoret", "Kisumu", "Kitui"],
}


# "Why us": every point is drawn from the approved copy above.
# icon = SVG path data in a 48x48 box, drawn as white line art.
WHY_US = [
    ("The Three Calls",
     "Loaded, plans changed, delivered. We call at the three moments that matter, before you have to ask.",
     "M14 8h6l3 8-4 3a22 22 0 0 0 10 10l3-4 8 3v6a3 3 0 0 1-3 3C21 37 11 27 11 11a3 3 0 0 1 3-3z M30 6a12 12 0 0 1 12 12 M30 12a6 6 0 0 1 6 6"),
    ("One accountable contact",
     "One named Ternion contact follows your load from collection to signed handover.",
     "M22 22a7 7 0 1 0 0-14 7 7 0 0 0 0 14z M8 40c0-8 6-13 14-13 4 0 7 1 9 3 M30 36l4 4 8-8"),
    ("The right truck",
     "Matched to cargo weight, dimensions, loading method and access at destination.",
     "M4 12h24v20H4z M28 19h8l7 7v6H28z M12 38a4 4 0 1 0 0.01 0 M35 38a4 4 0 1 0 0.01 0"),
    ("Clear, firm quotes",
     "Each quote states the route, agreed work, price and expiry. Any change is priced for your approval first.",
     "M12 4h18l8 8v32H12z M30 4v8h8 M18 22h14 M18 28h14 M18 34h8"),
    ("Planned delivery windows",
     "We agree the receiving slot before dispatch and plan around restricted access or early closing times.",
     "M24 42a18 18 0 1 0 0-36 18 18 0 0 0 0 36z M24 13v11l7 5"),
    ("Signed proof of delivery",
     "We follow up on the signed note and, where agreed, send a photo to your nominated WhatsApp contact.",
     "M16 8h-4v34h24V8h-4 M16 5h16v7H16z M17 25l5 5 9-10 M17 37c3-3 5 1 8-1s4-2 6 0"),
]
