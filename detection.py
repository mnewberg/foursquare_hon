import re
from django.http import HttpRequest

RE_MOBILE = re.compile(r"(iphone|ipod|blackberry|android|palm|IEMobile|windows\s+ce)", re.I)
RE_DESKTOP = re.compile(r"(windows|linux|os\s+[x9]|solaris|bsd)", re.I)
RE_BOT = re.compile(r"(spider|crawl|slurp|bot)", re.I)

def is_desktop(user_agent):
  """
  Anything that looks like a phone isn't a desktop.
  Anything that looks like a desktop probably is.
  Anything that looks like a bot should default to desktop.
  
  """
  return not bool(RE_MOBILE.search(user_agent)) and \
    bool(RE_DESKTOP.search(user_agent)) or \
    bool(RE_BOT.search(user_agent))


def get_user_agent(request):
  # Some mobile browsers put the User-Agent in a HTTP-X header
  return request.META.get('HTTP_X_OPERAMINI_PHONE_UA') or \
         request.META.get('HTTP_X_SKYFIRE_PHONE') or \
         request.META.get('HTTP_USER_AGENT', '')

