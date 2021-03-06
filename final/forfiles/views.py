from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from forms import UserDetailsForm
from models import UserDetails
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.generic import FormView,DetailView,ListView
from .forms import ProfileImageForm
from .models import ProfileImage



def main(request):
    return render_to_response('main.html')
# def registrationpage(request):
#     return render_to_response('registration.html')
def login(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('login.html',args)
def auth_view(request):
    print "came"
    username = request.GET.get('username','')
    password = request.GET.get('password','')
    try:
        user = UserDetails.objects.get(username = username)
        print user
        print username
    except UserDetails.DoesNotExist:
        html = "<html><body>userdetails does not exist</body></html>"
        return HttpResponse(html)
    if user is not None:
        if user.password == password:
            request.session['username'] = user.username
            return HttpResponseRedirect('/forfiles/profile/')
        else:
            html = "<html><body>Password incorrect</body></html>"
            return HttpResponse(html)
    else:
        html = "<html><body>username incorrect</body></html>"
        return HttpResponse(html)
def registration(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('registration.html',args)
def signup(request):
    form = UserDetailsForm()
    if request.POST:
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/forfiles/main/')
        else:
            temp = "<html><boby>Email-id or the mobile number already exists</body></html>"
            return HttpResponse(temp)
    return render_to_response('registration.html',{'form':form}, context_instance=RequestContext(request))
def profile(request):
    return render_to_response('profile.html')
def upload_file(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('profile_image.html',args)
class ProfileImageView(FormView):
    template_name = 'profile_image.html'
    form_class = ProfileImageForm
    print form_class
    def form_valid(self, form):
        print "form_class"
        profile_image = ProfileImage(
            image=self.get_form_kwargs().get('files')['image'])
            # keyword=self.get_form_kwargs().get('files')['keyword'])   
        profile_image.keyword = form.cleaned_data['keyword']
        profile_image.domain = form.cleaned_data['domain']
        profile_image.username = form.cleaned_data['username']
        profile_image.save()
        self.id = profile_image.id
        print self.get_form_kwargs()

        # return HttpResponseRedirect(self.get_success_url())
        return render_to_response('profile.html')

    def get_success_url(self):
        # print kwargs={'pk':self.id}
        # return reverse('profile', kwargs={'pk': self.id})
        return render_to_response('profile.html')

class ProfileDetailView(DetailView):
    model = ProfileImage
    template_name = 'profile_image.html'
    context_object_name = 'image'


class ProfileImageIndexView(ListView):
    model = ProfileImage
    template_name = 'profile_image.html'
    context_object_name = 'images'
    queryset = ProfileImage.objects.all()

def search(request):
    pgmName = request.GET.get('search','')
    return render_to_response('searchResults.html',
        {'results':ProfileImage.objects.filter(keyword=pgmName)}
        )
def loadProgram(request,pgmid):
        pgm =ProfileImage.objects.get(id=pgmid)
        filepath = str(pgm.image)
        filepath = filepath[2:]
        filepath='media\\'+filepath
        f = open(filepath,'r')
        data = f.readlines()
        return render_to_response('loadProgram.html',{'data':data})
