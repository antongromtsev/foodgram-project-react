# Generated by Django 3.0 on 2021-10-02 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20211001_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientvalue',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_value', to='recipes.Recipe'),
        ),
    ]
