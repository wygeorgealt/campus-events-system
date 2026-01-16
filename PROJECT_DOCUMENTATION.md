# Software Development Lifecycle Project Documentation
**Project Name:** Festejo - Campus Events System
**Course:** Software Engineering
**Academic Term:** 2025/2026
**Team:** [Your Team Name]

---

## Phase 1: Planning & Requirements Analysis

### 1.1 Project Charter

**Project Title:** Festejo - University Event Management System

**Project Description:**
Festejo is a centralized, web-based platform designed to streamline the discovery, creation, and management of university events. It empowers students to find and register for campus activities while providing organizers with tools to manage attendees, ticketing, and promotion.

**Objectives and Scope:**
- **Centralized Event Hub:** A single location for all campus events (academic, social, sports).
- **Ticketing System:** Secure digital ticketing with unique QR/ID verification.
- **Community Engagement:** Foster campus connection through easier access to events.
- **Scope:** The initial phase covers user authentication, event creation, browsing, paid/free ticket registration, and a calendar view.

**Stakeholders:**
- **Students:** Primary users attending events.
- **Event Organizers:** specific users (clubs, departments) creating events.
- **Administrators:** System oversight.
- **University Management:** Campus life oversight.

**Success Criteria:**
- Functional user registration and login.
- Successful creation and display of events.
- Accurate ticket generation and persistence.
- Responsive design on mobile and desktop.

**Resources:**
- Python/Django Framework
- MongoDB Database
- Tailwind CSS for frontend
- Render for cloud deployment

### 1.2 Requirements Specification

**Target Users:**
- University Students (Guests/Registered)
- Campus Organizations

**Functional Requirements:**
1.  **User Authentication:** Users must be able to sign up, log in, and log out securely. (Priority: Must-have)
2.  **Event Feed:** Display a list of upcoming events with images and summaries. (Must-have)
3.  **Event Detail:** Detailed view of event description, time, location, and price. (Must-have)
4.  **Registration/Ticketing:** Users can register for free or paid events and receive a digital ticket. (Must-have)
5.  **Event Creation:** Authorized users can create new events with details and images. (Should-have)
6.  **My Tickets:** Users can view a history of their registered events and tickets. (Should-have)
7.  **Ticket Verification:** Organizers can verify ticket validity using a unique Ticket ID. (Should-have)
8.  **Calendar View:** Visual calendar of upcoming events. (Could-have)
9.  **User Profile:** Users can manage their personal details. (Could-have)
10. **Search/Filter:** Users can filter events by type (Free/Paid). (Could-have)

**Non-functional Requirements:**
- **Security:** Passwords must be hashed; sensitive data protected.
- **Performance:** Pages should load within 2 seconds under normal load.
- **Usability:** Interface must be responsive and intuitive (Glassmorphism design).
- **Scalability:** System should handle concurrent registrations.

---

## Phase 2: System Design

### 2.1 System Architecture

**Architecture Overview:**
The system follows a **Model-View-Template (MVT)** architectural pattern, standard for Django applications.
- **Model:** Defines the data structure (Event, Ticket, User) and interacts with MongoDB.
- **View:** Handles business logic and routes requests to appropriate templates.
- **Template:** Renders the user interface using HTML5 and Tailwind CSS.

**Technology Stack:**
- **Backend:** Django 6.0 (Python) - Robust, secure, and rapid development.
- **Database:** MongoDB (via `django-mongodb-backend`) - Flexible schema for varying event details.
- **Frontend:** HTML5, Tailwind CSS - Modern, responsive styling.
- **Deployment:** Render (PaaS) - Scalable and easy to configure.

### 2.2 Database Design

**Schema Overview:**
The system uses a NoSQL document structure managed by Django ORM.

**Key Models (Entities):**

1.  **User (django.contrib.auth)**
    - Standard Django user attributes (username, password, email).

2.  **Event**
    - `id`: ObjectId (Primary Key)
    - `title`: String
    - `event_type`: Enum (FREE, PAID)
    - `price`: Decimal
    - `description`: Text
    - `capacity`: Integer
    - `organizer`: ForeignKey (User)
    - `event_date`: DateTime
    - `image`: ImageField

3.  **Ticket**
    - `id`: AutoField
    - `user`: ForeignKey (User)
    - `event`: ForeignKey (Event)
    - `ticket_id`: UUID (Unique String)
    - `purchase_date`: DateTime
    - `is_paid`: Boolean

**ER Diagram Description:**
- A **User** can create many **Events** (Organizer).
- A **User** can hold many **Tickets**.
- An **Event** can have many **Tickets** (Attendees).
- Relationship: User (1) ---- (*) Ticket (*) ---- (1) Event.

### 2.3 User Interface Design

**Design Rationale:**
The "Glassmorphism" aesthetic was chosen to appeal to the modern student demographic, featuring translucent cards, vivid gradients, and a clean layout to emphasize visual content (event images).

**Key Screens:**
- **Login/Signup:** Split screen with branding and form.
- **Feed:** Grid of event cards with "Book Now" actions.
- **Dashboard:** Sidebar navigation, ticket list, and profile settings.
- **Event Detail:** Large hero image, comprehensive info, and registration logic.

---

## Phase 3: Implementation

### 3.1 Source Code
*Code is provided in the accompanying repository/zip file.*

### 3.2 Implementation Report

**Technologies Used:**
- Integrated `django-mongodb-backend` for NoSQL support within Django's ORM.
- Used `Whitenoise` for static file serving in production.

**Key Algorithms/Patterns:**
- **Ticket Generation:** usage of `uuid.uuid4` to ensure globally unique non-guessable ticket IDs.
- **Authentication Flow:** Standard Django Auth adapted for a custom UI.

**Challenges & Solutions:**
- *Challenge:* MongoDB compatibility with Django's default relational assumptions.
  - *Solution:* Used the specific `django-mongodb-backend` engine and avoided unsupported relational features like complex joins where possible.
- *Challenge:* Deployment path issues on Render.
  - *Solution:* Restructured configuration (Project root `requirements.txt` and `Procfile`) to align with Render's build process.

---

## Phase 4: Testing & Quality Assurance

### 4.1 Test Plan
**Strategy:**
Hybrid approach using automated unit tests for core logic (Models) and manual functional testing for UI flows.

**Types of Testing:**
- **Unit Testing:** Validating Ticket creation and ID generation.
- **Functional Testing:** verifying the "Happy Path" of registering for an event.
- **Integration Testing:** Ensuring the database persists data correctly from the frontend.

### 4.2 Test Cases (Sample)

| ID | Description | Preconditions | Steps | Expected Result | Status |
|----|-------------|---------------|-------|-----------------|--------|
| TC1 | User Signup | None | Enter valid email/pass | Account created, redir to Feed | Pass |
| TC2 | Create Event | Logged in | Fill form, submit | Event appears on Feed | Pass |
| TC3 | Bookmark Event | Logged in | Click bookmark icon | Icon changes state | Pass |
| TC4 | Ticket Gen | Registered | Check "My Tickets" | Ticket with UUID visible | Pass |

---

## Phase 5: Deployment & Documentation

### 5.1 Deployment Guide (Render)

**Prerequisites:**
- GitHub Repository connected to Render.
- MongoDB Atlas Cluster URI.

**Steps:**
1.  **Push Code:** Ensure `requirements.txt`, `runtime.txt`, and `Procfile` are in the root.
2.  **Create Service:** New Web Service on Render > Connect Repo.
3.  **Environment Variables:** Set `MONGODB_URI`, `SECRET_KEY`, `DEBUG=False`.
4.  **Build Command:** `pip install -r requirements.txt`.
5.  **Start Command:** `gunicorn example.wsgi`.

### 5.2 User Manual

**Getting Started:**
1.  Navigate to the homepage.
2.  Click "Sign Up" to create an account.
3.  Browse the "Event Feed" to see what's happening.

**Registering for an Event:**
1.  Click on an event card.
2.  Review details and click "Get Ticket".
3.  Confirm registration.
4.  Navigate to "My Tickets" to view your entry pass.

---

## Phase 6: Project Presentation

*[This section contains points for the live presentation]*

- **Introduction:** The problem of fragmented campus event info.
- **Demo:** Walkthrough of Signup -> Discovery -> Registration flow.
- **Tech Highlight:** Running Django on MongoDB.
- **Future Work:** Mobile App adaptation, Payment Gateway integration, Social features (comments/likes).
