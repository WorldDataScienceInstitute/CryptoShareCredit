import requests
from django.http import HttpResponse, Http404
from common.utils import banned_countries

class IPFilterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # # DEVELOPMENT ENVIRONMENT ONLY
        # # DEVELOPMENT ENVIRONMENT ONLY
        # # DEVELOPMENT ENVIRONMENT ONLY

        # user_ip = request.META["HTTP_X_FORWARDED_FOR"]

        # url = f"https://api.ipregistry.co/{user_ip}?key=b8rzmx4u1idb24hw"
        # ipregistry_response = requests.get(url).json()

        # country_code = ipregistry_response["location"]["country"]["code"]


        # # DEVELOPMENT ENVIRONMENT ONLY
        # # DEVELOPMENT ENVIRONMENT ONLY
        # # DEVELOPMENT ENVIRONMENT ONLY
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------

        # PRODUCTION ENVIRONMENT ONLY
        # PRODUCTION ENVIRONMENT ONLY
        # PRODUCTION ENVIRONMENT ONLY
        # try:
        #     country_code = request.META["HTTP_X_SUCURI_COUNTRY"]
        # except KeyError:
        #     country_code = "US"

        # PRODUCTION ENVIRONMENT ONLY
        # PRODUCTION ENVIRONMENT ONLY
        # PRODUCTION ENVIRONMENT ONLY

        # if country_code in banned_countries:
        #     return HttpResponse(status=404)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response