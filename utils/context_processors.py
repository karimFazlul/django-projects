from catalog.models import Category
from ecomstore import settings


# these are like global variables that we can access from any where 
# of our project just by referencing the  specified key name 
def ecomstore(request):
	return {

		'site_name': settings.SITE_NAME,
		'meta_keywords': settings.META_KEYWORDS,
		'meta_description': settings.META_DESCRIPTION,
		'paypal_client_id': str(settings.PAYPAL_CLIENT_ID),
	}


