# 🐾 Django Anipat

> A production-oriented Django blog platform built to explore modern backend development — from REST APIs and authentication to caching, background tasks, testing, Docker, CI/CD, and deployment.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.x-darkgreen)
![DRF](https://img.shields.io/badge/DRF-REST_API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Redis](https://img.shields.io/badge/Redis-Cache_%26_Broker-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-black)

## ✨ About

**Django Anipat** is more than a traditional Django blog.

It combines a user-facing blog with a REST API and a production-style backend architecture. The project demonstrates how a Django application can be developed, tested, containerized, optimized, and prepared for automated deployment.

The project covers the journey from:

**Django Application → REST API → Redis & Celery → Testing → Docker → Nginx & Gunicorn → CI/CD → Production**

---

## 🚀 Key Features

| Area | Features |
|---|---|
| 📝 **Blog** | Posts, categories, tags, comments, search, pagination, popular posts, view counter |
| 👤 **Authentication** | Custom user model, email login, registration, logout, permissions, profiles |
| 🔐 **API Security** | JWT, Token, Session and Basic authentication |
| 🔌 **REST API** | CRUD endpoints, ViewSets, filtering, searching and ordering |
| 📚 **API Docs** | Swagger / drf-yasg |
| ⚡ **Caching** | Redis-backed caching for frequently accessed data |
| 📬 **Background Tasks** | Celery workers and welcome emails |
| ⏰ **Scheduled Tasks** | Celery Beat + django-celery-beat |
| 🐘 **Database** | PostgreSQL with persistent Docker storage and health checks |
| 📈 **Load Testing** | Locust master/worker architecture and authenticated API testing |
| 🧪 **Quality** | pytest, pytest-django, Black and Flake8 |
| 🐳 **Containers** | Docker and Docker Compose |
| 🌐 **Production** | Gunicorn + Nginx reverse proxy |
| 🔄 **CI/CD** | Automated testing and deployment with GitHub Actions |

---

## 🏗️ Architecture

```text
                         ┌─────────────┐
                         │   Client    │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │    Nginx    │
                         └──────┬──────┘
                                │
                                ▼
                     ┌──────────────────┐
                     │ Gunicorn / Django│
                     └──────┬─────┬─────┘
                            │     │
                  ┌─────────┘     └──────────┐
                  ▼                          ▼
           ┌────────────┐             ┌────────────┐
           │ PostgreSQL │             │   Redis    │
           │  Database  │             │Cache/Broker│
           └────────────┘             └─────┬──────┘
                                           │
                                  ┌────────┴────────┐
                                  ▼                 ▼
                            ┌───────────┐     ┌───────────┐
                            │  Celery   │     │Celery Beat│
                            │  Worker   │     │ Scheduler │
                            └───────────┘     └───────────┘
```

---

## 🧰 Tech Stack

**Backend**

`Python` · `Django` · `Django REST Framework`

**Database & Infrastructure**

`PostgreSQL` · `Redis` · `Celery` · `Celery Beat`

**Authentication & API**

`SimpleJWT` · `Django Auth` · `Swagger`

**Testing & Performance**

`pytest` · `pytest-django` · `Locust` · `Black` · `Flake8`

**DevOps**

`Docker` · `Docker Compose` · `Nginx` · `Gunicorn` · `GitHub Actions`

---

## 🔄 CI/CD Pipeline

Every push or pull request to `main` goes through automated quality checks:

```text
Push / Pull Request
        │
        ▼
   Build Docker
        │
        ▼
 PostgreSQL + Redis
        │
        ▼
 Django Migrations
        │
        ▼
 Django System Check
        │
        ▼
 Black + Flake8
        │
        ▼
      pytest
        │
        ▼
   Tests Passed?
        │
       YES
        │
        ▼
     Deploy
```

Deployment only proceeds after the test pipeline succeeds.

---

## 🐳 Production Stack

The production environment runs as independent Docker services:

```text
nginx
backend (Django + Gunicorn)
postgres
redis
celery_worker
celery_beat
migrate
```

PostgreSQL and Redis remain inside the Docker network and are not directly exposed publicly.

Nginx acts as the public entry point and forwards application traffic to Gunicorn.

---

## 💡 What This Project Demonstrates

This repository isn't only about implementing blog features. It demonstrates practical backend engineering concepts including:

- RESTful API design
- Authentication and authorization
- Custom Django users
- PostgreSQL integration
- Redis caching
- Asynchronous processing
- Scheduled background jobs
- Docker networking
- Persistent volumes
- Reverse proxies
- Application servers
- Load testing
- Automated testing
- Code quality checks
- Environment-based secrets
- CI/CD
- Production-oriented deployment

---

## 📁 Environment Separation

The project uses separate Docker configurations for different environments:

```text
docker-compose.yml          → Development
docker-compose-stage.yml    → Staging / testing
docker-compose-prod.yml     → Production
```

Sensitive production configuration is provided through environment variables rather than committed to the repository.

---

## 🎯 Project Goal

The goal of Django Anipat is to practice building a Django application beyond basic CRUD functionality and understand the surrounding infrastructure required to operate a modern backend application.

It brings together **application development, API design, performance, testing, infrastructure, and deployment** in one project.
