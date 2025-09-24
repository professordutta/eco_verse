from django.shortcuts import render
from django.http import Http404

# Create your views here.
def home(request):
    return render(request, 'mriic/home.html')

def game1(request):
    return render(request, 'mriic/game1.html')

def game2(request):
    return render(request, 'mriic/game2.html', {'title': 'EcoVerse 3D Mini Game'})


def games(request):
    games_list = []
    for i in range(1, 8):
        img = f'https://picsum.photos/seed/ecoverse-game-{i}/800/450'
        games_list.append({
            'number': i,
            'name': f'Game {i}',
            'url_name': 'game_play',
            'image': img,
            'template': f'mriic/game{i}.html',
        })
    return render(request, 'mriic/games.html', {'games': games_list})


def game_play(request, number: int):
    if number < 1 or number > 7:
        raise Http404('Game not found')
    template_name = f'mriic/game{number}.html'
    context = {'title': f'EcoVerse Game {number}'}
    return render(request, template_name, context)