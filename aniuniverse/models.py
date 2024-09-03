from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.utils.translation import gettext_lazy as _
import bcrypt
import json

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    mail= models.EmailField(max_length=255, default=None,null=True, blank=True)
    profilePicture= models.ImageField(upload_to='images/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))


class Animes(models.Model):
    anime_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=126)
    animetype = models.CharField(db_column='animeType', max_length=7, blank=True, null=True)  # Field name made lowercase.
    score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    scored_by = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=16)
    episodes = models.IntegerField(blank=True, null=True)
    aired_from = models.CharField(max_length=10, blank=True, null=True)
    aired_to = models.CharField(max_length=10, blank=True, null=True)
    animesource = models.CharField(db_column='animeSource', max_length=12, blank=True, null=True)  # Field name made lowercase.
    members = models.IntegerField()
    favorites = models.IntegerField()
    duration = models.CharField(max_length=18, blank=True, null=True)
    rating = models.CharField(max_length=30, blank=True, null=True)
    premiered_season = models.CharField(max_length=6, blank=True, null=True)
    premiered_year = models.IntegerField(blank=True, null=True)
    broadcast_day = models.CharField(max_length=10, blank=True, null=True)
    broadcast_time = models.CharField(max_length=5, blank=True, null=True)
    genres = models.CharField(max_length=126)
    themes = models.CharField(max_length=87)
    demographics = models.CharField(max_length=31)
    studios = models.CharField(max_length=148)
    producers = models.CharField(max_length=415)
    licensors = models.CharField(max_length=79)
    synopsis = models.CharField(max_length=8163, blank=True, null=True)
    main_picture = models.CharField(max_length=56, blank=True, null=True)
    trailer_url = models.CharField(max_length=44, blank=True, null=True)
    title_english = models.CharField(max_length=120, blank=True, null=True)
    title_japanese = models.CharField(max_length=85, blank=True, null=True)
    title_synonyms = models.CharField(max_length=277)

    class Meta:
        managed = False
        db_table = 'animes'
    def serialize(self):
        return {
            'anime_id': self.anime_id,
            'title': self.title,
            'animetype': self.animetype,
            'score': self.score,
           'scored_by': self.scored_by,
           'state': self.state,
            'episodes': self.episodes,
            'aired_from': self.aired_from,
            'aired_to': self.aired_to,
            'animesource': self.animesource,
           'members': self.members,
            'favorites': self.favorites,
            'duration': self.duration,
            'rating': self.rating,
            'premiered_season': self.premiered_season,
            'premiered_year': self.premiered_year,
            'broadcast_day': self.broadcast_day,
            'broadcast_time': self.broadcast_time,}

class Mangas(models.Model):
    manga_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=203)
    mangatype = models.CharField(db_column='mangaType', max_length=11, blank=True, null=True)  # Field name made lowercase.
    score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    scored_by = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=17)
    volumes = models.IntegerField(blank=True, null=True)
    chapters = models.IntegerField(blank=True, null=True)
    published_from = models.CharField(max_length=10, blank=True, null=True)
    published_to = models.CharField(max_length=10, blank=True, null=True)
    favorites = models.IntegerField()
    genres = models.CharField(max_length=113)
    themes = models.CharField(max_length=73)
    demographics = models.CharField(max_length=21)
    authors = models.CharField(max_length=1324)
    synopsis = models.CharField(max_length=4572, blank=True, null=True)
    main_picture = models.CharField(max_length=53, blank=True, null=True)
    title_english = models.CharField(max_length=207, blank=True, null=True)
    title_japanese = models.CharField(max_length=98, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mangas'
    def serialize(self):
        return json.dumps({
           'manga_id': self.manga_id,
            'title': self.title,
           'mangatype': self.mangatype,
           'score': self.score,
           'scored_by': self.scored_by,
           'state': self.state,
            'volumes': self.volumes,
            'chapters': self.chapters,
            'published_from': self.published_from,
            'published_to': self.published_to,
            'favorites': self.favorites,
            'genres': self.genres,
            'themes': self.themes,
            'demographics': self.demographics,
            'authors': self.authors,})

class AnimeUser(models.Model):
    class Status(models.TextChoices):
        unwatched= "U",_("Unwatched")
        watching= "W", _("Watching")
        completed= "C", _("Completed")
        on_hold= "OH", _("On Hold")
        dropped= "D", _("Dropped")
        plan_to_watch= "PW", _("Plan to Watch")
    animes = models.ForeignKey(Animes, on_delete=models.CASCADE)
    status= models.CharField(max_length=13,choices=Status.choices, default=Status.unwatched)
    episodes= models.IntegerField()
    score= models.IntegerField()
    def serialize(self):
        return {
            'id': self.id,
            'anime': self.animes.title,
           'status': self.status,
            'episodes': self.episodes,
           'score': self.score
        }

class MangaUser(models.Model):
    class Status(models.TextChoices):
        unread = "U", _("Unread")
        reading = "R", _("Reading")
        completed = "C", _("Completed")
        on_hold = "OH", _("On Hold")
        dropped = "D", _("Dropped")
        plan_to_read = "PR", _("Plan to Read")
    mangas= models.ForeignKey(Mangas,on_delete=models.CASCADE)
    status= models.CharField(max_length=12,choices=Status, default=Status.unread)
    chapters= models.IntegerField()
    score= models.IntegerField()
    def serialize(self):
        return {
            'id': self.id,
           'manga': self.mangas.title,
           'status': self.status,
            'chapters': self.chapters,
           'score': self.score
        }

class UserProfile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    favorite_anime= models.ManyToManyField(Animes, blank=True)
    favorite_manga= models.ManyToManyField(Mangas, blank=True)
    animeList= models.ManyToManyField(AnimeUser, blank=True)
    mangaList= models.ManyToManyField(MangaUser,blank=True)
    def serialize(self):
        return {
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.mail
            },
            'favorite_anime': [
                {
                    'id': anime.anime_id,
                    'title': anime.title,
                }
                for anime in self.favorite_anime.all()
            ],
            'favorite_manga': [
                {
                    'id': manga.manga_id,
                    'title': manga.title,
                }
                for manga in self.favorite_manga.all()
            ],
            'animeList': [anime.serialize() for anime in self.animeList.all()],
            'mangaList': [manga.serialize() for manga in self.mangaList.all()],
        }