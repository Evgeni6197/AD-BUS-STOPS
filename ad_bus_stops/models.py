from django.contrib.auth.models import AbstractUser
from django.db import models

user_status_choices = [
    ("customer", "customer"), 
    ("agency_staff", "agency_staff"),
]

confirmation_choices =[
    ('confirmed','confirmed'),
    ('not_confirmed','not_confirmed') 
] 

record_status_choices = [
    ('actual','actual'),
    ('deprecated','deprecated'),
]

# 'cart' - default.  The order is created at the moment the first  bus-stop is booked
# 'payment waiting' - is recorded when a customer  presses  checkout button 
# 'Paid. Exposition awaiting'  is recorded after staff member manual confirmation on the  dashboard
#  the rest are recorded automatically according to the current  date
current_order_status_choices = [
    ('cart','cart'),
    ('payment waiting','payment waiting'),
    ('Paid. Exposition awaiting','Paid. Exposition awaiting'),
    ('current exposition de jure','current exposition de jure'),
    ('end of exposition de jure','end of exposition de jure'),
]

# 'yes' and 'finished' are recorded after staff member manual confirmation on the  dashboard
exposition_de_facto_choices =[
    ('yes','yes'),
    ('no','no'),
    ('finished','finished'),
]

yes_no = [
    ('yes','yes'),
    ('no','no'),
]

# 'successfully completed' and 'canceled for non-payment' are recorded automatically
archived_order_status_choices = [
    ('successfully completed','successfully completed'),
    ('canceled for non-payment','canceled for non-payment'),
    ('canceled by staff','canceled by staff'),
] 

class App_Explorer(models.Model): 

    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=20, default ='')

    # is used to keep track for expiration of instance
    creation_date = models.DateField()

    # is used to set new  custom 'today'- date  and to keep track that there is no backwards
    #  time-coordinate movement
    current_date = models.DateField()

    # appearance of warning message
    show_warning = models.CharField(max_length=3, choices=yes_no, default="yes")


class User(AbstractUser): 

    # customer or agency staff
    status = models.CharField(
        max_length=12, choices=user_status_choices, default="customer")

    # code sent to user by email for registration confirmation
    code = models.CharField(max_length=4, default='zero')

    # value 'confirmed' is assigned after successful user registration
    confirmation =models.CharField(
        max_length=13, choices=confirmation_choices, default="not_confirmed")

    # app_explorer, who created this user
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, 
        related_name= 'created_customers', blank = True, null = True)

class User_Registration_Timestamp(models.Model): 
    '''
    Records the datetime when user registration began. Used to track registration expiration
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'timestamp')
    datetime = models.DateTimeField(auto_now_add=True)

class City(models.Model):
    name = models.CharField(max_length=20,unique=True )

    # app_explorer, who created this record. Blank for preset records
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, 
        related_name= 'cities_recorded', blank = True, null = True)

class Bus_Stop(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='bus_stops')
    street = models.CharField(max_length=30)
    house = models.CharField(max_length=20) # the nearest house , any additional info
    price =  models.IntegerField(default=100)

    # date of record - app's date (not necessarily coincided with real-world date), 
    # at the moment of record creation
    date  = models.DateField(blank = True, null = True)
    record_status = models.CharField(max_length=12, choices=record_status_choices, default="actual")
    
    # former bus_stop id - before editing (previous version)
    former_id = models.IntegerField(blank = True, null = True)

    # staff user account, that  was used by app_explorer while creating the record. 
    #Blank for pre-set bus-stops records. If a staff member is fired and his account is deleted - the record stays safe
    staff_user = models.ForeignKey(User,  on_delete=models.SET_NULL,
        related_name= 'bus_stops_edited',blank = True, null = True )

    # app_explorer, who created this record. Blank for pre-set bus-stops records
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, 
        related_name= 'bus_stops_recorded', blank = True, null = True )


class Preemption(models.Model):
    '''
    Records the user, that currently has preemptive opportunity to book bus stop for specific month
    Is used to overcome race condition vulnerability
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'preemption')

    # string, including bus_stop id, month,year, explorerID -represents 
    # date of booking of a specific stop in simulated world of a specific explorer 
    # four parameters are composed into one record to control uniqueness 
    # of booking by a single record - that helps to overcome race conditions vulnerability
    stopId_month_year_explorer = models.CharField(max_length=100, unique=True)

    # App_explorer account opened on the machine where  the app  manages this record.
    # For different app_explorer accounts, the booking process as well as all app activity 
    # is carried out independently,
    # i.e. different app_explorers have the opportunity to check app's operation simultaneously,
    # enabling them to make bookings for the same bus_stops and dates as if they were
    # the only app_explorer.
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, 
        related_name= 'preemptions')

class Current_Order(models.Model): 

    # customer that created the order
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'current_orders')

    # date launching timer for payment_waiting period
    first_booking_date = models.DateField()

    # Only the first day of a month
    exposition_starts = models.DateField()

    # Only the last day of a month
    exposition_ends = models.DateField()
    
    order_status = models.CharField(max_length=26, choices=current_order_status_choices, default="cart")
    total_sum =  models.IntegerField(default=0)
    current_exposition_de_facto = models.CharField(max_length=8,
                                             choices=exposition_de_facto_choices, default="no")

    # data of db payment record insertion - staff member and date
    #  If a staff member is fired and his account is deleted - the record stays safe
    payment_recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name= 'payment_recorded_orders', blank = True, null = True)        
    date_of_payment_recording = models.DateField(blank = True,  null = True)

    # data of db exposition_de_facto record insertion - staff member and date
    exposition_de_facto_recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name= 'exposition_de_facto_recorded_orders',blank = True,  null = True)
    date_of_exposition_de_facto_recording = models.DateField(blank = True,  null = True)

    # data of db ad_removal_de_facto record insertion - staff member and date
    ad_removal_de_facto_recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name= 'ad_removal_de_facto_recorded_orders',blank = True,  null = True)
    date_of_ad_removal_de_facto_recording = models.DateField(blank = True,  null = True)

    # App_explorer account  - see comment for Preemption model 
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, 
        related_name= 'current_orders')

class Reference(models.Model): 
    
    #Correspondence between current orders and bus stops booked
    
    order = models.ForeignKey(Current_Order, on_delete=models.CASCADE, related_name= 'bus_stops_booked')
    bus_stop = models.ForeignKey(Bus_Stop,on_delete=models.CASCADE, related_name= 'current_orders')
    
    # bus_stop's placement summary price at the booking moment
    booking_price =  models.IntegerField(default=0)

class Orders_Archived(models.Model):

    # date and status of record in Orders_Archived 
    date = models.DateField()
    order_status = models.CharField(max_length=24, choices=archived_order_status_choices, blank = True,  null = True)

    #  staff member canceled the order - if it was canceled
    canceled_by = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name= 'orders_canceled',blank = True,  null = True)

    # Initial id of the order in current_order db table
    # Is used to overcome race condition vulnerability or repeating the record due to the
    # interruption of every_day_orders_update function fulfillment (see comment inside this function)
    initial_order_id = models.IntegerField(unique=True)

    # These fields are automatically transferred here  from Current_Order model
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'archived_orders')
    exposition_starts = models.DateField()
    exposition_ends = models.DateField()        
    total_sum =  models.IntegerField(default=0)
    first_booking_date = models.DateField()
    payment_recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name= 'payment_recorded_orders_a', blank = True,  null = True)
    date_of_payment_recording = models.DateField(blank = True,  null = True)
    exposition_de_facto_recorded_by = models.ForeignKey(User,on_delete=models.SET_NULL,
        related_name= 'exposition_de_facto_recorded_orders_a',blank = True,  null = True)
    date_of_exposition_de_facto_recording = models.DateField(blank = True,  null = True)
    ad_removal_de_facto_recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name= 'ad_removal_de_facto_recorded_orders_a',blank = True,  null = True)
    date_of_ad_removal_de_facto_recording = models.DateField(blank = True,  null = True)

    # App_explorer account  - see comment for Preemption model 
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, 
        related_name= 'orders_archived')

class Reference_Archived(models.Model):    
    # Records are transferred here automatically from Reference model    
    order = models.ForeignKey(Orders_Archived, on_delete=models.CASCADE, related_name= 'bus_stops_used')
    bus_stop = models.ForeignKey(Bus_Stop,on_delete=models.CASCADE, related_name= 'archived_orders')   
    booking_price =  models.IntegerField(default=0)

    # similar to "initial_order_id' field in Orders_Archived model
    initial_reference_id = models.IntegerField(unique=True)

class Simulated_World_Update(models.Model):
    '''
    Used to keep track that order's  status is updated once a day in simulated world
    of every specific explorer
    Parameter  unique=True  is used to overcome race condition vulnerability
    in a specific simulated world
    '''    
    date = models.DateField()
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, 
            related_name = 'sim_w_update')

    # # str  composed of date and explorer id
    # date_explorer = models.CharField(max_length=20,unique=True)

class Last_Explorer_Update(models.Model):
    '''
    Used to ensure that  for all App_Explorer records  parameter App_Explorer.current_date 
    is updated once a day in real-world  timing. It is actual for explorers with no time similation.

    When time simulation does occur - App_Explorer.current_date  parameter is updated automatically
    This may happen many times in a single real-world day   
    '''
    date = models.DateField()



class SetUp_Parameters(models.Model):
    '''
    Stores only parameters that have been changed by an explorer
    Default is available as dict in parameters.py
    '''    
    # actual / deprecated
    record_status = models.CharField(max_length=12, choices=record_status_choices, default="actual")
    
    # data of record  - staff member and date. If a staff member is fired and his account is deleted - the record stays safe
    staff_member = models.ForeignKey(User, on_delete=models.SET_NULL,
                     related_name= 'set_up_records',blank = True, null = True)
    date = models.DateField(blank = True,  null = True) 

    # days from first booking till cancelation due to non-payment
    payment_waiting = models.IntegerField(default=5)

    # days for ad printing and other production needs
    preparation = models.IntegerField(default=3)

    # months for discount
    duration1 = models.IntegerField(default=2)
    duration2 = models.IntegerField(default=3)
    duration3 = models.IntegerField(default=4)

    # percentage of discount amount 
    discount1 = models.IntegerField(default=10)
    discount2 = models.IntegerField(default=20) 
    discount3 = models.IntegerField(default=30)

    # Year till which booking is being received
    year = models.IntegerField(default=2026)

    # App_explorer account  (see comment for Preemption model )
    app_explorer = models.ForeignKey(App_Explorer, on_delete = models.CASCADE, related_name= 'setup_parameters')







