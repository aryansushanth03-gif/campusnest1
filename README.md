# CampusNest - NoBroker-Style Student Hostel & Roommate Listing Portal

A modern, responsive, 100% zero-brokerage web application designed specifically for university students and hostel/PG owners. It connects students directly with property owners and fellow students looking for flatmates without any broker commissions, token visiting fees, or middlemen.

Built with **Django + HTML5 + CSS3 + Bootstrap 5.3 + JavaScript + SQLite / MySQL**.

---

## 🌟 Key Features

### 1. 0% Brokerage Direct Connect (NoBroker Architecture)
- **Direct Owner Connect**: Students unlock property owner calling numbers and trigger pre-composed WhatsApp messages directly.
- **Schedule a Free Visit**: In-app scheduler with date and time slots (Morning, Afternoon, Evening) for in-person or parent inspections.
- **Owner Visit Manager**: Owners can view, accept, decline, or mark student visits as completed from their dashboard.

### 2. Student Hostel & PG Engine
- **Room Occupancy Types**: Single, Double Sharing, Triple Sharing, 4+ Sharing, Full Flat.
- **Gender Filter**: Boys Only, Girls Only, Co-ed / Unisex.
- **Campus Proximity Indicator**: Proximity (KM) to colleges, universities, and nearest metro/bus stops.
- **Mess & Food Facilities**: 3 meals included, 2 meals, breakfast only, pure veg vs veg/non-veg, or self-cooking kitchen access.
- **Curfew & House Rules**: Detailed curfew hours, visitor policies, and quiet hours.
- **Amenities Checklist**: High-speed Wi-Fi, AC, Attached Washroom, Geyser, Power Backup, Laundry, CCTV, Study Desk, Biometric Entry, etc.
- **Multi-image Gallery**: Featured cover photo + additional room photos.

### 3. Roommate & Flatmate Finder
- **Student Profile Matching**: Students looking for a room or students who have an extra bed in a flat.
- **Lifestyle & Habit Tags**:
  - Sleep Routine: *Early Bird* vs *Night Owl* vs *Flexible*
  - Diet: *Vegetarian* vs *Non-Veg* vs *Eggetarian*
  - Smoking: *Strictly Non-Smoker* vs *Balcony Only*
  - Study Atmosphere: *Quiet & Focused* vs *Balanced* vs *Social*
- **Target Budget**: Monthly budget range per student.
- **Direct WhatsApp Chat**: Instant connect with student seekers.

### 4. Smart Search, Dynamic Filter & Sorting
- Search by College name, Locality, or City.
- Multi-facet filters: Budget slider, gender pills, room sharing, meals included, and amenities checkboxes.
- Sorting options: Price (Low to High / High to Low), Distance to Campus, Recently Added.

### 5. Verified Community & Safety
- Student College verification tags and Host verification badges.
- Verified student reviews with multi-category ratings (Cleanliness, Food, Safety).
- "Report Listing" modal to flag brokers posing as owners, fake photos, or misleading prices.

### 6. User Roles & Unified Dashboard
- **Role-Based Onboarding**: Student Seeker vs Hostel Owner.
- **Owner Dashboard**: Manage listings (Create, Edit, Toggle Live/Inactive, Delete), track incoming student visit requests.
- **Student Dashboard**: Saved wishlist properties, scheduled visit bookings, my roommate posts.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Virtual environment (`venv`)

### 1. Activate Virtual Environment
On Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```
On macOS/Linux:
```bash
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations & Seed Sample Data
The project includes a ready-to-use seed command that populates verified hostels near Delhi University, IIT Bombay, Christ University Bangalore, and Fergusson College Pune:
```powershell
python manage.py migrate
python manage.py seed_data
```

### 4. Start the Development Server
```powershell
python manage.py runserver
```
Visit: **`http://127.0.0.1:8000/`**

---

## 🔑 Demo User Accounts (Pre-Seeded)

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Full Django Admin (`/admin/`) access |
| **Owner** | `sharma_hostels` | `owner123` | Verified Owner (Oxford Scholar Boys PG, DU) |
| **Owner** | `stanza_nest` | `owner123` | Verified Owner (Lotus Haven Girls Hostel, Bangalore) |
| **Student** | `aarav_du` | `student123` | Verified DU Student (Hindu College) |
| **Student** | `ananya_iit` | `student123` | Verified IIT Bombay Student |

---

## 🗄️ Database Configuration (SQLite vs MySQL)

By default, the project runs on **SQLite** for zero-configuration, instant local execution.

To switch to **MySQL**:
1. Open `campusnest_project/settings.py`.
2. Change `USE_MYSQL = True`:
   ```python
   USE_MYSQL = True
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'campusnest_db',
           'USER': 'root',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'charset': 'utf8mb4',
           },
       }
   }
   ```
3. Create database in MySQL:
   ```sql
   CREATE DATABASE campusnest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
4. Run migrations:
   ```powershell
   python manage.py migrate
   python manage.py seed_data
   ```

---

## 🧪 Running Automated Tests

Run the test suite across all modules:
```powershell
python manage.py test
```

---

## 📁 Project Structure

```
d:/nobrokerproject/
│
├── campusnest_project/        # Core Django configuration (settings, root urls)
├── accounts/                  # User accounts, student/owner profiles, auth
├── listings/                  # Hostel & PG listings, amenities, reviews, visits
├── roommates/                 # Roommate & Flatmate finder module
├── dashboard/                 # Student and Owner dashboard management
│
├── templates/                 # Bootstrap 5.3 HTML templates
│   ├── base.html              # Base layout (navbar, footer, toast containers)
│   ├── home.html              # Homepage with hero search and featured stays
│   ├── accounts/              # Login, register, profile templates
│   ├── listings/              # List, detail, form, confirm delete
│   ├── roommates/             # Roommate cards list, detail, form
│   └── dashboard/             # Management dashboard
│
├── static/
│   ├── css/styles.css         # Modern styling & theme color variables
│   └── js/main.js             # AJAX wishlist, contact reveal, dynamic filters
│
├── media/                     # Uploaded hostel images and profile pictures
├── requirements.txt           # Python dependencies
└── manage.py                  # Django CLI management script
```
