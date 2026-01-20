# Project Context & Architecture

> **Note**: This document serves as the source of truth for AI agents and developers to understand the high-level context of the Battle Score backend. Please keep it updated as the architecture evolves.

## 1. System Overview
*   **Goal**: Backend for Battle Score, a platform to manage tournament participants (invite, team, role, ...), and matches (score, ordering, classment, ...).
*   **Main features**:
    *   **Authentication**: signup/signout with email, password and pseudo. Anonymous login is possible through a qrcode linked to a specific team and provided by the tournament admin.
    *   **Profile**: update pseudo, email, password.
    *   **Tournament**: create/update/delete tournaments, invite participants, define participant roles and teams.
    *   **Match**: create/update/delete matches, define match scores, define match ordering, define team classment.

## 2. Architecture
*   **Type**: Modular Monolith (Django).
*   **Key Applications**:
    *   `core`: Settings
    *   `billing`: Invoice generation
    *   `payment`: Subscriptions management (plans, payments, ...)
    *   `user`: Individual customers (email, password) and profiles (pseudo, avatar, ...)
    *   `tournament`: Tournament management (teams, matches, scores, ...)

## 3. Tech Stack & Conventions
*   **Framework**: Django (Python) with websockets (channels).
*   **Web**: Django Form (jinja) with HTMX and tailwindcss.
*   **API**: Django Rest Framework (DRF).
*   **Server**: uWSGI.
*   **Database**: PostgreSQL (inferred from file list).
*   **Testing**: `pytest` (via Django manage.py test).
*   **Task Queue**: RQ (via django-rq)
*   **Coding Standards**:
    *   Service layer pattern for business logic
    *   Fat models, thin views
    *   Tests are using a factory and mockers

## 4. Business Rules & Glossary
*   **User**: a django user which is linked to a profile or a client depending on the type of user.
*   **Profile**: a private customer profile which is linked to a user.
*   **Client**: a billing profile (company, association, ...) which is linked to a user.
*   **Participant**: a user participating to a tournament with a role (admin, player, ...).
*   **Team**: a group of participants (0 or more users) linked to a tournament.
*   **Tournament**: a tournament with all its settings (name, nb teams, nb players per team, location, datetime, ...).
*   **Match**: a match between two teams linked to a tournament with a score and an ordering.
*   **Score**: a score linked to a match.
*   **Ordering**: an ordering linked to a match.
*   **Classment**: a classment linked to a team.

## 5. Environment & Deployment
*   **Infrastructure**: Docker, CleverCloud, github.
*   **CI/CD**: github actions.
*   **Command runner**: just.