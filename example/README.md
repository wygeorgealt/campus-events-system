# Django MongoDB Backend - Project Template

This is a Django project starter template for the Django MongoDB Backend.
In order to use it with your version of Django: 

- Find your Django version. To do so from the command line, make sure you
  have Django installed and run:

```bash
django-admin --version
>> 6.0
```

## Create the Django project

From your shell, run the following command to create a new Django project
replacing the `{{ project_name }}` and `{{ version }}` sections. 

```bash
django-admin startproject {{ project_name }} --template https://github.com/mongodb-labs/django-mongodb-project/archive/refs/heads/{{ version }}.x.zip
```

For a project named `example` that runs on `django==6.0.*`
the command would look like this:

```bash
django-admin startproject example --template https://github.com/mongodb-labs/django-mongodb-project/archive/refs/heads/6.0.x.zip
```
##########################################################
This documentation is designed for a teammate who is stepping into the project with zero prior experience in Django or MongoDB. It covers everything from installation to the logic of how the system "thinks."

---

## 🚀 Project Overview

This is a **Campus Event System** built with **Django** (the Python web framework) and **MongoDB** (the database).

* **Django** acts as the brain: It handles users, URLs, and logic.
* **MongoDB** is the filing cabinet: It stores event details, user info, and tickets.

---

## 🛠 1. Environment Setup

Before running the code, you need to set up your "Virtual Environment." This keeps the project's tools separate from your computer's main settings.

1. **Open your terminal** in the project folder.
2. **Create the environment:**
```bash
python -m venv .venv

```


3. **Activate it:**
* *Windows:* `.venv\Scripts\activate`
* *Mac/Linux:* `source .venv/bin/activate`


4. **Install the "Ingredients":**
```bash
pip install django djongo pymongo pillow

```


*(Note: `djongo` is the bridge between Django and MongoDB; `pillow` handles event images.)*

---

## 🗄 2. Connecting the Database (MongoDB)

We use a library called **Djongo** to make Django talk to MongoDB.

In your `settings.py`, the configuration looks like this:

* **ENGINE**: `djongo`
* **NAME**: The name of your database (e.g., `campus_db`).
* **CLIENT**: If you are using a local MongoDB, it points to `localhost`.

### Essential Commands

Whenever the **Backend Lead** changes the "Models" (the database structure), you MUST run these two commands to update your local database:

1. `python manage.py makemigrations` (Prepares the changes).
2. `python manage.py migrate` (Actually applies the changes to MongoDB).

---

## 👤 3. Roles & The Admin Panel

Django comes with a built-in "God Mode" called the **Admin Panel**.

1. **Create your Admin account:**
```bash
python manage.py createsuperuser

```


2. **Access it:** Go to `http://127.0.0.1:8000/admin`.
3. **Roles:**
* **Staff/Superuser:** Can see the "Post Event" button and manage all tickets.
* **Regular User:** A student who can only see the feed, calendar, and their own tickets.



---

## 📂 4. Understanding the Project Folders

* **`example/`**: The main project folder (contains `settings.py` and `urls.py`).
* **`events/`**: Our specific app.
* **`models.py`**: Defines what an "Event" or "Ticket" looks like (title, date, price).
* **`views.py`**: The logic. It decides if a user should go to the Payment page or the Success page.
* **`templates/events/`**: The HTML files you will be editing.



---

## 🎟 5. The "Logic" Workflows

As a frontend user, you need to know how these three systems interact:

### A. Registration Logic

1. **Free Event:** User clicks "Join"  Backend creates a `Ticket`  Redirect to "My Registrations."
2. **Paid Event:** User clicks "Join"  Backend puts the Event ID in a "Session" (temporary memory)  Redirect to "Payment Page."

### B. The Ticket System

Each ticket is a unique link between a **User** and an **Event**.

* We use `uuid` (a long string of random letters/numbers) to make every ticket unique.
* **Frontend Tip:** Use `{{ ticket.ticket_id }}` to display the unique code on the UI.

---

## 🚦 6. Running the Project

To see the website live on your machine, always use this command:

```bash
python manage.py runserver

```

Then, open your browser and go to: `http://127.0.0.1:8000/`

---

## 🆘 Troubleshooting for Beginners

* **`TemplateDoesNotExist`**: You probably put the HTML file in the wrong folder. It must be inside `events/templates/events/`.
* **`NoReverseMatch`**: You used a link like `{% url 'calendar' %}` but forgot to add the path in `urls.py`.
* **Images not showing**: Make sure you have `MEDIA_URL` and `MEDIA_ROOT` configured in `settings.py`.
