'''
Module for working with spotify
'''

import os
import base64
import json
from requests import post, get
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    '''
    Function gets token
    '''
    auth_string =  client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers = headers, data = data, timeout = 10)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    '''
    Function get authorization header
    '''
    return {"Authorization" : "Bearer " + token}

def search_for_artist(token, artist_name):
    '''
    Function searches for artist
    '''
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers, timeout = 10)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("No artists")
        return None
    return json_result[0]

def get_artist_name(token, artist_id):
    '''
    Function gets artist name
    '''
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result.content)['name']
    return json_result

def get_songs_by_artist(token, artist_id):
    '''
    Function gets top ten most popular songs by artist
    '''
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_song(token, song_id):
    '''
    Function gets info about song
    '''
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result.content)
    return json_result

def main():
    '''
    Function communicates with user and runs other functions
    '''
    name = input('Please, input artist name: ')
    print('Please, input one of the parameters ')
    param = input('"artist_name", "artist_id", "most_popular_song" or "song_countries": ')

    token = get_token()
    result = search_for_artist(token, name)
    artist_id = result['id']

    if param == 'artist_name':
        return get_artist_name(token, artist_id)
    if param == 'artist_id':
        return artist_id
    songs = get_songs_by_artist(token, artist_id)
    if param == 'most_popular_song':
        return songs[0]['name']
    if param == 'song_countries':
        return get_song(token, songs[0]['id'])['available_markets']

    return 'You probably input wrong parameter or unexisting artist! Try again.'

print(main())
