import webbrowser, threading
from main_app import app
from werkzeug.serving import make_server

app.debug = False
host = '127.0.0.1'
port = 5025

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def start_server():
    global server
    server = ServerThread(app)
    server.start()

def stop_server():
    global server
    server.shutdown()

if __name__ == '__main__':
    start_server()
    webbrowser.open_new(f'http://{host}:{port}')
    exit = input('Чтобы выйти нажмите Ctrl+C или введите exit')
    if exit == 'exit':
        stop_server()
    else:
        print('Неверный ввод!')
