# routes/doctors.py

import json
from http.server import BaseHTTPRequestHandler
from app.services import auth_service
from app.services import doctor_service
from app.services import patient_service

class DoctorHandler:
    def handle_add_doctor(self):
        # Implementation of adding a doctor
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        required_fields = ['user_id', 'department_id', 'specialty', 'years_of_experience', 'contact_info']
        if not all(field in data for field in required_fields):
            self.send_error(400, 'Missing data for doctor creation')
            return

        user_id = data['user_id']
        if not auth_service.is_admin(user_id):
            self.send_error(403, 'Only admins can add doctors')
            return

        doctor_id = doctor_service.add_doctor(data['user_id'], data['department_id'], data['specialty'], data['years_of_experience'], data['contact_info'])

        if doctor_id:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Doctor added successfully", "doctor_id": doctor_id}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(500, 'Failed to add doctor')
        pass

    def handle_update_doctor(self):
        # Implementation of updating a doctor
        pass

    def handle_delete_doctor(self):
        # Implementation of deleting a doctor
        pass

    def handle_get_doctor(self):
        # Implementation of getting a doctor's details
        pass
    
    # Handler for assigning a doctor to a patient
    def handle_assign_doctor(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        success = patient_service.assign_doctor(data['patient_id'], data['doctor_id'])
        
        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Doctor assigned successfully"}).encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Failed to assign doctor"}).encode('utf-8'))
            pass