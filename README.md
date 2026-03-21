# Medical Reminder App

A desktop application designed to help patients manage their medication schedules and track medicine adherence. This app reminds users when to take their medications and monitors whether doses are taken on schedule.

## Features

✅ **Medication Management**
- Add and manage medications with custom dosage information
- Set how many days you need to take each medication
- Configure daily frequency (times per day)
- Store medication details in a local database

✅ **Medicine Tracking**
- Record when medicines are taken
- Log dosage adherence patterns
- View all medications in one place

✅ **Adherence Analysis**
- Track medication compliance over time
- Calculate overall adherence percentage
- Identify missed doses and patterns
- View adherence analytics on the dashboard

✅ **Dashboard**
- Real-time viewing of overall adherence percentage
- Easy-to-use graphical interface
- Quick access to all medication information

## Project Structure

```
medical-reminder/
├── main.py                 # Application entry point
├── README.md              # Project documentation
├── LICENSE                # Project license
├── analaysis/
│   └── adherence.py       # Adherence calculation and analysis module
├── DATABASE/
│   ├── db.py              # SQLite database management
│   
└── ui/
    ├── dashboard.py       # Dashboard with adherence overview
    ├── medice.py          # Medicine management interface
    ├── showall.py         # View all medicines
   
```

## Database Schema
    -medicine(id|,medicine_name,dosage,time,times_a_day,days_to take)
    Adherence(id|,med_id,date,taken)
### Medicine Table
Stores information about each medication:
- Medicine name
- Dosage (e.g., mg, ml)
- Times per day (frequency)
- Number of days to take the medication

### Adherence Table
Tracks compliance for patient:
- Medication ID (linked to Medicine table)
- Date of dose
- Whether dose was taken (1 = Yes, 0 = No)


## Usage

1. **Add a Medication**
   - Open the medicine management section
   - Enter medication name, dosage, and frequency
   - Specify how many days you need to take it
   - Save the medication

2. **Record Medicine Intake**
   - Mark medicines as taken when you consume them
   - The app automatically records the date and time
   - Track adherence in real-time

3. **View Dashboard**
   - Check your overall adherence percentage
   - Monitor your medication compliance
   - Review medication schedule

4. **View All Medicines**
   - See complete list of all active medications
   - Check dosage and frequency information
   - View adherence history

## How It Works

- **Local Database**: All data is stored locally using SQLite (medications.db)
- **Adherence Calculation**: The app calculates adherence percentage based on how many prescribed doses were actually taken
- **User-Friendly Interface**: Built with Tkinter for cross-platform compatibility

## Example

If a patient is prescribed to take:
- Medicine A: 2 times a day for 30 days
- Medicine B: 1 time a day for 7 days

The app will track each dose and calculate compliance percentage for each medicine and overall adherence.

## Future Enhancements

- Push notifications/reminders for medicine times
- Medication refill reminders
- Multiple user profiles
- Export adherence reports
- Mobile app support
## VEDIO
<video controls src="Video Project 1.mp4" title="Title"></video>

## future-updates
   day by day dashboard, more normalized database ,if patient miss a medicine message goes to there phone
## developed By:
    -sabari Raj RS
    https://github.com/sabari-D-raj