from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import DetailView,ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#Email Authentication STARTS
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import View
#Email Authentication ENDS

#Model Imports
from faculty.models import CourseSection
from .models import Competition
from .forms import CompetitionForm

# Create your views here.
def index(request):
    return render(request,'student/home.html')

# AUTHENTICATION STARTS
def check_user(request):
    if request.method == 'GET':
        username = request.GET['username']
        print(username)
        check = User.objects.filter(username=username)
        print(check,len(check))
        if len(check) == 1:
            return HttpResponse('UsernameExists')
        else:
            return HttpResponse('Not Exists')

def check_email(request):
    if request.method == 'GET':
        email = request.GET['email']
        print(email)
        check = User.objects.filter(email=email)
        print(check,len(check))
        if len(check) == 1:
            return HttpResponse('EmailExists')
        else:
            return HttpResponse('Email does not Exists')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/student')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                print(email)
                user = form.save()
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                email_subject = 'Activate your account'
                message = render_to_string('studentRegistration/activate.html',
                {
                    'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                }
                )

                email_message = EmailMessage(
                        email_subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                    )
                email_message.send()
                # messages.error(request, 'Please check the password validators')
                
                messages.success(request, f'Please check your inbox to activate your account.')
            else:
                for msg in form.error_messages:
                    messages.error(request, 'Please check all the password validations.')
                return render(request,'studentRegistration/register.html')

            return render(request,'student/home.html')
        else:
            form = RegisterForm()
        # form = RegisterForm()
        return render(request,'studentRegistration/register.html',{'form':form})

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            group = Group.objects.get(name='Student') 
            user.groups.add(group)
            messages.success(request, 'Your Account is successfully registered. You can now login.')
            return redirect('/student')
        return render(request,'studentRegistration/activation_failed.html',status=401)


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/student')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user = authenticate(username=username, password=password)

                if user:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'Welcome, ' +
                                        user.username+' you are now logged in')
                        return redirect("/student")
                    messages.error(
                        request, 'Account is not active,please check your email')
                    return render(request, 'studentRegistration/loginform.html')
                messages.error(
                    request, 'Invalid credentials,try again')
                return render(request, 'studentRegistration/loginform.html')

            messages.error(
                request, 'Please fill all fields')
        return render(request, 'studentRegistration/loginform.html')

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/student")
# AUTHENTICATION ENDS

def dashboard(request):
    return render(request,'student/dashboard.html')

def mycourses(request):
    courses = CourseSection.objects.all()
    return render(request,'student/mycourses.html',{'courses':courses})

class CourseDetailView(DetailView):
    model = CourseSection
    template_name = "student/courseDetails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = CourseSection.objects.all()
        return context

# def courseDetails(request):
#     return render(request,'student/courseDetails.html')

def showcase(request):
    return render(request,'student/showcase.html')

def courses(request):
    courses = CourseSection.objects.all()

    page_number = request.GET.get('page')
    paginator = Paginator(courses, 3) # Show 3 courses per page.
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'student/courses.html',{'courses':courses,'page_obj': page_obj})

class CategoryView(ListView):
    model = CourseSection
    template_name = "student/course_category.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = CourseSection.objects.filter(course_category=self.kwargs['category'])
        
        page_number = self.request.GET.get('page')
        paginator = Paginator(category, 10)
        try:
            page_object = paginator.page(page_number)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context["category"] = page_object
        return context

def competitions(request):
    data = Competition.objects.all()
    return render(request,'student/competitions.html',{'data':data})

class CompetitionDetailView(DetailView):
    model = Competition
    template_name = "student/competitionDetails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompetitionForm()
        return context