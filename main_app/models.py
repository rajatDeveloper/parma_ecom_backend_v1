from django.db import models
from django.contrib.auth.models import User


class StatusType(models.TextChoices):
    PENDING = "pending", "Pending"
    DISPATCH = "dispatch", "Dispatch"
    DILVERIED = "dilveried", "Dilveried"


class Product(models.Model):
    productName = models.CharField(max_length=50)
    imageData = models.ImageField(upload_to="product_image/")
    shortDes = models.TextField(max_length=120, default="")
    longDes = models.TextField(max_length=120, default="")
    mainPrice = models.IntegerField(default=0)
    afterDiscountPrice = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default="")
    isSale = models.BooleanField(default=False)
    stock = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.productName


class CartProduct(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product", null=True
    )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_cart_product"
    )
    isOrderItem = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return (
            self.user.username
            + " "
            + self.product.productName
            + " "
            + str(self.quantity)
        )


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_addresses"
    )
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipCode = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.address + " " + self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="orders"
    )
    cart_products = models.ManyToManyField(CartProduct)
    total = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=50, default="", null=True, blank=True)
    dilveryStatus = models.CharField(
        max_length=10,
        choices=StatusType.choices,  # Use the .choices property of the TextChoices class
    )

    def __str__(self):
        return self.user.username + " " + str(self.date)
