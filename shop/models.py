from django.db import models

# Create your models here.
class Products(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2,default="")
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    desc = models.CharField(max_length=300)
    publish_date = models.DateField()
    image = models.ImageField(upload_to="shop/images/" , default="")
    
    def __str__(self):
        return self.product_name
    
    
    
class Contact(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70, default="")
    phone = models.IntegerField(default="")
    desc = models.CharField(max_length=500, default="")
   
    
    def __str__(self):
        return self.name
    
    
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=100)    
    email = models.CharField(max_length=100)    
    address = models.CharField(max_length=100)    
    phone = models.CharField(max_length=15, default="",blank=True)    
    city = models.CharField(max_length=100)    
    state = models.CharField(max_length=100,default="")    
    zip_code = models.CharField(max_length=100)    
    
    def __str__(self):
        return str(self.order_id)



class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
        
    def __str__(self):
        return self.update_desc[0:7] + "..."
