# Generated by Django 5.0.6 on 2024-07-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aniuniverse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mangas',
            fields=[
                ('manga_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=203)),
                ('mangatype', models.CharField(blank=True, db_column='mangaType', max_length=11, null=True)),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('scored_by', models.IntegerField(blank=True, null=True)),
                ('state', models.CharField(max_length=17)),
                ('volumes', models.IntegerField(blank=True, null=True)),
                ('chapters', models.IntegerField(blank=True, null=True)),
                ('published_from', models.CharField(blank=True, max_length=10, null=True)),
                ('published_to', models.CharField(blank=True, max_length=10, null=True)),
                ('favorites', models.IntegerField()),
                ('genres', models.CharField(max_length=113)),
                ('themes', models.CharField(max_length=73)),
                ('demographics', models.CharField(max_length=21)),
                ('authors', models.CharField(max_length=1324)),
                ('synopsis', models.CharField(blank=True, max_length=4572, null=True)),
                ('main_picture', models.CharField(blank=True, max_length=53, null=True)),
                ('title_english', models.CharField(blank=True, max_length=207, null=True)),
                ('title_japanese', models.CharField(blank=True, max_length=98, null=True)),
            ],
            options={
                'db_table': 'mangas',
                'managed': False,
            },
        ),
    ]
