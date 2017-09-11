from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def past(request):
    return render(request, 'past.html')


def past_list(request):
    return render(request, 'pastlist.html')


def profile(request):
    return render(request, 'profile.html')


def coc(request):
    return render(request, 'coc.html')


def speaker(request):
    return render(request, 'speaker.html')


def speaker_list(request):
    return render(request, 'speakerlist.html')


def schedule(request):
    return render(request, 'schedule.html')


def program(request):
    return render(request, 'program.html')


def login(request):
    return render(request, 'login.html')


def mailsent(request):
    return render(request, 'mailsent.html')
