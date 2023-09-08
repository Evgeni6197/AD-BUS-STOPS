from ..parameters import *

@login_required(login_url="/login")
def book_confirm(request, stop_id, order_id, stops_id_paginated):

    explorer_name = app_explorer_username(request)

    if request.method == 'GET' and explorer_name != 'anonymous_check':

        #1. Getting app data for further usage                
        try:
            stop_obj = Bus_Stop.objects.get(pk = stop_id)
            actual_price = stop_obj.price
        except:
            print("Error in getting explorer obj  in book_confirm view")             
            return JsonResponse({'db_successful_connections':False})


        # 2. Access denied case
        
        # bus-stop should be preset or created by the current explorer
        try:
            if not  (stop_obj.app_explorer  is None  or stop_obj.app_explorer.username == explorer_name) : 
                print ('access denied in book_confirm view')
                return JsonResponse({'db_successful_connections':False})
        except:
            print("Access permission checking error  in book_confirm view")            
            return JsonResponse({'db_successful_connections':False})

        # 3. Checking if the bus-stop is inside the order - for the order opened before
        if order_id:
            try:
                order_obj = Current_Order.objects.get(pk = order_id)
                order_status = order_obj.order_status
                this_order_references = Reference.objects.filter(order = order_id)
                reference = this_order_references.filter(bus_stop = stop_id).first()
            except:
                print("Error in getting reference obj  in book_confirm view")            
                return JsonResponse({'db_successful_connections':False})

            # it is
            if reference:
                if order_status == "cart":
                    quantity_in_cart = len(this_order_references)
                else:
                    print("opened order is not in the cart status  in book_confirm view 1")             
                    return JsonResponse({'db_successful_connections':False})

                return JsonResponse({
                    'db_successful_connections':True,
                    'successful_cart_addition': True,
                    'quantity_in_cart':quantity_in_cart
                    })
            # cart addition faluire
            else:
                occupied_months = vacant_months_cart(stop_obj, request)[1]
                if occupied_months =='db_connection_error':
                    print('Error in db query1 in book_confirm view')
                    return JsonResponse({'db_successful_connections':False})

                open_order_months = get_open_order_months(order_obj)

                 # checking if the stop was not  added to the opened order due to intersection
                if open_order_months & occupied_months:
                    cart_addition_opportunity = False
                else:
                    cart_addition_opportunity = True
                
                return JsonResponse({
                    'db_successful_connections':True,
                    'successful_cart_addition': False,
                    'cart_addition_opportunity':cart_addition_opportunity,
                    'actual_price':actual_price,
                    })

        # 4. Brand new order            
        else:

            # checking the new order creation
            try:
                references = Reference.objects.filter(bus_stop = stop_obj)
                order_created = False
                for reference in references:
                    order = reference.order
                    if (    order.app_explorer.username == explorer_name and                       
                            order.user.username == request.user.username and 
                            order.order_status == "cart"
                        ):
                        order_created = True
                        order_id = order.id
                        new_order = order

                        # direct db extraction the quantity  in cart  for the new order            
                        quantity_in_cart = len(new_order.bus_stops_booked.all())

                        break                    
            except:
                print('Error in db query3 in book_confirm view')
                return JsonResponse({'db_successful_connections':False})              


            # success : composing
            #   1) str including id of stops where  the Book btn will be replaced with the  Info btn
            #   2) str including updated vacant_from  parameter for all paginated stops
            if order_created:

                new_order_months = get_open_order_months(new_order)
                stops_id_paginated_list = stops_id_paginated.split(',')
                where_to_place_info_btn = ''

                updated_paginated_VacantFrom_all = ''
                for item  in stops_id_paginated_list:
                    
                    # check for all paginated stops but the current stop
                    if int(item) != stop_id:

                        try:
                            stop_pagin_obj = Bus_Stop.objects.get(pk = int(item))
                        except:
                            print('Error in db query4 in book_confirm view')
                            return JsonResponse({'db_successful_connections':False})

                        (paginated_vacant_months, paginated_occupied_months,
                            temp) = vacant_months_cart(stop_pagin_obj, request)

                        if paginated_vacant_months:
                            paginated_vacant_from = paginated_vacant_months[0][0]
                        else:
                            paginated_vacant_from = ''
                        
                        updated_paginated_VacantFrom_all += paginated_vacant_from + '_' + str(item) + ','

                        # checking if the stop can be added to the new order
                        if new_order_months & paginated_occupied_months:
                            where_to_place_info_btn += item + ','

                return JsonResponse({
                    'db_successful_connections':True,
                    "order_created":order_created,
                    "order_id":order_id, 
                    'where_to_place_info_btn':where_to_place_info_btn.strip(','),
                    'updated_paginated_VacantFrom_all': updated_paginated_VacantFrom_all.strip(','),
                    'quantity_in_cart':quantity_in_cart
                    })

            # booking failure case
            else:
                # update vacant months
                vacant_months = vacant_months_cart(stop_obj, request)[0] 
                if vacant_months:
                    vacant_from = vacant_months[0][0]
                else:
                    vacant_from =''
                
                # converting  list to str
                vacant_months_str = ''
                for month in vacant_months:
                    vacant_months_str += month[0] + '_'+ str(month[1]) + ',' 

                return JsonResponse({
                    'db_successful_connections':True,
                    "order_created":order_created,
                    'actual_price':actual_price,
                    'vacant_from': vacant_from,
                    'vacant_months': vacant_months_str.strip(',')
                    })
    else:
        return HttpResponse(status=204)