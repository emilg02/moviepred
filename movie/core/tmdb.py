import requests
import json

from django.http import HttpResponse

API_key = 'f5b2aed42c73df0dd5ce12dfdba3b361'
URL_upcoming = 'https://api.themoviedb.org/3/movie/upcoming?api_key=' + API_key + '&language=en-US&page=1'
URL_details = 'https://api.themoviedb.org/3/movie/'
def get_upcoming(request):
    r = requests.get(URL_upcoming)
    return HttpResponse(json.dumps(r.json()), content_type="application/json")

def get_details(request):
    movieid = request.GET['movie']
    url = URL_details + movieid + '?api_key=' + API_key + '&language=en-US'
    r = requests.get(url)
    return HttpResponse(json.dumps(r.json()), content_type="application/json")
