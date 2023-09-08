from django.db.models import Q

from .parameters import *

def explorer_update(request):
    '''
    If App_Explorer model records were not yet updated today   - updates current date field
    or delets deprecated explorers
    Helper is called from index view

    '''
    # 1. return if the update has been already  made today
    try:
        last_update_obj = Last_Explorer_Update.objects.last()
        get_last_update_obj = True
    except:
        print('Error in first Last_Explorer_Update data retrieving in explorer_update helper func')
        get_last_update_obj = False
        
    if get_last_update_obj and last_update_obj :
        last_update = last_update_obj.date
    else:
        last_update = False

    today = date.today()
    if last_update and last_update >= today:
        return
    
    # 2. update  record in Last_Explorer_Update

    # deprecated records deletion
    try:
       last_update_objs =  Last_Explorer_Update.objects.all()
       for  obj in last_update_objs:
            obj.delete()
    except:
        print('Error in second Last_Explorer_Update data retrieving in explorer_update helper func')
        pass

    # update itself
    try:    
        Last_Explorer_Update.objects.create(date = today)
    except:
        # object will be created in some next function calling
        pass

    # 3. update Explorers
    
    #getting all explorers besides superuser explorer account
    try:
        explorers = App_Explorer.objects.exclude(username = SUPERUSER_NAME)   
    except:
        # db connection faluire
        print('Error in App_Explorer data retrieving in explorer_update helper func')
        return
    
    delta = timedelta(days = EXPLORER_ACCOUNT_EXPIRATION )

    
    for explorer in explorers:

        # delete deprecated explorers
        try:
            explorer_deprecated = today - explorer.creation_date > delta
            explorer_name = explorer.username
        except:
            # DB connection error: deprecated explorer will be deleted later
            explorer_deprecated = False

        try:
            curentDate_deprecated = explorer.current_date < today
        except:
            # DB connection error: deprecated current date  will be updated later
            print("db connection error in every_day.py")
            curentDate_deprecated  = False


        if explorer_deprecated:            
            try:                               
                # exit from the  explorer account if the app is currently in it
                if explorer_name == app_explorer_username(request):
                    request.session['app_explorer_username'] = 'anonymous_check'
                    request.session['show_anonymous_message'] = True

                explorer.delete()
            except:
                # db connection faluire
                pass

        # update deprecated today's date for actual explorers        
        elif curentDate_deprecated:
            
            try: 
                explorer.current_date = today   
                explorer.save()
            except:
                # db connection faluire
                pass    
    return


def every_day_orders_update(request):

    successful_update = True    # this parameter tracks order deletion  in to_archive(*args)
                                
    # 1. Gets explore name
    try:
        explorer_name = app_explorer_username(request)
        if explorer_name == 'anonymous_check':
            # there are no orders for this case
            print('exits from every_day_orders_update: anonymous_check')
            return
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 1 in every_day_orders_update')
        return

    # 2. Gets explorer
    try:
        explorer = App_Explorer.objects.get(username = explorer_name)
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 2 in every_day_orders_update')
        return

    # 3. Gets app's current date
    try:
        current_date = explorer.current_date
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 3 in every_day_orders_update')
        return

    # 4. Checking if orders were already  updated  "today" .
    try:
        update_obj = Simulated_World_Update.objects.filter(app_explorer = explorer).last()
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 4 in every_day_orders_update')
        return

    if update_obj:
        try:            
            if update_obj.date >= current_date:
                return
            update_obj_id = update_obj.id
        except:
            # db connection error. Update will be made in a further index view call
            print('query error 5 in every_day_orders_update')
            return

    
    #5.  Manipulates orders  with status 'cart'  and also 'payment waiting' of  the current explorer.
    
    # gets orders 
    try:
        orders_cart_payWait = Current_Order.objects.filter(Q(order_status = 'cart') | 
                                                            Q(order_status = 'payment waiting'),
                                                            app_explorer = explorer, )
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 6 in every_day_orders_update')
        return
    
    
    if orders_cart_payWait:

        # gets relevant setUp dict 'payment waiting' parameter
        try:
            actual_setUp_obj = explorer.setup_parameters.filter(record_status="actual").last()
        except:
            # db connection error. Update will be made in a further index view call
            print('query error 7 in every_day_orders_update')
            return

        if actual_setUp_obj:
            try:
                payment_waiting_period =  actual_setUp_obj.payment_waiting 
            except:
                # db connection error. Update will be made in a further index view call
                print('query error 8 in every_day_orders_update')
                return
        else:
            payment_waiting_period = DEFAULT_setUp['payment_waiting']

        # loops for order list
        for order in orders_cart_payWait:

            try:
                # parameter to check if the payment has expired
                payment_expired =  order.first_booking_date + timedelta(
                                                    days = payment_waiting_period) < current_date
            except:
                # db connection error. Update will be made in a further index view call
                print('query error 9 in every_day_orders_update')
                return
 
            
            if payment_expired : 
                # transfers the order to the  archive
                archived = to_archive(order,explorer,current_date,'canceled for non-payment',None)
                if not archived:
                    return
                elif archived == 'not complete':
                    successful_update = False


    # 6. Manipulates orders  with status 'Paid. Exposition awaiting' of  the current explorer.

    # gets orders
    try:
        orders_paid = Current_Order.objects.filter(order_status = 'Paid. Exposition awaiting',                                                           
                                                            app_explorer = explorer)
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 15 in every_day_orders_update')
        return

    # loops for order list
    for order in orders_paid:
        try:
            if order.exposition_starts  <= current_date:
                order.order_status = 'current exposition de jure'
                order.save()
        except:
            # db connection error. Update will be made in a further index view call
            print('query error 16 in every_day_orders_update')
            return 

    # 7. Manipulates orders  with status 'current exposition de jure' of  the current explorer.

    # gets orders
    try:
        orders_displayed = Current_Order.objects.filter(order_status = 'current exposition de jure',                                                           
                                                            app_explorer = explorer)
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 17 in every_day_orders_update')
        return

    # loops for order list
    for order in orders_displayed:
        try:
            if order.exposition_ends  <= current_date:
                order.order_status = 'end of exposition de jure'
                order.save()
        except:
            # db connection error. Update will be made in a further index view call
            print('query error 18 in every_day_orders_update')
            return     
    
    # 8. Manipulates orders  with current_exposition_de_facto ='finished' of the current explorer.

    # gets orders
    try:
        orders_finished = Current_Order.objects.filter(current_exposition_de_facto = 'finished',                                                           
                                                            app_explorer = explorer)
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 19 in every_day_orders_update')
        return

    for order in orders_finished: 

        # transfers the order to the  archive
        archived = to_archive(order,explorer,current_date,'successfully completed',None)
        if not archived:
            return
        elif archived == 'not complete':
            successful_update = False

    # 9. updates Simulated_World_Update instance if exists or creates it
    if successful_update:
        if update_obj:
            try:            
                update_obj.date = current_date
                update_obj.save()
                print('Simulated_World Updated successfully')
            except:
                # db connection error. Update will be made in a further index view call
                print('query error 20 in every_day_orders_update')
        else:
            try:
                Simulated_World_Update.objects.create(app_explorer = explorer, date = current_date )
                print('Simulated_World Updated successfully')           
            except:
                # db connection error. Update will be made in a further index view call
                print('query error 21 in every_day_orders_update')

            
def to_archive(order,explorer,current_date,reason,staff_member):
    '''
    Parameters:
    order : Current_Order instance
    explorer: App_Explorer instance
    current_date: date object
    reason: str  - one of list  archived_order_status_choices  (see models.py)
    staff_member:  User instance

    returns:
        one of : True  False 'not complete'
    '''

    try:
        order_archived = Orders_Archived(
            date = current_date,
            order_status =reason,
            
            # this unique=True field ensures  archive record uniqueness in case of the  further process
            # interruption due to db connection error and repeating the order update process in the next index view calling
            initial_order_id  = order.id,
            
            user = order.user,
            exposition_starts = order.exposition_starts,
            exposition_ends = order.exposition_ends,
            total_sum = order.total_sum, 
            first_booking_date = order.first_booking_date,
            app_explorer = explorer,
            payment_recorded_by = order.payment_recorded_by,
            date_of_payment_recording = order.date_of_payment_recording,
            exposition_de_facto_recorded_by =order.exposition_de_facto_recorded_by,
            date_of_exposition_de_facto_recording = order.date_of_exposition_de_facto_recording,
            ad_removal_de_facto_recorded_by = order.ad_removal_de_facto_recorded_by, 
            date_of_ad_removal_de_facto_recording  = order.date_of_ad_removal_de_facto_recording) 
        order_archived.save()
        
        if  reason == 'canceled by staff':
            order_archived.canceled_by = staff_member
            order_archived.save()
        
    except IntegrityError:
        print('orders_archived instance was created early')
        try:
            order_archived = Orders_Archived.objects.get(initial_order_id = order.id)
        except:
            # db connection error. Update will be made in a further index view call
            print('query error 1 in archived')
            return False                
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 2 in archived')
        return False

    # gets order reference instances 
    try:
        references = order.bus_stops_booked.all()
    except:
        # db connection error. Update will be made in a further index view call
        print('query error 3 in archived')
        return  False

    # transfers references to  the archive
    for reference in references:
        try:
            Reference_Archived.objects.create(  order = order_archived,
                                                bus_stop = reference.bus_stop,
                                                booking_price = reference.booking_price,
                                                
                                                # see comment in models.py
                                                initial_reference_id = reference.id )
        except IntegrityError:
            print('reference_archived instance was created early')
            pass
        except:
            # db connection error. Update will be made in a further index view call
            print('query error 4 in archived')
            return False
    
    # delets the order
    try:
        order.delete()
    except:
        # db connection error. Deletion will be made in a further index view call
        print('query error 5 in to_archive')
        # return "not complete" provides a continuation of the update process for orders and prevents 
        # update for Simulated_World_Update instance - so on the next index view call 
        #  the new order update attempt will be implemented and order.delete() may be successful
        return 'not complete'

    return True








