from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from .models import FriendRequest
from user_profile.models import Profile


User = get_user_model()


def send_friend_request(request,pk):
	if request.user.is_authenticated:
		user = get_object_or_404(User, id=pk)
		frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
		return  redirect('home')

def accept_friend_request(request, pk):
	from_user = get_object_or_404(User, id=pk)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	return redirect('home')

def cancel_friend_request(request, pk):
	if request.user.is_authenticated:
		user = get_object_or_404(User, id=pk)
		frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user).first()
		frequest.delete()
		return redirect('home')



def delete_friend_request(request, pk):
	from_user = get_object_or_404(User, id=pk)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return redirect('home')

def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'friend_request_sent'

	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests
	}

	return render(request, "HomePage/profile.html", context)

