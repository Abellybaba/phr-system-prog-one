# routes/patients.py

from http.server import BaseHTTPRequestHandler
from app.services import auth_service
from app.services import patient_service
import json

class PatientHandler:
    def handle_add_patient(self):
        length = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(length))
        patient_id = patient_service.add_patient(post_data['user_id'], post_data['assigned_doctor_id'], post_data['date_of_birth'], post_data['gender'], post_data['phone_number'], post_data['emergency_contact'])
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'message': 'Patient added', 'patient_id': patient_id}
        self.wfile.write(json.dumps(response).encode())
        pass

    def handle_update_patient(self, patient_id):
        length = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(length))
        patient_service.update_patient(patient_id, post_data['assigned_doctor_id'], post_data['date_of_birth'], post_data['gender'], post_data['phone_number'], post_data['emergency_contact'])
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'message': 'Patient updated'}
        self.wfile.write(json.dumps(response).encode())
        pass

    def handle_delete_patient(self):
        # Implementation of deleting a patient
        pass

    def handle_get_patient(self):
        # Implementation of retrieving patient details
        # Extract patient ID from the URL
        patient_id = int(self.path.split('/')[-1])
        patient = patient_service.get_patient(patient_id)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(patient).encode('utf-8'))
        pass
    
    def handle_get_all_patients(self):
        patients = patient_service.get_all_patients()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'patients': patients}).encode())

    def handle_get_patient_by_id(self, patient_id):
        patient = patient_service.get_patient_by_id(patient_id)
        if patient:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'patient': patient}).encode())
        else:
            self.send_error(404, 'Patient not found')