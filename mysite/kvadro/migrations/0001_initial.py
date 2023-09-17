# Generated by Django 4.2.4 on 2023-09-13 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, verbose_name='Product name')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Product price')),
                ('product_link', models.CharField(max_length=200, verbose_name='Product link')),
                ('product_image', models.CharField(max_length=200, verbose_name='Product image')),
            ],
        ),
        migrations.CreateModel(
            name='ProductMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productMeasure_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=200, verbose_name='Recipe name')),
                ('recipe_name_en', models.CharField(max_length=200, verbose_name='Recipe name (EN)')),
                ('image', models.ImageField(upload_to='images/')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipeGroup_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipeOwner_name', models.CharField(max_length=200, verbose_name='Owner')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipeStatus_name', models.CharField(max_length=200, verbose_name='Recipe Status')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kvadro.product')),
                ('recipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kvadro.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kvadro.recipeowner'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='product',
            field=models.ManyToManyField(through='kvadro.RecipeProduct', to='kvadro.product'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kvadro.recipegroup'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kvadro.recipestatus'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_measure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kvadro.productmeasure'),
        ),
        migrations.AddConstraint(
            model_name='recipeproduct',
            constraint=models.UniqueConstraint(fields=('product', 'recipe'), name='once_per_product_recipe'),
        ),
    ]
