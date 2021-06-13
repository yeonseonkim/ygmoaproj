from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import Post
from django.http import HttpResponse
import pyotp
import shutil
import qrcode
import cv2
import pyzbar.pyzbar as pyzbar
import webbrowser


# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username,password=password)
        
        if user is not None:
            print("성공")
            login(request, user)
            
            response = render(request, 'main/login.html')
            response.set_cookie('username',username)
            response.set_cookie('password',password)

            #nowuser = request.COOKIES.get('username')
            #nowpoint = User.objects.get(username=nowuser)
            #nowuserpoint = nowpoint.userpoint

            return response

        else:
            print("실패")

        # nowuser = request.COOKIES.get('username')
        # nowpoint = User.objects.get(username=nowuser)
        # nowuserpoint = nowpoint.userpoint


    return render(request, "main/login.html")



def logout_view(request):
    # logout(request)
    # return redirect("login")
    #로그아웃할 때 otpdata 0으로 만들기

    response = render(request, 'main/logout.html')
    response.delete_cookie('username')
    response.delete_cookie('password')
    logout(request)
    return response


def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        korname = request.POST["korname"]
        username = request.POST["username"]
        password = request.POST["password"]
        phonenum = request.POST["phonenum"]
        auth = request.POST["auth"]
        email = request.POST["email"]

        user = User.objects.create_user(username,email,password)
        user.korname = korname
        user.phonenum = phonenum
        user.auth = auth
        user.save()
        return redirect("login")

    return render(request, "main/signup.html")

def first_intro(request):
    return render(request, 'main/first_intro.html')

def second_my(request):
    username = request.COOKIES.get('username')
    dbsee = User.objects.get(username=username)
    korname = dbsee.korname
    usenums = dbsee.usenums
    phonenum = dbsee.phonenum
    userpoint = dbsee.userpoint

    return render(request, 'main/second_my.html',{'username':username, 'korname':korname, 'usenums':usenums, 'phonenum':phonenum, 'userpoint': userpoint})

def third_pchange(request):
    username = request.COOKIES.get('username')
    dbsee = User.objects.get(username=username)
    userpoint = dbsee.userpoint

    if request.method == "POST":
        pointzero = User.objects.get(username=username)
        pointzero.userpoint = 0
        pointzero.save()


        # HttpResponse("지역화폐로 전환 성공!")

    return render(request, 'main/third_pchange.html',{'username':username, 'userpoint': userpoint})

def storelogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username,password=password)
        if user is not None:
            print("성공")
            login(request, user)
        else:
            print("실패")

    return render(request, "main/storelogin.html")

def blog(request):
    # 모든 Post를 가져와 postlist에 저장합니다
    postlist = Post.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옵니다 
    return render(request, 'main/blog.html', {'postlist':postlist})


def otpmake(request):
    totp = pyotp.TOTP('GAYDAMBQGAYDAMBQGAYDAMBQGA======', 10)  # 180초 간격, 즉 3분마다 변경됨
    # totp = pyotp.TOTP('base32secret3232', 10)
    otpvalue = totp.now()
    otpvalue = str(otpvalue)            #잘리는 것 같아서 str으로 변환함!!!!!!!!!!!!!!!
    
    user = request.COOKIES.get('username')
    update = User.objects.get(username=user)
    update.otpdata = otpvalue
    update.save()

    return render(request,'main/otpmake.html',{'otpvalue':otpvalue})

def otpcheck(request):
    if request.method == "POST":
        getotp = request.POST["getotp"]

        userotp = User.objects.values_list('otpdata', flat=True)

        # users = User.objects.all()
        # str = ''
        # for user in users:
        #     str += "<p>{}번<br>".format(user.otpdata)
        # return HttpResponse(str)



        for a in userotp:
            b=str(a)

            if b == getotp:
                pointplus = User.objects.get(otpdata=a)
                pointplus.userpoint += 3000
                pointplus.usenums +=1
                pointplus.save()

                return HttpResponse("포인트적립 성공")
            else:
                return HttpResponse("실패")
        
    return render(request, 'main/otpcheck.html')

def otpreader(request):
    #cap = cv2.imread(0)

    cap = cv2.VideoCapture(0)

    num = 0

    while True:
        success, frame = cap.read()

        if success:
            for code in pyzbar.decode(frame):
                my_code = code.data.decode('utf-8')
                print("인식 성공: ", my_code)
                
                #webbrowser.open(my_code)
                my_code = str(my_code)
                if my_code == "http://127.0.0.1:8000/otpcheck/":
                    num += 1
                    return render(request, 'main/otpcheck.html')
                else:
                    continue
                

                                     

            cv2.imshow('cam', frame)
            

            key = cv2.waitKey(1)

            if (num > 0):
                break

            if (key == 27):
                break          

    cap.release()
    #frame = str(frame)
    cv2.destroyAllWindows()

    return render(request, 'main/otpreader.html')

def userpage(request):
    username = request.COOKIES.get('username')
    dbsee2 = User.objects.get(username=username)
    auth = dbsee2.auth

    if (auth == 'store'):
        return render(request, 'main/alert.html')
    
    korname = dbsee2.korname
    usenums = dbsee2.usenums
    phonenum = dbsee2.phonenum
    userpoint = dbsee2.userpoint


    return render(request, 'main/userpage.html',{'auth':auth, 'username':username, 'korname':korname, 'usenums':usenums, 'userpoint':userpoint, 'phonenum': phonenum})

def storepass(request):
    username = request.COOKIES.get('username')
    dbsee3 = User.objects.get(username=username)
    auth = dbsee3.auth
    test = 0

    if (auth == 'user'):
        return render(request, 'main/alert.html')


    #-------------------------------------------
    if request.method == "POST":
        inputnum = request.POST["inputnum"]

        phonenumlist = User.objects.values_list('phonenum', flat=True)



        for a in phonenumlist:

            if a==inputnum:
                test += 1

                pointplus = User.objects.get(phonenum=a)
                pointplus.userpoint += 3000
                pointplus.usenums +=1
                pointplus.save()

                return render(request, 'main/sucplus.html')
    
        if test == 0:
            return render(request, 'main/failplus.html')

    

    return render(request, 'main/storepass.html')
