from django.db import models

SIZES = ["XS", "S", "M", "L", "XL"]


class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
    def __str__(self): return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    fabric = models.CharField(max_length=120, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    color = models.CharField(max_length=7, default="#1d2a5c", help_text="Hex colour shown when no image is set")
    image_url = models.URLField(blank=True)
    badge = models.CharField(max_length=24, blank=True)
    stock = models.PositiveIntegerField(default=20)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
    def __str__(self): return self.name


class Order(models.Model):
    STATUS = [("new", "New"), ("packed", "Packed"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")]
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=80)
    pincode = models.CharField(max_length=10)
    shipping = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS, default="new")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
    def __str__(self): return f"Order #{self.pk} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    size = models.CharField(max_length=4)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    qty = models.PositiveIntegerField()
    def __str__(self): return f"{self.qty} x {self.name} ({self.size})"
