# Generated by Django 5.0.1 on 2024-07-06 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registerapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(default='Doctor', max_length=255)),
                ('username', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('image', models.ImageField(blank=True, upload_to='static/')),
                ('category', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('summary', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('content', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
