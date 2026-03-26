# Medical Reminder App

A comprehensive desktop application designed to help patients manage their medication schedules, track medicine adherence, monitor side effects, and prevent dangerous drug interactions. This app reminds users when to take their medications and provides detailed health analytics.

## Features

### Core Medication Management
✅ **Medication Management**
- Add and manage medications with custom dosage information
- Set how many days you need to take each medication
- Configure daily frequency (times per day)
- Track medication stock quantity
- Store all medication details in a local database

✅ **Medicine Tracking**
- Record when medicines are taken
- Log dosage adherence patterns
- View all medications in one place
- Quick mark medicine as taken

### Analytics & Insights
✅ **Individual Medicine Adherence**
- Track compliance for each specific medicine
- View weekly and monthly adherence percentages
- Daily breakdown of adherence patterns
- Compare performance across medicines

✅ **Trends & Reports**
- Weekly adherence trends
- Monthly adherence trends
- Missed doses report with detailed breakdown
- Adherence patterns analysis

✅ **Streak Tracking**
- Monitor consecutive days of perfect adherence per medicine
- Track longest adherence streak
- View current streak for all medicines
- Visualize medication compliance streaks

✅ **Dashboard**
- Real-time viewing of overall adherence percentage
- Easy-to-use graphical interface
- Quick access to all medication information
- Health score calculation

### Safety & Health Management
✅ **Side Effects Tracker**
- Log and track side effects for each medicine
- Categorize side effects by severity (mild, moderate, severe)
- Record side effect dates
- View most common side effects across all medicines
- Track side effect patterns

✅ **Drug Interactions Checker**
- Warning system for dangerous drug combinations
- Check interactions before adding new medicines
- Categorize interactions by severity (low, moderate, high)
- Highlight high-severity interactions
- Track all potential interactions between current medications

✅ **Doctor's Notes**
- Add special instructions from your doctor for each medicine
- Store important medical notes
- Update notes as needed
- View all doctor's notes in one place
- Date-stamped notes for reference

### Stock & Refill Management
✅ **Medicine Refill Reminders**
- Track stock quantity for each medicine
- Automatic low-stock alerts (≤10 units)
- Estimate refill dates based on usage
- Visual status indicators (Critical/Low/OK)
- Quick refill shortcuts (Add 10/20 pills)

## Project Structure

```
medical-reminder/
├── main.py                        # Application entry point
├── README.md                      # Project documentation
├── LICENSE                        # Project license
├── analaysis/
│   ├── __init__.py
│   └── adherence.py              # Adherence calculation and analysis module
├── DATABASE/
│   ├── __init__.py
│   └── db.py                     # SQLite database management & queries
└── ui/
    ├── __init__.py
    ├── showall.py                # Main window & navigation hub
    ├── medice.py                 # Medicine entry form
    ├── adherence_window.py       # Mark medicine as taken
    ├── dashboard.py              # Dashboard with adherence overview
    ├── analytics_window.py       # Analytics & trends analysis
    ├── side_effects_window.py    # Side effects tracker
    ├── interactions_window.py    # Drug interactions manager
    ├── doctor_notes_window.py    # Doctor notes storage
    └── refill_reminders_window.py # Stock & refill management
```

## Requirements

- **Python 3.7+**
- **Tkinter** (usually included with Python)
- **SQLite3** (usually included with Python)

## Installation

1. Clone or download the project:
```bash
git clone https://github.com/yourusername/medical-reminder.git
cd medical-reminder
```

2. Ensure Python 3.7+ is installed:
```bash
python --version
```

3. Run the application:
```bash
python main.py
```

The app will create a `medications.db` file on first run to store all data locally.

## Database Schema

### Medicine Table
Stores information about each medication:
```
medicine(id, medicine_name, dosage, time, times_a_day, days_to_take, stock_quantity)
```
- **id**: Unique identifier
- **medicine_name**: Name of the medication
- **dosage**: Dosage amount (e.g., 500mg)
- **time**: Time to take (user note)
- **times_a_day**: Daily frequency
- **days_to_take**: Number of days for this course
- **stock_quantity**: Current pills/tablets in stock

### Adherence Table
Tracks compliance for each dose:
```
Adherence(id, med_id, date, taken)
```
- **id**: Unique identifier
- **med_id**: Reference to medicine table
- **date**: Date of the dose (YYYY-MM-DD)
- **taken**: 1 if taken, 0 if missed

### SideEffects Table
Logs side effects reported by user:
```
SideEffects(id, med_id, effect_name, severity, date_reported)
```
- **id**: Unique identifier
- **med_id**: Reference to medicine table
- **effect_name**: Name of the side effect
- **severity**: mild, moderate, or severe
- **date_reported**: When the side effect was reported

### DrugInteractions Table
Stores potential interactions between medicines:
```
DrugInteractions(id, med_id_1, med_id_2, interaction_desc, severity)
```
- **id**: Unique identifier
- **med_id_1**: First medicine ID
- **med_id_2**: Second medicine ID
- **interaction_desc**: Description of the interaction
- **severity**: low, moderate, or high

### DoctorNotes Table
Stores special instructions and notes:
```
DoctorNotes(id, med_id, note_text, date_added)
```
- **id**: Unique identifier
- **med_id**: Reference to medicine table
- **note_text**: Doctor's note or special instruction
- **date_added**: When the note was added


## Usage Guide

### 1. Add a Medication
- Click **"+ Add Medicine"**
- Enter medication name, dosage, and frequency
- Specify how many days you need to take it
- Enter initial stock quantity
- Click **Save**

### 2. Record Medicine Intake
- Click **"Mark Taken"**
- Select the medicine from the list
- Click confirm to log the dose
- The app records date and time automatically

### 3. View Analytics & Trends
- Click **"📊 Analytics"** to open Analytics window
- **By Medicine**: Select a specific medicine to see weekly/monthly adherence
- **Trends**: View adherence patterns over weeks and months
- **Missed Doses**: See detailed report of all missed doses
- **Streaks**: Monitor consecutive days of adherence for each medicine

### 4. Track Side Effects
- Click **"⚠️ Side Effects"** to open Side Effects Tracker
- Add side effect: Select medicine, enter effect name, choose severity
- View by medicine: See all side effects for a specific medication
- View most common: See the most frequently reported side effects

### 5. Check Drug Interactions
- Click **"💊 Interactions"** to open Interactions Manager
- Add interaction: Select two medicines and describe the interaction
- Check severity levels (Low/Moderate/High)
- **Check Medicine**: Select any medicine to see all its potential interactions
- **High Severity**: View critical interactions requiring doctor review

### 6. Add Doctor Notes
- Click **"📝 Doctor Notes"** to open Notes Manager
- Add note: Select medicine and type special instructions
- Edit/Update: Modify existing notes as needed
- View all: See notes for all medicines in one place
- Delete: Remove outdated notes

### 7. Manage Stock & Refills
- Click **"🔔 Refill Reminders"** to open Stock Manager
- Update stock: Select medicine and enter new quantity
- Quick refill: Add 10 or 20 pills instantly
- Low stock alerts: Get warnings for medicines ≤10 units
- Refill dates: See estimated when each medicine runs out

### 8. Dashboard
- View overall adherence percentage at the top
- Automatically updates when you record doses
- Click refresh to see latest statistics

## Key Statistics

The app calculates:
- **Overall Adherence**: Percentage of all doses taken vs prescribed
- **Per-Medicine Adherence**: Individual compliance for each medication
- **Weekly/Monthly Trends**: Adherence patterns over time
- **Current Streak**: Consecutive days of perfect adherence
- **Health Score**: Overall medication compliance metric
- **Refill Days**: Estimated days until medicine runs out

## How It Works

### Data Storage
- **Local Database**: All data is stored locally using SQLite (medications.db)
- **No internet required**: Complete privacy and data control
- **Five tables**: Medicine, Adherence, SideEffects, DrugInteractions, DoctorNotes

### Calculations
- **Adherence Calculation**: Percentage based on doses taken vs. doses prescribed
- **Streak Tracking**: Consecutive days of perfect adherence
- **Refill Estimation**: Days until medication runs out based on daily usage
- **Trend Analysis**: Weekly and monthly adherence patterns

### Safety Features
- **Drug Interaction Warnings**: Alerts for potentially dangerous medicine combinations
- **Side Effect Monitoring**: Tracks adverse reactions to medications
- **Stock Alerts**: Warns when medicine is running low
- **Doctor Notes**: Stores critical medical instructions

### User Interface
- **Built with Tkinter**: Cross-platform compatibility (Windows, Mac, Linux)
- **Tabbed Windows**: Organized features in separate windows
- **Real-time Updates**: Dashboard refreshes instantly
- **Easy Navigation**: All features from main window

## Example Scenario

### Setup
Patient is prescribed:
- **Medicine A (Aspirin 500mg)**
  - 2 times a day for 30 days
  - 60 pills in stock
  - Doctor note: "Take with food"

- **Medicine B (Vitamin D 1000IU)**
  - 1 time a day for 60 days
  - 60 pills in stock
  - Possible interaction with Medicine A: "May increase bleeding risk" (High severity)

### Day 1 Usage
1. Add both medicines with stock quantities
2. Add doctor note for Medicine A
3. Log drug interaction between A and B
4. Mark both medicines as taken

### Week 1 Analysis
- Overall Adherence: 100% (7/7 doses)
- Medicine A: 100% (14/14 doses)
- Medicine B: 100% (7/7 doses)
- Current Streak: 7 days
- Refill estimate: A needs refill in ~30 days, B in ~60 days

### Benefits
- ✅ Never forget to take medication
- ✅ Track compliance for doctor visits
- ✅ Avoid dangerous drug interactions
- ✅ Monitor side effects
- ✅ Know when to refill prescriptions
- ✅ Follow doctor's special instructions

## Future Enhancements

- Push notifications/reminders for medicine times
- Medication refill reminders
- Multiple user profiles
- Export adherence reports
- Mobile app support
## VEDIO



https://github.com/user-attachments/assets/5b1b6fa3-a0c5-4938-a61a-965ea5b7d7c5


## future-updates
   day by day dashboard, more normalized database ,if patient miss a medicine message goes to there phone
## developed By:
    -sabari Raj RS
    -Adithyan T Nair
    https://github.com/sabari-D-raj
