# Generated by Django 5.0.6 on 2024-07-25 15:55

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animes',
            fields=[
                ('anime_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('title_english', models.CharField(blank=True, max_length=123, null=True)),
                ('title_japanese', models.CharField(blank=True, max_length=90, null=True)),
                ('title_synonym', models.CharField(blank=True, max_length=260, null=True)),
                ('image_url', models.CharField(blank=True, max_length=60, null=True)),
                ('animetype', models.CharField(db_column='animeType', max_length=7)),
                ('animesource', models.CharField(db_column='animeSource', max_length=13)),
                ('episodes', models.IntegerField()),
                ('state', models.CharField(max_length=16)),
                ('airing', models.CharField(max_length=5)),
                ('airing_string', models.CharField(max_length=28)),
                ('duration', models.CharField(max_length=21)),
                ('rating', models.CharField(max_length=30)),
                ('score', models.DecimalField(decimal_places=2, max_digits=4)),
                ('scored_by', models.IntegerField()),
                ('ranking', models.IntegerField(blank=True, null=True)),
                ('popularity', models.IntegerField()),
                ('favorites', models.IntegerField()),
                ('premiered', models.CharField(blank=True, max_length=11, null=True)),
                ('broadcast', models.CharField(blank=True, max_length=27, null=True)),
                ('producer', models.CharField(blank=True, max_length=370, null=True)),
                ('licensor', models.CharField(blank=True, max_length=66, null=True)),
                ('studio', models.CharField(blank=True, max_length=80, null=True)),
                ('genre', models.CharField(blank=True, max_length=125, null=True)),
                ('opening_theme', models.CharField(blank=True, max_length=3807, null=True)),
                ('ending_theme', models.CharField(blank=True, max_length=3777, null=True)),
            ],
            options={
                'db_table': 'animes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]