from django.shortcuts import render, redirect
from .models import Player, Room
from .forms import PlayerForm
from django.contrib.auth import authenticate, login

# Create your views here.


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# @login_required
def indexs(request):
    username = request.session.get('username')
    if not username:
        return redirect('loginUser')
    return render(request, 'rooms.html')

# @login_required
def rooms_list(request):
    rooms = Room.objects.all()
    current_user = request.user
    data_room = [
        {
            'id': room.id,
            'name': room.name,
            'players': [{'username': player.username, 'nickname': player.nickname, 'is_current_user': player == current_user} for player in room.players.all()],
            'is_full': room.is_full,
            # 'is_player': current_user in room.players.all()
        }
        for room in rooms
    ]
    return JsonResponse({'rooms': data_room, 'current_user': current_user.username})


def create_room(request):
    # if request.method == 'POST':
    username = request.user.username
    player = Player.objects.get(username=username)
    print('player.is_joining', player.is_joining, flush=True)
    if player.is_joining:
        print('You are already joining a room', flush=True)
        return JsonResponse({
            'success': False,
            'message': 'You are already joining a room'
        })
    room = Room.objects.create(name=f'Room {Room.objects.count() + 1}')
    return JsonResponse({
        'success': True,
        'room_id': room.id,
        'message': f'Created room {room.id}'
    })
    # return JsonResponse({
    #     'success': False,
    #     'message': 'Invalid request method'
    # })

# @login_required
@csrf_exempt
def join_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        if room_id:
            try:
                room = Room.objects.get(id=room_id)
                player = request.user
                if room.players.add(player):
                    # room.save()
                    return JsonResponse({
                        'success': True,
                        'room_id': room.id,
                        'message': f'Joined room {room.id}'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Failed to join a room. All rooms might be full.'
                    })
            except Room.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Room not found'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Room ID is required'
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

# @login_required
@csrf_exempt
def leave_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        if room_id:
            try:
                room = Room.objects.get(id=room_id)
                player = request.user
                if room.players.remove(player):
                    # room.save()
                    if room.count == 0:
                        room.delete()
                    return JsonResponse({
                        'success': True,
                        'message': f'Left room {room.id}'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Failed to leave a room'
                    })
            except Room.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Room not found'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Room ID is required'
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

def index(request):
    if 'username' in request.session:
        return render(request, 'game.html', {'username': request.session['username']})
    return redirect('loginUser')

def loginUser(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			user.is_online = True
			request.session['username'] = username
			return redirect('indexs')
	return render(request, 'login.html')

def signup(request):
	if request.method == 'POST':
		player_form = PlayerForm(request.POST)
		if player_form.is_valid():
			player_form.save()
			return redirect('loginUser')
	return render(request, 'signup.html')

def room(request):
	username = request.session.get('username')
	print('username===================>', username, flush=True)
	if not username:
		return redirect('loginUser')
	rooms = Room.objects.all()
	return render(request, 'rooms.html', {'rooms': rooms})

def tournament(request, room_name):
	username = request.session.get('username')
	if not username:
		return redirect('loginUser')
	if Room.objects.filter(name=room_name).exists():
		room = Room.objects.get(name=room_name)
		players = room.players.all()
	else:
		players = []
	return render(request, 'tournament.html', {'players': players, 'room_name': room_name})

def game_ai(request):
    return render(request, 'game_ai.html')  # Render the game_ai.html template

# def join_room(request, room_id):
# 	username = request.session['username']
# 	if not username:
# 		return redirect('loginUser')
# 	room = Room.objects.get(pk=room_id)
# 	room.players.add(Player.objects.get(username=username))
# 	room.count += 1
# 	room.save()
# 	return redirect('room')