import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

class RecipeStatus(models.Model):
    recipeStatus_name = models.CharField('Recipe Status',max_length=200)
    def __str__(self):
        return self.recipeStatus_name

class RecipeOwner(models.Model):
    recipeOwner_name = models.CharField('Owner',max_length=200)
    def __str__(self):
        return self.recipeOwner_name

class ProductMeasure(models.Model):
    productMeasure_name = models.CharField(max_length=200)
    def __str__(self):
        return self.productMeasure_name

class Product(models.Model):
    product_name = models.CharField('Product name',max_length=200)
    product_price = models.DecimalField('Product price',max_digits=10, decimal_places=2)
    product_link = models.CharField('Product link',max_length=200)
    product_image = models.CharField('Product image',max_length=200)
    product_measure = models.ForeignKey(ProductMeasure, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name
class RecipeGroup(models.Model):
    recipeGroup_name = models.CharField(max_length=200)
    def __str__(self):
        return self.recipeGroup_name
class Recipe(models.Model):
    owner = models.ForeignKey(RecipeOwner, on_delete=models.CASCADE)
    recipe_group = models.ForeignKey(RecipeGroup, on_delete=models.CASCADE)
    status = models.ForeignKey(RecipeStatus, on_delete=models.CASCADE)
    recipe_name = models.CharField('Recipe name',max_length=200)
    recipe_name_en = models.CharField('Recipe name (EN)',max_length=200)
    image = models.ImageField(upload_to='images/')
    product = models.ManyToManyField(Product , through='RecipeProduct')
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.recipe_name
    def was_published(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
class Calculate(models.Model):
    name = models.CharField('Calculate name',max_length=200,default='')
    visitor_id = models.CharField('Visitor ID',max_length=200,default='')
    step = models.IntegerField(default=0)
    count_people = models.IntegerField(default=3)
    count_man = models.IntegerField(default=2)
    count_woman = models.IntegerField(default=1)
    recipes = models.ManyToManyField(Recipe)
    create_date = models.DateTimeField("date create",auto_now_add=True)
    update_date = models.DateTimeField("date update",auto_now=True)
    def __str__(self):
        return self.name
class RecipeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField('Product price', max_digits=10, decimal_places=2, default=1.00)
    class Meta:
            constraints = [
                models.UniqueConstraint(fields=('product', 'recipe'), name='once_per_product_recipe')
            ]
    def __str__(self):
        return self.product.product_name

class Image(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name
