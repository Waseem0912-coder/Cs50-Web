from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(User)
admin.site.register(Bidder)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Winners)
