from ..parameters import *


@csrf_exempt
@login_required(login_url="/login")
def book(request):

    explorer_name = app_explorer_username(request)

    if request.method == "PUT" and explorer_name != 'anonymous_check':
        
        # 0. Getting app data for further usage                
        try:
            explorer_obj = App_Explorer.objects.get(username = explorer_name)
        except:
            print("Error in getting explorer obj  in book view")
            return HttpResponse(status=204)
        actual_setUp_d = actual_setUp(request)

        # 1. Getting customer's booking data
        data = json.loads(request.body)
        try:
            stop_id = data['stop_id']
            months_to_book = data['months_to_book'].strip(',').split(',')

            # price that was actual at the moment of customer's  booking submit
            price =  int(data['price'])

            # ID of the  opened order of the request.user for the current explorer  with "cart" status
            # zero  if the order does not exist 
            order_id = int(data['order_id'])            
        except:
            # case of malicious client side edition
            print("Error while fetch  in book view")
            return HttpResponse(status=204) 


        # 1.1 Checks redundancy (it is admitted not more than one order with cart status for a given user)
        try:
            redundant_query = Current_Order.objects.filter(user = request.user,
                                    app_explorer = explorer_obj, order_status = "cart" )
        except:
            print("Error in redundancy checking  in book view")
            return HttpResponse(status=204)

        
        if order_id and len(redundant_query)==1:
            redundancy_validation = True
        elif  order_id == len(redundant_query) == 0:
            redundancy_validation = True
        else:
            redundancy_validation = False

        if not redundancy_validation:
            print("Invalid redundancy  in book view")
            return HttpResponse(status=204)
            
    
        # 2 and 3 paragraphs : for brand new order
        if not order_id:

            # 2. Checking month consecutiveness  
            months_to_book_obj =[]  #list of date objects
            booking_valid = True
            count =  0        
            for month in months_to_book:
                month_obj = date(int(month.split('/')[1]), int(month.split('/')[0]), 1)
                months_to_book_obj.append(month_obj)
                if count == 0:
                    tmp = month_obj
                else:
                    if not(timedelta(days = 27) < month_obj - tmp < timedelta(days = 32)):
                        print("Not consecutive months  in book view")
                        return HttpResponse(status=204)
                    else:                    
                        tmp = month_obj           
                count += 1

            # 3. Checking booking start date validity 
            booking_start_date = months_to_book_obj[0]
            today_obj = current_today_obj(explorer_obj, explorer_name) 

            minimum_time_till_pub = actual_setUp_d['payment_waiting'] + actual_setUp_d['preparation']    
            if  booking_start_date - today_obj < timedelta(days=minimum_time_till_pub):
                print("Too early booking  start date  in book view")
                return HttpResponse(status=204)


        # 4. Getting list of the  exposition months for  the opened order 
        if order_id:
            try:
                opened_order_obj = Current_Order.objects.get(pk =order_id )
                exp_start_opened_order = opened_order_obj.exposition_starts 
                exp_end_opened_order = opened_order_obj.exposition_ends 
            except:
                print("Error while retrieving opened order parameters  in book view")
                return HttpResponse(status=204)

            opened_order_months_obj =[]
            temp = exp_start_opened_order
            while (temp < exp_end_opened_order):
                opened_order_months_obj.append(temp)
                temp += timedelta(days = 32)
                temp = date(temp.year,temp.month,1)

            months_to_book = []
            for month_obj in opened_order_months_obj:
                months_to_book.append(str(month_obj.month).zfill(2)+'/'+str(month_obj.year))

        # 5. Creating booking preemptions - for every month separately
        preemption_records = []
        preemption = True
        for month in months_to_book:
            record =  stop_id + "-" + month + "-" + explorer_name           
            try:
                Preemption.objects.create(
                    user = request.user, 
                    stopId_month_year_explorer = record,
                    app_explorer = explorer_obj
                    )
                preemption_records.append(record)
            except:
                # Faluire :  Uniqueness requirement violated or db connection failure
                preemption = False
                break

        if not preemption:
            delete_preemptions(preemption_records)
            return HttpResponse(status=204)


        # 6. Intersection Checking:  the booking period should not intersect with the already occupied period in other orders
        
        try:
            bus_stop_obj = Bus_Stop.objects.get(pk = int(stop_id))
        except:
            #db connection failure
            print("Error in getting bus-stop obj  in book view")
            return HttpResponse(status=204)
                   
        try:  
            references = bus_stop_obj.current_orders.all()
            
            # all already existing orders with this bus-stop
            existing_orders = []
            for reference in references:
                existing_orders.append(reference.order)

            #  all already existing orders with this bus-stop for current explorer   
            existing_orders_current_explorer =[]
            for existing_order in existing_orders:
                if existing_order.app_explorer.username == explorer_name:
                    existing_orders_current_explorer.append(existing_order)

            # all  already occupied month  for this bus-stop for current explorer 
            occupied_months = set()
            for ord in existing_orders_current_explorer:
                exposition_start = ord.exposition_starts
                exposition_end = ord.exposition_ends
                tmp = exposition_start
                while (tmp < exposition_end ):
                    occupied_months.add(tmp)
                    tmp +=  timedelta(days = 31)
                    tmp  = date(tmp.year,tmp.month,1)

            if order_id:
                months_to_book_obj = opened_order_months_obj       
        
            months_to_book_set = set(months_to_book_obj)
            booking_input_valid = True
            if  occupied_months & months_to_book_set:
                booking_input_valid = False
                print("Intersection   in book view")
           
        except:
            print('error in bus-stop occupation checking in book view ')
            booking_input_valid = False

        if not booking_input_valid:
            delete_preemptions(preemption_records)  
            return HttpResponse(status=204)

        # 7. Checking that the booking price corresponds to the current db price
        if bus_stop_obj.price != price:
            print('invalid price transferred  into  book view')
            delete_preemptions(preemption_records) 
            return HttpResponse(status=204)

        # 8. Calculates the summary price for the bus-stop
        months_quantity = len(months_to_book_obj)
        if months_quantity < actual_setUp_d['duration1']:
            discount = 0
        elif actual_setUp_d['duration1'] <= months_quantity < actual_setUp_d['duration2']:
            discount = actual_setUp_d['discount1']
        elif actual_setUp_d['duration2'] <= months_quantity < actual_setUp_d['duration3']:
            discount = actual_setUp_d['discount2']
        elif actual_setUp_d['duration3'] <= months_quantity :
            discount = actual_setUp_d['discount3'] 

        summary_price =( price * months_quantity *(1 - discount/100 ))//1
        

        # 9. Adds bus-stop to the opened order 
        if  order_id:
            try:
                reference_obj = Reference(  order = opened_order_obj, 
                                            bus_stop = bus_stop_obj,
                                            booking_price = summary_price )
                reference_obj.save()
                opened_order_obj.total_sum += summary_price
                opened_order_obj.save()
            except:
                return HttpResponse(status=204)

        # 10. Creates a brand new order
        else:
            start = months_to_book_obj[0]

            tmp = months_to_book_obj[-1] + timedelta(days = 32) 
            end = date(tmp.year, tmp.month, 1) - timedelta(days = 1) 

            try:
                new_order = Current_Order(
                    user = request.user,
                    first_booking_date = today_obj,
                    exposition_starts = start,
                    exposition_ends = end,
                    app_explorer = explorer_obj,
                )
                new_order.save()
                reference_obj = Reference(  order = new_order, 
                                            bus_stop = bus_stop_obj,
                                            booking_price = summary_price )
                reference_obj.save()
                new_order.total_sum += summary_price
                new_order.save()

            except:
                print('error in new order creation  in  book view')
                return HttpResponse(status=204)

        # 11.  Successful termination        
        delete_preemptions(preemption_records)   
        return HttpResponse(status=204)

    else:
        return HttpResponse(status=204)