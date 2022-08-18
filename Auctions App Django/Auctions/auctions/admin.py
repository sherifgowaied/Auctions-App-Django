from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import *

#Register your models here.
class BInlineAdmin(admin.TabularInline):
    model = Bids
    

class ListAdmin(admin.ModelAdmin):
    list_display = ("id","owner", "title", "category", "image_url","starting_bid","description","closed")
    inlines = [BInlineAdmin]
    
class userAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("id","aurthor","list","bid_offer")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id","user","comments","list")




admin.site.register(List ,ListAdmin)
admin.site.register(User,userAdmin)
admin.site.register(Bids,BidsAdmin)
admin.site.register(Comments,CommentsAdmin)