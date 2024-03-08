# File: server.py

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
from urllib.parse import parse_qs, urlparse
from app.services import auth_service
from app.services import patient_service
from app.services import doctor_service
from app.services import health_record_service
from app.db import models
from app.routes import doctors, patients, health_records

# Initialize logging
logging.basicConfig(level=logging.INFO)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler, doctors.DoctorHandler, patients.PatientHandler, health_records.HealthRecordHandler):
    
    def do_GET(self):
        if self.path.startswith('/doctor/'):
            self.handle_get_doctor()
        elif self.path == '/health_records':
            self.handle_get_all_health_records()
        elif self.path.startswith('/health_record/'):
                self.handle_get_health_record()
        elif self.path == '/patients':
            if not self.authenticate():
                return
            self.handle_get_all_patients()
        elif self.path.startswith('/patient/'):
            patient_id = self.path.split('/')[-1]
            if patient_id.isdigit():
                self.handle_get_patient_by_id(patient_id)
            else:
                self.handle_get_patient_by_id(patient_id)
        
            
    def authenticate(self):
        """Check if the request contains a valid token."""
        if 'Authorization' not in self.headers:
            self.send_error(401, 'Authorization token is missing')
            return False

        token = self.headers['Authorization'].split()[-1]
        user_id = auth_service.verify_token(token)
        if not user_id:
            self.send_error(403, 'Token is invalid')
            return False
        
        # User ID from the token can be used to further verify user's permissions if necessary
        self.user_id = user_id
        return True

    def is_user_admin(self):
    # Make sure the user is authenticated
        if not self.authenticate():
            return False
    # Check if the authenticated user is an admin
            return auth_service.is_admin(self.user_id)


    def do_POST(self):
        if self.path == '/register':
            self.handle_register()
        elif self.path == '/login':
            self.handle_login()
        if self.path == '/add_doctor':
            self.handle_add_doctor()
        elif self.path == '/assign_doctor':
            if not self.authenticate():
                return
            self.handle_assign_doctor()
        elif self.path == '/add_patient':
            if not self.authenticate():
                return
            self.handle_add_patient()
        elif self.path == '/add_health_record':
            if not self.authenticate():
                return
            self.handle_add_health_record()
    
    
    def do_PUT(self):
        # Dispatch to appropriate PUT handler based on path
        if self.path.startswith('/update_doctor/'):
            if not self.authenticate():
                return
            self.handle_update_doctor()
        elif self.path.startswith('/update_patient/'):
            if not self.authenticate():
                return
            self.handle_update_patient()
        elif self.path.startswith('/update_health_record/'):
            if not self.is_user_admin():
                self.send_error(403, "Only admins can perform this action.")
                return
            self.handle_update_health_record()
        # Add more PUT dispatch conditions as necessary

    def do_DELETE(self):
        # Dispatch to appropriate DELETE handler based on path
        if self.path.startswith('/delete_doctor/'):
            if not self.authenticate():
                return
            self.handle_delete_doctor()
        elif self.path.startswith('/delete_patient/'):
            if not self.authenticate():
                return
            self.handle_delete_patient()
        elif self.path.startswith('/delete_health_record/'):
            if not self.is_user_admin():
                self.send_error(403, "Only admins can perform this action.")
                return
            self.handle_delete_health_record()
        
    
    

    def handle_register(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if not all(key in data for key in ['username', 'password', 'role', 'email', 'fullname']):
            self.send_error(400, 'Missing registration information')
            return

        user_id = auth_service.register_user(data['username'], data['password'], data['role'], data['email'], data['fullname'])

        if user_id:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "User registered successfully", "user_id": user_id}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(400, 'Registration failed')


    def log_message(self, format, *args):
        # Override to direct http.server logs to standard logging
        logging.info("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

    def send_error(self, code, message=None):
        # Customize error handling
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if message:
            self.wfile.write(json.dumps({'error': message}).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({'error': 'An error occurred'}).encode('utf-8'))

    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if 'username' not in data or 'password' not in data:
            self.send_error(400, 'Username and password are required')
            return

        user_id = auth_service.login_user(data['username'], data['password'])
        if user_id:
            token = auth_service.generate_token(user_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Login successful", "token": token}).encode('utf-8'))
        else:
            self.send_error(401, 'Invalid username or password')


if __name__ == '__main__':
    models.setup_database()
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    logging.info("Server started on localhost:8000")
    httpd.serve_forever()