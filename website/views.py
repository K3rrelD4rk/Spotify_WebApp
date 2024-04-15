from email import header
from flask import Blueprint, jsonify, redirect, render_template, session
from .api import api_base_url, get, datetime, get_top_artists, get_top_tracks
from website.models import Playlists
from flask_login import current_user, login_required

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if 'access_token' not in session:
        return redirect('/auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    top_tracks = get_top_tracks()
    top_artists = get_top_artists()
    
    return render_template('home.html', user=current_user, top_image = top_tracks['images'][0]["url"], top_artists=top_artists['items'])
    #return jsonify(top_artists)
    #return jsonify(top_tracks)


@views.route('/library', methods=['GET', 'POST'])
@login_required
def library():
    if 'access_token' not in session:
        return redirect('/get_auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    headers = {
        'Authorization' :  f'Bearer {session["access_token"]}'
    }
    response = get(api_base_url + 'me/playlists', headers=headers)
    playlists = response.json()
    username = current_user.Username
    user_img = session['user_img']['url']
    img_height = session['user_img']['height']
    img_width = session['user_img']['width']
    return render_template('library.html', user=current_user, img_url=user_img, img_height=img_height, img_width=img_width, user_name=session['username'], username=username, playlists=playlists['items'], user_id=session['user_id'])
    #return jsonify(playlists)