import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

db = sqlite3.connect(":memory:")
cursor = db.cursor()

def run_query(query):
    cursor.execute(query)
    return cursor.fetchall()

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path in ['/', '/login', '/register', '/reset-password', '/delete-account', '/admin']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if self.path == '/':
                self.path = '/index'
            with open(self.path[1:] + '.html', 'rb') as f:
                content = f.read()
                self.wfile.write(content)

        elif self.path.endswith('.css') or self.path.endswith('.js') or self.path.endswith('.png') or self.path.endswith('.jpg') or self.path.endswith('.jpeg') or self.path.endswith('.gif'):
            self.send_response(200)
            if self.path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif self.path.endswith('.js'):
                self.send_header('Content-type', 'text/javascript')
            elif self.path.endswith('.png'):
                self.send_header('Content-type', 'image/png')
            elif self.path.endswith('.jpg') or self.path.endswith('.jpeg'):
                self.send_header('Content-type', 'image/jpeg')
            elif self.path.endswith('.gif'):
                self.send_header('Content-type', 'image/gif')
            self.end_headers()
            with open(self.path[1:], 'rb') as f:
                content = f.read()
                self.wfile.write(content)

        elif self.path in ['/api/auth/register', '/api/auth/login', '/api/auth/reset-password', '/api/auth/delete-account']:
            self.send_response(405)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "405 - Method Not Allowed"
            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/api/admin':
            try:
                query = f"SELECT * FROM user"
                result = run_query(query)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = {'message': 'Login successful', 'data': result}
                response_json = json.dumps(response_data)
                self.wfile.write(response_json.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = {'message': 'Internal Server Error'}
                response_json = json.dumps(response_data)
                self.wfile.write(response_json.encode('utf-8'))
            

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "404 - Not Found"
            self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        if self.path in ['/', 'styles.css', '/script.js', '/api/auth/reset-password', '/api/auth/delete-account']:
            self.send_response(405)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "405 - Method Not Allowed"
            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/api/auth/register':
            if self.headers.get('content-type') == 'application/json':
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    parsed_data = json.loads(post_data.decode('utf-8'))
                    if 'username' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Username is required'}
                    elif 'password' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Password is required'}
                    elif 'name' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Name is required'}
                    else:
                        name = parsed_data['name']
                        username = parsed_data['username']
                        password = parsed_data['password']
                        query = f"SELECT * FROM user WHERE username='{username}'"
                        search_res = run_query(query)
                        if len(search_res) > 0:
                            self.send_response(403)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response_data = {'message': 'Username has been taken.'}
                        else:
                            query = f"INSERT INTO user VALUES ('{name}', '{username}', '{password}')"
                            create_res = run_query(query)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response_data = {'message': 'User registered successfully. Login to continue.', 'data': create_res}
                    response_json = json.dumps(response_data)
                    self.wfile.write(response_json.encode('utf-8'))
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = {'message': 'Internal Server Error'}
                    response_json = json.dumps(response_data)
                    self.wfile.write(response_json.encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response = "Invalid content type. Only application/json is supported."
                self.wfile.write(response.encode('utf-8'))

        elif self.path == '/api/auth/login':
            if self.headers.get('content-type') == 'application/json':
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    parsed_data = json.loads(post_data.decode('utf-8'))

                    if 'username' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Username is required'}
                    elif 'password' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Password is required'}
                    else:
                        username = parsed_data['username']
                        password = parsed_data['password']
                        query = f"SELECT * FROM user WHERE username='{username}'"
                        search_res = run_query(query)
                        if len(search_res) == 0:
                            self.send_response(403)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response_data = {'message': 'Please register first.'}
                        else:
                            query = f"SELECT * FROM user WHERE (username='{username}' AND password='{password}')"
                            print("query to execute: " + query)
                            result = run_query(query)
                            if len(result) == 0:
                                self.send_response(401)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                response_data = {'message': 'Invalid credentials'}
                            else:
                                self.send_response(200)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                response_data = {'message': 'Login successful', 'data': result}
                        response_json = json.dumps(response_data)
                        self.wfile.write(response_json.encode('utf-8'))
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = {'message': 'Internal Server Error'}
                    response_json = json.dumps(response_data)
                    self.wfile.write(response_json.encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response = "Invalid content type. Only application/json is supported."
                self.wfile.write(response.encode('utf-8'))
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "404 - Not Found"
            self.wfile.write(response.encode('utf-8'))

    def do_PATCH(self):
        if self.path in ['/', 'styles.css', '/script.js', '/api/auth/register', '/api/auth/login', '/api/auth/delete-account']:
            self.send_response(405)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "405 - Method Not Allowed"
            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/api/auth/reset-password':
            if self.headers.get('content-type') == 'application/json':
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    parsed_data = json.loads(post_data.decode('utf-8'))
                    if 'username' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Username is required'}
                    elif 'oldPassword' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Password is required'}
                    elif 'newPassword' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Please provide new password'}
                    else:
                        username = parsed_data['username']
                        old_password = parsed_data['oldPassword']
                        new_password = parsed_data['newPassword']
                        query = f"SELECT * FROM user WHERE username='{username}' AND password='{old_password}'"
                        search_res = run_query(query)
                        if len(search_res) == 0:
                            self.send_response(403)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response_data = {'message': 'Invalid credentials'}
                        else:
                            query = f"UPDATE user SET password='{new_password}' WHERE username='{username}'"
                            update_res = run_query(query)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response_data = {'message': 'Password updated successfully', 'data': update_res}
                    response_json = json.dumps(response_data)
                    self.wfile.write(response_json.encode('utf-8'))
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = {'message': 'Internal Server Error'}
                    response_json = json.dumps(response_data)
                    self.wfile.write(response_json.encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response = "Invalid content type. Only application/json is supported."
                self.wfile.write(response.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "404 - Not Found"
            self.wfile.write(response.encode('utf-8'))

    def do_DELETE(self):
        if self.path in ['/', 'styles.css', '/script.js', '/api/auth/register', '/api/auth/login', '/api/auth/reset-password']:
            self.send_response(405)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "405 - Method Not Allowed"
            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/api/auth/delete-account':
            if self.headers.get('content-type') == 'application/json':
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    parsed_data = json.loads(post_data.decode('utf-8'))
                    if 'username' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Username is required'}
                    elif 'password' not in parsed_data:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {'message': 'Password is required'}
                    else:
                        username = parsed_data['username']
                        password = parsed_data['password']
                        query = f"SELECT * FROM user WHERE username='{username}' AND password='{password}'"
                        search_res = run_query(query)
                        if len(search_res) == 0:
                            self.send_response(403)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response_data = {'message': 'Invalid credentials'}
                        else:
                            query = f"DELETE FROM user WHERE username='{username}'"
                            update_res = run_query(query)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response_data = {'message': 'Deleted account successfully', 'data': update_res}
                    response_json = json.dumps(response_data)
                    self.wfile.write(response_json.encode('utf-8'))
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = {'message': 'Internal Server Error'}
                    response_json = json.dumps(response_data)
                    self.wfile.write(response_json.encode('utf-8'))
            
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response = "Invalid content type. Only application/json is supported."
                self.wfile.write(response.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "404 - Not Found"
            self.wfile.write(response.encode('utf-8'))

def init_db():
    run_query("""
        CREATE TABLE user (
            name VARCHAR(50),
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50)
        )
    """)

def run():
    try:
        init_db()
        server_address = ('127.0.0.1', 8080)
        httpd = HTTPServer(server_address, MyRequestHandler)
        print('Server is running...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Server is terminated')
        httpd.socket.close()
    except Exception as e:
        print('Error: ', e)
        httpd.socket.close()


if __name__ == '__main__':
    run()
