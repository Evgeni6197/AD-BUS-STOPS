from ..parameters import *


@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def dashboard(request, message):

    # 1. case of redirection to dashboard view from payment_verification, placement_verification, removal_verification
    if message == 'app_explorer_required':
        d={ 'dashboard_part':'front','message':'app_explorer_required',} 
        return render(request,'ad_bus_stops/dashboard.html',{**param(request, 'dashboard'),**d})

    # 2. gets explorer name
    try:
        explorer_name = app_explorer_username(request)
    except:
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))

    # 3. gets db queries for rendering
    if explorer_name != 'anonymous_check':
        try: 
            explorer = App_Explorer.objects.get(username = explorer_name)        
            payment_waiting_orders_qu = Current_Order.objects.filter(app_explorer = explorer,
                                                                 order_status = 'payment waiting')
            ad_to_place_orders = Current_Order.objects.filter(  app_explorer = explorer,
                                                                order_status = 'current exposition de jure',
                                                                current_exposition_de_facto  = "no")
            ad_to_remove_orders = Current_Order.objects.filter( app_explorer = explorer,
                                                                order_status = 'end of exposition de jure', 
                                                                current_exposition_de_facto  = "yes")
        except:
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        content =[  len(payment_waiting_orders_qu),
                    len(ad_to_place_orders ),
                    len(ad_to_remove_orders)
                ]
        if content == [0,0,0]:
            content =[]        
        d={ 'dashboard_part':'front', "content": content } 
        return render(request,'ad_bus_stops/dashboard.html',{**param(request, 'dashboard'),**d})
    else:
        d={ 'dashboard_part':'front'}
        return render(request,'ad_bus_stops/dashboard.html',{**param(request, 'dashboard'),**d})

@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def payment_verification(request):

    # 1. gets explorer name
    try:
        explorer_name = app_explorer_username(request)
    except:
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))
    
   # 2. gets db queries for rendering
    if explorer_name != 'anonymous_check':

        try:
            explorer = App_Explorer.objects.get(username = explorer_name) 
        except:
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        # 3.  recording the  payment reception to  the db
        if request.method == 'POST':
            try:
                order_id = int(request.POST['order_id']) 
                order_sum = int(request.POST['order_sum'])
            except:
                print('error in POST in  payment_verification view')
                return HttpResponseRedirect(reverse('message', args = ('w',)))

            try:
                order_obj = Current_Order.objects.get(pk = order_id )
                db_order_sum = order_obj.total_sum
                db_order_explorerName = order_obj.app_explorer.username
                db_order_status = order_obj.order_status
            except:
                return HttpResponseRedirect(reverse('message', args=('connection_error',)))

            # Validation of request.POST  data
            if (db_order_sum != order_sum or 
                db_order_explorerName != explorer_name  or
                db_order_status != 'payment waiting'):
                return HttpResponseRedirect(reverse('message', args=('w',)))
            
            try:
                order_obj.order_status = 'Paid. Exposition awaiting'
                customer = order_obj.user
                customer_name = customer.username
                customer_email = customer.email

                order_obj.payment_recorded_by = request.user
                order_obj.date_of_payment_recording = explorer.current_date
                order_obj.save()
            except:
                return HttpResponseRedirect(reverse('message', args=('connection_error',)))
            
            try:
                # sends payment reception message 
                send_mail(
                        "from AD - BUS - STOPS ",
                        message_to_customer(customer_name, order_id,
                                                        'deadline', order_sum,'paid'),
                        AGENCY_EMAIL,
                        [f"{customer_email}"],
                        fail_silently=False, )
            except:
                print('email sending error  in payment_verification view')
                pass
        
        #  4. composing list of payment waiting orders for rendering     
        payment_waiting_orders = []
        try:         
            payment_waiting_orders_qu = Current_Order.objects.filter(app_explorer = explorer,
                                                                 order_status = 'payment waiting')
            for ord_obj in payment_waiting_orders_qu:
                payment_waiting_orders.append([ ord_obj.id,
                                                ord_obj.total_sum,
                                                ord_obj.first_booking_date ]) 
        except:
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))
                                                      
        payment_waiting_orders.sort(key = lambda x:x[2])
        payment_waiting_orders_str = []       
        for ord_param in payment_waiting_orders:
            payment_waiting_orders_str.append(  ["Order &nbsp;№"+str(ord_param[0])+', '+
                                                ord_param[2].strftime('%d/%m/%Y')+" " + 
                                                f'{ord_param[1]:>5}'.replace(' ','&nbsp;') + "&nbsp;$",                                                
                                                ord_param[0], # order Id
                                                ord_param[1], # total sum str formatted 
                                                ]) 
        d={'dashboard_part':'payment_verification',
            "orders":payment_waiting_orders_str}
        return render(request,'ad_bus_stops/dashboard.html',{**param(request, 'dashboard_p'),**d})
    else:
        return HttpResponseRedirect(reverse('dashboard', args=('app_explorer_required',)))

@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def placement_verification(request):

    # 1. gets explorer name
    try:
        explorer_name = app_explorer_username(request)
    except:
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))
    
   
    if explorer_name != 'anonymous_check':
        # 2. gets explorer object
        try:
            explorer = App_Explorer.objects.get(username = explorer_name) 
        except:
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        # 3.  POST : gets data and modifies db
        if request.method == "POST":
            try:
                order_id = int(request.POST['order_id'])
            except:
                return HttpResponseRedirect(reverse('message', args=('w',)))
            
            # gets order object, validates  and updates it
            try:
                order_obj = Current_Order.objects.get(pk = order_id)

                if (order_obj.order_status != 'current exposition de jure' or 
                    order_obj.current_exposition_de_facto != "no" or 
                    order_obj.app_explorer != explorer):
                    return HttpResponseRedirect(reverse('message', args=('w',)))
                
                customer = order_obj.user
                customer_name = customer.username
                customer_email = customer.email

                order_obj.date_of_exposition_de_facto_recording = explorer.current_date
                order_obj.exposition_de_facto_recorded_by = request.user
                order_obj.current_exposition_de_facto = 'yes'
                order_obj.save()
            except:
                return HttpResponseRedirect(reverse('message', args=('connection_error',))) 

            try:
                # sends placement verification message 
                send_mail(
                        "from AD - BUS - STOPS ",
                        message_to_customer(customer_name, order_id,
                                                        'deadline', "order_sum",'placement'),
                        AGENCY_EMAIL,
                        [f"{customer_email}"],
                        fail_silently=False, )
            except:
                print('email sending error  in placement_verification view')
                pass
        
        # 4. gets db queries for rendering
        exposed_deJure_obj = []
        try:
            exposed_deJure_qu = Current_Order.objects.filter(app_explorer = explorer,
                                                        order_status = 'current exposition de jure',
                                                        current_exposition_de_facto  = "no")
            for ord_obj in exposed_deJure_qu:
                exposed_deJure_obj.append( [ord_obj.id, ord_obj.exposition_starts] )
        except:
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        # sorting by start exposition date
        exposed_deJure_obj.sort(key = lambda x:x[1])
        exposed_deJure = []
        for item in exposed_deJure_obj:
            exposed_deJure.append([item[0],item[1].strftime('%d/%m/%Y')])
        
        d={'dashboard_part':'placement_verification',
            "orders":exposed_deJure}
        return render(request,'ad_bus_stops/dashboard.html',{**param(request, 'dashboard_p'),**d})
    else:
        return HttpResponseRedirect(reverse('dashboard', args=('app_explorer_required',))) 

@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def removal_verification(request):

    # 1. gets explorer name
    try:
        explorer_name = app_explorer_username(request)
    except:
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))
       
    if explorer_name != 'anonymous_check':
        # 2. gets explorer object
        try:
            explorer = App_Explorer.objects.get(username = explorer_name) 
        except:
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        # 3.  POST : gets data and modifies db
        if request.method == "POST":
            try:
                order_id = int(request.POST['order_id'])
            except:
                return HttpResponseRedirect(reverse('message', args=('w',)))
            
            # gets order object, validates  and updates it
            try:
                order_obj = Current_Order.objects.get(pk = order_id)

                if (order_obj.order_status != 'end of exposition de jure' or 
                    order_obj.current_exposition_de_facto != "yes" or 
                    order_obj.app_explorer != explorer):
                    return HttpResponseRedirect(reverse('message', args=('w',)))
                
                customer = order_obj.user
                customer_name = customer.username
                customer_email = customer.email

                order_obj.date_of_ad_removal_de_facto_recording  = explorer.current_date
                order_obj.ad_removal_de_facto_recorded_by = request.user
                order_obj.current_exposition_de_facto = 'finished'
                order_obj.save()
            except:
                return HttpResponseRedirect(reverse('message', args=('connection_error',))) 
            try:
                # sends removal verification message 
                send_mail(
                        "from AD - BUS - STOPS ",
                        message_to_customer(customer_name, order_id,
                                                        'deadline', "order_sum",'removal'),
                        AGENCY_EMAIL,
                        [f"{customer_email}"],
                        fail_silently=False, )
            except:
                print('email sending error  in removal_verification view')
                pass

        # 4. gets db queries for rendering
        end_expos_deJure_obj = []
        try:
            end_expos_deJure_qu = Current_Order.objects.filter(app_explorer = explorer,
                                                        order_status = 'end of exposition de jure',
                                                        current_exposition_de_facto  = "yes")
            for ord_obj in end_expos_deJure_qu:
               end_expos_deJure_obj.append( [ord_obj.id, ord_obj.exposition_ends] )
        except:
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        # sorting by end exposition date
        end_expos_deJure_obj.sort(key = lambda x:x[1])
        end_expos_deJure = []
        for item in end_expos_deJure_obj:
            end_expos_deJure.append([item[0],item[1].strftime('%d/%m/%Y')])

        
        d={'dashboard_part':'removal_verification',
            "orders":end_expos_deJure}
        return render(request,'ad_bus_stops/dashboard.html',{**param(request, 'dashboard_p'),**d})

    else:
        return HttpResponseRedirect(reverse('dashboard', args=('app_explorer_required',))) 
