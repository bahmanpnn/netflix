from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .forms import ProfileForm
from .models import Profile, User, Movie


class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('profile-list'))
            # profile-list is name of profiles url that connected profilelist view
        return render(request, 'index.html')


# login required is for someone that is just login in site and others cant access this url
@method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        profiles = request.user.profiles.all()
        return render(request, 'profileList.html', {
            'profiles': profiles
        })


@method_decorator(login_required, name='dispatch')
class CreateProfile(View):
    def get(self, request):
        form = ProfileForm()
        context = {
            'form': form
        }
        return render(request, 'profileCreate.html', context)

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            # profile = Profile.objects.create(**form.cleaned_data)
            # if profile:
            #     request.user.profiles.add(profile)
            #     return redirect(reverse('profile-list'))
            profile_name = form.cleaned_data.get('name')
            user = request.user.id
            check_profile = User.objects.filter(id=user, profiles__name=profile_name).first()
            if check_profile is None:
                new_profile = Profile.objects.create(**form.cleaned_data)
                request.user.profiles.add(new_profile)
                return redirect(reverse('profile-list'))
            else:
                pass
                # todo:add e alert to show this profile exists and try another name!!
                # return JsonResponse({
                #     'status': 'profile-exists'
                # })

        context = {
            'form': form
        }
        return render(request, 'profileCreate.html', context)


@method_decorator(login_required, name='dispatch')
class MovieList(View):
    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit=profile.age_limit)
            if profile not in request.user.profiles.all():
                return redirect(reverse('profile-list'))
            context = {
                'movies': movies
            }
            return render(request, 'movieList.html', context)
        except Profile.DoesNotExist:
            return redirect(reverse('profile-list'))
