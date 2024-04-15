from datetime import datetime
from typing import final
from dotenv import load_dotenv
from flask_login import current_user
from requests import get, post
from youtubesearchpython import VideosSearch
import os
from pytube import YouTube
from . import app
import urllib.parse
from flask import jsonify, request, redirect, session, Blueprint, render_template, flash, url_for
load_dotenv()

api = Blueprint('api', __name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

auth_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
api_base_url = 'https://api.spotify.com/v1/'


#getting authorization by the user for
@api.route('/auth')
def get_auth():
    params = { 
              'client_id': client_id,
              'response_type': 'code',
              'redirect_uri': redirect_uri,
              'scope' : 'user-top-read user-modify-playback-state playlist-read-collaborative user-read-private user-read-email user-library-read playlist-read-collaborative playlist-read-private ',
              'show-dialog' : True
    }
    
    AUTH_URL = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(AUTH_URL)


#callback per auth-code
@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error" : request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code' : request.args['code'],
            'grant_type' : 'authorization_code',
            'redirect_uri' : redirect_uri,
            'client_id' : client_id,
            'client_secret' :  client_secret
        }
        
        response = post(url=token_url, data=req_body)
        token_info = response.json()
        
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        return redirect('/get_user')


#refresh-token
@api.route('/refresh_token', methods=['GET', 'POST'])
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
           'grant_type' : 'refresh_token',
           'refresh_token' : session['refresh_token'],
           'client_id' : client_id,
           'client_secret' : client_secret
        }
        req_headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
        response = post(token_url, data=req_body, headers=req_headers)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
    return redirect(request.path)


@api.route('/get_weekly')
def get_weekly():
    if 'access_token' not in session:
        return redirect('/auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    
@api.route('/get_user')
def get_user():
    if 'access_token' not in session:
        return redirect('/auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    url = api_base_url + 'me'
    headers = {
        'Authorization' : "Bearer " + session['access_token'],
    }
    response = get(url, headers=headers)
    user = response.json()
    session['username'] = user['display_name']
    session['user_id'] = user['id']
    session['user_img'] = user['images'][1]
    return redirect('/home')

@api.route('/get_playlist', methods=['POST', 'GET'])
def get_playlist():
    if 'access_token' not in session:
        return redirect('/get_auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    if request.method == 'POST':
        playlist_id = request.form.get("id")
        if playlist_id == 'offline_songs':
            playlist = offline_songs()
        else:
            url = api_base_url +'playlists/' + playlist_id
            headers = {
               'Authorization' : "Bearer " + session['access_token']
            }
            response = get(url, headers=headers)
            playlist = response.json()
            for element in playlist['tracks']['items']:
                element['track']['preview_url'] = get_yt_url(element['track']['name'] + " " + element['track']['artists'][0]['name'])
    
    return render_template('playlist.html', user=current_user, playlist=playlist)
    #return jsonify(playlist)
    

def get_top_artists():
    if 'access_token' not in session:
        return redirect('/get_auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    
    headers = {
        'Authorization' : "Bearer " + session['access_token']
    }
    
    url_artists = api_base_url + 'me/top/artists?time_range=short_term&limit=20'
    artists = get(url_artists, headers=headers).json()
    top_artists = {"items":[]}
    for element in artists['items']:
        top_artists['items'].append({
                                    "id" : element['id'],
                                    "images" : [{"url" : element['images'][0]['url']}],
                                    "name" : element['name']
                                    })
    return top_artists


def get_top_tracks():
    if 'access_token' not in session:
        return redirect('/get_auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    url_tracks = api_base_url + 'me/top/tracks?time_range=short_term&limit=20'
    headers = {
        'Authorization' : "Bearer " + session['access_token']
    }
    response_tracks = get(url_tracks, headers=headers)
    tracks = response_tracks.json()
    top_tracks = {"images" : [{"url" : tracks['items'][0]['album']['images'][0]['url']}], "tracks": {"items" : []}}
    for element in tracks['items']:
        top_tracks['tracks']['items'].append({
                                            "track" : {
                                                    "album": {
                                                        "images":[
                                                            {
                                                                "url" : element['album']['images'][0]['url']
                                                                }]},
                                                    "artists":[
                                                        {
                                                            "name" : element['artists'][0]['name']
                                                            }], 
                                                    "name" : element['name'], 
                                                    "preview_url" : 'None'
                                                    }
                                            })
    
    return top_tracks


def offline_songs():
    folder_path = 'website/static/audio/'
    
    
    offline_songs = {
        "images": [{"url": 'static/img/icon2.jpg'}],
        "name": 'Offline Songs',
        "tracks": {"items": []}
    }
    
    for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                offline_songs['tracks']['items'].append({"track":{
                    "album": {
                        "images": [{"url": 'static/img/songs_icon.png'}]
                    },
                    "artists": [{"name": "Unknown"}],
                    "name": file,
                    "preview_url": 'static/audio/' + file
                    }
                })
    return offline_songs

def get_yt_url(title):
    videos_search = VideosSearch(title, limit=1)
     
    try:
        # Cerca il video su YouTube
        videos_search = VideosSearch(title, limit=1)
        # Ottieni il primo risultato (se presente)
        result = videos_search.result()['result'][0]
        # Ottieni l'URL del video
        video_url = result['link']
        yt = YouTube(video_url)
        audio_url = yt.streams.filter(only_audio=True).first()
        return audio_url.url
    except Exception as e:
        flash("Error during search", category='error')
        return None

@api.route('/get_tops', methods=['GET', 'POST'])
def get_tops():
    if 'access_token' not in session:
        return redirect('/get_auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    if request.method == 'POST':
        playlist_id = request.form.get("id")
    
        if playlist_id == 'top_tracks':
            playlist = get_top_tracks()
            for element in playlist['tracks']['items']:
                element['track']['preview_url'] = get_yt_url(element['track'][0]['name'] + " " + element['track']['artists'][0]['name'])
        else:
            url = api_base_url + 'artists/'+ playlist_id
            final_url = url + '/top-tracks'
            headers = {
                'Authorization' : "Bearer " + session['access_token']
            }
            response = get(final_url, headers=headers)
            tracks = response.json()
            r = get(url, headers=headers).json()
            playlist = {
                "images" : [{"url" : r['images'][0]['url']}], 
                "name" : r['name'] + " Tops",
                "tracks" : {"items" : []}
            }
            for element in tracks['tracks']:
                playlist['tracks']['items'].append({
                    'track' : {
                        'artists' :
                            [
                                {
                                "name" : r['name']
                                }
                            ]
                        ,
                        'album' : {
                            'images' : [
                                    {
                                        'url' : element['album']['images'][0]['url']
                                    }
                                    ]
                    },
                    "name" : element['name'],
                    "preview_url" :  get_yt_url(element['name'] + " " + element['album']['artists'][0]['name'])                
                }})
                
            
    return render_template('playlist.html', playlist=playlist, user=current_user)
    #return jsonify(playlist)
