# AD-BUS-STOP

 ### 1.  [Video Demonstration ](https://youtu.be/86AK-NFmDu4 )

 ### 2. Distinctiveness and Complexity

   - It is a complete business project that could be used in real life. The essence of the project  
    is to present properly a commercial proposal  B2B. There are two parts elaborated:
     - A product itself:
       - a website for customers of an advertising agency selling ad space on bus stops
       - a business tool for agency staff to track the inner workflow
     - A way of presentation: a special environment for product examination by a representative
        of an agency 
   - The project incorporates the email correspondence between the agency and its customers
  - The project [is hosted on HEROKU](https://ad-bus-stops-677421a1e6cb.herokuapp.com)      
    - To make the project familiarization straightforward, the version committed here explicitly  
      contains SECRET_KEY and EMAIL_HOST_PASSWORD in settings.py, while in the Heroku version, 
      these parameters are assigned to the environmental variables and are not accessible publicly
    - The EMAIL_HOST_USER  parameter also differs in the Heroku version.
    - The minimal Heroku tariff used now sometimes leads to
       a lack of resources (db connections) and  *Server&nbsp;Error* message. Just refresh the page 
  - The front page and the index page are decorated by animation that not only serves as an ornament  
    but also introduces a business context. 
  - The project appearance depends on the user device type: it differs for phones, tablets,   
    and desktops to achieve the most appropriate user experience and clarity

   
### 3. Launching

   The procedure described below presumes that you are using Bash. 
   Inside an empty folder, run: 
   
   ```
   git clone https://github.com/Evgeni6197/AD-BUS-STOPS.git
   cd AD-BUS-STOPS
   python -m venv ./venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```
   For correct project functioning,  the superuser  username  should be `director`
   The superuser password and email are up to you.
   ```
   python manage.py createsuperuser
   python manage.py runserver
   ```
### 4. Business models. Detailed description.

   - **Product presentation**
     - Preview: a straightforward way to start agency website browsing with limited familiarization opportunities. 
     - Detailed exploration offers an opportunity for an agency representative:
        - to introduce his own dummy agency customers
        - place advertisements on their behalf 
        - tune the current date and track the inner agency actions developing over time.
      -  Detailed exploration is realized by:  
         - the preset demo bus stops db
         - Explorer Account:  
           To provide independent  product exploration with the same db by multiple individuals
           simultaneously,  every one of them is provided with a separate environment, 
            a.k.a. Explorer Account. Such an environment effectively isolates one from another.
           Explorer Accounts are automatically cleared from the database, along with all
            associated dummy customers and activities, after 10 days

   - **Product itself: Website for agency customers**
      - Without registration, a customer can get familiarized with the list of available bus stops, prices,
         discount policy, the main agency booking rules
       - Customer registration includes email and password validation. Additionally, it involves sending
         the authentication code to the customer's email, with a 180-second time limit for confirmation.
       - Booking bus stop address (registered customers):
            - To overcome race conditions vulnerability and prevent conflicting bookings,  the `Preemption Model`
              is introduced. The first action that is fulfilled while trying to book an address is the creation
               of a record composed of bus stop ID, ad exposition period and Explorer ID. The model field for
               this record has  `unique=True` attribute, so the db automatically rejects duplicates, effectively
               preventing conflicting bookings.         
            - On booking the first address, a customer chooses an ad exposition period. The booking
               automatically  opens a cart (creates a `Current_Order` model instance with `order_status` = `cart`) 
               with the period specified. Subsequent bookings of this customer can be added only
                to this particular cart. To choose another period, the customer should check out
                 the order associated with this cart (`order_status` is changed to `payment waiting`).
            - Cancelation:
              - a customer can remove an address from the cart
              - an order after checking out if not paid in time is automatically transferred to the archive   
                (the instance of `Current_Order` is deleted, and it is created an instance
                 of `Orders_Archived` model with `order_status` = `canceled for non-payment`)
              - to cancel a paid order, a customer should communicate with the agency staff 
        - Payment: After checking out the order, the customer should pay offline. The payment details and deadline
          is automatically  sent to him by email. 
        -  A customer can examine the complete list of his current and archived orders on  *"Your account"* page. 

  -  **Product itself: Tool for agency staff members**
     - Access levels:
        - Superuser. Username : `director`. Is created by the agency chief manager. The Superuser  makes
          the following actions by means of the django  admin interface:
          -  assigns `agency_staff` to the `status` field in the `User model`
          -  adds new addresses: creates `City`  and   `Bus_Stop` instances
          -  carries out audit: examines `payment_recorded_by`, `exposition_de_facto_recorded_by` 
            and similar fields, recording the history of staff operations
              in `Current_Order`, `Orders_Archived`,   `SetUp_Parameters`  to find out  which staff member
              made a mistake.  Such field have the attribute `on_delete = models.SET_NULL`. That prevents the
             deletion of the Order  instance in case of firing a staff member and deleting his user account.
        - Agency staff: 
          - there is one preset staff user with credentials available on the introductory page.
            This dummy staff user can be used by an agency representative to examine the app's staff member part.
          - on the real-life business stage, the staff user access is granted by the Superuser.
     - Dashboard. The order life cycle tracking (*with human participation*):
          - the orders with `payment waiting` status:<br>
             A staff member verifies the offline payment reception. The `Current_Order` instance  status
              is changed to `Paid. Exposition awaiting` . The current date and the staff
            user are recorded in the corresponding  `Current_Order` instance fields as a part
            of the staff operation history. An informative
            payment reception letter is automatically sent to the customer's email
          - the orders with `current exposition de jure` status (more on that status later):<br>
             A staff  member verifies the actual ad placement. This and the following action require
             human involvement
             to  confirm the actual fulfillment of the job made offline.  The `current_exposition_de_facto`
              field in the `Current_Order` instance is set to `yes`. The current date
               and the staff user are recorded in the corresponding `Current_Order` instance fields.
            An informative ad placement letter is automatically sent to the customer's email
          - the orders with `end of exposition de jure` status (more on that status later): <br> A staff
             member verifies the actual ad removal.  The `current_exposition_de_facto` field in the  
            `Current_Order` instance is set to `finished`. The current date
               and the staff user are recorded in the corresponding `Current_Order` instance fields.
             An informative successful order fulfillment
             letter is automatically sent to the customer's email

     - Additional staff member activities:
          - Order Analytics: <br> Selection of a set of orders by parameters with Total Sum to evaluate
            the agency performance.
          - Edit Business Settings:  <br> Changing business parameters like discounts and others. A new
             `SetUp_Parameters` instance with the status `actual` is created. The current date
             and the staff user are recorded in the corresponding fields of the  instance.  The status of
             the previous instance  is set to `deprecated`. The policy to store in db all previous
             business settings instead of deletion them may be useful for the consequent agency
             performance evaluation.
          - Cancel an Order:  <br> Deletion the `Current_Order` instance and creation an instance of
            the `Orders_Archived` model with `order_status` = `canceled by staff`. The current date
               and the staff user are recorded in the corresponding instance fields.

   -  **Product itself: Automatic part of the order life cycle tracking**
      - Periodicity:<br>
       The environment's current date can be changed by the agency representative up to his choice.
       The automatic tracking of the order's life cycle is carried out once a day according to
        the environment's "internal watch".
       The `Simulated_World_Update` model is introduced to keep track of the latest date inside
        the environment when the orders' status was updated.
      - Payment waiting expiration:  <br> A `Current_Order` instance not paid in time is deleted and
         a `Orders_Archived` instance is created with the status `canceled for non-payment`
      - Time to place ad: <br> The `order_status` of a `Current_Order` instance  is set
        to `current exposition de jure`  
      - Time  to remove ad:  <br> The `order_status` of a `Current_Order` instance
         is set to `end of exposition de jure`
      - Successful fulfillment:  <br> A `Current_Order` instance with
        the `current_exposition_de_facto` = `finished` is deleted and a `Orders_Archived` instance
         is created with the status `successfully completed`

### 5. Folders and files inside *ad_bus_stops* folder
*file locations:*<br>
   <i> *.html &nbsp;&nbsp;&nbsp;&nbsp;  inside &nbsp;&nbsp;&nbsp;&nbsp;  templates/ad_bus_stops </i><br>
   <i> *.js &nbsp;&nbsp;and&nbsp;&nbsp; *.css &nbsp;&nbsp;&nbsp;&nbsp;  inside &nbsp;&nbsp;&nbsp;&nbsp;
   static/ad_bus_stops  </i>

- **General considerations**
  - The project uses <i> try - except block </i> in all the db connection cases to mitigate connection error
     consequences. While an exception  occurs the flow sometimes is transferred to a <i> retry message </i>, sometimes
    the exception is ignored and the regular flow continues, or  the default values are used.
   - The <i> try - except block </i> in all the  <i>request.POST</i> data retrieving cases is used to overcome possible
      malicious client-side actions

- **Front page &nbsp;&nbsp;&nbsp;&nbsp;   views_folder/start_views.py**
  - `viewport` view and <i>start/viewport.html</i>: <br> getting viewport parameters
  - `start` view &nbsp;&nbsp;&nbsp;&nbsp;  and &nbsp;&nbsp; &nbsp;&nbsp;  <i> start&#47;&#42;.html </i>
      &nbsp;&nbsp; &nbsp;&nbsp; with  &nbsp;&nbsp; &nbsp;&nbsp; <i>js_start&#47;&#42;.js </i> :     
    rendering 5 types of front page appearances:
      - desktop  and tablet landscape: <i> *landscape.html</i>
      - tablet wide portrait:  <i> *wide.html</i>
      - tablet narrow portrait: <i> *narrow.html</i>
      - phone landscape: <i>*mobile.html </i>
      - phone portrait: <i>*mobile.html </i>

- **layout.html   &nbsp;&nbsp; &nbsp;&nbsp; and  &nbsp;&nbsp; &nbsp;&nbsp; layout.js**
    - present the logo and heading for all project pages
    - the appearance differs for phone portrait, phone landscape and desktop

- **Helper &nbsp;&nbsp;&nbsp;&nbsp; ad_bus_stops/parameters.py &nbsp;&nbsp;&nbsp;&nbsp; file**
    - is called from every view to define appearance parameters for <i>layout.html </i>
    - contains all the project's constants
    - presets the demo customer and staff users and the demo bus stops db. The data is
      retrieved from <i> data&#47;&#42;.csv </i> &nbsp;&nbsp; files
    - contains the majority of other helper functions

 - **Introductory page, Explorer Account, Change Current Date page: &nbsp;&nbsp; views_folder/app_explorer_view.py**
    - `app_explorer` view renders introductory <i>app_explorer.html</i>    
    - the Explorer Account paradigm is  implemented by:
        - `App_Explorer` model
        - the  `request.session`   dictionary entry  with key = `app_explorer_username`
    - `register_app_explorer` view:
      - renders <i> authentication/register_app_explorer.html </i>
      - validates `request.POST` data
      - creates a new `App_Explorer` model instance
      - creates a `request.session` entry . This action is identical to the  Explorer Account entering.
    - `enter_app_explorer` view :
      - renders <i> authentication/enter_app_explorer.html </i>
      - enter the Explorer Account similar to `register_app_explorer` view
    - `change_current_date` view: <br>
      renders a form  <i>change_current_date.html</i> to tune current date inside the environment and
       handles the `request.POST` data
    - `hide_study_message` view:
      handles the user command  <i>Don't show this message again </i>, which appears on the top when
      a new Explorer Account is registered or a new <i>Preview</i> mode is launched.

- **Index page, How to book link: &nbsp;&nbsp; views_folder/index_view.py**
     - `index` view:
        - runs <i>explorer_update</i> function ( <i>every_day.py</i>): <br>
          updates `App_Explorer` instances once a day
            - keeps track of the periodicity of update with `Last_Explorer_Update` model
            - deletes expired `App_Explorer` instances
            - maintains `current_date` field of `App_Explorer` instances up-to-date if deprecated
        - runs <i>every_day_orders_update</i> function ( <i>every_day.py</i>):<br> 
          carries out operations described in the *Automatic part of the order life cycle tracking* section above.
        - composes with the data from <i>data/index_text.py </i>  a parameter for animation on index page
        - renders <i>index.html</i>
        -  <i>  index.js </i>  provides animation and different appearance for :
            - phone portrait
            - phone landscape
            - desktop
  - `guidance` view:
          - retrieves actual business  settings by running *actual_setUp* function (*parameters.py*)
          - renders <i>guidance.html</i>

- **Customer Registration, Login, Log Out: &nbsp;&nbsp; views_folder/authentication_views.py**
  -  `register` view:
     - runs *delete_not_confirmed_user* function (*parameters.py*): clears previous registration
     - renders registration form <i>authentication/register.html</i>
     - validates `request.POST` data
     - creates `User_Registration_Timestamp` instance: launches registration timer
     - sends confirmation code email
  - `confirmation` view:<br> validates confirmation  `request.POST` data
  - *register.js*  &nbsp;&nbsp;and&nbsp;&nbsp; *confirmation.js*: <br>
    run  spinner and reverse counting
  - `login_view` : just regular Log In
  - `logout_view` : transfers   through Log Out:
      - `request.session['app_explorer_username']`  -  current Explorer Account  
      - `request.session['show_anonymous_message']` - parameter managing the Explorer Account informative
         message appearance on the page top

- **Bus Stop List and Booking: &nbsp;&nbsp; views_folder/stops_view.py, &nbsp;&nbsp; views_folder/book_view.py,    &nbsp;&nbsp; views_folder/book_confirm_view.py**
    - `bus_stops` view:
      - composes the bus stop list for rendering
      - realizes pagination
      - handles street filtering `request.POST` data
      - renders *stops.html*
      - *stops.js*   provides different appearance for :
          - phone portrait
          - phone landscape
          - desktop
      - *booking.js*  fetch:
        - `request.PUT` to `book` view to make booking
        - `request.GET` from  `book_confirm` view to get new bus stop parameters after booking
    - `book` view:
      - server side validation of the data fetched
      - creates `Preemption` instances 
      - calculates the total considering discounts 
      - creates `Reference` model instance. This action is identical to the  insertion of the bus stop to the order.
    - `book_confirm` view:
      - validates the view input parameters
      - composes parameters for the new *stops.html* appearance
      
 - **Cart and checking out the order: &nbsp;&nbsp; views_folder/cart_view.py**
    - `cart` view:
      - cancels a specific address:
        - validates `request.POST` data
        - handles the db connection error cases
      - renders *cart.html*
      - *cart.js* :<br> dynamically disables the form submit buttons to prevent the duplicate submissions
    - `checkout` view:
      - validates `request.POST` data
      - validates the address cancelation in `cart` view
      - sends a letter to the customer email
      - changes the order status
        
- **Staff member part: Dashboard  &nbsp;&nbsp; views_folder/dashboard_view.py**
    - `@user_passes_test`  decorator :<br>
    validates the `agency_staff` status of the `request.user` 
    - `dashboard` view: 
      - retrieves db data and renders *dashboard.html* (`front` part is visible) 
      - *dashboards.js*: 
        - dynamically disables form submit buttons
        - exchanges the template appearance for phone and desktop
    - `payment_verification` , `placement_verification`, `removal_verification` views:
      - validates the `request.POST` data
      - modifies the order db record
      - sends a letter to the customer email 
      - retrieves db data and renders *dashboard.html* ( the parts with the view names are visible) 
    - these four views are unified by the single template *dashboard.html*  to simplify the vertical sidebar rendering

- **Staff member part: More  &nbsp;&nbsp; views_folder/analytics_views.py  and views_folder/staff_actions_view.py**  
    - `order_query` view: <br>
      renders *order_query.html*  and *orders_selected.html*
    - `order_page` view:
      - validates the access
      - renders *order_page.html*
      - *order_page.js*  handles the *Confirm Order Cancelation* button appearance
    - `edit_setUp` view:
      - renders *edit_setUp.html*
      - validates the `request.POST` data
      - creates  a `SetUp_Parameters` instance
    - `prepare_cancel` view:
      - validates the `request.POST` data
      - calls the `order_page` view
    - `cancel_order` view:
      - validates the `request.POST` data
      - transfers the order to the archive
    
- **The customer account page and the message page: &nbsp;&nbsp; views_folder/account_view.py and views_folder/message_views.py**
    - `account` view:<br>
    renders *account.html*
    - `message` view:<br>
    renders *message.html*
    
