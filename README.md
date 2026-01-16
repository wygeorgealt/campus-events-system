# Festejo - University Event Management System

**Festejo** is a modern, social event platform designed for university campuses. It allows students to discover events, purchase tickets, and connect with their campus community.

![Festejo Banner](example/events/static/events/images/wordlogo.png)

## 🚀 Features

*   **Event Discovery**: personalized feed of paid and free campus events.
*   **Ticketing System**: Secure digital ticketing with PDF downloads.
*   **User Profiles**: Track ticket history, event attendance, and user stats.
*   **Event Management**: Organizers can create, manage, and track event signups.
*   **Modern UI**: Built with Tailwind CSS for a premium, responsive "glassmorphism" aesthetic.
*   **NoSQL Database**: Powered by MongoDB for flexible data storage.

## 🛠 Tech Stack

*   **Backend**: Django 6.0 (Python 3.14)
*   **Database**: MongoDB (via `django-mongodb-backend`)
*   **Frontend**: HTML5, Tailwind CSS
*   **Deployment**: Ready for Render/Railway (Gunicorn, WhiteNoise)

## 📦 Installation & Setup

Follow these steps to run the project locally.

### Prerequisites
*   Python 3.10+
*   MongoDB Atlas Account (Database URI)

### 1. Clone the Repository
```bash
git clone https://github.com/wygeorgealt/campus-events-system.git
cd campus-events-system
git checkout phase1
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `example` directory (same level as `manage.py` or inside the inner project folder depending on structure, for this project it is at `example/.env`):

```ini
DEBUG=True
SECRET_KEY=your_secret_key
allowed_hosts=localhost,127.0.0.1
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?appName=Cluster0
MONGODB_NAME=campus_db
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Seed the Database (Optional)
Populate the database with sample events and users (Note: requires an existing superuser or user).
```bash
python manage.py createsuperuser # Create admin first
python manage.py seed_events
```

### 7. Run the Server
```bash
python manage.py runserver
```
Visit `http://localhost:8000` to view the app.

## 📂 Project Structure

*   `example/`: Main Django project configuration (`settings.py`, `urls.py`).
*   `events/`: Core application logic.
    *   `models.py`: Database schemas (Event, Ticket).
    *   `views.py`: Business logic and route handlers.
    *   `templates/events/`: HTML templates.
    *   `static/`: CSS, Images, and Favicons.
*   `requirements.txt`: Python dependencies.
*   `build.sh`: Deployment script.

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
