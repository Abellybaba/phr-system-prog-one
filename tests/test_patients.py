import unittest
from app.services import patient_service

class TestPatientService(unittest.TestCase):

    def test_add_patient(self):
        patient_id = patient_service.add_patient(1, '1980-01-01', 'male', '1234567890', 'emergency_contact_info')
        self.assertIsNotNone(patient_id)

    # Adding more tests for update, delete, and retrieval of patients

if __name__ == '__main__':
    unittest.main()
