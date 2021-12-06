from django.contrib import admin
from .models import Category, Product, AllUsers, Driver, Sponsor, SponsorOrg, Application, Point_Update, Point, Order, OrderItem




@admin.register(AllUsers)
class AllUsers_Config(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    list_filter = ['is_driver', 'is_sponsor', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']

admin.site.register(Driver)

admin.site.register(Sponsor)

admin.site.register(SponsorOrg)

@admin.register(Application)
class Application_Config(admin.ModelAdmin):
    list_display = ['applying', 'apply_to', 'is_active', 'accepted']
    list_filter = ['accepted', 'is_active']
    search_fields = ['applying__user__email', 'apply_to__sponsor_org']
# Register your models here.

@admin.register(Category)
class Category_Config(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    list_filter = ['sponsor_org']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class Product_Config(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'in_stock', 'created_at', 'updated_at']
    list_filter = ['in_stock', 'is_active','category']
    list_editable = ['price', 'in_stock']
    search_fields = ['title', 'category__name']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Point_Update)
class Point_Update_Config(admin.ModelAdmin):
    list_display = ['user', 'organization', 'updated_by', 'point_change', 'updated']
    search_fields = ['user__user__email']

@admin.register(Point)
class Points_Config(admin.ModelAdmin):
    list_display = ['user', 'sponsor_org', 'point_total']
    list_filter = ['sponsor_org']
    search_fields = ['user__user__email', 'sponsor_org__sponsor_org']   
   
@admin.register(Order)
class Orders_Config(admin.ModelAdmin):
    list_display = ['user', 'org_total_paid', 'order_total', 'order_status']  

@admin.register(OrderItem)
class Order_Items_Config(admin.ModelAdmin):
    list_display = ['order_id', 'order', 'product', 'price', 'quantity']  


# Team1-pswd