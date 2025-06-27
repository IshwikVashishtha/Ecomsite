from django.contrib import admin
from .models import Products , Orders

# Register your models here.
admin.site.site_title = "Abc shoping"
admin.site.site_header = "E-commerse site"
admin.site.index_title = "E-commerse site"





class ProductAdmin(admin.ModelAdmin):

    def change_category_default(self , request , queryset):
        queryset.update(category="default")
    change_category_default.short_description = "default category"
    list_display=( "title",
                    "price",
                    "discount_price",
                    "description",
                    "category",
                    )
    search_fields = ('category',)
    actions =('change_category_default',)
    fields = ()
    list_editable = ('price' , 'category',)
    

admin.site.register(Products , ProductAdmin)
admin.site.register(Orders)