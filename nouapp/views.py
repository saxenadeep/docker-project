from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from .models import registration, login, tbl_contact, tbl_Usm, upload_lecture, Upload_Assignment, Feedback, Complaints, tbl_noti
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .import smssender
from django.core.mail import send_mail
# Create your views here.

def index(request):
    return render(request,'home.html')


def Registration(request):
    return render(request, 'registration.html')


def regsave(request):
    rollno=request.POST['rollno']
    name=request.POST['name']
    fname=request.POST['fname']
    mname=request.POST['mname']
    gender=request.POST['gender']
    program=request.POST['program']
    branch=request.POST['branch']
    address=request.POST['address']
    year=request.POST['year']
    contactno=request.POST['contactno']
    email=request.POST['email']
    password=request.POST['password']
    regdate=timezone.now()
    usertype='student'
    status='pending'
    ab=registration(rollno=rollno,name=name,fname=fname,mname=mname,gender=gender,program=program,branch=branch,address=address,year=year,contactno=contactno,email=email,password=password,regdate=regdate)
    bc=login(userid=email,password=password,usertype=usertype,status=status)
    ab.save()
    bc.save()
    subject = 'Registration Confirmation'
    message = f'''
    Welcome to Nou Egyan!
    We’re excited to have you as a part of our community. 
    Below, you’ll find your login details for accessing the Nou Egyan portal.

    Your Userid And Password is:
    Userid: {email}
    Password: {password}

    Please keep this information secure and do not share it with anyone.
    '''
    from_email = 'rashmivartika5@gmail.com'
    recipient_list = [email]

        # Send email
    send_mail(subject, message, from_email, recipient_list)

        # Add success message and redirect
    messages.success(request, 'Registration successful! Please check your email for confirmation.')
    return render(request, 'registration.html') # Replace with your success URL
      #  return redirect('registartion')
    return redirect('registration')


def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        gender=request.POST['gender']
        address=request.POST['address']
        contactno=request.POST['contactno']
        email=request.POST['email']
        enquirytext=request.POST['enquirytext']
        enqdate=timezone.now()
        cs=tbl_contact(name=name,gender=gender,address=address,contactno=contactno,email=email,enquirytext=enquirytext,enqdate=enqdate)
        cs.save()
        smssender.sendsms(contactno)
        return redirect('contact')
    return render(request, 'contact.html')


def Login(request):
    return render(request, 'login.html')

def logcode(request):
    if request.method=='POST':
        userid=request.POST['userid']
        password=request.POST['password']
        usertype=request.POST['usertype']
        # .all(), .get(), .filter()
        # special data ko fetch krana filter se krenge
        # get() keval ek hi data uthata hai
        # first() ka matlab ek row 
        user=login.objects.filter(userid=userid,password=password).first()         
        if user:
            # iska matlab user ke andar data aa gya
            if user.usertype=='student' and usertype=='student':
                request.session['userid']=userid
                return redirect('studenthome')
            
            elif user.usertype=='admin' and usertype=='admin':
                return redirect('adminhome')
            else:
                return render(request,'login.html')
            
        else:
            return render(request,'login.html')
        



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def studentzone(request):
    if 'userid' in request.session:
        return render(request,'studentzone.html')
    
    else:
        return render(request,'login.html')


def logout(request):
    request.session.flush()
    return redirect('login')



def studenthome(request):
    ab=tbl_noti.objects.all()
    return render(request,'studenthome.html',{'ab':ab})


def updateprofile(request):
    user_email=request.session.get('userid')
    user=registration.objects.filter(email=user_email).first()
    show={
        'show': user,
    }
    return render(request,'updateprofile.html', show)


def upprofile(request):
    user_email=request.session.get('userid')
    user=registration.objects.filter(email=user_email).first()
    # user ka data user variable me aa gya h
    show={
        'show': user,
    }

    if request.method=="POST":
        if user:
            user.rollno=request.POST['rollno']
            user.name=request.POST['name']
            user.fname=request.POST['fname']
            user.mname=request.POST['mname']
            user.gender=request.POST['gender']
            user.address=request.POST['address']
            user.contactno=request.POST['contactno']
            user.email=request.POST['email']
            user.password=request.POST['password']
            if 'profile_pic' in request.FILES:
                user.profile_pic=request.FILES['profile_pic']
            user.save()
            return redirect('upprofile')
   
    return render(request,'upprofile.html', show)



def upsave(request):
    user_email=request.session.get('userid')
    user=registration.objects.filter(email=user_email).first()
    # user ka data user variable me aa gya h
    show={
        'show': user,
    }

    if request.method=="POST":
        if user:
            user.rollno=request.POST['rollno']
            user.name=request.POST['name']
            user.fname=request.POST['fname']
            user.mname=request.POST['mname']
            user.gender=request.POST['gender']
            user.address=request.POST['address']
            user.contactno=request.POST['contactno']
            user.email=request.POST['email']
            user.password=request.POST['password']
            if 'profile_pic' in request.FILES:
                user.profile_pic=request.FILES['profile_pic']
            user.save()

    return redirect('updateprofile')

def adminzone(request):
    return render(request, 'adminzone.html')

def adminhome(request):
    return render(request, 'adminhome.html')


def adminlogout(request):
    request.session.flush()
    return redirect('login')


def managestudent(request):
    ab=registration.objects.all()
    return render(request,'managestudent.html', {'show': ab})


def showenq(request):
    sh=tbl_contact.objects.all()
    show={
        'sh': sh
    }
    return render(request,'showenq.html', show)


def Usm(request):
    ab=tbl_Usm.objects.all()
    return render(request,'usm.html',{'ab':ab})



def usmsave(request):
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    new_file=request.FILES['new_file']
    av=tbl_Usm(program=program,branch=branch,year=year,subject=subject,new_file=new_file)
    av.save()
    messages.success(request,'Study Material Upload Successfully')
    return redirect('Usm')


def Upload_lecture(request):
    ab=upload_lecture.objects.all()
    return render(request, 'upload_lecture.html', {'ab':ab})


def lecturesave(request):
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    link=request.POST['link']
    df=upload_lecture(program=program,branch=branch,year=year,subject=subject,link=link)
    df.save()
    messages.success(request,'Lecture Upload Successfully')
    return render(request, 'upload_lecture.html')


def viewstudy(request):
    if 'userid' in request.session:
        branch=request.session.get('branch')
        user=tbl_Usm.objects.filter()
        # if branch:
        #     ab=tbl_Usm.objects.filter(branch=branch)
        #     return render(request, 'viewstudy.html', {'ab': ab})
        # else:
        #     messages.error(request,'Branch Information Is Missing')

        #     return render(request, 'viewstudy.html')
        ab=tbl_Usm.objects.all()
        return render(request, 'viewstudy.html',{'ab': ab})

    else:
        return redirect('login')
    


def showlecture(request):
    ab=upload_lecture.objects.all()
    return render(request, 'viewlecture.html',{'ab': ab})
        


def upass(request):
    ab=Upload_Assignment.objects.all()
    return render(request, 'uploadassignment.html',{'ab':ab})


def upasssave(request):
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    new_file=request.FILES['new_file']
    av=Upload_Assignment(program=program,branch=branch,year=year,subject=subject,new_file=new_file)
    av.save()
    messages.success(request,'Upload Assignment Successfully')
    return render(request, 'usm.html')


def viewassignment(request):
    ab=Upload_Assignment.objects.all()
    return render(request, 'viewassignment.html', {'ab': ab})


def feedback(request):
    ab=Feedback.objects.all()
    return render(request, 'feedback.html',{'ab':ab})

def feedsave(request):
    if request.method=='POST':
        subject=request.POST.get('subject')
        feedback=request.POST.get('feed')
        user_email=request.session.get('userid')
        user=registration.objects.filter(email=user_email).first()
    if user:
            Feedback.objects.create(
            name=user.name,
            program=user.program,
            branch=user.branch,
            year=user.year,
            subject=subject,
            feed=feedback,
            reqdate=timezone.now()
        )

            messages.success(request, 'Feedback Submitted Successfully')
    else:
        messages.success(request,'Not Found')



    return redirect('feedback')

def comp(request):
    ab=Complaints.objects.all()
    return render(request, 'comp.html',{'ab':ab})

def compsave(request):
    if request.method=='POST':
        subject=request.POST.get('subject')
        comp=request.POST.get('comp')
        user_email=request.session.get('userid')
        user=registration.objects.filter(email=user_email).first()
    if user:
            Complaints.objects.create(
            name=user.name,
            program=user.program,
            branch=user.branch,
            year=user.year,
            subject=subject,
            comp=comp,
            reqdate=timezone.now()
        )

            messages.success(request, 'Complaint Submitted Successfully')
    else:
        messages.success(request,'Not Found')
    return redirect('comp')


def deletefeed(request,id):
    ab=Feedback.objects.get(pk=id)
    ab.delete()
    return redirect('feedback')


def deletecomp(request,id):
    ab=Complaints.objects.get(pk=id)
    ab.delete()
    return redirect('comp')


def ViewComp(request):
    sh=Complaints.objects.all()
    return render(request,'viewcomp.html',{'sh':sh})


def ViewFeed(request):
    sh=Feedback.objects.all()
    return render(request,'viewfeed.html',{'sh':sh})




def deletestu(request):
    ab=registration.objects.get(pk=id)
    ab.delete()
    return render('managestudent')

def editstu(request,id):
    show=registration.objects.get(pk=id)
    return render(request,'editstu.html', {'show':show})

def stusave(request):
    # # user_email=request.session.get('userid')
    # # user=registration.objects.filter(email=user_email).first()
    # # # user ka data user variable me aa gya h
    # show={
    #     'show': user,
    # }

    rollno=request.POST['rollno']
    name=request.POST['name']
    fname=request.POST['fname']
    mname=request.POST['mname']
    gender=request.POST['gender']
    address=request.POST['address']
    contactno=request.POST['contactno']
    email=request.POST['email']
    password=request.POST['password']
    # email=registration.objects.get(pk=id)
    registration.objects.filter(rollno=rollno).update(rollno=rollno,name=name,fname=fname,mname=mname,gender=gender,address=address,contactno=contactno,email=email,password=password)
    return redirect('managestudent')


def deleteenq(request,id):
    ab=tbl_contact.objects.get(pk=id)
    ab.delete()
    return redirect('showenq')


def deleteusm(request,id):
    ab=tbl_Usm.objects.get(pk=id)
    ab.delete()
    return redirect('Usm')




def deletelec(request,id):
    ab=upload_lecture.objects.get(pk=id)
    ab.delete()
    return redirect('Upload_lecture')



def deleteass(request,id):
    ab=Upload_Assignment.objects.get(pk=id)
    ab.delete()
    return redirect('upass')



def deletecomp(request,id):
    ab=Complaints.objects.get(pk=id)
    ab.delete()
    return redirect('viewcomp')



def deletefeed(request,id):
    ab=Feedback.objects.get(pk=id)
    ab.delete()
    return redirect('viewfeed')


def addnoti(request):
    tb=tbl_noti.objects.all()
    if request.method=='POST':
        notif=request.POST['notif']
        notireg=timezone.now()
        ab=tbl_noti(notif=notif,notireg=notireg)
        ab.save()
        return redirect('addnoti')
    return render(request,'addnoti.html',{'tb':tb})


def services(request):
    return render(request,'services.html')


def editenq(request,id):
    show=tbl_contact.objects.get(pk=id)
    return render(request,'editenq.html', {'show':show})

def enqsave(request,id):
    # # user_email=request.session.get('userid')
    # # user=registration.objects.filter(email=user_email).first()
    # # # user ka data user variable me aa gya h
    # show={
    #     'show': user,
    # }

    # rollno=request.POST['rollno']
    
    
    name=request.POST['name']
    gender=request.POST['gender']
    address=request.POST['address']
    contactno=request.POST['contactno']
    email=request.POST['email']
    enquirytext=request.POST['enquirytext']
    enqdate=timezone.now()
    # email=registration.objects.get(pk=id)
    tbl_contact.objects.filter(id=id).update(name=name,gender=gender,address=address,contactno=contactno,email=email,enquirytext=enquirytext,enqdate=enqdate)
    return redirect('showenq')


def editass(request,id):
    show=Upload_Assignment.objects.get(pk=id)
    return render(request,'editass.html', {'show':show})

def asssave(request):
    # # user_email=request.session.get('userid')
    # # user=registration.objects.filter(email=user_email).first()
    # # # user ka data user variable me aa gya h
    # show={
    #     'show': user,
    # }

    # rollno=request.POST['rollno']
   
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    new_file=request.FILES.get('new_file')
    
    # email=registration.objects.get(pk=id)
    Upload_Assignment.objects.update(program=program,branch=branch,year=year,subject=subject,new_file=new_file)
    return redirect('upass')

def editfeed(request,id):
    show=Feedback.objects.get(pk=id)
    return render(request,'editfeed.html', {'show':show})

def efeedsave(request,id):
    # # user_email=request.session.get('userid')
    # # user=registration.objects.filter(email=user_email).first()
    # # # user ka data user variable me aa gya h
    # show={
    #     'show': user,
    # }

    # rollno=request.POST['rollno']
    
    
    name=request.POST['name']
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    feed=request.POST['feed']
    
    # email=registration.objects.get(pk=id)
    Feedback.objects.filter(id=id).update(name=name,program=program,branch=branch,year=year,subject=subject,feed=feed)
    return redirect('viewfeed')


def editcomp(request,id):
    show=Complaints.objects.get(pk=id)
    return render(request,'editcomp.html', {'show':show})

def ecompsave(request,id):
    # # user_email=request.session.get('userid')
    # # user=registration.objects.filter(email=user_email).first()
    # # # user ka data user variable me aa gya h
    # show={
    #     'show': user,
    # }

    # rollno=request.POST['rollno']
    
    
    name=request.POST['name']
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    comp=request.POST['comp']
    
    # email=registration.objects.get(pk=id)
    Complaints.objects.filter(id=id).update(name=name,program=program,branch=branch,year=year,subject=subject,comp=comp)
    return redirect('viewcomp')
