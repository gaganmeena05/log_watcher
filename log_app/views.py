from django.shortcuts import render

def log_watcher_view(request):
    return render(request, './log_app/log_watcher.html')


