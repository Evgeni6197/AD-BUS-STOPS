from ..parameters import *


@login_required(login_url="/login")
def cart(request, city, num_page, letters):

    d1 ={'city':city,'letters':letters,'num_page':num_page}
    reload= {**d1,**{'message':'reload'}}

    # 1 Gets explorer name
    try:
        explorer_name = app_explorer_username(request)
        explorer = App_Explorer.objects.get(username = explorer_name)
    except:
        print('db connection error 1 in cart view')
        return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})

    # 2 Access denied case
    if explorer_name == 'anonymous_check':
        return HttpResponseRedirect(reverse('message', args = ('anonymous_check',)))

    # 3 Specific address cancellation
    if request.method == "POST":
        try:
            reference_id_to_erase = int(request.POST['reference'])
        except:
            return HttpResponseRedirect(reverse('message', args = ('w',)))  

        # Access validation
        validation = False
        reference_to_erase = False
        try:
            reference_to_erase = Reference.objects.filter(pk= reference_id_to_erase).first()
            if reference_to_erase:
                order = reference_to_erase.order            
                if (order.app_explorer.username == explorer_name and
                        order.user.username == request.user.username):
                    validation  = True
        except:
            print('db connection error 0 in cart view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})


        # Case of reloading after server error  - "db connection error 7 " - see print() below
        if not reference_to_erase:
            try:
                order_to_delete = Current_Order.objects.filter(app_explorer = explorer ,
                     user = request.user, order_status = "cart").first()
                if  order_to_delete: 
                    #  case of canceled order by staff while customer is going to cancel address 
                    order_to_delete.delete()
            except:
                print('db connection error 7.1 in cart view')
                return HttpResponseRedirect(reverse('message', args = ('assist1',)))
            return HttpResponseRedirect(reverse('bus_stops', args = (city, num_page, letters,)))   

        # Unauthorized access attempt
        if not validation :
            return HttpResponseRedirect(reverse('message', args = ('a',)))

        # updates  order's total sum
        try:
            sum_decrement = reference_to_erase.booking_price            
            order.total_sum -=  sum_decrement
            order.save()            
        except:
            print('db connection error 6 in cart view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})

        # deletes specific address
        try:    
            reference_to_erase.delete()
        except:
            print('db connection error 6.1 in cart view')

            # order's total sum update cancellation
            try:
                order.total_sum +=  sum_decrement 
                order.save()
            except:
                # prompt:  communicate with staff
                print('db connection error 6.2 in cart view')    
                return HttpResponseRedirect(reverse('message', args = ('assist2',)))
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})
    # 4  Gets db data for later usage
    try:        
        opened_order = request.user.current_orders.filter(app_explorer = explorer, order_status = "cart").first()
        if not opened_order:
            #case of canceling the order by staff member while the customer ig going to checkout
            return HttpResponseRedirect(reverse('message', args = ('no_order',)))
        opened_order_id = opened_order.id
        references = Reference.objects.filter(order = opened_order)
    except:
        print('db connection error 2 in cart view')
        return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})

    # 5. erases empty order - after request.post  the last (or the only) address deletion
    if not references:
        try:
            opened_order.delete()
        except:
            print('db connection error 7 in cart view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})
        return HttpResponseRedirect(reverse('bus_stops', args = (city, num_page, letters,)))
        
    # 6. Gets list of the booked stops  in the cart for the request.user
    stops_booked_obj = []
    for reference in references:
        try:
            stops_booked_obj.append((reference.bus_stop, reference.booking_price, reference.id ))
        except:
            print('db connection error 3 in cart view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})

    stops_booked =[]
    for stop_booked_obj in stops_booked_obj:
        try:
            address = (
            stop_booked_obj[0].city.name + ', ' + 
            stop_booked_obj[0].street +' '+ 
            stop_booked_obj[0]. house)
        except:
            print('db connection error 4 in cart view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})
        
        sum = stop_booked_obj[1]
        reference_id = stop_booked_obj[2]
        stops_booked.append((address, sum, reference_id ))

    stops_booked.sort(key = lambda x: x[0])  

    count = 0
    stops_booked_enumerated = []
    for stop_booked in stops_booked:
        count += 1
        stops_booked_enumerated.append((str(count)+". "+ stop_booked[0], stop_booked[1],stop_booked[2] ))
    
    # 7. Gets exposition parameters, payment deadline and the total sum
    try:
        exposition_starts = opened_order.exposition_starts.strftime("%d/%m/%Y")
        exposition_ends = opened_order.exposition_ends.strftime("%d/%m/%Y")
        deadline = (opened_order.first_booking_date + timedelta(days = 
                        actual_setUp(request)['payment_waiting'])).strftime("%d/%m/%Y")
        total = opened_order.total_sum
    except:
        print('db connection error 5 in cart view')
        return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})



    d2={'stops_booked_enumerated':stops_booked_enumerated,
    'exposition_starts':exposition_starts,
    'exposition_ends':exposition_ends,
    'deadline':deadline,
    'total':total,
    'opened_order_id':opened_order_id,}
    return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**d1,**d2})


@login_required(login_url="/login")
def checkout(request, city, num_page, letters):

    if request.method == "POST":

        d1 ={'city':city,'letters':letters,'num_page':num_page}
        reload= {**d1,**{'message':'reload'}}

        # 1 Gets explorer name
        try:
            explorer_name = app_explorer_username(request)
        except:
            print('db connection error 1 in checkout view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})

        # 2 Access denied case
        if explorer_name == 'anonymous_check':
            return HttpResponseRedirect(reverse('message', args = ('anonymous_check',)))

        #3 Gets POST parameter
        try:
            order_to_checkout_id = int(request.POST['order_to_checkout'])
            deadline = request.POST['deadline']
            total = request.POST['total']
        except:
            print('error in getting post param in checkout view' )
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        # 4. Permission checking
        try:
            order_obj = Current_Order.objects.filter(pk = order_to_checkout_id).first()
            if not order_obj:
                # case of order cancelation by staff while customer is going to checkout
                return HttpResponseRedirect(reverse('message', args = ('no_order',)))
            username = request.user.username
            email = request.user.email
            if (order_obj.app_explorer.username == explorer_name and
                    order_obj.user.username == username and
                    order_obj.order_status == "cart"):
                validation  = True
            else: 
                validation  = False
        except:
            print('db connection error 2  in checkout view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})

        if not validation:
            print('validation failed in checkout view' )
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        # 5. checking if there were no errors  in the  address cancelation  process in the cart view
        # validating the order's total sum against the set of the booked addresses 
        # When this error arises the print('db connection error 6.2 in cart view') is called
        try:
            references = order_obj.bus_stops_booked.all()  
            sum = 0
            for reference in references:
                sum += reference.booking_price

            # Error case in the  address cancelation  process
            if sum != order_obj.total_sum:
                order_obj.delete()
                print('detected Error case in the  address cancelation  process  in checkout view' )
                return HttpResponseRedirect(reverse('message', args = ('w',)))
        except:
            print('db connection error 3  in checkout view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})
       
        # 6. sends congratulatory email
        try:
            send_mail(
                "from AD - BUS - STOPS ",
                message_to_customer(username, order_to_checkout_id, 
                                            deadline, total,'success'),
                AGENCY_EMAIL,
                [f"{email}"],
                fail_silently=False, )
        except:
            print('email sending error1  in checkout view')
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload})

        # 7 changing order status. This action indicates the successful checkout process termination
        try:
            order_obj.order_status = 'payment waiting'
            order_obj.save()
    
        except:
            print('db connection error 3  in checkout view')
            try:
                # sends apologies for misinformation 
                send_mail(
                        "from AD - BUS - STOPS ",
                        message_to_customer(username, order_to_checkout_id,
                                                        deadline, total,'failure'),
                        AGENCY_EMAIL,
                        [f"{email}"],
                        fail_silently=False, )
            except:
                print('email sending error2  in checkout view')
                pass
            return render(request,'ad_bus_stops/cart.html',{**param(request, 'cart'),**reload}) 

        return HttpResponseRedirect(reverse('message', args = ('successful_checkout',)))

    else:
        # Access denied message
        return HttpResponseRedirect(reverse('message', args = ('a',))) 