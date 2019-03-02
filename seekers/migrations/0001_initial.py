# Generated by Django 2.1.7 on 2019-02-21 23:45

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields
import seekers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seeker',
            fields=[
                ('id', models.CharField(default=seekers.models.seeker_id_gen, editable=False, max_length=4, primary_key=True, serialize=False)),
                ('first_names', models.CharField(max_length=120)),
                ('last_names', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('state', localflavor.us.models.USStateField(default='NC', max_length=2)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('sober_anniversary', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('inactive_date', models.DateField(blank=True, null=True)),
                ('facebook_username', models.CharField(blank=True, max_length=30)),
                ('facebook_alias', models.CharField(blank=True, max_length=120)),
                ('contact_preference', models.IntegerField(choices=[(1, 'Email'), (2, 'SMS'), (3, 'Facebook')])),
                ('listener_trained', models.BooleanField(default=False, editable=False, verbose_name='Listener trained?')),
                ('extra_care', models.BooleanField(default=False, editable=False, verbose_name='Extra care program?')),
                ('extra_care_graduate', models.BooleanField(default=False, editable=False, verbose_name='Extra care graduate?')),
            ],
            options={
                'ordering': ['last_names', 'first_names'],
            },
        ),
        migrations.CreateModel(
            name='SeekerMilestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('milestone', models.IntegerField(choices=[(1, 'Listening trained'), (2, 'Extra-care enrolled'), (3, 'Extra-care graduated')])),
                ('seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seekers.Seeker')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='SeekerPairing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair_date', models.DateField(auto_now=True)),
                ('unpair_date', models.DateField(blank=True, null=True)),
                ('left', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='left_pair', to='seekers.Seeker')),
                ('right', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='right_pair', to='seekers.Seeker')),
            ],
            options={
                'ordering': ['pair_date'],
            },
        ),
        migrations.AddField(
            model_name='seeker',
            name='seeker_pairings',
            field=models.ManyToManyField(through='seekers.SeekerPairing', to='seekers.Seeker'),
        ),
        migrations.AlterUniqueTogether(
            name='seeker',
            unique_together={('last_names', 'first_names', 'birthdate')},
        ),
    ]
