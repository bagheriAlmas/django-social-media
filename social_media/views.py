from django.shortcuts import render


def home_view(request):
    context = {
        'user': request.user,
        'message': 'Hello '
    }
    return render(request, 'main/home.html', context)
