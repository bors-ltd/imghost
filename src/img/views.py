from django.conf import settings

from annoying.decorators import render_to


@render_to("legal_mentions.html")
def legal_mentions(request):

    return {"legal_mentions": settings.LEGAL_MENTIONS}
