from ..parameters import *

def bus_stops(request, city, num_page, letters):

    # 1. getting explorer
    
    explorer_name = app_explorer_username(request)
    if  explorer_name == 'anonymous_check' :        
        get_explorer = False
    else:
        try:
            explorer_obj = App_Explorer.objects.get(username = explorer_name)
            get_explorer =True
        except:
            print('error in db App_Explorer data retrieving in bus_stops view')
            get_explorer = False


    # 2. checking if there exists order with status = cart for request.user  & for current explorer
    if  explorer_name == 'anonymous_check'  or  not request.user.is_authenticated : 
        order_opened = False 
    else:
        try:
            order_opened = request.user.current_orders.filter(app_explorer = explorer_obj, 
                                            order_status = "cart").first()                               
        except:
            print('error in order_opened retrieving in bus_stops view')   
            order_opened = False    
    
    #  retrieves quantity of stops in cart  and order id
    if order_opened :
        try:
            order_id = order_opened.id
            quantity_in_cart = len(order_opened.bus_stops_booked.all())
        except:
            print('error in quantity_in_cart/order_id  retrieving in bus_stops view')
            quantity_in_cart = 0
            order_id = 0
    else:
        quantity_in_cart = 0
        order_id = 0  

    open_order_months = get_open_order_months(order_opened)


    # 3. gets city
    try:
        city_obj = City.objects.get(name = city)
    except:
        # direct typing in  to the browser url field some city name
        return HttpResponseRedirect(reverse('message', args = ('city',)))


    # 4. gets  all bus-stops of this city for current explorer 
    
    preset_stops = city_obj.bus_stops.filter(app_explorer__exact = None, record_status = "actual")
    
    # if  not anonymous_check and success while getting explorer object from db 
    if get_explorer:   
        # combines bus-stops entered to db by current explorer   with preset stops 
        stops_qu = chain(preset_stops,
            city_obj.bus_stops.filter(app_explorer = explorer_obj,
            record_status = "actual"))
    else:
        # only preset bus-stops
        stops_qu = preset_stops  


    # 5. filters bus-stops by first letters of street name  - if needed
    if request.method == 'POST':
        try:
            letters_raw = request.POST['letters'].strip()
        except:
            # case of malicious  browser editing
            print('Error in POST parameters in bus_stops view')
            return HttpResponseRedirect(reverse('message', args = ('w',)))
        if letters_raw :
            letters = letters_raw

    if letters != '_':   # if really filtering of streets is being done 
        stops_raw =[]
        for stop in stops_qu:
            if  stop.street.lower().strip().startswith(letters.lower().strip()):
                stops_raw.append(stop)
    else:
        stops_raw = stops_qu   # no street filtering


    # 6. composes source for futher pagination  -  list of lists 
    stops_list =[]
    for stop in stops_raw:
        stops_list.append([stop,1,2,3,4])

    # sorting it  by street names
    stops_list.sort(key = lambda x: x[0].street.lower().strip())

    # appending number of bus-stop into the  output list
    count = 0
    for record in stops_list:
        count += 1
        record.append(count)


    # 7. pagination
    paginator = Paginator(stops_list, PAGINATION)
    num_pages = paginator.num_pages
    stops_id_paginated = ''
    if 0 < num_page <= num_pages:
        page_obj = paginator.get_page(num_page)
        for item in page_obj:
            stops_id_paginated += str(item[0].id)+','
    else:
        # Case of malicious client side editing or wrong typing in to the url browser field
        print(' page with such number does not exist in pagination object')
        return HttpResponseRedirect(reverse('message', args = ('pagination',)))  


    #  Pagination buttons appearance
    if num_pages == 1:
        pagin_appearance = 'transparent'
    else:
        pagin_appearance = ''


    # 8.  Filling the raw paginated rendring list of lists with the additional content    
    for item  in page_obj:
        stop = item[0]
        (vacant_months, occupied_months, in_cart) = vacant_months_cart(stop, request)
        if vacant_months == 'db_connection_error':
            print('Error in db query in bus_stops view')
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        # checking if the stop can be added to the opened order
        if open_order_months & occupied_months:
            cart_addition_opportunity = False
        else:
            cart_addition_opportunity = True  

        if vacant_months:
            vacant_from = vacant_months[0][0]
        else:
            vacant_from =''

        # converting  list to str
        vacant_months_str = ''
        for month in vacant_months:
            vacant_months_str += month[0] + '_'+ str(month[1]) + ',' 


        #   page_obj structure:
        #  info:    item[0] = stop  object
        item[1] = vacant_from
        item[2] = in_cart
        item[3] = vacant_months_str.strip(',')
        item[4] = cart_addition_opportunity
        #  info:  item[5] = count



    d = {'stops':page_obj, 
        "num_pages": num_pages,
        'stops_id_paginated':stops_id_paginated.strip(','),
        'pagin_appearance':pagin_appearance,
        'num_page':num_page,
        'next_page': num_page + 1,
        'prev_page': num_page - 1,
        'letters':letters,
        'quantity_in_cart': quantity_in_cart,
        'order_id':order_id,        
        'city':city} 
    return render(request,'ad_bus_stops/stops.html',{**param(request, 'bus_stops'),**d})
      


