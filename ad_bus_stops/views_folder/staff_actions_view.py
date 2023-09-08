from ..parameters import *
from ..every_day import to_archive


@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def edit_setUp(request):

    if device(request) == 'mobile':
        return HttpResponseRedirect(reverse('message', args = ('desktop_required',)))

    message = ''
    if request.method == "POST" :

        # 1. Gets explorer name
        try:
            explorer_name = app_explorer_username(request)
        except:
            # db connection error. 
            print('query error 1 in edit_setUp view')
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

        # 2. explorer required message
        if  explorer_name ==  'anonymous_check':
            return HttpResponseRedirect(reverse('message', args = ('anonymous_check',))) 


        # 3. gets POST parameters
        try: 
            payment_waiting = int(request.POST['payment_waiting'])
            preparation = int(request.POST['preparation'])
            duration1 = int(request.POST['duration1'])
            duration2 = int(request.POST['duration2'])
            duration3 = int(request.POST['duration3'])
            discount1 = int(request.POST['discount1'])
            discount2 = int(request.POST['discount2'])
            discount3 = int(request.POST['discount3'])
            year      = int(request.POST['year'])
        except:
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        # 4. POST data validation
        if (payment_waiting < 1 or preparation < 1 or duration1 < 2 or duration2 <3 or duration3 <4 or
               duration1 >= duration2 or duration2 >= duration3 or year <2024 or year >2030 or 
               discount1 < 0 or discount1 > 100 or discount2 < 0 or discount2 > 100 or 
               discount3 < 0 or discount3 > 100) :
               message = "Not valid input"
        
        # 5. update db SetUp_Parameters instance
        else:
            try:     
                explorer = App_Explorer.objects.get(username = explorer_name)     
            except:
                return HttpResponseRedirect(reverse('message', args = ('connection_error',)))
 
            try:
                records = SetUp_Parameters.objects.filter(app_explorer = explorer)
            except:
                return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

            if len(records) > 0:
                for record in records:
                    try:
                        record.record_status = 'deprecated'
                        record.save()
                    except:
                        return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

            try:
                SetUp_Parameters.objects.create(staff_member = request.user,
                                                date = explorer.current_date,
                                                app_explorer = explorer,
                                                payment_waiting = payment_waiting,
                                                preparation = preparation,
                                                duration1 = duration1,
                                                duration2 = duration2,
                                                duration3 = duration3,
                                                discount1 = discount1,
                                                discount2 = discount2,
                                                discount3 = discount3,
                                                year =  year)
            except:
                return HttpResponseRedirect(reverse('message', args = ('connection_error',))) 

            return HttpResponseRedirect(reverse('message', args = ('successful update',))) 
              
    d = actual_setUp(request)
    d1 ={'message' : message }
    return render(request,'ad_bus_stops/edit_setUp.html',{**param(request, 'edit_setUp'),**d, **d1} )

@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def cancel_order(request):

    if request.method == "POST":
        # 1. Gets explorer
        try:
            explorer_name = app_explorer_username(request)
            if explorer_name != 'anonymous_check':
                explorer = App_Explorer.objects.get(username = explorer_name)
        except:
            # db connection error. 
            print('query error 1 incanceled for non-payment cancel_order view')
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

        # 2. 'explorer required' message
        if explorer_name == 'anonymous_check':
            return HttpResponseRedirect(reverse('message', args = ('anonymous_check',))) 

        # 3. gets request.POST data    
        try:
            order_id = int(request.POST['order_id'])
        except:
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        # 4. checks the order existence
        try:
            order = Current_Order.objects.get( pk = order_id,  app_explorer = explorer )
        except:
            # db connection error. 
            print('query error 2 in cancel_order view')
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

        # 5. Transfers order to archive
        archived = to_archive(order,explorer,explorer.current_date,'canceled by staff',request.user)

        if not archived or archived == 'not complete':
            print('query error 3 in cancel_order view')
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

        return HttpResponseRedirect(reverse('message', args = ('successful update',)))
    else:
        return HttpResponseRedirect(reverse('message', args = ('a',)))

@login_required(login_url="/login")
@user_passes_test(staff_permission_check, login_url="/a")
def prepare_cancel(request):

    if device(request) == 'mobile':
        return HttpResponseRedirect(reverse('message', args = ('desktop_required',)))

    if request.method == 'POST':
        # 1. Gets explorer name
        try:
            explorer_name = app_explorer_username(request)
        except:
            # db connection error. 
            print('query error 1 in prepare_cancel view')
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

        # 2. explorer required message
        if  explorer_name ==  'anonymous_check':
            return HttpResponseRedirect(reverse('message', args = ('anonymous_check',))) 

        # 3. Gets request data
        try:
            order_id = int(request.POST['order_id'])
        except:
            return HttpResponseRedirect(reverse('message', args = ('w',)))

        # 4. Gets explorer           
        try:        
            explorer = App_Explorer.objects.get(username = explorer_name)  
        except:
            # db connection error. 
            print('query error 2 in prepare_cancel view')
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

        # 5. Checks the order existence
        try:
            order_qu = Current_Order.objects.filter( pk = order_id,  app_explorer = explorer )
        except:
            # db connection error. 
            print('query error 3 in prepare_cancel view')
            return HttpResponseRedirect(reverse('message', args = ('connection_error',)))

        if len(order_qu) == 0:
            return HttpResponseRedirect(reverse('message', args = ('no_order',)))

        return HttpResponseRedirect(reverse('order_page', args = (order_id,'cancel')))
    else:
        return HttpResponseRedirect(reverse('message', args = ('a',)))    


    

    