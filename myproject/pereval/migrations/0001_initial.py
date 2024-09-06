# Generated by Django 4.1.3 on 2024-09-06 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pereval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beautyTitle', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('other_titles', models.CharField(blank=True, max_length=255, null=True)),
                ('connect', models.TextField(blank=True, null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('winter_level', models.CharField(blank=True, max_length=50, null=True)),
                ('summer_level', models.CharField(blank=True, max_length=50, null=True)),
                ('autumn_level', models.CharField(blank=True, max_length=50, null=True)),
                ('spring_level', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='new', max_length=20)),
                ('coord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.coords')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerevalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pereval.pereval')),
            ],
        ),
        migrations.AddField(
            model_name='pereval',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.user'),
        ),
    ]
