from ..parameters import *

@login_required(login_url="/login")
def account(request):

    # 1. gets explorer name
    try:
        explorer_name = app_explorer_username(request)
    except:
        print('db connection error 1 in account view')
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))

    #2. explorer required message
    if explorer_name == 'anonymous_check':
        return HttpResponseRedirect(reverse('message', args = ('anonymous_check',)))

    # 3. gets explorer    
    try:
        explorer = App_Explorer.objects.get(username = explorer_name)
    except:
        print('db connection error 2 in account view')
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))

    # 4. Gets orders
    try:
        current_ords_qu = Current_Order.objects.filter(app_explorer  = explorer, user = request.user)
        archived_ords_qu = Orders_Archived.objects.filter(app_explorer  = explorer, user = request.user)
    except:
        print('db connection error 3 in account view')
        return HttpResponseRedirect(reverse('message', args=('connection_error',)))

    current_ords =[]
    for order in current_ords_qu:
        current_ords.append((order.id, 
                            order.exposition_starts.strftime('%d/%m/%Y'),
                            order.exposition_ends.strftime('%d/%m/%Y'),
                            order.total_sum))
    archived_ords =[]
    for order in archived_ords_qu:
        archived_ords.append((order.initial_order_id, 
                            order.exposition_starts.strftime('%d/%m/%Y'),
                            order.exposition_ends.strftime('%d/%m/%Y'),
                            order.total_sum))
    current_ords.sort(key = lambda x: x[0])
    archived_ords.sort(key = lambda x: x[0])
    
    if not current_ords and not archived_ords:
        no_orders = True
    else:
        no_orders = False


    d = {"customer_name":request.user.username,
        'customer_email':request.user.email,
        'current_ords':current_ords,
        'archived_ords':archived_ords,
        'no_orders':no_orders}
    return render(request,'ad_bus_stops/account.html',{**param(request, 'account'),**d})
