from ..parameters import *

@login_required(login_url="/login")
def order_page(request, order_id, action):

    # 1. gets explorer name
    try:
        explorer_name = app_explorer_username(request)
    except:
        print('db connection error 1 in order_page view')
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))

    if explorer_name != 'anonymous_check':
        # 1. getting order object and checking it's belonging to current explorer
        try:
            current_order_obj_qu = Current_Order.objects.filter(pk = order_id)
            if current_order_obj_qu:
                order_obj =  current_order_obj_qu.first()
                source = 'current'
            else:
                archive_order_obj_qu = Orders_Archived.objects.filter(initial_order_id = order_id)
                if archive_order_obj_qu:
                   order_obj = archive_order_obj_qu.first()
                   source = 'archive'
                else:                    
                    return HttpResponseRedirect(reverse('message', args=('no_order',))) 
            if  order_obj.app_explorer.username != explorer_name :
                return HttpResponseRedirect(reverse('message', args=('no_order',))) 
        except:
            print('db connection error 2 in order_page view')
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        
        # 2. Access validation
        try:
            order_username = order_obj.user.username
            if request.user.status == "customer" and request.user.username != order_username:
                return HttpResponseRedirect(reverse('message', args=('a',)))
        except:
            print('db connection error 3 in order_page view')
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))


        #3. Getting order parameters
        parameters = []
        try:
            parameters.append(order_obj.first_booking_date.strftime('%d/%m/%Y'))
            parameters.append(order_obj.exposition_starts.strftime('%d/%m/%Y'))
            parameters.append(order_obj.exposition_ends.strftime('%d/%m/%Y'))
            parameters.append(order_obj.order_status)
            parameters.append(order_obj.total_sum)
            parameters.append(order_username)
        except:
            print('db connection error 4 in order_page view')
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        #4. Getting bus-stops list 
        bus_stops_list = []       
        try:
            # taking Reference model
            if source == 'current':
                references = order_obj.bus_stops_booked.all()

            # taking Reference_Archived   model 
            else:
                references = order_obj.bus_stops_used.all()
            
            # composing list of [address, booking price]
            for reference in references:
                stop_obj = reference.bus_stop
                bus_stops_list.append([stop_obj.city.name +", " + stop_obj.street+'&nbsp;'+
                                        stop_obj.house , reference.booking_price  ]) 
        except:
            print('db connection error 5 in order_page view')
            return HttpResponseRedirect(reverse('message', args=('connection_error',)))

        # Sorts and enumerates
        bus_stops_list.sort(key = lambda x:x[0])

        count = 0
        bus_stops_enum = []
        for item in bus_stops_list:
            count += 1
            bus_stops_enum.append([str(count)+'.&nbsp;'+item[0],item[1]])

        d={ "order_id":order_id,
            'parameters':parameters,
            "stops":bus_stops_enum,
            "action":action,}
        return render(request,'ad_bus_stops/order_page.html',{**param(request, 'order_page'),**d} )
    
    else:
        'anonymous_check'
        return HttpResponseRedirect(reverse('message', args=('anonymous_check',))) 

@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def order_query(request):

    if device(request) == 'mobile':
        return HttpResponseRedirect(reverse('message', args = ('desktop_required',)))

    # 1. Gets explorer
    try:
        explorer_name = app_explorer_username(request)
        if explorer_name != 'anonymous_check':
            explorer = App_Explorer.objects.get(username = explorer_name)
        else:
            explorer = None
    except:
        # db connection error. 
        print('query error 1 in order_query view')
        return HttpResponseRedirect(reverse('message', args = ('connection_error',)))


    # 2. Processing  POST request
    if request.method == "POST" :
        if not explorer:
            return HttpResponseRedirect(reverse('message', args = ('anonymous_check',)))

        orders_to_render = orders_selected(request,explorer) 

        if orders_to_render == 'Wrong post paramerters':
            return HttpResponseRedirect(reverse('message', args = ('w',)))         
        elif orders_to_render == 'connection_error':
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))
        
        current_orders, archived_orders = orders_to_render

        orders_to_template = []
        total = 0
        for order in current_orders:            
            orders_to_template.append((order.id, order))
            total += order.total_sum

        for order in archived_orders:            
            orders_to_template.append((order.initial_order_id, order))
            total += order.total_sum

        orders_to_template.sort(key = lambda x: x[0])

        count = 0
        orders_to_template_enumerated = []
        for item in orders_to_template:
            count += 1
            orders_to_template_enumerated.append(( 
                                            count,
                                            item[0],
                                            item[1].user.username,
                                            item[1].first_booking_date.strftime('%d/%m/%Y'),
                                            item[1].exposition_starts.strftime('%d/%m/%Y'),
                                            item[1].exposition_ends.strftime('%d/%m/%Y'),
                                            item[1].order_status,
                                            item[1].total_sum))

        d={'orders': orders_to_template_enumerated, "total":total }
        return render(request,'ad_bus_stops/orders_selected.html',{**param(request, 'orders_selected'),**d})



    # 3. Gets customer list for rendering
    users = []
    if explorer:
        try:
            users_qu = User.objects.filter(app_explorer = explorer).exclude(status = "agency_staff")
        except:
            # db connection error. 
            print('query error 20 in order_query view') 
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))           
        
        users = ["All", "customer"]
        for user in users_qu:
            users.append(user.username)

    # 4. gets statuses for rendering : list of statuses imported from models.py        
    order_statuses =["All", "all current orders", 'all archived orders']
    for status in current_order_status_choices + archived_order_status_choices:
         order_statuses.append( status[0] )
        
    d={'users':users,"statuses":order_statuses }
    return render(request,'ad_bus_stops/order_query.html',{**param(request, 'order_query'),**d})



def orders_selected(request,explorer):
    '''
    Helper for order_query view
    Gets request.POST parameters and selects orders by the criteria of them 
    '''
    try:
        customer = request.POST['customer_name']
        status = request.POST['status']
        date_created_from = request.POST["date_created_from"]        
        date_created_to = request.POST["date_created_to"]
        exposition_start_from = request.POST["exposition_start_from"]
        exposition_start_to = request.POST["exposition_start_to"]
        exposition_end_from = request.POST["exposition_end_from"]
        exposition_end_to = request.POST["exposition_end_to"]
    except:
        return 'Wrong post paramerters'

    if customer == 'No customers':
        return [],[]
    
    # selects current explorer's orders 
    try:
        orders_qu1 = Current_Order.objects.filter(app_explorer = explorer)
        orders_qu2 = Orders_Archived.objects.filter(app_explorer = explorer)
    except:
        # db connection error. 
        print('query error 1 in orders_selected function')
        return 'connection_error'

    if not orders_qu1 and not orders_qu2:
        return [],[]

    # Selects orders of customers chosen
    if customer != 'All':
        try:
            customer_obj = User.objects.get(username = customer) 
            orders_qu1 = orders_qu1.filter(user = customer_obj)
            orders_qu2 = orders_qu2.filter(user = customer_obj)
        except:
            # db connection error. 
            print('query error 2 in orders_selected function')
            return 'connection_error'
  
    if not orders_qu1 and not orders_qu2:
        return [],[]

    # Filtering by date_created_from
    if date_created_from:
        date_created_from_obj = datetime.strptime(date_created_from, '%Y-%m-%d').date()       
        try:          
            orders_qu1 = orders_qu1.filter(first_booking_date__gte = date_created_from_obj)
            orders_qu2 = orders_qu2.filter(first_booking_date__gte = date_created_from_obj)
        except:
            # db connection error. 
            print('query error 3 in orders_selected function')
            return 'connection_error'
            
    # Filtering by date_created_to
    if date_created_to:
        date_created_to_obj = datetime.strptime(date_created_to, '%Y-%m-%d').date()       
        try:          
            orders_qu1 = orders_qu1.filter(first_booking_date__lte = date_created_to_obj)
            orders_qu2 = orders_qu2.filter(first_booking_date__lte = date_created_to_obj)
        except:
            # db connection error. 
            print('query error 4 in orders_selected function')
            return 'connection_error'    

    # Filtering by exposition_start_from
    if exposition_start_from:
        exposition_start_from_obj = datetime.strptime(exposition_start_from, '%Y-%m-%d').date()       
        try:          
            orders_qu1 = orders_qu1.filter(exposition_starts__gte = exposition_start_from_obj)
            orders_qu2 = orders_qu2.filter(exposition_starts__gte = exposition_start_from_obj)
        except:
            # db connection error. 
            print('query error 5 in orders_selected function')
            return 'connection_error'        
        
    # Filtering by exposition_start_to
    if exposition_start_to:
        exposition_start_to_obj = datetime.strptime(exposition_start_to, '%Y-%m-%d').date()       
        try:          
            orders_qu1 = orders_qu1.filter(exposition_starts__lte = exposition_start_to_obj)
            orders_qu2 = orders_qu2.filter(exposition_starts__lte = exposition_start_to_obj)
        except:
            # db connection error. 
            print('query error 6 in orders_selected function')
            return 'connection_error'        
        

    #  Filtering by exposition_end_from
    if exposition_end_from:
        exposition_end_from_obj = datetime.strptime(exposition_end_from, '%Y-%m-%d').date()       
        try:          
            orders_qu1 = orders_qu1.filter(exposition_ends__gte = exposition_end_from_obj)
            orders_qu2 = orders_qu2.filter(exposition_ends__gte = exposition_end_from_obj)
        except:
            # db connection error. 
            print('query error 7 in orders_selected function')
            return 'connection_error'        
          
    #  Filtering by exposition_end_to
    if exposition_end_to:
        exposition_end_to_obj = datetime.strptime(exposition_end_to, '%Y-%m-%d').date()       
        try:          
            orders_qu1 = orders_qu1.filter(exposition_ends__lte = exposition_end_to_obj)
            orders_qu2 = orders_qu2.filter(exposition_ends__lte = exposition_end_to_obj)
        except:
            # db connection error. 
            print('query error 8 in orders_selected function')
            return 'connection_error'        
        
    #  Filtering by status
    if status != 'All':
        # archive query
        if status in (  'all archived orders',
                        archived_order_status_choices[0][0],
                        archived_order_status_choices[1][0],
                        archived_order_status_choices[2][0]):              
            orders_qu1 = []
            if status != 'all archived orders':
                try:
                   orders_qu2 =  orders_qu2.filter(order_status = status)
                except:
                    # db connection error. 
                    print('query error 9 in orders_selected function')
                    return 'connection_error'   

        #current orders query    
        else:
            orders_qu2 = []   
            if status != "all current orders":
                try:
                   orders_qu1 =  orders_qu1.filter(order_status = status)
                except:
                    # db connection error. 
                    print('query error 10 in orders_selected function')
                    return 'connection_error'    

    return orders_qu1, orders_qu2
    

        
