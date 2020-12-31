from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import RegisterForm
from .models import CourseOverview,ProfileSection
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

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

#Models
from .models import ProfileSection,CourseSection,BankDetail,CourseOverview,Schedule

def index(request): # HOME PAGE
    return render(request,'faculty/index.html')

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
        return redirect('/faculty')
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
                message = render_to_string('registration/activate.html',
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
                return render(request,'registration/register.html')

            return render(request,'faculty/index.html')
        else:
            form = RegisterForm()
        # form = RegisterForm()
        return render(request,'registration/register.html',{'form':form})

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
            group = Group.objects.get(name='Faculty') 
            user.groups.add(group)
            messages.success(request, 'Your Account is successfully registered. You can now login.')
            return redirect('/faculty')
        return render(request,'registration/activation_failed.html',status=401)


# def login_request(request):
#     if request.user.is_authenticated:
#         return redirect('/faculty')
#     else:
#         if request.method == "POST":
#             form = AuthenticationForm(request, request.POST)
#             registered = False
#             if form.is_valid():
#                 username = form.cleaned_data.get("username")
#                 password = form.cleaned_data.get("password")
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     regsitered = True
#                     messages.info(request, f"You are now logged in as {username}")
#                     return redirect("/faculty")
#                 else:
#                     messages.error(request, "Invalid username or password")
#             else:
#                 messages.error(request, "Invalid username or password")
#         form = AuthenticationForm()
#         return render(request, "registration/loginform.html",{"form": form})

def login_request(request):
    if request.user.is_authenticated:
        return redirect('/faculty')
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
                        return redirect("/faculty")
                    messages.error(
                        request, 'Account is not active,please check your email')
                    return render(request, 'registration/loginform.html')
                messages.error(
                    request, 'Invalid credentials,try again')
                return render(request, 'registration/loginform.html')

            messages.error(
                request, 'Please fill all fields')
        return render(request, 'registration/loginform.html')

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/faculty")
# AUTHENTICATION ENDS

# Profile Section STARTS
@login_required(login_url='/faculty/login/')
#@permission_required('faculty.add_bankdetail',login_url='/faculty/login/')
def profile_section(request):
    current_user = request.user.username
    print(current_user)
    profile_data = ProfileSection.objects.filter(username=current_user)
    return render(request,'faculty/profile_section.html',{'profile_data':profile_data})

def profile_section_submit(request):
    if request.method == 'POST':
        print(request.POST['q5_email'])
        print(request.POST['q4_name[first]'])
        print(request.POST['q4_name[last]'])
        print(request.POST['q8_gender'])
        print(request.POST['q19_tellUs'])
        username = request.POST['q16_username']
        fname = request.POST['q4_name[first]']
        lname = request.POST['q4_name[last]']
        email = request.POST['q5_email']
        phoneno = request.POST['q6_phoneNumber[full]']
        gender = request.POST['q8_gender']
        place = request.POST['q9_yourPlace']
        profession = request.POST['q10_profession']
        years = request.POST['q11_yearsOf']
        hobbies = request.POST['q12_whatAre']
        areaofinterest = request.POST['q13_whatAre13']
        socialprof = request.POST['q14_enterYour']
        yourself = request.POST['q19_tellUs']
        keylearn = request.POST['q17_keyLearning']
        Profile_Section = ProfileSection(  
            user = request.user,
            username = username, 
            fname=fname,
            lname=lname,
            email=email,
            phoneno=phoneno,
            gender=gender,
            place=place,
            profession=profession,
            years=years,
            hobbies=hobbies,
            areaofinterest=areaofinterest,
            socialprof=socialprof,
            yourself=yourself,
            keylearn=keylearn,
        )
        Profile_Section.save()

        messages.success(request, 'Profile Section successfully saved.')
        return profile_section(request)
        
    return render(request,'faculty/profile_section.html')
# Profile Section ENDS

#Course Section STARTS
@login_required(login_url='/faculty/login/')
#@permission_required('faculty.add_bankdetail',login_url='/faculty/login/')
def course_new(request):
    return render(request,'faculty/course_new.html')

def course_section(request):
    current_user = request.user.username
    print(current_user)
    course_data = CourseSection.objects.filter(username=current_user)
    return render(request,'faculty/course_section.html',{'course_data':course_data})

def course_section_submit(request):
    if request.method == 'POST':
        print(request.POST['q3_name[first]'])
        print(request.POST['q3_name[last]'])
        username = request.POST['q30_username']
        fname = request.POST['q3_name[first]']
        lname = request.POST['q3_name[last]']
        email = request.POST['q4_email']
        course_category = request.POST.get('q8_category')
        course_name = request.POST['q22_sessionOr']
        batch_count = request.POST['q23_whatCould']
        course_details = request.POST['q25_sessionOr25']
        duration = request.POST['q9_sessionOr9']
        medium = request.POST['q11_mediumOf']
        days = request.POST['q12_daysWhen']
        key_learnings = request.POST['q14_keyLearning14']
        age_group = request.POST['q27_ageGroup']
        prerequisites = request.POST['q28_prerequisites']
        things = request.POST['q29_thingsTo']

        Course_Section = CourseSection(
            user = request.user,
            username = username,
            fname = fname,
            lname = lname,
            email = email,
            course_category=course_category,
            course_name = course_name,
            batch_count = batch_count,
            course_details = course_details,
            duration = duration,
            medium = medium,
            days = days,
            key_learnings=key_learnings,
            age_group=age_group,
            prerequisites=prerequisites,
            things = things,
        )
        Course_Section.save()

        messages.success(request, 'Course Section successfully saved.')
        return course_section(request)

    return render(request, 'faculty/course_section.html')
#Course Section ENDS

#BANK Details STARTS
@login_required(login_url='/faculty/login/')
#@permission_required('faculty.add_bankdetail',login_url='/faculty/login/')
def bank_details(request):
    current_user = request.user.username
    print(current_user)
    bank_details = BankDetail.objects.filter(username=current_user)
    return render(request,'faculty/bank_details.html',{'bank_details':bank_details})

def bank_details_submit(request):
    if request.method == 'POST':
        print(request.POST['q5_accountNo'])
        username = request.POST['q16_username']
        accountNo = request.POST['q5_accountNo']
        accountType = request.POST['q6_accountType']
        ifsc = request.POST['q8_ifscCode']
        bankName = request.POST['q9_bankName']
        branch = request.POST['q10_branch']
        Bank_Detail = BankDetail(
            user = request.user,
            username = username,
            accountNo = accountNo,
            accountType = accountType,
            ifsc = ifsc,
            bankName = bankName,
            branch = branch,
        )
        Bank_Detail.save()

        messages.success(request, 'Bank Details successfully saved.')
        return bank_details(request)
        
    return render(request, 'faculty/bank_section.html')
    
#BANK Details ENDS

#Course Overview STARTS
@login_required(login_url='/faculty/login/')
#@permission_required('faculty.add_bankdetail',login_url='/faculty/login/')
def course_overview(request):
    try:
        current_user = request.user.username
        field_name = 'duration'
        obj = CourseOverview.objects.filter(username=current_user).last()
        field_value = getattr(obj, field_name)
    except:
        field_value = CourseOverview._meta.get_field('duration').get_default()
    return render(request, 'faculty/course_overview.html',{'field_value':field_value})

def course_overview_submit(request):
    try:
        current_user = request.user.username
        field_name = 'duration'
        obj = CourseOverview.objects.filter(username=current_user).last()
        field_value = getattr(obj, field_name)
    except:
        field_value = CourseOverview._meta.get_field('duration').get_default()
    if request.method == 'POST':
        print(request.POST['q3_courseName'])
        username = request.POST['q16_username']
        courseName = request.POST['q3_courseName']
        courseSubtitle = request.POST['q4_courseSubtitle']
        duration = request.POST['q18_input18[shorttext-1]']
        age = request.POST['q5_ageGroup']
        batch = request.POST['q6_batchSize']
        mediumOfInstruct = request.POST['q7_mediumOf']
        level = request.POST['q9_level']
        courseReq = request.POST['q10_courseRequirements']
        topics = request.POST['q12_topicsCovered']
        payment = request.POST['q19_input19[number-1]']
        Course_Overview = CourseOverview(
            user = request.user,
            username = username,
            courseName = courseName,
            courseSubtitle = courseSubtitle,
            duration = field_value-int(duration),
            age = age,
            batch = batch,
            mediumOfInstruct = mediumOfInstruct,
            level = level,
            courseReq = courseReq,
            topics = topics,
            payment = payment
        )
        Course_Overview.save()
        messages.success(request, 'Course Overview Details successfully saved.')
        return course_overview(request)
    return render(request, 'faculty/course_overview.html')
#Course Overview ENDS

def schedule(request):
    return render(request,'faculty/schedule.html')


def feedback(request):
    return render(request,'faculty/feedback.html')

@login_required(login_url='/faculty/login/')
#@permission_required('faculty.add_bankdetail',login_url='/faculty/login/')
def dashboard(request):
    current_user = request.user.username
    print(current_user)
    course_data = CourseSection.objects.filter(username=current_user)
    print(course_data)
    schedule_data = Schedule.objects.filter(username=current_user)
    print(schedule_data)
    counter = 0
    return render(request,'faculty/dashboard.html',{'course_data':course_data,'schedule_data':schedule_data,'counter':counter})


#Schedule Section Starts
def schedule_submit(request):
    if request.method == 'POST':
        print(request.POST.get('dates'))
        print(request.POST['q16_username'])
        username = request.POST['q16_username']
        dates = request.POST.get('dates')
        my_list = dates.split(",")
        print(my_list)
        for i in my_list:
            print(i)
            schedule = Schedule(user = request.user,username = username,dates = i)
            schedule.save()
        # schedule = Schedule(
        #     username = username,
        #     dates = dates,
        # )
        # schedule.save()

        messages.success(request, 'Schedule successfully saved.')
    return render(request, 'faculty/schedule.html')