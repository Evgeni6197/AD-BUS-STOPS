from ..parameters import *

def message(request,x): 

    if x in ('w', 'w_s'):
        message = 'Something went wrong - try again'
    elif x in ('a','a_s'):
        message = 'Access denied'
    elif x == 'anonymous_check':
        message = "To make this action, you'll need an Exploration Account. Just click on the logo and register!"
    elif x== 'city':
        message = "No data for this city"
    elif x== 'pagination':
        message = "Wrong pagination" 
    elif x == 'successful_checkout':
        message  = "Congratulations! Your order has been registered. Payment details have been sent to your email. "
    elif x.startswith('assist'):
        message = f"Server Error {x[-1]}: We apologize for the inconvenience. Kindly inform our staff regarding this matter."
    elif x == 'connection_error': 
        message = "DB Connection Error. Try again"
    elif x == 'no_order': 
        message = "Order not Found" 
    elif x == 'desktop_required':
        message = "This page is not available for mobile phones. Please access it from a desktop" 
    elif x == 'successful update':
        message = "DB successfully updated!"

    else:
        message = "404 Not Found"

    if x in ('w_s','a_s'):
        template_name = 'study_message'               
    else:
        template_name = 'regular_message' 

    d={"message": message }
    return render(request,"ad_bus_stops/message.html",{
        **param(request, template_name),**d})



