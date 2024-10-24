from django.shortcuts import render

def getAbout(req):
    return render(req, "about.html")
