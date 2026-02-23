from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.formats import number_format
import uuid

# FoodProducts va RawMaterials alohida qolmoqda
class FoodProducts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_product_name = models.CharField(max_length=255, verbose_name="Oziq-ovqat nomi")
    measurement_unit = models.CharField(max_length=64, blank=True, verbose_name="O'lchov birligi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "Oziq-ovqat "
        verbose_name_plural = "Oziq-ovqatlar "
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.food_product_name} ({self.measurement_unit})"

class RawMaterials(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    raw_material_name = models.CharField(max_length=255, verbose_name="Xom-ashyo nomi")
    measurement_unit = models.CharField(max_length=64, blank=True, verbose_name="O'lchov birligi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "Xom-ashyo "
        verbose_name_plural = "Xom-ashyolar "
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.raw_material_name} ({self.measurement_unit})"

class Expenses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Yaratgan foydalanuvchi")
    date = models.DateField(unique=True, verbose_name="Sana")
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, editable=False, verbose_name="Umumiy summa")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def clean(self):
        if self.date and Expenses.objects.filter(date=self.date).exclude(pk=self.pk).exists():
            raise ValidationError({'date': 'Bu sana uchun xarajat allaqachon yaratilgan.'})

    def update_total_cost(self):
        """
        Xarajatning umumiy summasini FoodItem va RawItem'lar asosida hisoblaydi.
        """
        food_sum = sum(item.total_item_price for item in self.food_items.all())
        raw_sum = sum(item.total_item_price for item in self.raw_items.all())
        self.total_cost = food_sum + raw_sum
        self.save()

    @property
    def food_items_total(self):
        return sum(item.total_item_price for item in self.food_items.all())

    @property
    def raw_items_total(self):
        return sum(item.total_item_price for item in self.raw_items.all())

    class Meta:
        verbose_name = "Xarajat "
        verbose_name_plural = "Xarajatlar "

    def __str__(self):
        return f"Expense - {self.date}"

class FoodItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE, related_name="food_items")
    food_product = models.ForeignKey(FoodProducts, on_delete=models.CASCADE, verbose_name="Oziq-ovqat nomi")
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Narxi") # Narx majburiy bo'lgani ma'qul
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "[ Oziq-ovqat elementi ] "
        verbose_name_plural = "[ Oziq-ovqat elementlari ] "

    @property
    def total_item_price(self):
        total = self.quantity * self.price
        return total

    def __str__(self):
        return f"{self.food_product.food_product_name} - {self.quantity}"

class RawItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE, related_name="raw_items")
    raw_material = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, verbose_name="Xom-ashyo nomi")
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Narxi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "[ Xom-ashyo elementi ] "
        verbose_name_plural = "[ Xom-ashyo elementlari ] "

    @property
    def total_item_price(self):
        total = self.quantity * self.price
        return total

    def __str__(self):
        return f"{self.raw_material.raw_material_name} - {self.quantity}"