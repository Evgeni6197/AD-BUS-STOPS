from ..parameters import *

def app_explorer(request):
    """
    Renders first informative page after introductory animation
    """

    d = {"lifetime": EXPLORER_ACCOUNT_EXPIRATION}

    return render(request,'ad_bus_stops/app_explorer.html',{**param(request, 'app_explorer'),**d})

def register_app_explorer(request):
    """
    Creates explorer account
    """
    # Exit from add_explorer account 
    request.session['app_explorer_username'] = 'anonymous_check'
    request.session['show_anonymous_message'] = True

    if request.method == "POST":
        try:
            username = request.POST["username"]        
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
        except:
            #case of malicious client side editing
            print('Error in POST parameters in register_app_explorer view')
            return HttpResponseRedirect(reverse('message', args = ('w_s',)))

        # username and password length checking
        if len(username)>10 or len(password)>20 :
            d={"message": "Too long username or password"}
            return render(request,"ad_bus_stops/authentication/register_app_explorer.html",
                    {**param(request, 'register_app_explorer'),**d})            

        # Ensure password matches confirmation
        if password != confirmation:
            d={"message": "Passwords must match."}
            return render(request,"ad_bus_stops/authentication/register_app_explorer.html",
                    {**param(request, 'register_app_explorer'),**d}) 

        # username availability checking
        if not username.strip():
            d={"message": "Username must not be empty."}
            return render(request,"ad_bus_stops/authentication/register_app_explorer.html",
                    {**param(request, 'register_app_explorer'),**d}) 
        
        # password validation
        if ENABLE_PASSWORD_VALIDATION:
            try:
                validate_password(password, user=None, password_validators=None)
            except ValidationError as e:
                #password_validation_failure_list = list(e)

                d={ "message": "Password validation failed",
                    'password_validation_failure_list': list(e)}
                return render(request,"ad_bus_stops/authentication/register_app_explorer.html",
                        {**param(request, 'register_app_explorer'),**d}) 
        
        # Attempt to create a new explorer
        try:
            app_explorer = App_Explorer.objects.create(
                username = username, 
                password = password,
                creation_date = date.today(),
                current_date = date.today(),                
                )
        except IntegrityError:
            d={"message": "Username already taken."}
            return render(request,"ad_bus_stops/authentication/register_app_explorer.html",
                    {**param(request, 'register_app_explorer'),**d}) 
        except :
            # db connection falure
            d={"message": "Try again"}
            return render(request,"ad_bus_stops/authentication/register_app_explorer.html",
                    {**param(request, 'register_app_explorer'),**d})         



        # app explorer account entrance
        request.session['app_explorer_username'] = username
        
        return HttpResponseRedirect(reverse('change_current_date'))

    else:
        return render(request,"ad_bus_stops/authentication/register_app_explorer.html",
                    param(request, 'register_app_explorer')) 

def enter_app_explorer(request):
    """
    Entering to the explorer 'account' - is implemented by sessions' records
    """

    # Exit from add_explorer account 
    request.session['app_explorer_username'] = 'anonymous_check'
    request.session['show_anonymous_message'] = True

    if request.method == 'POST':
        
        try:
            username = request.POST["username"]
            password = request.POST["password"]
        except:
            #case of malicious client side editing
            return HttpResponseRedirect(reverse('message', args = ('w_s',)))

        # look for this account in db
        try:
            app_explorer = App_Explorer.objects.filter(username = username, password = password)
        except:
            print('error during retrieving data from db in enter_app_explorer view')
            return HttpResponseRedirect(reverse('message', args = ('w_s',)))
        
        # enter into  explorer 'account' 
        if len(app_explorer) == 1:
            request.session['app_explorer_username'] = username
            
            return HttpResponseRedirect(reverse('change_current_date'))

        # warning message
        else:
            d={"message": "Invalid username and/or password."}

            return render(request,"ad_bus_stops/authentication/enter_app_explorer.html",
                    {**param(request, 'enter_app_explorer'),**d}) 

    else:
        return render(request,"ad_bus_stops/authentication/enter_app_explorer.html",
                param(request, 'enter_app_explorer')) 

def change_current_date(request):
    '''
    Changes current today's date for the simulated world of the app for current explorer
    '''

    if request.method == 'POST':
        try:
            current_date_str = request.POST['current_date']
        except:
            #case of malicious client side editing
            print('Error in POST parameters in change_current_date view')
            return HttpResponseRedirect(reverse('message', args = ('w_s',)))

        if not current_date_str:
            #message = "Please enter a date"

            d={ "message": "Please enter a date",
                'current_today':current_today(app_explorer_username(request)),
                'superuser_name':SUPERUSER_NAME }

            return render(request,"ad_bus_stops/change_current_date.html",
                    {**param(request, 'change_current_date'),**d}) 

        try:
            app_explorer = App_Explorer.objects.get(username = app_explorer_username(request))
        except:
            print('Error in db data retrieving in change_current_date view')
            return HttpResponseRedirect(reverse('message', args = ('w_s',)))

        try:
            currentDate_dateObject = datetime.strptime(current_date_str , '%Y-%m-%d').date()
        except:
            #case of malicious client side editing
            print('invalid date  in change_current_date view')
            return HttpResponseRedirect(reverse('message', args = ('w_s',)))
        
        #  if the new date is earlier then the previous 
        if currentDate_dateObject < app_explorer.current_date:

            d={ "message": "Too early date - time cannot move backwards",
                'current_today':current_today(app_explorer_username(request)),
                'superuser_name':SUPERUSER_NAME  }

            return render(request,"ad_bus_stops/change_current_date.html",
                    {**param(request, 'change_current_date'),**d}) 

        else:
            app_explorer.current_date = currentDate_dateObject
            try:
                app_explorer.save()
            except:
                # db connection faluire
                pass
            return HttpResponseRedirect(reverse("index"))

    else:

        d={ 'current_today': current_today(app_explorer_username(request)),
            'superuser_name':SUPERUSER_NAME ,}
        return render(request,"ad_bus_stops/change_current_date.html",
                {**param(request, 'change_current_date'),**d}) 


def hide_study_message(request, template_name):
    '''
    Hides informative message on top of app pages, that reminds what explorer  is now 
    investigating the app and how to ajust settings for app exploration
    '''

    # keep status of message appearance in session for anonymous
    # and in db for specific explorer
    try:
        explorer_name = app_explorer_username(request)
    except:
        #db connection error
        explorer_name = 'anonymous_check'

    if explorer_name == 'anonymous_check':
        try:
            request.session['show_anonymous_message'] = False
        except:
            #db connection error
            pass
    else:
        try:
            app_explorer =  App_Explorer.objects.get(username = app_explorer_username(request)) 
            get_explorer = True
        except:
            print('Error while receiving db data in hide_study_message view')
            get_explorer = False
        
        if get_explorer:
            app_explorer.show_warning = 'no'
            try:
                app_explorer.save()
            except: 
                #db connection error
                pass

    return HttpResponseRedirect(reverse('index'))

def preset_db_view(request):
    '''
    Initiated by superuser only. Initial recording to db default demo bus stops
    '''

    if app_explorer_username(request) == SUPERUSER_NAME :       
        try:
            preset_db()
            db_preset_message = 'Bus stops successfully set to db'
        except:
            db_preset_message = 'Installation process failed: internal server error'
    else:
        db_preset_message = 'Installation process restriction: Superuser access required'
    
    d={ 'current_today': current_today(app_explorer_username(request)),
        'superuser_name':SUPERUSER_NAME ,
        'db_preset_message':db_preset_message }
    return render(request,"ad_bus_stops/change_current_date.html",
            {**param(request, 'change_current_date'),**d}) 


