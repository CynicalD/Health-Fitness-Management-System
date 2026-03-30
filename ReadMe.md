
# Health & Fitness Club Management System

## Project Overview

This project is a command-line Gym Management System built for managing core health club operations.
It supports three user roles:

- Member: register, update profile, record health metrics, and register for group classes.
- Trainer: view personal class schedule and view members enrolled in trainer-owned classes.
- Admin: create new fitness classes and update existing class details.

The system connects to a PostgreSQL database and enforces key workflow checks such as:

- unique member/trainer emails,
- class capacity limits,
- duplicate class-registration prevention,
- trainer ownership validation when viewing class member lists.

Database artifacts include schema creation, sample seed data, and an ERD file in the docs folder.

## Technologies Used

- Python 3
- psycopg2 (PostgreSQL database adapter for Python)
- PostgreSQL
- SQL (DDL, DML, view and index definitions)
- Command-line interface (CLI)

## Operations Implemented

### Member

- User registration
- Profile management
- Health history/metrics tracking
- Group class registration

### Trainer

- Member lookup within trainer-owned classes
- Schedule view

### Admin

- Class management (create and update fitness classes)
- Room assignment through class creation workflow

## Prerequisites

- Python 3
- PostgreSQL
- pip

## Setup

Because this project uses psycopg2, create and activate a virtual environment first:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install psycopg2-binary
```

## Create and Populate Database

```bash
createdb gym_management
psql -d gym_management -f sql/DDL.sql
psql -d gym_management -f sql/DML.sql
```

## Run the Application

```bash
python app/app.py
```

You will see the role-based CLI menu. Choose a role and follow the prompts to test the operations.