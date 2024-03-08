Personal Health Record (PHR) System User Guide
Overview
This guide provides instructions for end-users on how to effectively use the Personal Health Record (PHR) system. It aims to help patients and healthcare providers navigate the system, manage health records, and utilize available features.

Table of Contents
Introduction
Getting Started
User Account Management
Registration
Login
Profile Management
Health Records
Viewing Health Records
Adding Health Records (For Doctors)
Updating Health Records (For Doctors)
Deleting Health Records (For Doctors)
Search Functionality
Notifications
Data Visualization
FAQs
Troubleshooting
Contact Support

1. Introduction
   Overview
   The Personal Health Record (PHR) system is designed to store and manage health-related information, allowing patients and healthcare providers to access, update, and manage medical data effectively. The system facilitates improved communication between patients and doctors, enhances the efficiency of health record management, and supports better health outcomes through informed decision-making.

Purpose
The PHR system aims to:

Provide patients with easy access to their health information.
Allow healthcare providers to view and update patient records, ensuring accurate and up-to-date health data.
Enable secure communication and data exchange within the healthcare ecosystem.
Benefits
For Patients:

Access health records anytime, anywhere.
Track health progress and understand health trends.
Take a more active role in personal healthcare.
For Healthcare Providers:

Access patient health records quickly, facilitating better patient care.
Update health records in real-time, ensuring data accuracy.
Enhance collaboration among healthcare team members.

2. Getting Started
   System Requirements
   To run the PHR system locally, you'll need the following:

Python 3.x installed on your machine.
Local or virtual environment setup for Python.
Dependencies installed, typically via a requirements file or pip install.
SQLite or similar DBMS if you're handling the database locally.
Running the System Locally
Clone the Repository: Clone the PHR system's repository to your local machine using Git.

bash
Copy code
git clone https://github.com/your-repo/phr-system.git
cd phr-system
Environment Setup: Set up a Python virtual environment and activate it (optional but recommended).

bash
Copy code
Install Dependencies: Prebuilt libraries

bash
Copy code
pip install -r requirements.txt

Initialize the Database: Run the script to set up your database. This usually involves creating tables and possibly seeding data.

python server.py

Run the Server: Start the local server.
python server.py

Using Postman for API Testing
Install Postman: Download and install Postman from their website.

Start a New Request: Open Postman and start a new request by clicking on the "New" button and selecting "Request."

Set Request Details:

For the URL, use http://localhost:8000/ followed by the endpoint path. For example, to access the login endpoint, use http://localhost:8000/login.

Select the HTTP method (GET, POST, PUT, DELETE) according to the action you want to perform.
Add any necessary headers, such as Content-Type: application/json for JSON requests.
If you're sending data (like in a POST request), switch to the "Body" tab, select "raw", and enter your JSON.

Send Request and View Response: Click the "Send" button to make the request and view the response in the lower section of Postman.

Postman Example: Register
Set the method to POST and URL to http://localhost:8000/register.
Under the "Body" tab, select "raw" and input the JSON payload with your credentials:
json
Copy code
{
"username": "johndoe",
"password": "securepassword"
}

Postman Example: Logging In
Set the method to POST and URL to http://localhost:8000/login.
Under the "Body" tab, select "raw" and input the JSON payload with your credentials:
json
{
"username": "johndoe",
"password": "securepassword"
}
Hit "Send" to see the response, which should include an authentication token if the login is successful.

Responds example: {
"message": "Login successful",
"token": "KmWjzXW917zIQSY2PK9o8rZ-TdfpIoSmkbq5QU6ciJQ"
}

3. User Account Management
   Registration
   To create a new account in the PHR system, you need to provide necessary user details.

Curl Command Example:
curl -X POST http://localhost:8000/register \
-H "Content-Type: application/json" \
-d '{
"username": "newuser",
"password": "newpassword",
"role": "patient",
"email": "newuser@example.com",
"fullname": "New User"
}'
This command sends a POST request to the /register endpoint with a JSON payload containing the new user's information.

Login
Users can log in to the system using their credentials. Upon successful login, the system will return an authentication token.

Curl Command Example:

curl -X POST http://localhost:8000/login \
-H "Content-Type: application/json" \
-d '{
"username": "newuser",
"password": "newpassword"
}'
This command sends a POST request to the /login endpoint with the username and password. The response includes a token that should be used for subsequent authenticated requests.

Profile Management
Users can update their profile information using an API endpoint. Let's assume there's an endpoint /update_profile that allows users to update their email and fullname.

Curl Command Example:

curl -X PUT http://localhost:8000/update_profile \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{
"email": "updateduser@example.com",
"fullname": "Updated User"
}'
Replace YOUR_ACCESS_TOKEN with the token received upon login. This command sends a PUT request to update the user's profile information.

4. Health Records
   Viewing Health Records
   Patients can view their own health records.
   Doctors can view health records of their patients.
   Curl Command Example to View Health Records (for a Patient):
   curl -X GET http://localhost:8000/health_records \
   -H "Authorization: Bearer ACCESS_TOKEN"
   Replace PATIENT_ACCESS_TOKEN with the actual access token of the patient.

Adding Health Records (For Doctors)
Only doctors can add health records.
Curl Command Example to Add a Health Record (for a Doctor):
bash
Copy code
curl -X POST http://localhost:8000/add_health_record \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ACCESS_TOKEN" \
-d '{"patient_id": 1, "record_type": "General Checkup", "summary": "Annual physical examination", "detailed_record_link": "http://example.com/records/1", "created_by_doctor_id": 2}'
Replace DOCTOR_ACCESS_TOKEN with the actual access token of the doctor.

Updating Health Records (For Doctors)
Only doctors can update health records.
Curl Command Example to Update a Health Record (for a Doctor):
bash
Copy code
curl -X PUT http://localhost:8000/update_health_record/RECORD_ID \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ACCESS_TOKEN" \
-d '{"patient_id": 1, "record_type": "Updated Record Type", "summary": "Updated summary", "detailed_record_link": "http://example.com/updated_link", "created_by_doctor_id": 2}'
Replace RECORD_ID and ACCESS_TOKEN with the actual record ID and doctor's access token, respectively.

Deleting Health Records (For Doctors)
Only doctors can delete health records.
Curl Command Example to Delete a Health Record (for a Doctor):

curl -X DELETE http://localhost:8000/delete_health_record/RECORD_ID \
-H "Authorization: Bearer ACCESS_TOKEN"

Replace RECORD_ID and ACCESS_TOKEN with the actual record ID and doctor's access token, respectively.

5. Search Functionality(FUTURE FEATURES)
   The PHR system offers robust search functionality, allowing users to quickly locate specific health records based on various criteria. This section outlines how patients and doctors can utilize search features.

Searching for Health Records
Both patients and doctors can search for health records. Patients can search within their records, while doctors can search across all patient records they have access to.

Curl Command Example to Search Health Records:

# Example of a doctor searching for health records by patient ID and record type

curl -X GET "http://localhost:8000/search_health_records?patient_id=1&record_type=General+Checkup" \
-H "Authorization: Bearer DOCTOR_ACCESS_TOKEN"
Replace DOCTOR_ACCESS_TOKEN with the doctor's actual access token. Adjust the query parameters (patient_id and record_type) based on your search criteria.

Advanced Search
The system should support advanced search queries, allowing users to combine multiple search parameters for more refined results.

Curl Command Example for Advanced Search: (FUTURE UPDATE)

# Example of an advanced search using multiple criteria

curl -X GET "http://localhost:8000/search_health_records?start_date=2021-01-01&end_date=2021-12-31&record_type=X-Ray" \
-H "Authorization: Bearer ACCESS_TOKEN"

Curl Documentation for Doctors, Patients, and Health Records

Doctors
Adding a Doctor
curl -X POST http://localhost:8000/add_doctor \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
-d '{"user_id": 1, "department_id": 2, "specialty": "Cardiology", "years_of_experience": 10, "contact_info": "doctor@example.com"}'

Getting a Doctor
curl -X GET http://localhost:8000/doctor/DOCTOR_ID \
-H "Authorization: Bearer ADMIN_ACCESS_TOKEN"

Updating a Doctor
curl -X PUT http://localhost:8000/update_doctor/DOCTOR_ID \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
-d '{"department_id": 2, "specialty": "General Practice", "years_of_experience": 12, "contact_info": "newemail@example.com"}'

Deleting a Doctor
curl -X DELETE http://localhost:8000/delete_doctor/DOCTOR_ID \
-H "Authorization: Bearer ADMIN_ACCESS_TOKEN"

Patients
Adding a Patient

curl -X POST http://localhost:8000/add_patient \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
-d '{"user_id": 3, "date_of_birth": "1980-01-01", "gender": "male", "phone_number": "1234567890", "emergency_contact": "0987654321"}'

Getting a Patient

curl -X GET http://localhost:8000/patient/PATIENT_ID \
-H "Authorization: Bearer ACCESS_TOKEN"

Updating a Patient

curl -X PUT http://localhost:8000/update_patient/PATIENT_ID \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ACCESS_TOKEN" \
-d '{"date_of_birth": "1980-02-01", "gender": "male", "phone_number": "1234567891", "emergency_contact": "0987654322"}'

Deleting a Patient

curl -X DELETE http://localhost:8000/delete_patient/PATIENT_ID \
-H "Authorization: Bearer ADMIN_ACCESS_TOKEN"

Health Records
Adding a Health Record

curl -X POST http://localhost:8000/add_health_record \
-H "Content-Type: application/json" \
-H "Authorization: B
