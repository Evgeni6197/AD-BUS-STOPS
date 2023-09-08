import csv, json, os, random

from datetime import  timedelta, date, datetime
from itertools import chain


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone

from .models import *

START_MESSAGE_CONTAINER_HEIGHT = 50  # template start_*.html parameter : min gap for hello message
PADDING_2_PHOTO = 15  # css parameter needed for start view in portrait case
PADDING_3_PHOTO = 15  # css parameter needed for start view in landscape case
VIEWPORT_WIDTH_PERCENTAGE = 0.95  #css parameter - percentage of viewport  width used for output
VIEWPORT_HEIGHT_PERCENTAGE = 0.95 #css parameter - percentage of viewport  height used for output
IMAGE_RATIO =1.3 #Height / width ratio of images rendered to start_*.html  template
MOBILE = False  # mobile mode for development layout checking

ENABLE_PASSWORD_VALIDATION = True # May be False for development  - set True for production
AGENCY_EMAIL = "ad.bus.stop3000@gmail.com"
REGISTRATION_EXPIRY = timedelta(seconds = 183)  #in that much seconds not confirmed user is deleted
PAGINATION = 10   # that much records  for html layout for page
EXPLORER_ACCOUNT_EXPIRATION  = 10 # in that much days app check account expires is deleted from db with all dependencies 
SUPERUSER_NAME = 'director'


# this list is passed to /start/start*.html for animation with images
CONTAINER_NUMBERS = [ 
    (1,'ad_bus_stops/images/1.JPG'),
    (2,'ad_bus_stops/images/2.JPG'),
    (3,'ad_bus_stops/images/3.JPG'),    
    (4,'ad_bus_stops/images/4.JPG'),
    (5,'ad_bus_stops/images/5.JPG'),
    (6,'ad_bus_stops/images/1.JPG'),
    (7,'ad_bus_stops/images/3.JPG'),
    (8,'ad_bus_stops/images/2.JPG'),
]

# See models.py (SetUp_Parameters) for comments for keys' meaning (SetUp_Parameters) 
DEFAULT_setUp = {
    'payment_waiting':5,
    'preparation':3,
    'duration1':2,
    'duration2':3,
    'duration3':4,
    'discount1':10,
    'discount2':20,
    'discount3':30,
    'year':2026, 
}


'''
Here you see not  views  - just regular helper functions, that retrieve parameters from request
'''

def app_explorer_username(request):
    '''
    helper for param function, vacant_months func - see below
    also is called from book view  - see below
    '''

    if 'app_explorer_username' in request.session:
        return request.session['app_explorer_username']
    else:
        return 'anonymous_check' 

def get_explorer_obj(explorer_name):
    try:
        return App_Explorer.objects.get(username = explorer_name)
    except:
        return


def show_anonymous_message(request):
    '''
    helper for param function - see below
    '''

    if 'show_anonymous_message' in request.session:            
        return request.session['show_anonymous_message'] 
    else:
        return True    

def user_status_name(request):
    '''
    helper for param function - see below
    '''

    if request.user.is_authenticated: 
        user_status = request.user.status
        user_name = request.user.username
    else:
        user_status = 'anonymous'
        user_name = ' '
    return (user_status, user_name )

def device(request):
    '''
    helper for param function - see below
    '''

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    is_mobile = 'Mobile' in user_agent or 'Android' in user_agent
    if is_mobile:
       return 'mobile'
    else:
        return"desktop" 

def current_today_obj(explorer_obj, explorer_name): 
    '''  
    is called from  book view, vacant_months func 
     and current_today - see below and book_view.py
    '''

    if explorer_name == 'anonymous_check':        
        return date.today()  
    else:
        try:
            date_in_db = explorer_obj.current_date
        except:
            print('error while App_Explorer data retrieving in current_today helper function' )
            return date.today()   

        if date.today() > date_in_db:
            return date.today()             
        else:
            return date_in_db  


def current_today(explorer_name): 
    '''helper for param function - see below'''
    #return current_today_obj(get_explorer_obj(explorer_name),explorer_name).strftime('%m/%d/%Y') 
    return current_today_obj(get_explorer_obj(explorer_name),explorer_name).strftime('%d/%m/%Y')



def show_registered_message(app_explorer_username):
    '''
    helper for param function - see below
    '''

    if app_explorer_username != 'anonymous_check':
        try:
            app_explorer =  App_Explorer.objects.get(username = app_explorer_username) 
            return app_explorer.show_warning
        except:
            print('Error while receiving db data in show_registered_message helper function') 
            return 'yes'              
    else:
        return 'yes' 


def param(request, template_name): 
    '''
    General helper for all views besides start views
    '''
    a = app_explorer_username(request)
    print( a )

    return   {
        "device":device(request),
        'user_status': user_status_name(request)[0],        
        'user_name': user_status_name(request)[1],
        'template_name':template_name,
        'app_explorer_username': a, 
        'current_today': current_today(a),
        'show_anonymous_message':show_anonymous_message(request),
        'show_registered_message':show_registered_message(a) ,         
    }

def staff_permission_check(user):
    '''
    Checker for dashboard view
    '''
    return user.status == "agency_staff"


def preset_db():
    """
    Writes to  models City, Bus_Stop records from  csv files
    is called from  preset_db_view

    Also to User  - demo customer and staff    
    """
    #1.  presets addresses
    path1 = os.path.join(os.path.dirname(__file__), 'data','London_streets.csv')
    path2 = os.path.join(os.path.dirname(__file__), 'data', 'Manchester_streets.csv')

    for p in (path1,path2):   
        with open(p,"r", encoding = 'utf-8') as f:
            for line in f:
                [city,street,house, price] = (line.strip().split(','))
                try:
                    City.objects.create(name = city.lower().capitalize())                
                except:
                    # this city name is already in City model
                    pass

                # Create a record if not already created
                try:
                    city_obj = City.objects.get(name = city.lower().capitalize())  
                    if len(Bus_Stop.objects.filter(city = city_obj,
                                street = street, house = house, price = price)) == 0 :                       
                        Bus_Stop.objects.create(city = city_obj,street = street,
                                                house = house,price = price)
                except:
                    #error in db data retrieving
                    pass

    # 2. Preset demo  users 
    try:
        User.objects.create_user(username = "customer", password = "demo_client1", email = AGENCY_EMAIL,
                                status = "customer", confirmation = 'confirmed')
        User.objects.create_user(username = "staff", password = "demo_staff1", email = AGENCY_EMAIL,
                                status = "agency_staff", confirmation = 'confirmed')  
    except IntegrityError:
        pass 
    except:                   
        # db connection error
        pass
    return
preset_db()


def actual_setUp(request):
    '''
    called from guidance view, bus_stops view, book view

    returns: dict  including default setUp for anonymous_check or if  an explorer 
    did not entered changes to setUp    OR   actual changed setUp for the current explorer
    if he has made changes
    '''
    explorer_name = app_explorer_username(request) 
    actual_setUp_obj =False   
    if explorer_name != 'anonymous_check' :
        try:
            #the latest record with actual status. 
            actual_setUp_obj = App_Explorer.objects.get(username = explorer_name
                    ).setup_parameters.filter(record_status="actual").last()                          
        except:
            print('error in db retrieving  in  actual_setUp  helper function')
            actual_setUp_d = DEFAULT_setUp

        if not actual_setUp_obj:
            actual_setUp_d = DEFAULT_setUp
        else:
            actual_setUp_d = {
                'payment_waiting':actual_setUp_obj.payment_waiting,
                'preparation':actual_setUp_obj.preparation,
                'duration1':actual_setUp_obj.duration1,
                'duration2':actual_setUp_obj.duration2,
                'duration3':actual_setUp_obj.duration3,
                'discount1':actual_setUp_obj.discount1,
                'discount2':actual_setUp_obj.discount2,
                'discount3':actual_setUp_obj.discount3,
                'year':actual_setUp_obj.year,
            }
    else:
        # take default
        actual_setUp_d = DEFAULT_setUp

    return actual_setUp_d


def vacant_months_cart(stop, request):  #explorer_name, year_till, minimum_time_till_pub):
    '''
    called from  bus_stops  view  ,  book_confirm view

    stop: instance of Bus_Stop model
    returns: tuple 
                tuple[0] - list of tuples: ( str(month, year), int) - vacant months for   booking 
                        in the simulated world of the current explorer , int - helper sorting number 
                tuple[1] - set of date obj 
                tuple [2] - bool   
            
    '''
    # 1. Gets all orders with this bus-stop  for the current explorer
    orders =[]
    explorer_name = app_explorer_username(request)
    try:
        for reference in stop.current_orders.all():
            order = reference.order
            if order.app_explorer.username == explorer_name:
                orders.append(order)
    except:
        # db connection error
        print('Error in db query  1 in parameters.py')
        return ('db_connection_error','db_connection_error',False)


    # 2. Gets set of all occupied months for this bus-stop for the current explorer
    occupied_months = set()
    for order_item in orders:

        try:
            tmp = order_item.exposition_starts
            while tmp < order_item.exposition_ends:
                occupied_months.add(tmp)
                tmp += timedelta(days = 32)
                tmp = date(tmp.year, tmp.month, 1)
        except:
            # db connection error
            print('Error in db query  2 in parameters.py')
            return ('db_connection_error','db_connection_error',False)


    
    # 3. Current bus-stop  is already in the cart of the request.user  
    for order_item in orders:
        try:
            if order_item.user == request.user  and order_item.order_status == "cart":
                return ([],occupied_months,True)
        except:
            # db connection error
            print('Error in db query  3 in parameters.py')
            return ('db_connection_error','db_connection_error',False)
    
    # 4. getting list of all months counting FROM current app' today to the setUp month  
    actual_setUp_d = actual_setUp(request)
    minimum_time_till_pub = actual_setUp_d['payment_waiting'] + actual_setUp_d['preparation']    
    first_possible_date_obj = current_today_obj(
        get_explorer_obj(explorer_name),explorer_name) + timedelta(days=minimum_time_till_pub)

    # list of all months  - maximum coverage defined by setUp
    potential_booking_dates = []
    for y in range(2023,actual_setUp_d['year']):
        for m in range (1,13):
            potential_booking_dates.append(date(y,m,1))


    # vacant_months  is complementary sequence to occupied_months in terms of (month,year)
    vacant_months = []
    count = 0
    for date_item in potential_booking_dates:
        count += 1
        vacant = False
        if date_item >= first_possible_date_obj: # the month starts after min gap from booking to placement
            vacant = True
            for order_item in orders:

                try:
                    if order_item.exposition_starts <= date_item <= order_item.exposition_ends:
                        vacant = False
                        break
                except:
                    # db connection error
                    print('Error in db query  4 in parameters.py')
                    return ('db_connection_error','db_connection_error',False)


        if vacant:
            vacant_months.append((date_item.strftime("%m/%Y"),count))

    return (vacant_months, occupied_months, False)

def delete_preemptions(preemption_records):
    '''
    helper is called from book view
    '''
    for item in preemption_records:
        try:
            Preemption.objects.get(stopId_month_year_explorer = item).delete()
        except:
            print('error in  preemption deletion in book view ')
    return

def get_open_order_months(order_opened):
    """
    Gets the set of months taken in the opened order if exists

    order_opened: order obj   or  bool:False
    return: set of date obj

    called from stops_view  ,  book_confirm_view
    """
     
    if order_opened: 
        try:
            start = order_opened.exposition_starts       
            end = order_opened.exposition_ends
        except:
            # db connection error
            order_opened = False 

    open_order_months = set()
    if order_opened:
        tmp = start
        while tmp < end:
            open_order_months.add(tmp)
            tmp += timedelta(days = 32)
            tmp = date(tmp.year, tmp.month, 1) 
    return open_order_months


def message_to_customer(username, order_id, deadline, total,message):

    if message == 'success':

        return (f"  Dear {username}! Your order №{order_id} has been successfully registered! " +
        f" To complete the process, please arrange an offline payment of {total}$ before {deadline}. " + 
        f" Payment details: xxx xxx xxx xxx . " +
        f" For comprehensive order insights, kindly access your account page on our website. ")
    
    elif message == 'failure':
        return (f"  Dear {username}! Apologies  for the misinformation earlier." + 
        f"Regrettably, the registration for the order №{order_id} was unsuccessful. " +
        f"We kindly request you to reattempt the checkout process." )

    elif message == 'paid':
        return (f"  Dear {username}! We are writing to inform you that we have received your " +
        f"payment of {total}$  for  Order №{order_id}. We want to assure you that we will be following "+
        f"the timeline outlined in the order for the subsequent steps.  For more detailed information, "+
        f"please visit your account page on our website.")

    elif message == 'placement':
        return (f"  Dear {username}! We are pleased to inform you that your advertisement has been " +
        f"successfully placed in accordance with Order No. {order_id}. To access the details " +
        f"of your order, please visit your account page on our website.")

    elif message == 'removal':
        return (f"  Dear {username}! We are pleased to inform you that your Order No. {order_id} " +
        f" has been successfully fulfilled. We appreciate your business " +
        f"and look forward to serving you again in the future.")

 
 

def delete_not_confirmed_user(): 

    '''
    Checks all User_Registration_Timestamp  instances for expiration
    For expired entries checks corresponding users - if yet not confirmed - deletes them
    Deletes expired User_Registration_Timestamp  instances


    Also checks all not confirmed users - if there are not corresponding User_Registration_Timestamp  instance
     - it means db error during creating such instance -  deletes this not confirmed user
    '''
    
    #1  Deleting  according to User_Registration_Timestamp expiration - regular case
    try:
        registration_records = User_Registration_Timestamp.objects.all() 
    except:
        print('error in db timestamp retrieving in delete_not_confirmed_user.py')
        registration_records =[]

    for record in registration_records: 

        # registration time expired

        try:
            time_expired =  timezone.now() - record.datetime > REGISTRATION_EXPIRY 
        except:
            # db connection faluire
            time_expired = True

        if time_expired:    
            
            try:
                user = User.objects.get(pk = record.user.id)
                confirmation = user.confirmation
            except:
                # due to race conditions - user object is already deleted by another thread 
                # or db connection faluire
                continue

            if confirmation == "not_confirmed":
                try:
                    user.delete()  # automatic record deletion through cascade model mechanism
                except:
                    #db connection failure
                    pass    
            else:
                # record deletion for confirmed user
                try:
                    record.delete()
                except:
                    #db connection failure
                    pass  

    # 2   Deleting in case of no   User_Registration_Timestamp  instance

    try:
        not_confirmed_users = User.objects.filter(confirmation = "not_confirmed").exclude(username = SUPERUSER_NAME)
    except:
        #db connection error
        return

    for not_confirmed_user in not_confirmed_users:
        try:
            if not not_confirmed_user.timestamp.first():
                not_confirmed_user.delete()
        except:
            pass















            

        
        



