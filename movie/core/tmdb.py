import requests
import json

from django.http import HttpResponse

base_poster_url = 'http://image.tmdb.org/t/p/w300/'
API_key = 'f5b2aed42c73df0dd5ce12dfdba3b361'
URL_upcoming = 'https://api.themoviedb.org/3/movie/upcoming?api_key=' + API_key + '&language=en-US&page=1'

def get_upcoming(request):
    r = requests.get(URL_upcoming)
    return HttpResponse(json.dumps(r.json()), content_type="application/json")
