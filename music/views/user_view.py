from django.shortcuts import render

def library(request):
    """View for Library page (User's saved songs & albums)"""
    return render(request, 'music/library.html')

def profile(request):
    """View for Profile page (User's details)"""
    return render(request, 'music/profile.html')
