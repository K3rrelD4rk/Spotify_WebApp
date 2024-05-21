from pytube import YouTube
from youtubesearchpython import VideosSearch
from flask import flash, Flask
from pytube import YouTube
from youtubesearchpython import VideosSearch


if __name__ == '__main__':
    
    #flask webserver
    app = Flask(__name__)
    
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
    
    app.run(host='::1', port=8080, debug=True)