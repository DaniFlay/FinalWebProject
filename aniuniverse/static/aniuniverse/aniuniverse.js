document.addEventListener('DOMContentLoaded', function(){
    let topTabs= document.getElementById('topTabs');
    if(topTabs){
        let tabs= topTabs.children[0].children;
    let link= window.location.pathname.split('/')[2]
    for(i=0; i< tabs.length ;i++){
        tabs[i].classList.remove('selected');
    }
    if(link.includes('all')){
        tabs[0].classList.add('selected');
    }
    else if(link.includes('Airing')||link.includes('Manga')){
        tabs[1].classList.add('selected');
    }
    else if(link.includes('Upcoming')||link.includes('One-shot')){
        tabs[2].classList.add('selected');
    }
    else if(link.includes('TV')||link.includes('Doujinshi')){
        tabs[3].classList.add('selected');
    }
    else if(link.includes('Movies')||link.includes('LightNovel')){
        tabs[4].classList.add('selected');
    }
    else if(link.includes('OVA')||link.includes('Novel')){
        tabs[5].classList.add('selected');
    }
    else if(link.includes('ONA')||link.includes('Manhwa')){
        tabs[6].classList.add('selected');
    }
    else if(link.includes('Special')||link.includes('Manhua')){
        tabs[7].classList.add('selected');
    }
    else if(link.includes('Popular')){
        tabs[8].classList.add('selected');
    }
    else if(link.includes('Favorites')){
        tabs[9].classList.add('selected');
    }
    }
    let form= document.getElementById('itemUpdateFormAnime');
    let form2= document.getElementById('itemUpdateFormManga');
    let form3= document.getElementById('animeSeasonForm');
    if(form){
        let update= document.getElementById('update');
        let favorite= document.getElementById('addFav');
        let add=document.getElementById('add');
        let eps= document.getElementById('episodes');
        const id= window.location.pathname.split('/')[2];
        favorite.addEventListener('click', function(event){
            event.preventDefault();
            addFav(id,'anime');
            if(favorite.value =='Add to favorites'){
                favorite.value='Remove from favorites';
            }else{
                favorite.value='Add to favorites';
            }
        });
        update.addEventListener('click',function(event){
            event.preventDefault();
            updateAnime(id);
        });
        add.addEventListener('click',function(event){
            event.preventDefault();
            addChapters();
        });
        eps.addEventListener('blur',function(event){
            event.preventDefault();
            if(eps.value==''){
                eps.value=0;
            }
        });

    }
    if(form2){
        let update = document.getElementById('update');
        let favorite = document.getElementById('addFav');
        let add=document.getElementById('add');
        let chps= document.getElementById('chapters');
        const id= window.location.pathname.split('/')[2];
        favorite.addEventListener('click', function(event){
            event.preventDefault();
            addFav(id,'manga');
            if(favorite.value =='Add to favorites'){
                favorite.value='Remove from favorites';
            } else{
                favorite.value='Add to favorites';
            }
        });
        update.addEventListener('click',function(event){
            event.preventDefault();
            updateManga(id);
        });
        add.addEventListener('click',function(event){
            event.preventDefault();
            addChapters();
        });
        chps.addEventListener('blur',function(event){
            event.preventDefault();
            if(chps.value==''){
                chps.value=0;
            }
        });
    }
})
async function addFav(id,type){
    if(type=='anime'){
        await fetch(`/addAnime`,{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':getCSRFToken(),
        },
        body: JSON.stringify({
            'favorite': id
        })
    })
    }else if(type == 'manga'){
        await fetch(`/addManga`,{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            'favorite': id
        })
    })

}
}

async function updateAnime(id){
    let status= document.getElementById('status');
    let eps= document.getElementById('episodes');
    let score= document.getElementById('score');
    let message= document.getElementsByClassName('message')[0];
    await fetch(`/addAnime`,{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            'id':id,
            'status': status.value,
            'episodes': eps.value,
            'score': score.value
        })
    })
    message.setAttribute('style', 'visibility:visible');
    message.innerHTML=`<p>Anime updated successfully!</p>`;
}

async function updateManga(id){
    let status= document.getElementById('status');
    let chps= document.getElementById('chapters');
    let score= document.getElementById('score');
    let message= document.getElementsByClassName('message')[0];
    await fetch(`/addManga`,{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            'id':id,
            'status': status.value,
            'chapters': chps.value,
            'score': score.value
        })
    })
    message.setAttribute('style', 'visibility:visible');
    message.innerHTML=`<p>Manga updated successfully!</p>`;
}
function addChapters(){
    let eps= document.getElementById('episodes');
    if(eps){
        eps= parseInt(eps.value);
        eps++;
        document.getElementById('episodes').value= eps;
    }else{
        eps=document.getElementById('chapters');
        eps= parseInt(eps.value);
        eps++;
        document.getElementById('chapters').value=eps;
    }

}


function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return token;
}