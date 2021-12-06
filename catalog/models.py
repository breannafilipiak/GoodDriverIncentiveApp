from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group)
from django.urls import reverse
from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, DecimalValidator
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Admin must be staff')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Admin must be superuser')

        return self.create_user(email, password, **other_fields)    

    # def create_sponsoruser(self, email, password, **other_fields):
    #     other_fields.setdefault('is_staff', True)
    #     other_fields.setdefault('is_superuser', False)
    #     other_fields.setdefault('is_active', True)

    #     if other_fields.get('is_staff') is not True:
    #         raise ValueError('Sponsor must be staff')

    #     return self.create_user(email, password, **other_fields)   

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('You must have an email address')

        email = self.normalize_email(email)
        user = self.model(email = email, **other_fields)
        user.set_password(password)
        user.save()

        return user


class AllUsers(AbstractBaseUser, PermissionsMixin):
    history = AuditlogHistoryField()
    email = models.EmailField(('email'),unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False) 
   
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()
    USERNAME_FIELD= 'email'

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message, from_email = settings.EMAIL_HOST_USER):
        send_mail(
            subject,
            message,
            from_email,
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.email
auditlog.register(AllUsers)        

class SponsorOrg(models.Model):
    history = AuditlogHistoryField()
    sponsor_org = models.CharField(max_length=150, blank = True, unique=True)
    point_value = models.DecimalField(validators=[MinValueValidator((0))], decimal_places=2, max_digits=5, default= 0.01)
    class Meta:
        verbose_name = "SponsorOrg"
        verbose_name_plural = "SponsorOrgs"
       
    def __str__(self):
        return self.sponsor_org
auditlog.register(SponsorOrg)  

class Sponsor(models.Model):
    history = AuditlogHistoryField()
    user = models.OneToOneField(AllUsers, on_delete= models.CASCADE, primary_key=True, related_name = 'sponsor_account')
    sponsor_org = models.ForeignKey(SponsorOrg, max_length=150, on_delete = models.CASCADE, blank = True)
    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
    #point_value = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.user.email
auditlog.register(Sponsor)  
    
class Driver(models.Model):
    history = AuditlogHistoryField()
    user = models.OneToOneField(AllUsers, on_delete=models.CASCADE, primary_key=True, related_name= 'driver_account')  
    sponsor = models.ManyToManyField(SponsorOrg, blank=True)   
    street_address = models.CharField(max_length=150, blank = True, default='')
    address_line = models.CharField(max_length=150, blank=True, default='')
    city = models.CharField(max_length=50, blank = True, default='')
    state = models.CharField(max_length=2, blank=True, default='')
    zip_code = models.CharField(max_length=5, blank=True, default='')
    
    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
        return self.user.email

    def apply(self, sponsor_org):

        if not sponsor_org in self.sponsor.all():
            self.sponsor.add(sponsor_org)
auditlog.register(Driver)      

class Application(models.Model):
    history = AuditlogHistoryField()
    applying = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="applying")
    apply_to = models.ForeignKey(SponsorOrg, on_delete=models.CASCADE, related_name="apply_to")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    accepted = models.BooleanField(default = False)
    reason = models.TextField(max_length= 250, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.applying.user.email

    def accept(self):
        driverlist = Driver.objects.get(user=self.applying)
        driverlist.apply(self.apply_to)
        self.is_active = False
        self.status = True
        self.save()
    
    def reject(self):
        self.is_active = False
        self.status = False
        self.save()

    def cancel(self):
        self.is_active = False
auditlog.register(Application)  

class Point(models.Model):
    history = AuditlogHistoryField()
    user = models.ForeignKey(Driver, on_delete=models.CASCADE)
    sponsor_org = models.ForeignKey(SponsorOrg, on_delete=models.CASCADE)
    point_total = models.PositiveIntegerField(default=0)
    monetary_value = models.DecimalField(default = 0.0, decimal_places=2, max_digits=7,)

    def __str__(self):
        return self.user.user.email
auditlog.register(Point)  

# @receiver(post_save, sender= AllUsers)
class Point_Update(models.Model):
    history = AuditlogHistoryField()
    user = models.ForeignKey(Driver, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    organization = models.ForeignKey(SponsorOrg, on_delete=models.CASCADE)
    point_change = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    reason = models.TextField(max_length=250)
    
    def __str__(self):
        return self.user.user.email
auditlog.register(Point_Update)  

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active = True)

# Category Model
class Category(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(max_length= 50, db_index= True)
    slug = models.SlugField(max_length= 50, unique= True)
    sponsor_org = models.ManyToManyField(SponsorOrg)
   
    class Meta:
        verbose_name_plural = 'categories'
 
    def get_url(self):
        return reverse('category', args=[self.slug])  
    
    def __str__(self):
        return self.name
auditlog.register(Category)  

# Product Model
class Product(models.Model):
    history = AuditlogHistoryField()
    category = models.ForeignKey(Category, related_name= 'product', on_delete=models.CASCADE)
    title = models.CharField(max_length= 128)
    slug = models.SlugField(max_length= 128, unique=True)
    description = models.TextField(blank= True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    quantity = models.IntegerField()
    sponsored_by = models.ManyToManyField(SponsorOrg)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = models.Manager()
    products = ProductManager()
    users_wishlist = models.ManyToManyField(Driver, related_name="user_wishlist", blank=True)

    class Meta:
        verbose_name_plural = 'Products'

    def get_url(self):
        return reverse('product', args=[self.slug])  
    
    def __str__(self):
        return self.title
auditlog.register(Product)  

class Order(models.Model):
    history = AuditlogHistoryField()
    user = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='order_user')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sponsor_org = models.ManyToManyField(SponsorOrg)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    org_total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_total = models.DecimalField(max_digits=5, decimal_places=2)
    order_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)
auditlog.register(Order)  

class OrderItem(models.Model):
    history = AuditlogHistoryField()
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

auditlog.register(OrderItem)  