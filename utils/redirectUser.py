from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.conf import settings

def redirect_after_login(request, nxt_url):
    # nxt = request.GET.get("next", None)
    if nxt_url is None:
        print("+++++++++++++ 1st")
        # go to my_account page
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not is_safe_url(
            url=nxt_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        # go to my_account page
        print("+++++++++++++ 2nd")
        print("=========================" + settings.LOGIN_REDIRECT_URL)
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        # go to  nxt_url
        print("+++++++++++++ 3rd")
        return redirect(nxt_url)