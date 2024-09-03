from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('anime/<str:id>', views.animeItem, name='animeItem'),
    path('manga/<str:id>', views.mangaItem, name='mangaItem'),
    path('topAnime/<str:type>',views.topAnime, name='topAnime'),
    path('topManga/<str:type>', views.topManga, name='topManga'),
    path('searchAnime',views.searchAnime, name='searchAnime'),
    path('searchManga',views.searchManga, name='searchManga'),
    path('search/<str:work>/<str:type>/<str:name>', views.search, name='search'),
    path('login',views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('getAnime/<str:id>',views.getAnime, name='getAnime'),
    path('getUser', views.getUser, name='getUser'),
    path('addAnime', views.addAnime, name='addAnime'),
    path('addManga',views.addManga, name='addManga'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/favoriteAnime',views.favoriteAnime, name='favoriteAnime'),
    path('profile/<str:username>/favoriteManga',views.favoriteManga, name='favoriteManga'),
    path('profile/<str:username>/animeList/<str:status>',views.animeList, name='animeList'),
    path('profile/<str:username>/mangaList/<str:status>',views.mangaList, name='mangaList'),
    path('searchSeasonAnime',views.animeSeason, name='animeSeason'),
    path('animeSeasonResults', views.animeSeasonResult,name='animeSeasonResults'),
    path('animeTitleResults', views.animeTitleResults, name='animeTitleResults'),
    path('mangaTitleResults', views.mangaTitleResults, name='mangaTitleResults')
]