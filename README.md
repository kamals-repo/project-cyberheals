# Django User Management System

A Django-based RESTful API for managing users, roles, and authentication using JWT. Supports role assignment, custom user model, email notifications, Celery integration, and admin-restricted endpoints.

---

## Features

- Custom user model with email & username validation
- JWT Authentication (via SimpleJWT)
- Role-based access control (Admin, Manager, Staff)
- User self and admin update/delete support
- User registration with conditional permissions:
  - Admin users can register without authentication
  - Staff/Regular users must be created by an authenticated admin
- Email notifications (SMTP integrated)
- Celery + RabbitMQ setup for async tasks
- Hourly admin summary task via Celery Beat

---

##  Tech Stack

- **Django** 5.1
- **Django REST Framework**
- **SimpleJWT** for authentication
- **Celery** with **RabbitMQ** broker
- **MySQL** (or any DB configured via `.env`)
- **django-environ** for environment variable management

---


