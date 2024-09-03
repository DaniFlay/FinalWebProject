from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib.auth import  login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import bcrypt
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.

def login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user is not None:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'aniuniverse/login.html', {'error': 'Password is incorrect'})
        else:
            return render(request, 'aniuniverse/login.html', {'error': 'Invalid username'})
    else:
        return render(request, 'aniuniverse/login.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    if request.method == 'POST':
        form= RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            userProfile= UserProfile(user=user)
            userProfile.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm()
        return render(request, 'aniuniverse/register.html', {'form': form})

def home(request):
    animes=Animes.objects.all().order_by('-score')[:10]
    mangas= Mangas.objects.all().order_by('-score')[:10]
    criteria1 = Q(aired_to__isnull=True)
    criteria2= Q(animetype= 'TV')
    animesAired= Animes.objects.filter(criteria1 & criteria2).order_by('-score')[:10]
    ovas= Animes.objects.filter(animetype='OVA').order_by('-score')[:10]
    movies= Animes.objects.filter(animetype='Movie').order_by('-score')[:10]
    publishingMangas= Mangas.objects.filter(state='Publishing').order_by('-score')[:10]
    return render(request, 'aniuniverse/home.html',{
        'animes': animes,
        'mangas': mangas,
        'animesAired': animesAired,
        'ovas': ovas,
        'movies': movies,
        'publishingMangas': publishingMangas,
    })

def animeItem(request, id):
    anime = Animes.objects.get(anime_id=id)
    animeUser= UserProfile.objects.filter(user=request.user.pk).first()
    animeStats= AnimeUser.objects.filter(animes=anime, userprofile=animeUser).first()
    favorite=False
    favorites= animeUser.favorite_anime.all() or []
    if anime in favorites:
        favorite= True
    link=None
    if anime.trailer_url:
        link= anime.trailer_url.replace('watch?v=','embed/')
    criteria1 = Q(genres=anime.genres)
    criteria2= Q(demographics=anime.demographics)
    similarTitles= Animes.objects.filter(title__contains=anime.title.split(' ')[0].split(':')[0]).exclude(title=anime.title)[:6]
    similarAnime= Animes.objects.filter(criteria1 & criteria2).exclude(title=anime.title).order_by('-score')[:6]
    if len(similarAnime) < 6:
        similarAnime= Animes.objects.filter(criteria1).exclude(title=anime.title).order_by('-score')[:6]
        if len(similarAnime) < 6:
            similarAnime= Animes.objects.filter(criteria2).exclude(title=anime.title).order_by('-score')[:6]
    return render(request, 'aniuniverse/animeItem.html',
                  {'animeItem': anime,
                   'animeUser': animeUser,
                   'link': link,
                   'similarTitles': similarTitles,
                   'similarAnime': similarAnime,
                   'favorite': favorite,
                   'animeStats': animeStats,
                  })

def mangaItem(request, id):
    manga = Mangas.objects.get(manga_id=id)
    mangaUser= UserProfile.objects.filter(user=request.user.pk).first()
    mangaStats= MangaUser.objects.filter(mangas=manga, userprofile=mangaUser).first()
    favorite=False
    favorites= mangaUser.favorite_manga.all() or []
    if manga in favorites:
        favorite= True
    criteria1 = Q(genres=manga.genres)
    criteria2= Q(demographics=manga.demographics)
    similarManga= Mangas.objects.filter(criteria1 & criteria2).exclude(title=manga.title).order_by('-score')[:6]
    if len(similarManga) < 6:
        similarManga= Mangas.objects.filter(criteria1).exclude(title=manga.title).order_by('-score')[:6]
        if len(similarManga) < 6:
            similarManga= Mangas.objects.filter(criteria2).exclude(title=manga.title).order_by('-score')[:6]
    return render(request, 'aniuniverse/mangaItem.html',{
        'mangaItem': manga,
        'mangaUser': mangaUser,
        'similarManga': similarManga,
        'favorite': favorite,
        'mangaStats': mangaStats,
    })

def topAnime(request,type):
    animes= None
    upcoming = False
    if type == 'all':
        animes= Animes.objects.all().order_by("-score")
    elif type == 'OVA':
        animes= Animes.objects.filter(animetype='OVA').order_by("-score")
    elif type == 'TV':
        animes= Animes.objects.filter(animetype='TV').order_by('-score')
    elif type == 'Movie':
        animes= Animes.objects.filter(animetype='Movie').order_by("-score")
    elif type == 'Special':
        animes= Animes.objects.filter(animetype='Special').order_by("-score")
    elif type == 'Airing':
        animes= Animes.objects.filter(state='Currently Airing').order_by("-score")
    elif type == 'Upcoming':
        animes= Animes.objects.filter(state='Not yet aired').order_by("-score")
        upcoming = True
    elif type == 'Popular':
        animes= Animes.objects.all().order_by('-members')
    elif type == 'Favorites':
        animes= Animes.objects.all().order_by('-favorites')
    elif type == 'ONA':
        animes= Animes.objects.filter(animetype='ONA').order_by("-score")
    paginator= Paginator(animes, per_page=50)
    page_number= request.GET.get("page")
    length= animes.count()
    animes= paginator.get_page(page_number)
    return render(request, 'aniuniverse/topAnime.html',{
        'animes': animes,
        'length': length,
        'upcoming': upcoming,
    })

def topManga(request,type):
    mangas= None
    if type == 'all':
        mangas= Mangas.objects.all().order_by("-score")
    elif type == 'Manga':
        mangas= Mangas.objects.filter(mangatype='Manga').order_by("-score")
    elif type == 'One-shot':
        mangas= Mangas.objects.filter(mangatype='One-shot').order_by('-score')
    elif type == 'Doujinshi':
        mangas= Mangas.objects.filter(mangatype='Doujinshi').order_by("-score")
    elif type == 'LightNovel':
        mangas= Mangas.objects.filter(mangatype='Light Novel').order_by("-score")
    elif type == 'Novel':
        mangas= Mangas.objects.filter(mangatype='Novel').order_by("-score")
    elif type == 'Manhwa':
        mangas= Mangas.objects.filter(mangatype='Manhwa').order_by("-score")
    elif type == 'Manhua':
        mangas= Mangas.objects.filter(mangatype='Manhua').order_by('-score')
    elif type == 'Favorites':
        mangas= Mangas.objects.all().order_by('-favorites')
    elif type == 'Popular':
        mangas= Mangas.objects.all().order_by("-scored_by")
    paginator= Paginator(mangas, per_page=50)
    page_number= request.GET.get("page")
    length= mangas.count()
    mangas= paginator.get_page(page_number)
    return render(request, 'aniuniverse/topManga.html',{
        'mangas': mangas,
        'length': length,
    })
def searchAnime(request):
    if request.method == 'GET':
        return render(request, 'aniuniverse/searchAnime.html')

def animeTitleResults(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        request.session['title'] = title
    else:
        title = request.session.get('title')

    animeList = Animes.objects.filter(title__icontains=title)

    paginator = Paginator(animeList, per_page=50)
    page_number = request.GET.get('page')

    try:
        animeList = paginator.get_page(page_number)
    except PageNotAnInteger:
        animeList = paginator.get_page(1)
    except EmptyPage:
        animeList = paginator.get_page(paginator.num_pages)

    length = paginator.count

    return render(request, 'aniuniverse/animeTitleResult.html', {
        'animes': animeList,
        'length': length,
        'title': title,
    })
def mangaTitleResults(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        request.session['title'] = title
    else:
        title = request.session.get('title')
    mangas = Mangas.objects.filter(title__icontains=title)
    paginator = Paginator(mangas, per_page=50)
    page_number = request.GET.get('page')

    try:
        mangas = paginator.get_page(page_number)
    except PageNotAnInteger:
        mangas = paginator.get_page(1)
    except EmptyPage:
        mangas = paginator.get_page(paginator.num_pages)

    length = paginator.count
    return render(request, 'aniuniverse/mangaTitleResults.html', {
       'mangas': mangas,
        'length': length,
        'title': title,
    })

def searchManga(request):
    if request.method == 'GET':
        return render(request, 'aniuniverse/searchManga.html')
    else:
        title= request.POST.get('title')
        mangas= Mangas.objects.filter(title__icontains=title)
        paginator= Paginator(mangas, per_page=10)
        page_number= request.GET.get("page")
        length= mangas.count()
        mangas= paginator.get_page(page_number)
        return render(request, 'aniuniverse/mangaTitleResults.html',{
           'mangas': mangas,
            'length': length,
            'title':title,
        })

def search(request,work, type, name):
    animes= None
    mangas=None
    paginator=None
    if work =='Anime':
        if type=='genre':
            animes= Animes.objects.filter(genres__contains=name).order_by('-score')
        elif type=='demographics':
            animes= Animes.objects.filter(demographics__contains=name).order_by('-score')
        elif type=='type':
            animes= Animes.objects.filter(animetype=name).order_by('-score')
        elif type=='themes':
            animes= Animes.objects.filter(themes__contains=name).order_by('-score')
        paginator= Paginator(animes, per_page=30)
        page_number= request.GET.get("page")
        length= animes.count()
        animes= paginator.get_page(page_number)
    elif work =='Manga':
        if type=='genre':
            mangas= Mangas.objects.filter(genres__contains=name).order_by('-score')
        elif type=='demographics':
            mangas= Mangas.objects.filter(demographics__contains=name).order_by('-score')
        elif type=='type':
            mangas= Mangas.objects.filter(mangatype=name).order_by('-score')
        elif type=='themes':
            mangas= Mangas.objects.filter(themes__contains=name).order_by('-score')
        paginator= Paginator(mangas, per_page=30)
        page_number= request.GET.get("page")
        length= mangas.count()
        mangas= paginator.get_page(page_number)
    return render(request, 'aniuniverse/search.html',{
        'animes': animes,
       'mangas': mangas,
        'anime': work,
        'type': type,
        'name': name,
        'length': length,
    })
def getUser(request):
    user= UserProfile.objects.filter(user=User.objects.get(id=request.user.id)).first()
    print(user.serialize())
    return JsonResponse(user.serialize(),safe=False)
def getAnime(request, id):
    anime= Animes.objects.get(anime_id=id)
    return JsonResponse(anime.serialize(),safe=False)
def addAnime(request):
    user= UserProfile.objects.filter(user=request.user).first()
    if request.method == 'PUT':
        try:
            data= json.loads(request.body)
            if 'favorite' in data:
                anime_id= data.get('favorite')
                anime=get_object_or_404(Animes, anime_id=anime_id)
                favorites= user.favorite_anime.all() or []
                if anime in favorites:
                    user.favorite_anime.remove(anime)
                    messages.success(request,'Anime removed to favorites')
                else:
                    user.favorite_anime.add(anime)
                    messages.success(request,'Anime added from favorites')
                user.save()
                
                return JsonResponse({'message': 'Added to favorites'}, status=200)
            elif 'episodes' in data:
                anime_id= data.get('id')
                status= data.get('status')
                eps= data.get('episodes')
                score= data.get('score')
                anime= get_object_or_404(Animes, pk=anime_id)
                if AnimeUser.objects.filter(animes=anime, userprofile=user).exists():
                    anime= AnimeUser.objects.filter(userprofile=user, animes=anime).first()
                    anime.episodes= eps
                    anime.score= score
                    anime.status= status
                else:
                    anime= AnimeUser.objects.create(animes=anime, episodes=eps, score=score, status=status)
                    user.animeList.add(anime)
                anime.save()
                user.save()
                messages.success(request,'Anime updated successfully')
                return JsonResponse({'message': 'Added to anime list'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
def addManga(request):
    user= UserProfile.objects.filter(user=request.user).first()
    if request.method == 'PUT':
        try:
            data= json.loads(request.body)
            if 'favorite' in data:
                manga_id= data.get('favorite')
                manga= get_object_or_404(Mangas, manga_id=manga_id)
                favorites= user.favorite_manga.all() or []
                if manga in favorites:
                    user.favorite_manga.remove(manga)
                    messages.success(request,'Manga removed to favorites')
                else:
                    user.favorite_manga.add(manga)
                    messages.success(request,'Manga added to favorites')
                user.save()
                return JsonResponse({'message': 'Added to favorites'}, status=200)
            elif 'chapters' in data:
                manga_id= data.get('id')
                chapters= data.get('chapters')
                score= data.get('score')
                status= data.get('status')
                manga= get_object_or_404(Mangas, pk=manga_id)
                if MangaUser.objects.filter(mangas=manga, userprofile=user).exists():
                    manga= MangaUser.objects.filter(userprofile=user, mangas=manga).first()
                    manga.chapters= chapters
                    manga.score= score
                    manga.status= status
                else:
                    manga= MangaUser.objects.create(mangas=manga, chapters=chapters, score=score, status=status)
                    user.mangaList.add(manga)
                messages.success(request,'Manga updated successfully')
                manga.save()
                user.save()
                return JsonResponse({'message': 'Added to manga list'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
def profile(request,username):
    user= UserProfile.objects.filter(user=request.user).first()
    animeScore=0.0
    mangaScore=0.0
    totalScore=0.0
    #Anime Stats
    watching=0
    completedAnime=0
    droppedAnime=0
    onholdAnime=0
    plan_to_watch=0
    animeList= user.animeList.all()
    for anime in animeList:
        watching+= anime.status == 'Watching'
        completedAnime+= anime.status == 'Completed'
        droppedAnime+= anime.status == 'Dropped'
        onholdAnime+= anime.status == 'On-Hold'
        plan_to_watch+= anime.status == 'Plan to Watch'
        animeScore+= anime.score
        totalScore+= anime.score
    #Manga Stats
    mangaList= user.mangaList.all()
    reading=0
    completedManga=0
    on_holdManga=0
    droppedManga=0
    plan_to_read=0
    for manga in mangaList:
        reading+= manga.status == 'Reading'
        completedManga+= manga.status == 'Completed'
        on_holdManga+= manga.status == 'On-Hold'
        droppedManga+= manga.status == 'Dropped'
        plan_to_read+= manga.status == 'Plan to Read'
        mangaScore+= manga.score
        totalScore+= manga.score
    #General Stats
    total_anime= animeList.count()
    total_manga= mangaList.count()
    total_favorite_anime= user.favorite_anime.count()
    total_favorite_manga= user.favorite_manga.count()
    average_score= totalScore / (total_anime + total_manga) if total_anime + total_manga > 0 else 0
    if total_anime > 0:
        animeScore= animeScore/total_anime
    else:
        animeScore= 0.0
    if total_manga > 0:
        mangaScore= mangaScore/total_manga
    else:
        mangaScore= 0.0

    favorite_anime= user.favorite_anime.all()[:12]
    favorite_manga= user.favorite_manga.all()[:12]
    return render(request, 'aniuniverse/profile.html',
                  {'userProfile': user,
                   'total_anime': total_anime,
                   'total_manga': total_manga,
                   'total_favorite_anime': total_favorite_anime,
                   'total_favorite_manga': total_favorite_manga,
                   'average_score': average_score,
                   'animeScore':animeScore,
                   'mangaScore':mangaScore,
                   'watching': watching,
                   'completeAnime': completedAnime,
                   'droppedAnime': droppedAnime,
                   'onholdAnime': onholdAnime,
                   'plan_to_watch': plan_to_watch,
                   'reading': reading,
                   'completedManga': completedManga,
                   'on_holdManga': on_holdManga,
                   'droppedManga': droppedManga,
                   'plan_to_read': plan_to_read,
                   'favorite_anime': favorite_anime,
                   'favorite_manga': favorite_manga,
                   })
def favoriteAnime(request,username):
    user= UserProfile.objects.filter(user=request.user).first()
    animes=user.favorite_anime.all()
    paginator= Paginator(animes, per_page=50)
    page_number= request.GET.get("page")
    length= animes.count()
    animes= paginator.get_page(page_number)
    return render(request, 'aniuniverse/favoriteAnime.html', 
                  {'animes': animes,
                   'length':length
})

def favoriteManga(request, username):
    user= UserProfile.objects.filter(user=request.user).first()
    mangas=user.favorite_manga.all()
    paginator= Paginator(mangas, per_page=50)
    page_number= request.GET.get("page")
    length= mangas.count()
    mangas= paginator.get_page(page_number)
    return render(request, 'aniuniverse/favoriteManga.html',
                  {'mangas': mangas,
                   'length':length
    })

def animeList(request, username, status):
    user= UserProfile.objects.filter(user=request.user).first()
    if status == 'all':
        animeList= user.animeList.all()
    else:
        animeList= user.animeList.filter(status=status)
    paginator= Paginator(animeList, per_page=50)
    page_number= request.GET.get("page")
    length= animeList.count()
    animeList= paginator.get_page(page_number)
    return render(request, 'aniuniverse/animeList.html',
                  {'animes': animeList,
                   'length':length,
                   'status': status
    })

def mangaList(request, username, status):
    user= UserProfile.objects.filter(user=request.user).first()
    if status == 'all':
         mangaList= user.mangaList.all()
    else:
        mangaList= user.mangaList.filter(status=status)
    paginator= Paginator(mangaList, per_page=50)
    page_number= request.GET.get("page")
    length= mangaList.count()
    mangaList= paginator.get_page(page_number)
    return render(request, 'aniuniverse/mangaList.html',
                  {'mangas': mangaList,
                   'length':length
    })

def animeSeason(request):
    if request.method == 'GET':
        years= list(Animes.objects.all().values_list('premiered_year',flat=True).distinct().order_by('-premiered_year').exclude(premiered_year=None))
        seasons= list(Animes.objects.all().values_list('premiered_season',flat=True).distinct().order_by('premiered_season').exclude(premiered_season=None))
        return render(request, 'aniuniverse/animeSearchSeason.html',
                      {
                          'years': years,
                          'seasons': seasons,
                      })
def animeSeasonResult(request):
    if request.method == 'POST':
        season = request.POST.get('season', 'all')
        year = request.POST.get('year', 'all')

        # Store season and year in session to use for pagination
        request.session['season'] = season
        request.session['year'] = year
    else:
        # Retrieve season and year from session for GET requests (pagination)
        season = request.session.get('season', 'all')
        year = request.session.get('year', 'all')

    # Initialize animeList
    animeList = Animes.objects.all()

    # Apply filtering based on season and year
    if season != 'all':
        animeList = animeList.filter(premiered_season=season)
    if year != 'all':
        animeList = animeList.filter(premiered_year=year)

    # Order by score
    animeList = animeList.order_by('-score')

    # Pagination
    paginator = Paginator(animeList, per_page=50)
    page_number = request.GET.get('page')

    try:
        animeList = paginator.get_page(page_number)
    except PageNotAnInteger:
        animeList = paginator.get_page(1)
    except EmptyPage:
        animeList = paginator.get_page(paginator.num_pages)

    length = paginator.count

    # Set year and season labels for display
    if year == 'all':
        year = 'All Years'
    if season == 'all':
        season = 'All Seasons'

    return render(request, 'aniuniverse/animeSeasonResult.html', {
        'animes': animeList,
        'length': length,
        'year': year,
        'season': season,
    })