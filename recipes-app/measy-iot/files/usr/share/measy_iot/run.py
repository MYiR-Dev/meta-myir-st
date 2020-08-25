from app import app
from app.ws import  socketio
import sys
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    socketio.run(app, host='0.0.0.0', port=8080, use_reloader=False, debug=False)

if __name__ == '__main__': main()


