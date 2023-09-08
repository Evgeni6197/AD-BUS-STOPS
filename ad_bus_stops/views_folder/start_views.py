from ..parameters import *

def viewport(request):
    '''
    renders helper template, that checks viewport dimensions and makes redirection
    to start view with parameters of client side viewport
    '''

    return render(request,'ad_bus_stops/start/viewport.html')


def start(request):

    if request.method == 'POST':

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_mobile = 'Mobile' in user_agent or 'Android' in user_agent
        try:
            width = round(float(request.POST['width']))  # viewport width in px
            height = round(float(request.POST['height']))  # viewport height in px
        except:
            #case of malicious client side editing
            print ('error in POST data in start view')
            return HttpResponseRedirect(reverse('message', args =('w',)))

        # landscape orientation of client side viewport
        if width > height:

            # mobile landscape
            if is_mobile or MOBILE: #real mobile on client side or testing mobile layout
                return render(request, 'ad_bus_stops/start/start_mobile.html',{
                    'container_numbers_additional':CONTAINER_NUMBERS[1:5],
                    'data_device':'mobile_landscape',
                    'insertion1':'empty',
                    'insertion2': ' height_100',
                    'insertion3': 'height_100 ',
                })


            # width of container for one image in template in  'wide lanscape' case 
            # that is then three images occupy all viewport width and below images
            # there  is space for hello message not less then START_MESSAGE_CONTAINER_HEIGHT
            width_1_photo = (VIEWPORT_WIDTH_PERCENTAGE*width - PADDING_3_PHOTO *2)/3 

            # wide landscape case
            if (width_1_photo *IMAGE_RATIO < height*VIEWPORT_HEIGHT_PERCENTAGE - START_MESSAGE_CONTAINER_HEIGHT):
                
                # width of container for three images together
                width_3_photo = 'width:100%'
            
            # narrow landscape case:  
            else:

                # reverse calculation of   allowable width_1_photo value 
                width_1_photo = (height*VIEWPORT_HEIGHT_PERCENTAGE
                                - START_MESSAGE_CONTAINER_HEIGHT)/IMAGE_RATIO

                # calculation of allowable width_3_photo value in px
                width_3_photo_numeric = int(width_1_photo *3 + PADDING_3_PHOTO *2)

                # width_3_photo in form appropriate for css
                width_3_photo = 'width:'+str(width_3_photo_numeric)+'px'
            
            return render(request,'ad_bus_stops/start/start_landscape.html',{
                'width_3_photo':width_3_photo,
                'container_numbers_initial':CONTAINER_NUMBERS[:3],
                'container_numbers_additional':CONTAINER_NUMBERS[3:5],
            })
        else: 

            # mobile portrait
            if is_mobile or MOBILE: #real mobile on client side or testing mobile layout
                return render(request, 'ad_bus_stops/start/start_mobile.html',{
                    'container_numbers_additional':CONTAINER_NUMBERS[1:5],
                    'data_device':'mobile_portrait',
                    'insertion1':'general_container_mobile',
                    'insertion2':' height_80',
                    #'insertion3': 'empty',
                    'insertion3': 'width_100 '
                    })

            # narrow portrait            
            if 2*IMAGE_RATIO*(width*VIEWPORT_WIDTH_PERCENTAGE
            - PADDING_2_PHOTO*2)/2  < (height*VIEWPORT_HEIGHT_PERCENTAGE 
            - START_MESSAGE_CONTAINER_HEIGHT ):  
                return render(request,'ad_bus_stops/start/start_portrait_narrow.html',{
                    'container_numbers_initial_top':CONTAINER_NUMBERS[:2],
                    'container_numbers_initial_bottom':CONTAINER_NUMBERS[2:4],
                    'container_numbers_additional':CONTAINER_NUMBERS[4:],                    
                }) 

            # wide portrait
            else:
                return render(request,'ad_bus_stops/start/start_portrait_wide.html',{
                    'container_numbers_initial':CONTAINER_NUMBERS[:2],
                    'container_numbers_additional':CONTAINER_NUMBERS[2:5],
                }) 
    else:
        return HttpResponseRedirect(reverse('message', args =('x',)))