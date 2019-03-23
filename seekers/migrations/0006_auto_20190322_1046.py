# Generated by Django 2.1.7 on 2019-03-22 14:46

import decimal
from django.db import migrations, models


def fwd(apps, schema_editor):
    SeekerBenefit = apps.get_model('seekers', 'SeekerBenefit')
    db_alias = schema_editor.connection.alias
    for obj in SeekerBenefit.objects.using(db_alias).all():
        obj.cost = obj.benefit_type.default_cost
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('seekers', '0005_auto_20190321_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seekerbenefitproxy',
            options={'verbose_name': 'Seeker benefit report'},
        ),
        migrations.RenameField(
            model_name='seekerbenefittype',
            old_name='cost',
            new_name='default_cost',
        ),
        migrations.AddField(
            model_name='seekerbenefit',
            name='cost',
            field=models.DecimalField(decimal_places=2, null=True, max_digits=5),
        ),
        migrations.RunPython(fwd, reverse_code=lambda *args, **kwargs: None),
        migrations.AlterField(
            model_name='seekerbenefit',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=5, default=decimal.Decimal("0"))
        )
    ]
