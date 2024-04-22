from pytube import YouTube
from youtubesearchpython import VideosSearch
from flask import flash, Flask
from pytube import YouTube
from youtubesearchpython import VideosSearch

app = Flask(__name__)
def create_app():
    return app
    
@app.route('/', methods=['GET', 'POST'])
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
    
def serverstart():
    if __name__ == '__main__':
        create_app().run(host='::1', port=8080, debug=True)