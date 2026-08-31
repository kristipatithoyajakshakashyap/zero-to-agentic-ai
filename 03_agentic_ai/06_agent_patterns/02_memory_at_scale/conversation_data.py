"""A long shared conversation, used by every notebook in this module.

Why a .py file instead of pasting it into each notebook: the conversation is
deliberately long (that is the whole point of the module), and repeating 40
turns at the top of five notebooks would bury the actual lesson. Import it and
get on with the work.

The conversation is a product-planning thread between a founder and an
assistant. Scattered through it are DURABLE facts - decisions and constraints
that must survive any amount of compression - mixed with EPHEMERAL chatter that
is safe to discard. Which is which is recorded below, so the notebooks can grade
their own summarisation instead of asking you to eyeball it.
"""

CONVERSATION = [
    ("user", "Hi - I'm starting a small SaaS for bike shops and I'd like help planning it."),
    ("assistant", "Happy to help. What does it need to do on day one?"),
    ("user", "Book service appointments and track repair jobs. Nothing else for v1."),
    ("assistant", "A tight scope. Booking plus a repair board covers a real workflow."),

    ("user", "Important constraint: it must run entirely inside the EU. Our customers are "
             "German bike shops and they will not accept US data hosting."),
    ("assistant", "Understood - EU-only hosting is a hard requirement, so that rules out "
                  "several managed services or forces their EU regions."),

    ("user", "What's the weather like for launching in autumn, business-wise?"),
    ("assistant", "Autumn is the quiet season for bike retail, which is actually good: "
                  "shops have time to adopt new tooling before spring."),

    ("user", "The product is called Spannerbox, by the way."),
    ("assistant", "Noted - Spannerbox it is."),

    ("user", "Do you think we need a mobile app?"),
    ("assistant", "Not for v1. A responsive web app covers the counter and the workshop."),

    ("user", "Our budget is 12,000 EUR for the first six months, all in."),
    ("assistant", "That is tight but workable if you stay on managed hosting and avoid hires."),

    ("user", "I keep going back and forth on pricing. Any instinct?"),
    ("assistant", "Per-shop flat monthly usually beats per-seat for small retail."),

    ("user", "Right. Let's say 49 EUR per shop per month, but I might revisit."),
    ("assistant", "Reasonable starting point. Easy to raise later, hard to lower."),

    ("user", "Random question - do you know any good bike routes near Freiburg?"),
    ("assistant", "The Dreisam valley path is lovely and mostly flat."),

    ("user", "Ha, thanks. Back to work. What stack would you pick?"),
    ("assistant", "Postgres, a boring server framework, and server-rendered pages."),

    ("user", "We've decided on Postgres and Django. That's locked in."),
    ("assistant", "Good - Django's admin alone will save you weeks on the repair board."),

    ("user", "How long do you think v1 takes?"),
    ("assistant", "Six to ten weeks for one developer working full time, at that scope."),

    ("user", "One more hard rule: no customer data may ever be sent to a third-party LLM. "
             "Our lawyer was extremely clear about that."),
    ("assistant", "Then any AI features must run on self-hosted models, or not at all."),

    ("user", "What about the design? I have no designer."),
    ("assistant", "Use an off-the-shelf component library and resist customising it."),

    ("user", "Do people still use fax? One shop asked."),
    ("assistant", "In German retail, occasionally yes - but do not build for it in v1."),

    ("user", "Our first pilot customer is Radhaus Krueger in Freiburg, starting in March."),
    ("assistant", "A named pilot with a date is the single most useful thing you have."),

    ("user", "Should we do a free tier?"),
    ("assistant", "For twenty-odd shops, a 30-day trial beats a free tier - less support load."),

    ("user", "Fine, 30-day trial. What should I do first this week?"),
    ("assistant", "Write the booking flow end to end, with no styling, and show it to Krueger."),

    ("user", "What's the best way to handle no-shows?"),
    ("assistant", "A deposit is the only thing that reliably works, but it hurts adoption."),

    ("user", "Let's skip deposits for now. Anything else I'm forgetting?"),
    ("assistant", "Backups and a way to export a shop's data. Both are trust features."),
]

# The facts that MUST survive compression. Each entry is
#   (short label, list of substrings that count as evidence of retention)
DURABLE_FACTS = [
    ("product name",     ["spannerbox"]),
    ("EU-only hosting",  ["eu", "europe", "german"]),
    ("budget 12,000 EUR", ["12,000", "12000", "12 000", "12k"]),
    ("price 49 EUR/shop", ["49"]),
    ("stack: Postgres + Django", ["django"]),
    ("no third-party LLM", ["llm", "third-party", "third party", "self-host"]),
    ("pilot: Radhaus Krueger, March", ["krueger", "kruger", "march"]),
    ("30-day trial, no free tier", ["30-day", "30 day", "trial"]),
]

# Turns that are safe to throw away entirely.
EPHEMERAL_MARKERS = ["weather", "bike routes", "dreisam", "fax", "no-shows", "deposit"]


def as_text(turns=None) -> str:
    """Render turns as the flat transcript a model actually receives."""
    turns = CONVERSATION if turns is None else turns
    return "\n".join("%s: %s" % (r.upper(), t) for r, t in turns)


# Questions whose correct answers depend on facts stated early in the thread.
# Used to grade whether a memory strategy actually preserved anything.
PROBE_QUESTIONS = [
    ("What is the product called?", ["spannerbox"]),
    ("Where must the product be hosted, and why?", ["eu", "europe"]),
    ("What is the monthly price per shop?", ["49"]),
    ("Which database and web framework were chosen?", ["django"]),
    ("Who is the first pilot customer and when do they start?", ["krueger", "kruger"]),
    ("Is it acceptable to send customer data to a hosted LLM API?", ["no", "not", "never"]),
]
