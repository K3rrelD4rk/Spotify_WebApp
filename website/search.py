from .api import api_base_url, get_yt_url
from datetime import datetime
from requests import get
from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, session, jsonify

search = Blueprint('search', __name__)

@search.route('/search', methods=['POST','GET'])
def get_tracks():
    if 'access_token' not in session:
        return redirect('/get_auth')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    if request.method == 'POST':
        title = request.form.get('title')
        url = api_base_url + f'search?q={title}&type=track,artist&limit=10'
        headers = {
            'Authorization' : "Bearer " + session['access_token']
            }
        response = get(url, headers=headers)
        results = response.json()
        for element in results['tracks']['items']:
            element['preview_url'] = get_yt_url(element['name'] + element['artists'][0]['name'])
            
    return render_template("search.html", user=current_user, tracks=results['tracks'], artists=results['artists'], query=title)
    #return jsonify(results)