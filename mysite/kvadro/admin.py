from django.contrib import admin
from django.utils.html import format_html
from .models import Image, Product, Recipe,RecipeProduct, ProductMeasure, RecipeOwner, RecipeStatus ,RecipeGroup
from import_export.admin import ImportExportModelAdmin
from import_export import resources
class ProductResource(resources.ModelResource):
   class Meta:
      model = Product
class ProductAdmin(ImportExportModelAdmin):
   resource_class = ProductResource

class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ["image_tag","total_price"]
    def image_tag(self, obj):
        html = '<img src="{img}" style="max-width:200px; max-height:200px"/>'
        return format_html(html,img=obj.image.url)
    def total_price(self, obj):
        items = RecipeProduct.objects.filter(recipe_id=obj.id)
        qty = 0
        for item in items:
            qty +=  item.quantity
        return qty
    total_price.short_description = 'Total volume'
    inlines = (RecipeProductInline,)

class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ["image_tag"]
    def image_tag(self, obj):
        html = '<img src="{img}" style="max-width:200px; max-height:200px"/>'
        return format_html(html,img=obj.image.url)
    image_tag.allow_tags = True
    image_tag.short_description = 'Preview'
    list_display = ['name', 'image_tag',]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeOwner,admin.ModelAdmin)
admin.site.register(RecipeGroup,admin.ModelAdmin)
admin.site.register(RecipeStatus,admin.ModelAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductMeasure, admin.ModelAdmin)
admin.site.register(Image, ImageAdmin)