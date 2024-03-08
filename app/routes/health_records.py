# routes/health_records.py
import json
from http.server import BaseHTTPRequestHandler
from app.services import auth_service
from app.services import health_record_service

class HealthRecordHandler:
    def handle_add_health_record(self):
        if not self.authenticate():
            return
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        # Assuming the data includes patient_id, record_type, summary, detailed_record_link
        record_id = health_record_service.add_health_record(data['patient_id'], data['record_type'], data['summary'], data['detailed_record_link'], self.user_id)
        
        if record_id:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Health record added successfully", "record_id": record_id}).encode('utf-8'))
        else:
            self.send_error(400, 'Failed to add health record')
        pass

    def handle_update_health_record(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        health_record_service.update_health_record(data['record_id'], data['patient_id'], data['record_type'], data['summary'], data['detailed_record_link'], data['created_by_doctor_id'])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Health record updated successfully"}).encode('utf-8'))

        pass

    def handle_delete_health_record(self):
        record_id = self.path.split('/')[-1]
        health_record_service.delete_health_record(record_id)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Health record deleted successfully"}).encode('utf-8'))

        pass

    def handle_get_health_record(self):
        record_id = self.path.split('/')[-1]
        record = health_record_service.get_health_record_by_id(record_id)

        if record:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(record).encode('utf-8'))
        else:
            self.send_error(404, "Health record not found")
        
        pass

    def handle_get_all_health_records(self):
        records = health_record_service.get_health_records()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(records).encode('utf-8'))
        pass
