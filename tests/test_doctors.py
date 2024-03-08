import unittest
from app.services import doctor_service

class TestDoctorService(unittest.TestCase):

    def test_add_doctor(self):
        doctor_id = doctor_service.add_doctor(1, 2, 'Cardiology', 10, 'contact@example.com')  # Add sample data
        self.assertIsNotNone(doctor_id)

    # Adding more tests for update, delete, and retrieval of doctors

if __name__ == '__main__':
    unittest.main()
