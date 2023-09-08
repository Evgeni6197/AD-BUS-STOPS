
from ..parameters import *
from ..data.index_text  import *
from ..every_day import *


def index(request):

    explorer_update(request) 
    every_day_orders_update(request)

    # composing text_list parameter to pass to template
    # this structure serves to implement animation effect 
    text_list =[]
    words= [heading_text.split(' '), main_text.split(' ')]      
    count = 0
    for i in (0,1):
        temp = []
        for word in words[i]:
            letters =[]
            for letter in word:
                letters.append((count,letter))
                count += 1
            temp.append(letters)
        text_list.append(temp)
        if device(request) == 'mobile':
            break

    # retrieving cities from db - preset ones  and alse cities set by current explorer
    personal_cities = False 
    city_list =[]  
    explorer_name = app_explorer_username(request)
    if explorer_name != 'anonymous_check':
        try:
            personal_cities = App_Explorer.objects.get(username = 
                        explorer_name).cities_recorded.all()
        except:
            # db connection faluire
            pass
    try:
        cities = City.objects.filter(app_explorer__exact = None)  # preset cities
    except:
        # db connection faluire
        cities = []

    if personal_cities:
        cities = chain(cities, personal_cities)    
    for city in cities:
        city_list.append(city.name)
    city_list.sort()

    d = {'text_list':text_list,
        'count':count,
        'cities':city_list}
    return render(request,'ad_bus_stops/index.html',{**param(request, 'index'),**d})

def guidance(request):

    actual_setUp_d = actual_setUp(request)           
    d =  {"minimum_time_till_pub":(actual_setUp_d['payment_waiting']+actual_setUp_d['preparation'])}     
    return render(request,'ad_bus_stops/guidance.html',{
        **param(request, 'guidance'),**d,**actual_setUp_d }) 

