from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Session)
admin.site.register(User_Registration_Timestamp)
admin.site.register(City)
admin.site.register(Bus_Stop)
admin.site.register(Preemption)
admin.site.register(Current_Order)
admin.site.register(Reference)
admin.site.register(Orders_Archived)
admin.site.register(Reference_Archived)
admin.site.register(Simulated_World_Update)
admin.site.register(Last_Explorer_Update)
admin.site.register(SetUp_Parameters)
admin.site.register(App_Explorer)



