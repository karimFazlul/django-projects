from accounts.models import UserProfile
from accounts.forms import UserProfileForm

def retrieve(request):
    ''' note that this requires an authenticated
    user before we try calling it '''
    try:
        # user.name_of_the_model all in lower case
        #  user.userprofile
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    return profile
def set(request):
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()