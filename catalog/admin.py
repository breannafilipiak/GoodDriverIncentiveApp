from django.contrib import admin
from .models import Category, Product, AllUsers, Driver, Sponsor, SponsorOrg, Application, Point_Update, Point, Order, OrderItem



admin.site.register(AllUsers)

admin.site.register(Driver)

admin.site.register(Sponsor)

admin.site.register(SponsorOrg)

@admin.register(Application)
class Application_Config(admin.ModelAdmin):
    list_display = ['applying', 'apply_to', 'is_active', 'accepted']

# Register your models here.

@admin.register(Category)
class Category_Config(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class Product_Config(admin.ModelAdmin):
    list_display = ['title', 'price', 'in_stock', 'created_at', 'updated_at']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Point_Update)
class Point_Update_Config(admin.ModelAdmin):
    list_display = ['user', 'organization', 'updated_by', 'point_change', 'updated']
    

@admin.register(Point)
class Points_Config(admin.ModelAdmin):
    list_display = ['user', 'sponsor_org', 'point_total']
       
   
@admin.register(Order)
class Orders_Config(admin.ModelAdmin):
    list_display = ['user', 'org_total_paid', 'order_total', 'order_status']  

@admin.register(OrderItem)
class Order_Items_Config(admin.ModelAdmin):
    list_display = ['order_id', 'order', 'product', 'price', 'quantity']  


# Team1-pswd