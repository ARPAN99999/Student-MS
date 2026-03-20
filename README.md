# Student Management System (SMS) 🎓

A modern, comprehensive, and responsive Student Management System built with **Django 5.2.12**. This platform is designed to streamline academic operations for school and college campuses, providing dedicated portals for Administrators, Staff, and Students.

## ✨ Features

-   **Admin Dashboard:** Oversee the entire institution, manage staff, students, courses, and sessions.
-   **Staff Portal:** Manage attendance, update results, and handle leave applications.
-   **Student Portal:** View attendance history, check results, and apply for leave.
-   **Modern UI:** Beautiful, light sky-blue theme with glass-morphism effects and responsive design.
-   **Real-time Tracking:** Attendance and performance analytics.
-   **Vercel Ready:** Pre-configured for seamless deployment on Vercel.

## 🚀 Tech Stack

-   **Backend:** Django 5.2.12
-   **Database:** SQLite (Development) / PostgreSQL (Production)
-   **Frontend:** HTML5, CSS3 (Flexbox/Grid), JavaScript
-   **Styles:** Google Fonts (Syne, DM Sans), Glass-morphism, Custom Animations.

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Snehasish-tech/Student-MS.git
    cd Student-MS
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Migration:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## 📦 Deployment

This project is optimized for deployment on **Vercel**. 
- `vercel.json` and `build_files.sh` are already included.
- Static files are managed via `Whitenoise`.

## 📄 License

This project is open-source. Feel free to use and modify it for your educational purposes.

---
Built with ❤️ by TEAM PLUTO
