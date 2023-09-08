from ..parameters import *

def login_view(request):

    if request.method == "POST":

        try:
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
        except:
            #case of malicious client side editing
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            d={"message": "Invalid username and/or password."}
            return render(request,"ad_bus_stops/authentication/login.html",{**param(request, 'login'),**d})

    else:
        return render(request,"ad_bus_stops/authentication/login.html",param(request, 'login'))


def logout_view(request):

    # traverse parameters from one session to another through logout
    a = app_explorer_username(request)
    s = show_anonymous_message(request)

    logout(request)
    
    request.session['app_explorer_username'] = a 
    request.session['show_anonymous_message'] = s

    return HttpResponseRedirect(reverse("index"))


def register(request): 

    delete_not_confirmed_user()

    # 1. "Access denied" message rendering
    explorer_name = app_explorer_username(request)
    if explorer_name == 'anonymous_check':
        return HttpResponseRedirect(reverse('message', args = ('anonymous_check',)))

    # 2. Getting data
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"].strip()         
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
        except:
            #case of malicious client side editing
            print('Error in POST parameters in register view')
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        # 3. Username length checking
        if len(username)>10:
            d={"message": "Too long username."}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})

        # 4.Ensures that  password matches confirmation
        if password != confirmation:
            d={"message": "Passwords must match."}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})

        # 5. username availability checking
        if not username.strip():
            d={"message": "Username must not be empty."}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})

        # 6. email validation
        try:
            validate_email(email)
        except ValidationError:
            d={"message": "Email validation failed."}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})
        
        # 7. password validation
        if ENABLE_PASSWORD_VALIDATION:
            try:
                validate_password(password, user=None, password_validators=None)
            except ValidationError as e:
                #password_validation_failure_list = list(e)
                d={ "message": "Password validation failed",
                    'password_validation_failure_list': list(e)}            
                return render(request,"ad_bus_stops/authentication/register.html",{
                    **param(request, 'register'),**d})

        # 8. Attempt to create  a new user

        # gets explorer object
        try:
            explorer = App_Explorer.objects.get(username = explorer_name)
        except:
            # db connection faluire
            d={"message": "Try again"}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})

        try:
            user = User.objects.create_user(username, email, password, app_explorer = explorer )
            user.save()
        except IntegrityError:
            d={"message": "Username already taken."}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})
        except:
            #  db connection failure
            d={"message": "Try again"}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})

        # 9. Creates User_Registration_Timestamp model  instance
        # Such creation  launches  a timer for life-time of registration process
        try:
            registration_timestamp = User_Registration_Timestamp(user = user)
            registration_timestamp.save()
            timestamp_created = True
        except:
            #db connection faluire
            timestamp_created = False
            print('timestamp creation failed')
            pass

        # 10. Sends email to customer with authentication code
        try:
            user.code = str(random.randint(0,9999)).zfill(4)
            user.save()
        except:
            # db connection faluire
            pass
        
        try:
            send_mail(
                "from AD - BUS - STOPS ",
                f"Authentication code {user.code}",
                AGENCY_EMAIL,
                [f"{email}"],
                fail_silently=False, )
        except:
            print('confirmation code sending failure')
            if user.confirmation == 'not_confirmed':
                try:
                    user.delete()
                except:
                    # db connection faluire
                    pass

            d={"message": "Not valid email"}
            return render(request,"ad_bus_stops/authentication/register.html",{
                **param(request, 'register'),**d})

        # 11. Counting time_left  parameter for rendering
        if timestamp_created:
            time_left = int((registration_timestamp.datetime 
                            + REGISTRATION_EXPIRY
                            - timezone.now()).total_seconds())
        else:
            time_left = 0

        d={'user_id': user.id, 
            'time_left':time_left }

        return render(request,"ad_bus_stops/authentication/confirmation.html",{
            **param(request, 'register'),**d})
    else:
        return render(request,"ad_bus_stops/authentication/register.html",param(request,'register'))

def confirmation(request, user_id):

    if request.method == "POST":
        try:
            code = request.POST["code"]
        except:
            #case of malicious client side editing
            print('Error in POST parameters in confirmation view')
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        try:
            user = User.objects.get(pk = user_id)
        except:
            #case of malicious client side editing or registration time expired
            print('Error in user_id parameter in confirmation view  or registration time expired')
            return render(request,"ad_bus_stops/authentication/register.html",
                    param(request,'register'))

        #case of malicious client side editing and passing to POST another user_id
        if   user.confirmation == 'confirmed':
            print('Error in user_id parameter in confirmation view - user already confirmed')
            return render(request,"ad_bus_stops/authentication/register.html",
                    param(request,'register'))           
        
        # regular case
        else:
            if code == user.code:
                user.confirmation = 'confirmed'
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

            #  wrong confirmation code inserted  
            else:
                d={'user_id': user.id, 
                    'message':'Not correct code',
                    'time_left':int((user.timestamp.all()[0].datetime 
                                + REGISTRATION_EXPIRY 
                                - timezone.now()).total_seconds()) }
                return render(request,"ad_bus_stops/authentication/confirmation.html",{
                    **param(request, 'register'),**d})
    else:
        return HttpResponseRedirect(reverse('message', args = ('x', )))
