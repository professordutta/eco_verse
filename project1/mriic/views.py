from django.shortcuts import render
from django.http import Http404

# Create your views here.
def home(request):
    return render(request, 'mriic/home.html')

def about(request):
    return render(request, 'mriic/about.html')

def game1(request):
    return render(request, 'mriic/game1.html')

def game2(request):
    return render(request, 'mriic/game2.html', {'title': 'EcoVerse 3D Mini Game'})


def games(request):
    # Actual game data with descriptions and details
    games_data = [
        {
            'number': 1,
            'name': 'Ozone Defender',
            'description': 'Defend Earth\'s atmosphere by shooting down harmful greenhouse gases. Protect our ozone layer from depletion!',
            'duration': '8-12 min',
            'difficulty': 'Medium',
            'points': 500,
            'icon': 'bi-shield-exclamation',
        },
        {
            'number': 2,
            'name': 'Albatross Ocean Foraging',
            'description': 'Guide an albatross through the ocean, collecting fish while avoiding plastic waste. Learn about marine ecosystem challenges.',
            'duration': '5-8 min',
            'difficulty': 'Easy',
            'points': 300,
            'icon': 'bi-water',
        },
        {
            'number': 3,
            'name': 'Ocean Cleanup Adventure',
            'description': 'Navigate underwater depths to collect marine debris and rescue sea creatures from pollution. Make a real difference for our oceans!',
            'duration': '10-15 min',
            'difficulty': 'Hard',
            'points': 600,
            'icon': 'bi-droplet',
        },
        {
            'number': 4,
            'name': 'EcoSort 3D',
            'description': 'Sort recyclable materials on a conveyor belt in this 3D puzzle game. Master the art of waste management and recycling!',
            'duration': '6-10 min',
            'difficulty': 'Medium',
            'points': 400,
            'icon': 'bi-box-seam',
        },
        {
            'number': 5,
            'name': 'Forest Guardian',
            'description': 'Explore a beautiful 3D forest environment to rescue trapped animals and clean up environmental hazards. Be the guardian nature needs!',
            'duration': '12-18 min',
            'difficulty': 'Hard',
            'points': 700,
            'icon': 'bi-tree',
        },
        {
            'number': 6,
            'name': 'Farm Flow',
            'description': 'Connect pipes to deliver water to farms in this engaging puzzle game. Learn about sustainable agriculture and water management.',
            'duration': '5-7 min',
            'difficulty': 'Easy',
            'points': 250,
            'icon': 'bi-flower1',
        },
        {
            'number': 7,
            'name': 'Environmental Quiz',
            'description': 'Test your environmental knowledge with challenging questions. Learn fascinating facts about sustainability and climate action!',
            'duration': '3-5 min',
            'difficulty': 'Easy',
            'points': 200,
            'icon': 'bi-question-circle',
            'is_quiz': True,
        },
        {
            'number': 8,
            'name': 'Pet Care Clinic',
            'description': 'Care for adorable virtual pets by matching their needs with appropriate items. Learn responsibility and animal welfare!',
            'duration': '4-6 min',
            'difficulty': 'Easy',
            'points': 350,
            'icon': 'bi-heart-pulse',
        },
        {
            'number': 9,
            'name': 'Eco Challenge Master',
            'description': 'Complete daily eco-challenges and earn badges for sustainable living. Track your environmental impact and compete with friends!',
            'duration': '10-20 min',
            'difficulty': 'Medium',
            'points': 550,
            'icon': 'bi-lightning-charge',
        },
    ]
    
    # Separate quiz from regular games and sort by difficulty
    quiz_game = None
    regular_games = []
    
    for game in games_data:
        if game.get('is_quiz', False):
            quiz_game = game
        else:
            regular_games.append(game)
    
    # Sort regular games by difficulty: Easy -> Medium -> Hard
    difficulty_order = {'Easy': 0, 'Medium': 1, 'Hard': 2}
    regular_games.sort(key=lambda x: (difficulty_order.get(x['difficulty'], 999), x['number']))
    
    # Add quiz back to the end if it exists
    if quiz_game:
        regular_games.append(quiz_game)
    
    games_list = []
    for game in regular_games:
        local_img = f'/static/images/game{game["number"]}.png'
        fallback_img = f'https://picsum.photos/seed/ecoverse-game-{game["number"]}/800/450'
        
        games_list.append({
            'number': game['number'],
            'name': game['name'],
            'description': game['description'],
            'duration': game['duration'],
            'difficulty': game['difficulty'],
            'points': game['points'],
            'icon': game['icon'],
            'is_quiz': game.get('is_quiz', False),
            'url_name': 'game_play',
            'image': local_img,
            'fallback_image': fallback_img,
            'template': f'mriic/game{game["number"]}.html',
        })
    
    return render(request, 'mriic/games.html', {'games': games_list})


def game_play(request, number: int):
    if number < 1 or number > 9:
        raise Http404('Game not found')
    template_name = f'mriic/game{number}.html'
    context = {'title': f'EcoVerse Game {number}'}
    return render(request, template_name, context)