# Management System

## Overview

Management System is a web application designed to facilitate the management of a psychology clinic. The system allows psychologists to register patients, track consultations, manage tasks, and store relevant patient data efficiently.

## Features

- **Patient Management:** Add, update, and view patient details, including contact information, complaints, and payment status.
- **Consultation Records:** Log consultations with details such as mood assessment, general notes, and video recordings.
- **Task Management:** Assign specific tasks to patients with predefined frequency options.
- **Data Visualization:** Generate mood trend charts based on past consultations.
- **Secure Access:** Ensure consultations are only accessible to paying patients.

## Technologies Used

- **Backend:** Django (Python)
- **Database:** SQLite (or configurable to PostgreSQL/MySQL)
- **Frontend:** HTML, CSS (Django templates)
- **Image Processing:** Pillow
- **Other Libraries:** Django Messages Framework

## Installation

### Clone the Repository

```sh
git clone https://github.com/yourusername/management-system.git
cd management-system
```

### Start the Server

```sh
python manage.py runserver
```

## Usage

- Navigate to `http://127.0.0.1:8000/` to access the patient management interface.
- Register new patients by providing their details and a profile photo.
- Add consultation records with mood tracking and video attachments.
- Assign and manage tasks for each patient.

## API Endpoints

| Endpoint                        | Method | Description                                                     |
| ------------------------------- | ------ | --------------------------------------------------------------- |
| `/`                             | GET    | View all patients                                               |
| `/<int:id>`                     | GET    | View a specific patient’s details                               |
| `/update_patient/<int:id>`      | POST   | Update a patient's payment status                               |
| `/delete_consultation/<int:id>` | POST   | Delete a consultation record                                    |
| `/public_consultation/<int:id>` | GET    | View a public consultation if the patient has an active payment |

## Observations
- IDE used: <a href="https://code.visualstudio.com/download">Visual Studio Code</a>.
- Database viewer used: <a href="https://github.com/qwtel/sqlite-viewer-vscode">SQLite Viwer for VS Code</a>.

