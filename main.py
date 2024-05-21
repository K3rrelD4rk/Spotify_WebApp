from website import create_app
from yt_api.main import serverstart
import threading

app = create_app()
x = threading.Thread(target=serverstart, args=())

if __name__ == '__main__':
    x.start()
    app.run(host='127.0.0.1', port=5000, debug=True)