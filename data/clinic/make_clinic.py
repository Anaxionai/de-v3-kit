"""Make a made-up clinic's data for CareLine (P13, and its visit notes for P15).

The clinic sends one appointments file a day, plus its patient and doctor lists.
This script writes all of them for the days you ask for, with the small flaws a
real clinic's files have. Your profile and your checks must find those flaws.

Run it from inside your careline/ folder:

    uv run python ~/de-kit/data/clinic/make_clinic.py --student <your-id> --days 30

Everything is made up: every name, phone number and email address. No row
belongs to a real person. The same --student always gives the same data.

Other ways to run it:

    --end 2026-11-12          the last day (default: yesterday)
    --resend 2026-11-03       write that one day's file again, as a corrected file from the clinic
    --notes                   also write the pilot doctors' visit notes into notes/ (P15)
    --check                   test this script (writes to a temporary folder, then deletes it)

It uses only the Python standard library, so it runs in any uv project.
"""

import argparse
import csv
import hashlib
import random
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------- the clinic

APPOINTMENT_COLUMNS = [
    "appointment_id", "patient_id", "doctor_id", "appointment_date", "slot_time", "booked_at",
    "status", "fee_rupees", "payment_mode", "reason_category", "reason",
]
PATIENT_COLUMNS = [
    "patient_id", "full_name", "phone", "email", "date_of_birth", "gender", "city", "pin_code",
    "registered_on",
]
DOCTOR_COLUMNS = ["doctor_id", "full_name", "speciality", "branch", "joined_on"]

SPECIALITIES = ["general", "paediatrics", "dermatology", "cardiology",
                "orthopaedics", "gynaecology", "ent", "dental"]
BRANCHES = ["north", "south", "east", "west", "central"]
STATUSES = {"completed": 75, "cancelled": 9, "no_show": 8, "booked": 8}          # weights in %
PAYMENT_MODES = {"upi": 45, "cash": 25, "card": 18, "insurance": 12}
REASON_CATEGORIES = ["consultation", "follow_up", "test_results", "vaccination", "procedure"]

# Each doctor charges one fee, in this range for the speciality (rupees).
FEE_RANGE = {
    "general": (300, 500), "paediatrics": (400, 700), "dermatology": (600, 1000),
    "cardiology": (1000, 1500), "orthopaedics": (800, 1200), "gynaecology": (600, 1000),
    "ent": (500, 800), "dental": (400, 900),
}
LOWEST_FEE, HIGHEST_FEE = 300, 1500

# How often each speciality sees each kind of visit (weights for REASON_CATEGORIES).
CATEGORY_WEIGHTS = {
    "general": [50, 20, 15, 10, 5], "paediatrics": [40, 15, 5, 35, 5],
    "dermatology": [50, 25, 5, 0, 20], "cardiology": [40, 30, 25, 0, 5],
    "orthopaedics": [45, 30, 15, 0, 10], "gynaecology": [45, 25, 15, 5, 10],
    "ent": [55, 20, 5, 0, 20], "dental": [35, 20, 0, 0, 45],
}

# 8 cities with the first 3 digits of their PIN codes.
CITIES = {"Mumbai": "400", "Delhi": "110", "Bengaluru": "560", "Chennai": "600",
          "Kolkata": "700", "Hyderabad": "500", "Pune": "411", "Ahmedabad": "380"}

# Names are drawn at random from these short lists, so any match with a real person is chance.
FIRST_NAMES_F = [
    "Aarti", "Aisha", "Ananya", "Anjali", "Bhavna", "Deepa", "Divya", "Farah", "Fatima", "Gauri",
    "Geeta", "Grace", "Harpreet", "Hema", "Ishita", "Jaya", "Kavya", "Lakshmi", "Leela", "Mary",
    "Meera", "Nandini", "Neha", "Nisha", "Pooja", "Priya", "Radha", "Rekha", "Revathi", "Ritu",
    "Sana", "Shalini", "Simran", "Sneha", "Sunita", "Swati", "Tanvi", "Uma", "Vandana", "Zoya",
]
FIRST_NAMES_M = [
    "Aarav", "Abdul", "Ajay", "Amit", "Anil", "Arjun", "Arun", "Ashok", "Bala", "Chetan",
    "Deepak", "Dev", "Farhan", "Ganesh", "Gaurav", "Gurpreet", "Harish", "Imran", "Jatin", "Joseph",
    "Karan", "Manoj", "Mohan", "Nikhil", "Prakash", "Rahul", "Rajesh", "Ravi", "Rohit", "Sameer",
    "Sanjay", "Senthil", "Sourav", "Suresh", "Tarun", "Thomas", "Varun", "Vijay", "Yusuf", "Zubin",
]
FIRST_NAMES_X = ["Kiran", "Noor", "Sam", "Jyoti", "Ira", "Alex"]
LAST_NAMES = [
    "Agarwal", "Ahmed", "Banerjee", "Bhat", "Bose", "Chatterjee", "Chauhan", "Das", "Desai",
    "D'Souza", "Fernandes", "Gill", "Gupta", "Hussain", "Iyer", "Jain", "Joshi", "Kapoor", "Khan",
    "Kulkarni", "Kumar", "Menon", "Mishra", "Mukherjee", "Naidu", "Nair", "Pandey", "Patel",
    "Pillai", "Qureshi", "Rao", "Reddy", "Saxena", "Sen", "Shah", "Sharma", "Shetty", "Singh",
    "Sinha", "Thomas", "Varghese", "Verma", "Yadav",
]
EMAIL_DOMAINS = ["example.com", "example.net", "example.org"]  # reserved for examples: never real mailboxes

# Short reason texts, written by the receptionist when the visit is booked.
REASONS_CONSULTATION = {
    "general": ["fever and cough for three days", "headache since last week", "stomach pain after meals",
                "feeling tired all the time", "sore throat and mild fever", "body ache, chills"],
    "paediatrics": ["child has had a fever since yesterday", "child not eating well", "cough and cold in a toddler",
                    "rash on the baby's arms", "growth check for a two-year-old"],
    "dermatology": ["itchy rash on both arms", "acne on the face", "hair fall for two months",
                    "dry patches on the skin", "dark spots on the cheeks"],
    "cardiology": ["chest discomfort when climbing stairs", "high blood pressure readings at home",
                   "racing heartbeat at night", "short of breath when walking"],
    "orthopaedics": ["knee pain while walking", "lower back pain after lifting", "shoulder stiffness for a month",
                     "ankle swelling after a fall", "neck pain from desk work"],
    "gynaecology": ["irregular periods", "pregnancy check, second trimester", "pelvic pain for a week",
                    "advice before planning a pregnancy"],
    "ent": ["ear pain on the left side", "blocked nose for two weeks", "hearing loss in one ear",
            "sore throat that keeps coming back"],
    "dental": ["tooth pain on the left side", "bleeding gums when brushing", "teeth sensitive to cold drinks",
               "broken filling"],
}
REASONS_FOLLOW_UP = ["follow-up after last week's visit", "review of medicine dose",
                     "check after the course of antibiotics", "follow-up, pain is better",
                     "follow-up, no change yet", "second visit to review progress"]
REASONS_TEST_RESULTS = ["discuss blood test results", "review X-ray report", "review scan report",
                        "review thyroid test", "review sugar test results", "review ECG report"]
REASONS_VACCINATION = ["flu vaccine", "child's scheduled vaccine dose", "tetanus booster",
                       "hepatitis B second dose", "typhoid vaccine before travel"]
REASONS_PROCEDURE = {
    "general": ["dressing of a small wound", "removal of stitches"],
    "paediatrics": ["nebuliser session", "removal of stitches"],
    "dermatology": ["removal of a skin tag", "chemical peel, first sitting", "wart removal"],
    "cardiology": ["treadmill stress test", "24-hour heart monitor fitting"],
    "orthopaedics": ["plaster removal", "knee injection"],
    "gynaecology": ["ultrasound scan", "pap smear"],
    "ent": ["ear wax removal", "nasal endoscopy"],
    "dental": ["root canal, second sitting", "tooth cleaning", "tooth extraction", "new filling"],
}
# Free text that holds personal data: the receptionist typed a phone number or an email address.
REASONS_WITH_PHONE = ["{base}, call back on {phone}", "patient asked for a reminder on {phone}",
                      "{base}; reach patient on {phone} if the doctor is late"]
REASONS_WITH_EMAIL = ["{base}, send the report to {email}", "send the bill to {email}",
                      "{base}; reports to be emailed to {email}"]

# How often the small realistic flaws appear (share of appointment rows).
UNKNOWN_PATIENT_SHARE = 0.003   # patient registered after the export: not in patients.csv yet
FEE_TEN_TIMES_SHARE = 0.002     # fee typed with one zero too many
LATE_BOOKING_SHARE = 0.005      # walk-in recorded after the visit started
PERSONAL_REASON_SHARE = 0.02    # a phone number or email inside the free-text reason

SAMPLE_ROWS = 150
LAST_REGISTRATION = date(2026, 7, 1)  # patients.csv was exported after this day
DAY_ZERO = date(2000, 1, 1)     # appointment ids start with the number of days since this date
IST = "+05:30"


# ---------------------------------------------------------------- helpers

def normalise_student(student: str) -> str:
    """Capital and small letters, and spaces around the id, do not change the data."""
    return student.strip().lower()


def rng_for(student: str, *parts: object) -> random.Random:
    """A random number generator that always gives the same numbers for the same inputs."""
    text = "|".join([normalise_student(student), *map(str, parts)])
    seed = int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")
    return random.Random(seed)


def pick(rng: random.Random, weights: dict[str, int]) -> str:
    return rng.choices(list(weights), weights=list(weights.values()))[0]


def make_phone(rng: random.Random) -> str:
    """A made-up 10-digit mobile number: it starts with 6, 7, 8 or 9."""
    return str(rng.randint(6, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(9))


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    """UTF-8, one header row, "\\n" line endings, quotes only where a value needs them."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def day_file(out: Path, day: date) -> Path:
    return out / "appointments" / f"appointments_{day.isoformat()}.csv"


# ---------------------------------------------------------------- patients and doctors

def make_patients(student: str) -> tuple[list[dict], list[str]]:
    """About 1,200 patients, with the flaws of a real registration desk.

    Returns the rows and a list of ids that are NOT in the file yet (patients who
    registered after the clinic exported it). A few appointments use those ids.
    """
    rng = rng_for(student, "patients")
    people = []
    for _ in range(rng.randint(1180, 1215)):
        gender = rng.choices(["F", "M", "X"], weights=[49, 49, 2])[0]
        first = rng.choice({"F": FIRST_NAMES_F, "M": FIRST_NAMES_M, "X": FIRST_NAMES_X}[gender])
        last = rng.choice(LAST_NAMES)
        age = rng.choices([rng.randint(0, 12), rng.randint(13, 17), rng.randint(18, 39),
                           rng.randint(40, 59), rng.randint(60, 90)], weights=[15, 5, 35, 28, 17])[0]
        city = rng.choice(list(CITIES))
        born = date(2026 - age, 7, 1) - timedelta(days=rng.randint(0, 364))
        first_day = max(date(2018, 1, 1), born)                   # nobody registers before birth
        people.append({
            "first": first, "last": last, "gender": gender, "date_of_birth": born,
            "city": city, "pin_code": CITIES[city] + f"{rng.randint(1, 99):03d}",
            "digits": make_phone(rng),
            "has_email": rng.random() >= 0.30,                    # about 30% have no email: allowed
            "email_number": rng.choice(["", str(rng.randint(1, 99))]),
            "registered_on": first_day + timedelta(days=rng.randint(0, max(0, (LAST_REGISTRATION - first_day).days))),
        })
    # No two people share a phone number, so the duplicate registrations below are the only pairs.
    seen = set()
    for p in people:
        while p["digits"] in seen:
            p["digits"] = make_phone(rng)
        seen.add(p["digits"])
        # Flaw: the desk types phone numbers in three ways.
        digits = p["digits"]
        style = rng.choices(["plain", "plus91", "zero"], weights=[70, 20, 10])[0]
        p["phone"] = {"plain": digits,
                      "plus91": f"+91 {digits[:5]} {digits[5:]}",
                      "zero": f"0{digits[:5]}-{digits[5:]}"}[style]
        p["email"] = ""
        if p["has_email"]:
            name = f"{p['first']}.{p['last']}".lower().replace("'", "")
            p["email"] = f"{name}{p['email_number']}@{rng.choice(EMAIL_DOMAINS)}"

    # Flaw: about 1% of people registered twice (same name and phone, a second id, a later date).
    registrations = [(p["registered_on"], i, p) for i, p in enumerate(people)]
    for i in rng.sample(range(len(people)), round(len(people) * 0.01)):
        later = people[i]["registered_on"] + timedelta(days=rng.randint(20, 400))
        second = dict(people[i], registered_on=min(later, LAST_REGISTRATION))
        registrations.append((second["registered_on"], len(registrations), second))
    registrations.sort(key=lambda item: (item[0], item[1]))

    rows = []
    next_id = rng.randint(100000, 200000)
    for _, _, p in registrations:
        rows.append({
            "patient_id": f"P{next_id:06d}", "full_name": f"{p['first']} {p['last']}", "phone": p["phone"],
            "email": p["email"], "date_of_birth": p["date_of_birth"].isoformat(), "gender": p["gender"], "city": p["city"],
            "pin_code": p["pin_code"], "registered_on": p["registered_on"].isoformat(),
            # kept for the appointments, not written to the file:
            "_digits": p["digits"], "_age": 2026 - p["date_of_birth"].year,
        })
        next_id += rng.randint(1, 9)
    # Flaw: 6 impossible birth dates (0.5%): 3 placeholders and 3 dates in the future.
    for n, i in enumerate(rng.sample(range(len(rows)), 6)):
        rows[i]["date_of_birth"] = ("1900-01-01" if n < 3 else
                                    date(rng.randint(2030, 2035), rng.randint(1, 12), rng.randint(1, 28)).isoformat())
    not_registered_yet = []
    for _ in range(40):
        next_id += rng.randint(1, 9)
        not_registered_yet.append(f"P{next_id:06d}")
    return rows, not_registered_yet


def make_doctors(student: str) -> list[dict]:
    """40 doctors: one of each speciality in each of the 5 branches. This file has no flaws."""
    rng = rng_for(student, "doctors")
    names = set()
    while len(names) < 40:
        first = rng.choice(FIRST_NAMES_F + FIRST_NAMES_M)
        names.add(f"{first} {rng.choice(LAST_NAMES)}")
    names = sorted(names)
    rng.shuffle(names)
    doctors = []
    for n, (branch, speciality) in enumerate(((b, s) for b in BRANCHES for s in SPECIALITIES), start=1):
        low, high = FEE_RANGE[speciality]
        doctors.append({
            "doctor_id": f"D{n:03d}", "full_name": names[n - 1], "speciality": speciality, "branch": branch,
            "joined_on": (date(2010, 1, 1) + timedelta(days=rng.randint(0, 5800))).isoformat(),
            "_fee": rng.randrange(low, high + 1, 50),       # kept for the appointments, not written
        })
    return doctors


# ---------------------------------------------------------------- one day of appointments

def make_day(student: str, day: date, patients: list[dict], unknown_ids: list[str],
             doctors: list[dict]) -> list[dict]:
    """All appointments of one day, in booking order. The same student and day give the same rows."""
    rng = rng_for(student, "day", day.isoformat())
    weekday = day.weekday()                                    # 6 is Sunday
    count = rng.randint(300, 340) if weekday == 6 else rng.randint(360, 450)
    slots = [f"{9 + q // 4:02d}:{(q % 4) * 15:02d}" for q in range(44)]   # 09:00 to 19:45
    pairs = rng.sample([(d, s) for d in range(len(doctors)) for s in slots], count)  # one patient per doctor and slot

    children = [p for p in patients if p["_age"] < 18]
    women = [p for p in patients if p["gender"] == "F" and 18 <= p["_age"] <= 50]
    rows = []
    for doctor_index, slot in pairs:
        doctor = doctors[doctor_index]
        speciality = doctor["speciality"]
        pool = children if speciality == "paediatrics" else women if speciality == "gynaecology" else patients
        patient = rng.choice(pool)
        category = rng.choices(REASON_CATEGORIES, weights=CATEGORY_WEIGHTS[speciality])[0]
        fee = doctor["_fee"]
        if category == "follow_up":
            fee = max(LOWEST_FEE, fee // 100 * 50)             # half price, rounded to 50
        elif category == "procedure":
            fee = min(HIGHEST_FEE, fee + 300)
        if category == "consultation":
            reason = rng.choice(REASONS_CONSULTATION[speciality])
        elif category == "follow_up":
            reason = rng.choice(REASONS_FOLLOW_UP)
        elif category == "test_results":
            reason = rng.choice(REASONS_TEST_RESULTS)
        elif category == "vaccination":
            reason = rng.choice(REASONS_VACCINATION)
        else:
            reason = rng.choice(REASONS_PROCEDURE[speciality])
        slot_start = datetime.combine(day, datetime.strptime(slot, "%H:%M").time())
        if rng.random() < 0.25:                                # booked the same day
            booked = slot_start - timedelta(minutes=rng.randint(30, 360))
        else:                                                  # booked 1 to 14 days before
            booked = datetime.combine(slot_start.date() - timedelta(days=rng.randint(1, 14)),
                                      datetime.min.time()) + timedelta(minutes=rng.randint(7 * 60, 22 * 60))
        row = {
            "patient_id": patient["patient_id"], "doctor_id": doctor["doctor_id"],
            "appointment_date": day.isoformat(), "slot_time": slot, "booked": booked,
            "status": pick(rng, STATUSES), "fee_rupees": fee, "payment_mode": pick(rng, PAYMENT_MODES),
            "reason_category": category, "reason": reason, "_flaw": "",
        }
        # The small realistic flaws, each in a small share of rows. _flaw marks the row (not written).
        if rng.random() < UNKNOWN_PATIENT_SHARE:
            row["patient_id"], row["_flaw"] = rng.choice(unknown_ids), "unknown patient"
        if rng.random() < FEE_TEN_TIMES_SHARE:
            row["fee_rupees"], row["_flaw"] = fee * 10, "fee ten times"
        if rng.random() < LATE_BOOKING_SHARE:
            row["booked"], row["_flaw"] = slot_start + timedelta(minutes=rng.randint(5, 120)), "late booking"
        if rng.random() < PERSONAL_REASON_SHARE:
            row["reason"], row["_flaw"] = personal_reason(rng, reason, patient), "personal data"
        rows.append(row)

    rows.sort(key=lambda r: (r["booked"], r["doctor_id"]))    # ids follow the booking order
    for seq, row in enumerate(rows, start=1):
        row["appointment_id"] = f"A{(day - DAY_ZERO).days:05d}{seq:03d}"
        row["booked_at"] = row.pop("booked").isoformat(timespec="seconds") + IST
        row["fee_rupees"] = str(row["fee_rupees"])
    return rows


def personal_reason(rng: random.Random, base: str, patient: dict) -> str:
    """A reason text that holds the patient's (made-up) phone number or an email address."""
    first, last = patient["full_name"].lower().replace("'", "").split(" ", 1)
    template = rng.choice(REASONS_WITH_PHONE + REASONS_WITH_EMAIL)
    return template.format(base=base, phone=patient["_digits"], email=f"{first}.{last}@example.com")


def add_duplicates(student: str, rows: list[dict]) -> list[dict]:
    """The clinic's system sent 4 rows twice: same values, same appointment_id."""
    rng = rng_for(student, "duplicates")
    plain = [i for i, row in enumerate(rows) if not row["_flaw"]]
    result = list(rows)
    for i in sorted(rng.sample(plain, 4), reverse=True):
        result.insert(rng.randint(i + 1, len(result)), dict(rows[i]))
    return result


def duplicate_day(student: str, days: list[date]) -> date:
    """The one day with duplicate ids: chosen by the student id, between day 10 and day 25."""
    low, high = min(10, len(days)), min(25, len(days))
    return days[rng_for(student, "duplicate day").randint(low, high) - 1]


def public(row: dict, columns: list[str]) -> dict:
    """Only the file's columns, without the helper fields that start with _."""
    return {column: row[column] for column in columns}


# ---------------------------------------------------------------- the sample files

def make_samples(student: str, day: date, patients, unknown_ids, doctors) -> tuple[list[dict], list[dict]]:
    """150 rows of one day's file, all without flaws, and the same rows with four planted faults."""
    clean = [row for row in make_day(student, day, patients, unknown_ids, doctors) if not row["_flaw"]]
    rng = rng_for(student, "sample")
    good = [public(row, APPOINTMENT_COLUMNS) for row in sorted(rng.sample(clean, SAMPLE_ROWS),
                                                                key=lambda r: r["appointment_id"])]
    bad = [dict(row) for row in good]
    copy_from, same_id, no_patient, negative, done = rng.sample(range(SAMPLE_ROWS), 5)
    bad[same_id]["appointment_id"] = bad[copy_from]["appointment_id"]    # one duplicated appointment_id
    bad[no_patient]["patient_id"] = ""                                   # one empty patient_id
    bad[negative]["fee_rupees"] = "-" + bad[negative]["fee_rupees"]      # one negative fee
    bad[done]["status"] = "DONE"                                         # one status outside the list
    return good, bad


# ---------------------------------------------------------------- visit notes (--notes, P15)
#
# Only two pilot doctors type their notes: the central branch's general doctor (D033) and its
# orthopaedic doctor (D037). Every completed visit of theirs gets a consultation note, and about
# 1 in 3 also gets a triage note from the nurse first. Two notes a day are corrected two days
# later. The notes use their own seeds ("notes" and "corrections"), so every P13 file is the
# same bytes with or without --notes.

NOTE_COLUMNS = ["note_id", "version", "appointment_id", "note_type", "written_at", "note_text"]
PILOT_DOCTORS = ("D033", "D037")
TRIAGE_SHARE = 1 / 3
BODY_AREAS = ["head", "throat", "chest", "abdomen", "skin", "whole body", "back", "neck", "shoulder",
              "wrist", "hip", "knee", "ankle"]
DURATIONS = ["since yesterday", "for two days", "for three days", "for five days", "for a week",
             "for ten days", "for two weeks", "for a month", "for three months"]
SIDES = ["left", "right"]
CONSULTATION_WORDS = (45, 76)          # before a planted sentence (at most 9 words): notes stay under 86 words


def complaint(doctor, text, area, details, findings, plans, advice, feverish=False) -> dict:
    """One complaint and the sentences a note about it is made of. {side} is left or right."""
    return {"doctor": doctor, "text": text, "area": area, "details": details, "findings": findings,
            "plans": plans, "advice": advice, "feverish": feverish}


COMPLAINTS = {
    # D033, general
    "fever": complaint("D033", "fever and body ache", "whole body",
                       ["Chills and shivering in the evenings.", "Aches in the legs and arms all day.",
                        "Not eating well and feels thirsty.", "No rash, no cough and no vomiting.",
                        "Sweats a lot at night.", "Feels weak and slow when walking."],
                       ["Temperature {temp} C, pulse {pulse}.", "Chest clear, no rash on the skin.",
                        "Throat slightly red, glands not swollen."],
                       ["Paracetamol every six hours when needed.", "Blood count and malaria test ordered today.",
                        "Plenty of fluids and rest at home."],
                       ["Drink at least three litres of water a day.", "Sponge with lukewarm water if the fever is high."],
                       feverish=True),
    "cough": complaint("D033", "dry cough", "chest",
                       ["Worse at night and when lying flat.", "No phlegm and no blood when coughing.",
                        "Tickle in the throat before each bout.", "Mild fever only at the start.",
                        "Coughing fits wake the patient at night."],
                       ["Chest clear on both sides on listening.", "A few wheezes when breathing out.",
                        "Temperature {temp} C, pulse {pulse}."],
                       ["Cough syrup at night for five nights.", "Steam inhalation twice a day.",
                        "Chest X-ray if the cough is no better."],
                       ["Avoid dust, smoke and cold drinks.", "Drink warm water through the day."], feverish=True),
    "throat": complaint("D033", "sore throat", "throat",
                        ["Pain when swallowing food and water.", "Voice hoarse in the mornings.",
                         "Mild fever at night with chills.", "No cough and no runny nose.", "Ears ache when swallowing."],
                        ["Throat red, both tonsils swollen.", "Glands in the neck swollen and tender.",
                         "Temperature {temp} C, pulse {pulse}."],
                        ["Salt water gargles three times a day.", "Throat lozenges when needed.",
                         "Antibiotics if the fever has not settled by the review."],
                        ["Rest the voice and avoid shouting.", "Warm fluids and soft food only."], feverish=True),
    "headache": complaint("D033", "headache", "head",
                          ["Dull pain across the forehead.", "Worse in bright light and noise.",
                           "Worse towards the end of the working day.", "No vomiting and no blurred vision.",
                           "Eyes feel strained after screen work."],
                          ["Blood pressure {bp}, pulse {pulse}.", "Eyes, pupils and nerves normal.",
                           "Neck and shoulder muscles tight."],
                          ["Paracetamol when needed, at most three a day.", "Eye test at the optician advised.",
                           "Headache diary to bring to the next visit."],
                          ["Regular meals, water and sleep.", "Short breaks from screens every hour."]),
    "stomach": complaint("D033", "stomach pain after meals", "abdomen",
                         ["Burning feeling under the ribs.", "Worse after spicy or oily food.",
                          "Bloating and burping in the evenings.", "No vomiting and no blood in the stool.",
                          "Sour taste in the mouth in the mornings."],
                         ["Abdomen soft, tender just below the ribs.", "No lumps felt in the abdomen.",
                          "Weight steady since the last visit."],
                         ["Antacid tablets after meals.", "Stool test ordered.", "Ultrasound of the abdomen if no better."],
                         ["Small meals and no late dinners.", "Avoid tea and coffee on an empty stomach."]),
    "diarrhoea": complaint("D033", "diarrhoea", "abdomen",
                           ["Five or six loose watery stools a day.", "Cramps in the belly before each stool.",
                            "No blood or mucus in the stool.", "Mild nausea but no vomiting.",
                            "Drinking less water than usual."],
                           ["Mildly dry mouth, pulse {pulse}.", "Abdomen soft, mild tenderness all over.",
                            "Temperature {temp} C, no rash."],
                           ["Oral rehydration salts after each loose stool.", "Zinc tablets once a day.",
                            "Stool test if it continues."],
                           ["Boiled or bottled water only.", "Light food such as rice, bananas and toast."], feverish=True),
    "tired": complaint("D033", "feeling tired all the time", "whole body",
                       ["Sleeps badly and wakes up tired.", "Short of breath on the stairs.",
                        "Low mood at times, no interest in hobbies.", "Appetite poor, often skips lunch.",
                        "Hair falling more than usual."],
                       ["Looks pale, inner eyelids pale.", "Pulse {pulse}, regular, blood pressure {bp}.",
                        "Thyroid gland normal size, no lumps."],
                       ["Blood count, thyroid and sugar tests ordered.", "Iron tablets if the blood count is low.",
                        "Vitamin D level ordered."],
                       ["Regular sleep and a short walk every day.", "Iron-rich food such as greens and lentils."]),
    "rash": complaint("D033", "itchy rash on both arms", "skin",
                      ["Itch much worse at night.", "Small red raised spots that come and go.", "No new medicines or foods.",
                       "Nobody else at home has an itch.", "Scratching has broken the skin in places."],
                      ["Raised red spots on both forearms.", "No blisters and no signs of infection.",
                       "Skin on the face and legs clear."],
                      ["Antihistamine tablets at night.", "Calamine lotion twice a day.",
                       "Mild steroid cream on the worst patches."],
                      ["Loose cotton clothes only.", "Avoid hot showers and scented soaps."]),
    "dizziness": complaint("D033", "dizziness when standing up", "head",
                           ["Room spins for a few seconds on standing.", "Worse in the mornings after waking.",
                            "No fainting and no falls.", "Ringing in the ears at times.", "Drinks very little water at work."],
                           ["Blood pressure {bp} lying, lower when standing.", "Pulse {pulse}, regular.",
                            "Ears and eye movements normal."],
                           ["Blood count and sugar test ordered.", "Blood pressure tablets reviewed.",
                            "ECG ordered to check the heart rhythm."],
                           ["Stand up slowly from a chair or bed.", "More water and a little more salt."]),
    "chest": complaint("D033", "chest tightness when climbing stairs", "chest",
                       ["Settles within minutes of rest.", "No pain at rest or at night.",
                        "Some sweating with the tightness.", "Breathless by the second floor.",
                        "Father had heart disease in his fifties."],
                       ["Blood pressure {bp}, pulse {pulse}.", "Heart sounds normal, no murmur.",
                        "Chest clear, no swelling of the feet."],
                       ["ECG done in the clinic today.", "Treadmill test arranged.", "Cholesterol and sugar tests ordered."],
                       ["No heavy exercise until the tests are back.", "Stop smoking if a smoker."]),
    # D037, orthopaedics
    "knee": complaint("D037", "pain in the {side} knee", "knee",
                      ["Worse on climbing stairs.", "Clicking when bending the knee.", "Mild swelling by the evening.",
                       "Cannot squat or sit on the floor.", "Stiff for a while after sitting."],
                      ["Knee tender on the inner side, full movement.", "Mild swelling over the {side} kneecap.",
                       "Walks with a slight limp."],
                      ["Paracetamol when needed.", "Knee strengthening exercises shown.", "X-ray of the {side} knee ordered."],
                      ["Avoid squatting, kneeling and stairs.", "Ice pack on the knee twice a day."]),
    "back": complaint("D037", "lower back pain", "back",
                      ["Worse on bending forward or lifting.", "No pain or numbness down the legs.",
                       "Stiff in the mornings for an hour.", "Sleeps on an old soft mattress.",
                       "Pain eases a little when walking."],
                      ["Muscles tight on both sides of the spine.", "Straight leg raise normal on both sides.",
                       "No numbness in the feet, reflexes normal."],
                      ["Pain relief gel twice a day.", "Back exercises shown in the clinic.", "Physiotherapy referral made."],
                      ["Bend the knees when lifting anything.", "Sleep on a firm mattress."]),
    "neck": complaint("D037", "neck pain", "neck",
                      ["Stiff when turning the head.", "Pain spreads to the shoulders.",
                       "No tingling or weakness in the hands.", "Worse after long phone calls.",
                       "Headache at the back of the head."],
                      ["Neck muscles tender and tight.", "Turning reduced to both sides.", "Arm strength and reflexes normal."],
                      ["Warm compress twice a day.", "Neck stretches shown in the clinic.", "Muscle relaxant at night."],
                      ["Keep the screen at eye level.", "Use one firm pillow at night."]),
    "shoulder": complaint("D037", "stiffness in the {side} shoulder", "shoulder",
                          ["Cannot lift the {side} arm above the head.", "Pain when reaching behind the back.",
                           "Worse at night, wakes from sleep.", "Dressing and combing the hair are difficult.",
                           "Sleeps badly on that side."],
                          ["Movement limited in all directions.", "Tender over the front of the {side} shoulder.",
                           "Arm strength normal, no wasting."],
                          ["Pendulum exercises shown.", "Physiotherapy referral made.",
                           "Ultrasound of the {side} shoulder if no better."],
                          ["Keep the arm moving gently every day.", "Avoid carrying heavy bags on that side."]),
    "ankle": complaint("D037", "swelling of the {side} ankle", "ankle",
                       ["Pain on putting weight on it.", "Bruising on the outer side.", "Swelling worse by the evening.",
                        "Can walk only with a limp.", "No numbness in the toes."],
                       ["Tender below the outer ankle bone.", "Can bear weight for four steps.",
                        "No bone tenderness at the back."],
                       ["Crepe bandage applied.", "X-ray of the {side} ankle ordered.", "Pain relief gel twice a day."],
                       ["Rest, ice and keep the foot raised.", "Wear firm flat shoes."]),
    "wrist": complaint("D037", "pain in the {side} wrist", "wrist",
                       ["Pain when gripping or lifting a cup.", "Swelling on the thumb side.",
                        "Worse when typing or writing.", "Grip weak when opening jars.", "Clicking when turning the hand."],
                       ["Tender on the thumb side of the {side} wrist.", "Grip weaker than the other hand.",
                        "No deformity and normal feeling in the fingers."],
                       ["Wrist splint to wear at night.", "X-ray of the {side} wrist ordered.", "Pain relief gel twice a day."],
                       ["Rest the hand from heavy work.", "Ice pack after use."]),
    "hip": complaint("D037", "pain in the {side} hip", "hip",
                     ["Pain in the groin when walking.", "Stiff in the mornings for half an hour.", "Limps after long walks.",
                      "Difficulty getting out of a car.", "Pain at night when lying on that side."],
                     ["Hip movement reduced, painful at the end.", "Walks with a limp.", "Leg lengths equal, no shortening."],
                     ["X-ray of the pelvis ordered.", "Hip exercises shown.", "Paracetamol when needed."],
                     ["Use a walking stick on long walks.", "Avoid sitting cross-legged on the floor."]),
}
HISTORY = ["Takes tablets for blood pressure every morning.", "No past illnesses of note.",
           "Has diabetes, controlled on tablets.", "Had a similar problem last year.", "Allergic to penicillin.",
           "Does not smoke or drink alcohol.", "Smokes a few cigarettes a day.", "Has had asthma since childhood.",
           "Takes thyroid tablets every morning.", "Works long hours at a desk.", "On no regular medicines."]
URGENCY_WEIGHTS = {"routine": 60, "soon": 30, "urgent": 10}
# Only these sentences may hold the words "urgent" or "emergency".
URGENCY_SENTENCES = {
    "routine": ["No warning signs; routine care.", "Routine follow-up only."],
    "soon": ["Review within a week if it is no better.", "Come back in three days if no better."],
    "urgent": ["Urgent: sent to the emergency department today.",
               "Urgent: go to the emergency department at once if it gets worse.",
               "Urgent referral to the specialist today."],
}
FOLLOW_UPS = ["Follow up in two weeks.", "Follow up in one week.", "Follow up in five days.",
              "Follow up in a month.", "Follow up after the test results."]

# Story sentences: two a day, one in a D033 note and one in a D037 note. Day k (days since
# DAY_ZERO) uses story k mod 32 of each list, so any 32 days in a row hold 64 different stories.
# {p} is she, he or they, and {q} her, his or their, from the patient's gender.
GENERAL_STORIES = [
    ("fever", "It started after {p} got soaked in a cold downpour while waiting for a delayed train."),
    ("cough", "It started after {p} spent a weekend cleaning a dusty storeroom."),
    ("throat", "It started after {p} sang for three hours at a family wedding."),
    ("headache", "It started when {p} began working night shifts at a call centre."),
    ("stomach", "It started after {p} ate at a roadside stall at a night market."),
    ("diarrhoea", "It started after {p} ate leftover rice that had stood out overnight at a picnic."),
    ("tired", "It started after {p} took on a second job delivering parcels at night."),
    ("rash", "It started after {p} tried a new washing powder."),
    ("dizziness", "It started after {p} began new tablets for high blood pressure."),
    ("chest", "It started when {p} moved to a top-floor flat in an old building with steep stairs."),
    ("fever", "It started soon after {p} came back from a crowded three-day music festival."),
    ("cough", "It started when {p} began sanding old furniture in a closed garage."),
    ("throat", "It started after {p} cheered all afternoon at a school sports day."),
    ("headache", "It started after {p} gave up drinking coffee all at once."),
    ("stomach", "It started when {p} began taking painkillers on an empty stomach for a sports injury."),
    ("diarrhoea", "It started after {p} drank stream water on a trekking holiday in the hills."),
    ("tired", "It started when {p} began caring for a newborn baby and an elderly parent at home."),
    ("rash", "It started after {p} pulled weeds bare-armed in a neighbour's overgrown garden."),
    ("dizziness", "It started after {p} skipped breakfast and lunch on a busy moving day."),
    ("chest", "It started after {p} took up jogging again after many years without exercise."),
    ("fever", "It started after {p} looked after a nephew who had the flu over a long weekend."),
    ("cough", "It started after {p} moved into a freshly painted flat next to a building site."),
    ("throat", "It started when {p} drank several glasses of iced juice at a summer fair."),
    ("headache", "It started after {p} bumped {q} head on a low kitchen cupboard door."),
    ("stomach", "It started after {p} switched to eating dinner just before going to bed."),
    ("diarrhoea", "It started after {p} shared a seafood dinner at a beach restaurant."),
    ("tired", "It started after {p} switched to a strict diet of only fruit and salad."),
    ("rash", "It started after {p} wore a borrowed woollen jumper on a cold mountain trip."),
    ("dizziness", "It started after {p} gave blood at a donation drive at the office."),
    ("fever", "It started after {p} spent a night camping in a damp tent beside a river."),
    ("throat", "It started after {p} shouted through a football match in the pouring rain."),
    ("headache", "It started after {p} read small print on a phone in a dark room every night."),
]
ORTHO_STORIES = [
    ("knee", "It started when {p} slipped on wet tiles at a swimming pool."),
    ("back", "It started when {p} carried a heavy suitcase up four floors because the lift was broken."),
    ("neck", "It started after {p} slept sitting up on a long overnight bus journey."),
    ("shoulder", "It started when {p} reached up to a high shelf for a box of books."),
    ("ankle", "It started when {p} stepped off a moving bus."),
    ("wrist", "It started when {p} fell off a bicycle onto an outstretched hand."),
    ("hip", "It started after {p} sat cross-legged on the floor through a long ceremony."),
    ("knee", "It started when {p} knelt for hours laying a new floor at home."),
    ("back", "It started after {p} spent a whole day bent over weeding a vegetable patch."),
    ("neck", "It started when a car bumped into {q} scooter from behind at a red light."),
    ("shoulder", "It started after {p} served again and again at a badminton tournament."),
    ("ankle", "It started when {p} landed badly after a jump in a basketball game."),
    ("wrist", "It started after {p} typed long reports on a laptop with no wrist rest."),
    ("hip", "It started when {p} fell from a stepladder while hanging curtains."),
    ("knee", "It started after {p} ran a charity half marathon without any training."),
    ("back", "It started when {p} lifted a sack of cement off a delivery van."),
    ("neck", "It started after {p} painted a high ceiling, looking upwards all weekend."),
    ("shoulder", "It started when {p} grabbed a handrail to stop a fall on a moving train."),
    ("ankle", "It started when {p} stepped into a hidden pothole on a dark street."),
    ("wrist", "It started when {p} slipped on a wet market floor and put a hand out."),
    ("hip", "It started after {p} began a new job standing at a shop counter all day."),
    ("knee", "It started when {p} missed the last step on a dark staircase at a cinema."),
    ("back", "It started after {p} drove through the night to collect a relative from the airport."),
    ("neck", "It started when {p} began working on a laptop at the kitchen table."),
    ("shoulder", "It started after {p} hung wet laundry on a high line every morning."),
    ("ankle", "It started when {p} wore new high heels on a cobbled square."),
    ("wrist", "It started after {p} kneaded dough by hand for a big family feast."),
    ("hip", "It started after {p} climbed hundreds of steps to a hilltop fort."),
    ("knee", "It started when {p} twisted awkwardly while dancing at a birthday party."),
    ("back", "It started when {p} bent down to pick up a toddler from the floor."),
    ("neck", "It started after {p} rode a roller coaster at an amusement park."),
    ("shoulder", "It started after {p} slept on that arm on a hard hotel mattress."),
]
PRONOUNS = {"F": ("she", "her"), "M": ("he", "his"), "X": ("they", "their")}

# Planted personal data: the mistakes task 7 must find and mask. Never in a note whose
# patient_id is not in patients.csv. "capitals" is for triage notes only.
CONSULTATION_PLANTED_SHARE = 0.12
TRIAGE_PLANTED_SHARE = 0.25
PLANTED_WEIGHTS = {"phone": 30, "email": 15, "full name": 10, "capitals": 5, "first name": 10,
                   "title": 10, "family": 15, "doctor": 5}
PLANTED_TEMPLATES = {
    "phone": ["Call back on {phone} with the results.", "Patient asked for a reminder on {phone}.",
              "Ring {phone} if the report is late."],
    "email": ["Send the report to {email}.", "Reports to be emailed to {email}."],
    "full name": ["{full} asked for a morning slot next time.", "{full} asked for a copy of the prescription."],
    "capitals": ["Name on the file: {full}."],
    "first name": ["{first} says it is worse at night.", "{first} asked about the cost of the tests."],
    "title": ["{title} {last} asked for a sick note for work.", "{title} {last} prefers an early slot."],
    "family": ["A family member, {family}, will collect the report."],
    "doctor": ["Referred to Dr {doctor} for a second opinion."],
}

# Corrections: on day D, two notes written on day D-2 are corrected (version 2).
CORRECTIONS_PER_DAY = 2
CORRECTION_WEIGHTS = {"side": 30, "duration": 30, "follow-up": 20, "urgency": 10, "contact": 10}
ADDED_FOLLOW_UP = "Added on review: Follow up in one week."


def phone_form(digits: str, form: int) -> str:
    """The five ways a phone number is typed into a note."""
    return [digits, f"{digits[:5]} {digits[5:]}", f"{digits[:5]}-{digits[5:]}", f"+91 {digits[:5]} {digits[5:]}",
            f"0{digits[:5]}-{digits[5:]}"][form]


def note_text(note: dict) -> str:
    return " ".join(text for _, text in note["parts"])


def complaint_sentence(key: str, side: str | None, duration: str, triage: bool) -> str:
    phrase = f"{COMPLAINTS[key]['text'].format(side=side)} {duration}"
    return f"Came in with {phrase}." if triage else f"{phrase[0].upper()}{phrase[1:]}."


def planted_part(rng: random.Random, kind: str, patient: dict, names: dict) -> dict:
    """One planted sentence: its kind, template and values, so a correction can change a value."""
    first, last = patient["full_name"].split(" ", 1)
    values = {"phone": "", "email": "", "full": patient["full_name"], "first": first, "last": last,
              "title": {"F": "Ms", "M": "Mr"}.get(patient["gender"], ""), "family": "", "doctor": ""}
    if kind == "phone":
        values["phone"] = phone_form(patient["_digits"], rng.randrange(5))
    elif kind == "email":
        values["email"] = patient["email"] or f"{first}.{last}@example.com".lower().replace("'", "")
    elif kind == "capitals":
        values["full"] = patient["full_name"].upper()
    elif kind == "title" and not values["title"]:
        kind = "full name"                                     # gender X: the full name instead of a title
    elif kind == "family":
        values["family"] = rng.choice(names["first"])
    elif kind == "doctor":
        values["doctor"] = rng.choice(names["doctor"])
    template = rng.choice(PLANTED_TEMPLATES[kind])
    return {"kind": kind, "template": template, "values": values}


def render_planted(planted: dict) -> str:
    return planted["template"].format(**planted["values"])


def vital_values(rng: random.Random, feverish: bool) -> dict:
    temperature = rng.randint(376, 394) if feverish else rng.randint(365, 373)
    return {"bp": f"{rng.randint(110, 165)}/{rng.randint(70, 100)}", "pulse": str(rng.randint(64, 108)),
            "temp": f"{temperature / 10:.1f}", "oxygen": str(rng.randint(95, 99))}


def consultation_parts(rng: random.Random, key: str, side: str | None, duration: str, story: str | None,
                       values: dict) -> tuple[list[list[str]], str]:
    """The sentences of a consultation note, in the README's order. With a planted sentence of
    up to 9 words, a note has 50 to 85 words. Returns the parts and the urgency level."""
    spec = COMPLAINTS[key]
    for _ in range(100):
        details = rng.sample(spec["details"], 2)
        findings = rng.sample(spec["findings"], rng.choice([1, 1, 2]))
        plans = rng.sample(spec["plans"], rng.choice([1, 1, 2]))
        level = pick(rng, URGENCY_WEIGHTS)
        parts = [["complaint", complaint_sentence(key, side, duration, triage=False)]]
        parts += [["detail", d] for d in details] + [["history", rng.choice(HISTORY)]]
        parts += [["story", story]] if story else []
        parts += [["finding", f] for f in findings] + [["urgency", rng.choice(URGENCY_SENTENCES[level])]]
        parts += [["plan", p] for p in plans]
        parts += [["advice", rng.choice(spec["advice"])], ["follow-up", rng.choice(FOLLOW_UPS)]]
        parts = [[kind, text.format(side=side, **values)] for kind, text in parts]
        if CONSULTATION_WORDS[0] <= sum(len(text.split()) for _, text in parts) <= CONSULTATION_WORDS[1]:
            return parts, level
    raise RuntimeError(f"no consultation note in {CONSULTATION_WORDS} words for {key}")   # never happens with these lists


def day_notes(student: str, day: date, patients, unknown_ids, doctors, names: dict) -> list[dict]:
    """The original notes (version 1) written on one day: one per completed visit of D033 and
    D037, plus a triage note before about 1 in 3 of them."""
    rng = rng_for(student, "notes", day)
    by_id = {p["patient_id"]: p for p in patients}
    visits = sorted((r for r in make_day(student, day, patients, unknown_ids, doctors)
                     if r["doctor_id"] in PILOT_DOCTORS and r["status"] == "completed"),
                    key=lambda r: r["appointment_id"])
    k = (day - DAY_ZERO).days
    stories = {}
    for doctor, story_list in (("D033", GENERAL_STORIES), ("D037", ORTHO_STORIES)):
        candidates = [v for v in visits if v["doctor_id"] == doctor]
        if candidates:
            stories[rng.choice(candidates)["appointment_id"]] = (k % len(story_list), *story_list[k % len(story_list)])
    notes = []
    for visit in visits:
        patient = by_id.get(visit["patient_id"])               # None for a patient not in patients.csv yet
        story = stories.get(visit["appointment_id"])
        key = story[1] if story else rng.choice([c for c, s in COMPLAINTS.items() if s["doctor"] == visit["doctor_id"]])
        side = rng.choice(SIDES) if "{side}" in COMPLAINTS[key]["text"] else None
        duration = rng.choice(DURATIONS)
        values = vital_values(rng, COMPLAINTS[key]["feverish"])
        subject, possessive = PRONOUNS.get(patient["gender"] if patient else "X", PRONOUNS["X"])
        story_text = story[2].format(p=subject, q=possessive) if story else None
        slot = datetime.combine(day, datetime.strptime(visit["slot_time"], "%H:%M").time())
        number = visit["appointment_id"][1:]
        base = {"appointment_id": visit["appointment_id"], "doctor_id": visit["doctor_id"], "version": 1,
                "complaint": key, "side": side, "duration": duration, "planted": None, "day": day}
        visit_notes = []
        if rng.random() < TRIAGE_SHARE:
            parts = [["complaint", complaint_sentence(key, side, duration, triage=True)],
                     ["vitals", "BP {bp}, pulse {pulse}, temperature {temp} C, oxygen {oxygen} percent.".format(**values)]]
            visit_notes.append(dict(base, note_type="triage", parts=parts, urgency=None, story=None,
                                    written_at=slot - timedelta(minutes=rng.randint(5, 20))))
        parts, level = consultation_parts(rng, key, side, duration, story_text, values)
        visit_notes.append(dict(base, note_type="consultation", parts=parts, urgency=level,
                                story=(visit["doctor_id"], story[0]) if story else None,
                                written_at=slot + timedelta(minutes=rng.randint(10, 25))))
        for n, note in enumerate(visit_notes, start=1):
            note["note_id"] = f"N{number}-{n}"
            share = TRIAGE_PLANTED_SHARE if note["note_type"] == "triage" else CONSULTATION_PLANTED_SHARE
            if patient and rng.random() < share:
                weights = dict(PLANTED_WEIGHTS)
                if note["note_type"] != "triage":
                    del weights["capitals"]
                note["planted"] = planted_part(rng, pick(rng, weights), patient, names)
                note["parts"].insert(rng.randint(1, len(note["parts"])), ["planted", render_planted(note["planted"])])
        notes.extend(visit_notes)
    return notes


def swap_sides(text: str) -> str:
    return re.sub(r"\b(left|right)\b", lambda m: "right" if m.group(1) == "left" else "left", text)


def correct_note(rng: random.Random, note: dict, kind: str, day: date) -> dict:
    """Version 2 of a note: the full new text, the same ids, written on `day` between 09:00 and 19:00."""
    new = dict(note, version=2, correction=kind, parts=[list(part) for part in note["parts"]],
               written_at=datetime.combine(day, datetime.min.time()) + timedelta(minutes=9 * 60 + rng.randint(0, 600)))
    if kind == "side":
        new["side"] = "right" if note["side"] == "left" else "left"
        new["parts"] = [[k, text if k == "planted" else swap_sides(text)] for k, text in new["parts"]]
    elif kind == "duration":
        new["duration"] = rng.choice([d for d in DURATIONS if d != note["duration"]])
        new["parts"][0][1] = complaint_sentence(note["complaint"], note["side"], new["duration"],
                                                triage=note["note_type"] == "triage")
    elif kind == "follow-up":
        new["parts"].append(["follow-up", ADDED_FOLLOW_UP])
    elif kind == "urgency":
        new["urgency"] = rng.choice([level for level in URGENCY_WEIGHTS if level != note["urgency"]])
        i = next(i for i, (k, _) in enumerate(new["parts"]) if k == "urgency")
        new["parts"][i][1] = rng.choice(URGENCY_SENTENCES[new["urgency"]])
    else:                                                      # contact: new digits or a new email number
        planted = dict(note["planted"], values=dict(note["planted"]["values"]))
        if planted["kind"] == "phone":
            digits = re.sub(r"\D", "", planted["values"]["phone"])[-10:]
            form = [phone_form(digits, f) for f in range(5)].index(planted["values"]["phone"])
            new_digits = make_phone(rng)
            while new_digits == digits:
                new_digits = make_phone(rng)
            planted["values"]["phone"] = phone_form(new_digits, form)
        else:
            local, domain = planted["values"]["email"].split("@")
            stem = local.rstrip("0123456789")
            number = str(rng.randint(1, 99))
            while number == local[len(stem):]:
                number = str(rng.randint(1, 99))
            planted["values"]["email"] = f"{stem}{number}@{domain}"
        new["planted"] = planted
        i = next(i for i, (k, _) in enumerate(new["parts"]) if k == "planted")
        new["parts"][i][1] = render_planted(planted)
    return new


def corrections(student: str, day: date, earlier: list[dict]) -> list[dict]:
    """Exactly two notes written two days before `day` (versions 1) come back corrected.

    The kind is drawn first, then a note it fits: a side for a note with a side, an urgency
    sentence or a follow-up line for a consultation note, a contact for a note with a planted
    phone number or email. If no note fits, the duration is corrected instead.
    """
    rng = rng_for(student, "corrections", day)
    remaining = sorted(earlier, key=lambda n: n["note_id"])
    fits = {"side": lambda n: n["side"] is not None,
            "follow-up": lambda n: n["note_type"] == "consultation",
            "urgency": lambda n: n["note_type"] == "consultation",
            "contact": lambda n: n["planted"] is not None and n["planted"]["kind"] in ("phone", "email"),
            "duration": lambda n: True}
    result = []
    for _ in range(min(CORRECTIONS_PER_DAY, len(remaining))):
        kind = pick(rng, CORRECTION_WEIGHTS)
        candidates = [n for n in remaining if fits[kind](n)]
        if not candidates:
            kind, candidates = "duration", remaining
        note = rng.choice(candidates)
        remaining.remove(note)
        result.append(correct_note(rng, note, kind, day))
    return result


def make_notes(student: str, window: list[date], patients, unknown_ids, doctors) -> dict[date, list[dict]]:
    """Every note row of every day in the window, each day's rows sorted by written_at."""
    names = {"first": sorted({p["full_name"].split(" ", 1)[0] for p in patients}),
             "doctor": sorted({d["full_name"].split(" ", 1)[1] for d in doctors})}
    originals = {day: day_notes(student, day, patients, unknown_ids, doctors, names) for day in window}
    files = {}
    for day in window:
        rows = list(originals[day])
        if day - timedelta(days=2) in originals:               # the first two days of a window have no corrections
            rows += corrections(student, day, originals[day - timedelta(days=2)])
        files[day] = sorted(rows, key=lambda n: (n["written_at"], n["note_id"], n["version"]))
    return files


def notes_file(out: Path, day: date) -> Path:
    return out / "notes" / f"notes_{day.isoformat()}.csv"


def note_row(note: dict) -> dict:
    return {"note_id": note["note_id"], "version": str(note["version"]), "appointment_id": note["appointment_id"],
            "note_type": note["note_type"], "written_at": note["written_at"].isoformat(timespec="seconds") + IST,
            "note_text": note_text(note)}


def write_notes(student: str, window: list[date], patients, unknown_ids, doctors, out: Path) -> dict:
    """Write one notes file per day of the window and remove notes files outside it."""
    files = make_notes(student, window, patients, unknown_ids, doctors)
    for day, rows in files.items():
        write_csv(notes_file(out, day), NOTE_COLUMNS, [note_row(n) for n in rows])
    wanted = {notes_file(out, day).name for day in window}
    for old in (out / "notes").glob("notes_*.csv"):
        if old.name not in wanted:
            old.unlink()
    rows = [n for day_rows in files.values() for n in day_rows]
    newest = {}
    for note in rows:
        if note["version"] > newest.get(note["note_id"], {"version": 0})["version"]:
            newest[note["note_id"]] = note
    return {"files": len(files), "notes": sum(n["version"] == 1 for n in rows),
            "corrections": sum(n["version"] == 2 for n in rows),
            "words": sum(len(note_text(n).split()) for n in newest.values()),
            "planted": sum(n["planted"] is not None for n in rows)}


# ---------------------------------------------------------------- writing the files

def generate(student: str, days: int, end: date, out: Path, notes: bool = False) -> dict:
    """Write every file. Returns the numbers the script prints (and --check tests)."""
    patients, unknown_ids = make_patients(student)
    doctors = make_doctors(student)
    window = [end - timedelta(days=days - 1 - n) for n in range(days)]
    twice = duplicate_day(student, window)

    write_csv(out / "patients.csv", PATIENT_COLUMNS, [public(p, PATIENT_COLUMNS) for p in patients])
    write_csv(out / "doctors.csv", DOCTOR_COLUMNS, [public(d, DOCTOR_COLUMNS) for d in doctors])
    total = 0
    for day in window:
        rows = make_day(student, day, patients, unknown_ids, doctors)
        if day == twice:
            rows = add_duplicates(student, rows)
        write_csv(day_file(out, day), APPOINTMENT_COLUMNS, [public(r, APPOINTMENT_COLUMNS) for r in rows])
        total += len(rows)

    # Safe to run twice: a day file from an earlier run that is outside these days is removed.
    wanted = {day_file(out, day).name for day in window}
    removed = 0
    for old in (out / "appointments").glob("appointments_*.csv"):
        if old.name not in wanted:
            old.unlink()
            removed += 1

    good, bad = make_samples(student, window[0], patients, unknown_ids, doctors)
    write_csv(out / "sample" / "appointments_good.csv", APPOINTMENT_COLUMNS, good)
    write_csv(out / "sample" / "appointments_bad.csv", APPOINTMENT_COLUMNS, bad)
    result = {"patients": len(patients), "doctors": len(doctors), "day_files": len(window),
              "rows": total, "first": window[0], "last": window[-1], "removed": removed,
              "duplicate_day": twice}
    if notes:                                                  # P15: only with --notes
        result["notes"] = write_notes(student, window, patients, unknown_ids, doctors, out)
    return result


def resend(student: str, day: date, out: Path) -> int:
    """Write one day's file again, as the clinic would send a corrected file: no duplicates."""
    patients, unknown_ids = make_patients(student)
    doctors = make_doctors(student)
    rows = make_day(student, day, patients, unknown_ids, doctors)
    write_csv(day_file(out, day), APPOINTMENT_COLUMNS, [public(r, APPOINTMENT_COLUMNS) for r in rows])
    return len(rows)


def warn_if_not_ignored(out: Path) -> None:
    """Generated data must stay out of Git. Warn if Git would commit the output folder."""
    try:
        inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=out, check=False,
                                capture_output=True, text=True).stdout.strip() == "true"
        ignored = inside and subprocess.run(["git", "check-ignore", "-q", "patients.csv"], cwd=out, check=False,
                                            capture_output=True).returncode == 0
    except OSError:                                            # Git is not installed: nothing to check
        return
    if inside and not ignored:
        print(f"WARNING: Git does not ignore {out.as_posix()}/. Add `{out.name}/` to .gitignore before you commit.")


# ---------------------------------------------------------------- the command line

def parse_day(text: str) -> date:
    try:
        day = date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not a date like 2026-11-12") from None
    if not date(2020, 1, 1) <= day <= date(2099, 12, 31):
        raise argparse.ArgumentTypeError("use a date between 2020-01-01 and 2099-12-31")
    return day


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Make a made-up clinic's patients, doctors and daily appointments files for CareLine (P13).")
    parser.add_argument("--student", help="your student id: the same id always gives the same data")
    parser.add_argument("--days", type=int, default=30, help="how many daily files to write, 1 to 90 (default 30)")
    parser.add_argument("--end", type=parse_day, default=date.today() - timedelta(days=1),
                        help="the last day, YYYY-MM-DD (default: yesterday)")
    parser.add_argument("--out", type=Path, default=Path("data"), help="the folder to write to (default: data)")
    parser.add_argument("--resend", type=parse_day, metavar="YYYY-MM-DD",
                        help="write only this day's appointments file again, as a corrected file")
    parser.add_argument("--notes", action="store_true",
                        help="also write the pilot doctors' visit notes into notes/ (P15 CareLine part 2)")
    parser.add_argument("--check", action="store_true", help="test this script in a temporary folder")
    args = parser.parse_args(argv)

    if args.check:
        return run_check()
    if not args.student or not args.student.strip():
        parser.error("--student is required, for example --student DE-0042")
    if not 1 <= args.days <= 90:
        parser.error("--days must be between 1 and 90")

    print("Made-up clinic data for CareLine. No row belongs to a real person.")
    if args.resend:
        rows = resend(args.student, args.resend, args.out)
        print(f"re-sent {day_file(args.out, args.resend).as_posix()}: {rows:,} appointment rows")
        return 0

    result = generate(args.student, args.days, args.end, args.out, notes=args.notes)
    print(f"patients:   {result['patients']:,} in {(args.out / 'patients.csv').as_posix()}")
    print(f"doctors:    {result['doctors']:,} in {(args.out / 'doctors.csv').as_posix()}")
    print(f"day files:  {result['day_files']:,} in {(args.out / 'appointments').as_posix()}/ "
          f"({result['first']} to {result['last']})")
    print(f"appointment rows: {result['rows']:,}")
    print(f"samples:    {SAMPLE_ROWS} rows each in {(args.out / 'sample').as_posix()}/ "
          f"(appointments_good.csv, appointments_bad.csv)")
    if args.notes:
        n = result["notes"]
        print(f"notes:      {n['files']:,} files in {(args.out / 'notes').as_posix()}/ "
              f"({n['notes']:,} notes, {n['corrections']:,} corrections, {n['words']:,} words)")
        print(f"notes with planted personal data: {n['planted']:,} (task 7 must find them all, then mask them)")
    if result["removed"]:
        print(f"removed {result['removed']} older day files that are outside these days")
    print(f"To make exactly these files again in another folder, add --end {result['last']} to the command.")
    warn_if_not_ignored(args.out)
    return 0


# ---------------------------------------------------------------- --check: test the script

def run_check() -> int:
    """Generate data for test ids in a temporary folder and check every promise in the README."""
    problems: list[str] = []

    def expect(condition: bool, message: str) -> None:
        print(("ok    " if condition else "FAIL  ") + message)
        if not condition:
            problems.append(message)

    end = date(2026, 11, 12)
    folder = Path(tempfile.mkdtemp(prefix="make-clinic-check-"))
    try:
        a, a_again, b = folder / "a", folder / "a-again", folder / "b"
        result = generate("CHECK-0001", 30, end, a)
        generate("  check-0001 ", 30, end, a_again)
        generate("CHECK-0002", 30, end, b)

        files = sorted(p.relative_to(a).as_posix() for p in a.rglob("*.csv"))
        same = all((a / f).read_bytes() == (a_again / f).read_bytes() for f in files)
        expect(same, "the same --student (any case, spaces around it) gives the same bytes")
        expect((a / "patients.csv").read_bytes() != (b / "patients.csv").read_bytes()
               and day_file(a, end).read_bytes() != day_file(b, end).read_bytes(),
               "a different --student gives different data")
        raw_bytes = b"".join((a / f).read_bytes() for f in files)
        expect(b"\r\n" not in raw_bytes, "every file has \\n line endings")

        patients = read_csv(a / "patients.csv")
        doctors = read_csv(a / "doctors.csv")
        known = {p["patient_id"] for p in patients}
        expect(1150 <= len(patients) <= 1260, f"about 1,200 patients ({len(patients)})")
        expect(list(patients[0]) == PATIENT_COLUMNS, "patients.csv has the README's columns")
        expect(len(known) == len(patients) and all(re.fullmatch(r"P\d{6}", i) for i in known),
               "patient ids are unique, P and 6 digits")
        styles = Counter("plain" if re.fullmatch(r"[6-9]\d{9}", p["phone"]) else
                         "plus91" if re.fullmatch(r"\+91 [6-9]\d{4} \d{5}", p["phone"]) else
                         "zero" if re.fullmatch(r"0[6-9]\d{4}-\d{5}", p["phone"]) else "other" for p in patients)
        expect(styles["other"] == 0 and 0.62 < styles["plain"] / len(patients) < 0.78
               and 0.14 < styles["plus91"] / len(patients) < 0.26 and 0.05 < styles["zero"] / len(patients) < 0.15,
               f"three phone formats, about 70/20/10% ({dict(styles)})")
        no_email = sum(p["email"] == "" for p in patients) / len(patients)
        expect(0.25 < no_email < 0.35 and all(p["email"].endswith(tuple(EMAIL_DOMAINS)) for p in patients
                                              if p["email"]), f"about 30% empty emails, all at example domains ({no_email:.1%})")
        impossible = sum(p["date_of_birth"] == "1900-01-01" or p["date_of_birth"] > "2026-12-31" for p in patients)
        expect(impossible == 6, f"6 impossible birth dates, about 0.5% ({impossible})")
        pairs = Counter((p["full_name"], re.sub(r"\D", "", p["phone"])[-10:]) for p in patients)
        same_phone = Counter(re.sub(r"\D", "", p["phone"])[-10:] for p in patients)
        twice = [key for key, n in pairs.items() if n == 2]
        expect(8 <= len(twice) <= 16 and max(pairs.values()) == 2 and
               sum(n == 2 for n in same_phone.values()) == len(twice),
               f"about 1% duplicate registrations: same name and phone, two ids ({len(twice)} pairs)")
        expect({p["gender"] for p in patients} == {"F", "M", "X"} and {p["city"] for p in patients} == set(CITIES)
               and all(re.fullmatch(r"\d{6}", p["pin_code"]) for p in patients), "gender, city and pin_code values")
        expect(all(p["date_of_birth"] <= p["registered_on"] <= LAST_REGISTRATION.isoformat() for p in patients
                   if "1901" < p["date_of_birth"] < "2027"), "nobody registered before birth or after the export")

        expect(len(doctors) == 40 and [d["doctor_id"] for d in doctors] == [f"D{n:03d}" for n in range(1, 41)]
               and len({d["full_name"] for d in doctors}) == 40
               and {d["speciality"] for d in doctors} == set(SPECIALITIES) and {d["branch"] for d in doctors} == set(BRANCHES),
               "doctors.csv: D001 to D040, no flaws")
        doctor_ids = {d["doctor_id"] for d in doctors}

        day_files = sorted((a / "appointments").glob("*.csv"))
        expect(len(day_files) == 30 and day_files[-1].name == f"appointments_{end}.csv", "30 day files ending on --end")
        all_rows, days_with_twice, flaws = [], [], Counter()
        for n, path in enumerate(day_files, start=1):
            rows = read_csv(path)
            if list(rows[0]) != APPOINTMENT_COLUMNS:
                expect(False, f"{path.name} has the README's columns in order")
            day = path.stem.split("_")[1]
            counts = Counter(r["appointment_id"] for r in rows)
            repeated = [i for i, c in counts.items() if c > 1]
            if repeated:
                days_with_twice.append((n, len(rows) - len(repeated), repeated, rows))
            elif not 300 <= len(rows) <= 450:
                expect(False, f"{path.name} has 300 to 450 rows ({len(rows)})")
            for r in rows:
                if r["appointment_date"] != day:
                    flaws["wrong date"] += 1
                slot = datetime.fromisoformat(f"{day}T{r['slot_time']}:00{IST}")
                booked = datetime.fromisoformat(r["booked_at"])
                if booked > slot:
                    flaws["late booking"] += 1
                elif slot - booked > timedelta(days=15):
                    flaws["booked too early"] += 1
                fee = int(r["fee_rupees"])
                if fee > HIGHEST_FEE:
                    flaws["fee ten times"] += 1 if fee % 10 == 0 and LOWEST_FEE <= fee // 10 <= HIGHEST_FEE else 1000
                elif fee < LOWEST_FEE:
                    flaws["fee too low"] += 1
                if r["patient_id"] not in known:
                    flaws["unknown patient"] += 1
                if re.search(r"[0-9]{10}|@", r["reason"]):
                    flaws["personal data"] += 1
                if r["doctor_id"] not in doctor_ids:
                    flaws["unknown doctor"] += 1
                if (r["status"] not in STATUSES or r["payment_mode"] not in PAYMENT_MODES
                        or r["reason_category"] not in REASON_CATEGORIES or r["slot_time"] < "09:00"
                        or r["slot_time"] > "19:45" or r["slot_time"][3:] not in ("00", "15", "30", "45")):
                    flaws["bad value"] += 1
                if any(re.search(r"[0-9]{10}|@", r[c]) for c in APPOINTMENT_COLUMNS if c != "reason"):
                    flaws["10 digits or @ outside reason"] += 1
                if not all(r[c] for c in APPOINTMENT_COLUMNS):
                    flaws["empty value"] += 1
            all_rows.extend(rows)
        n_rows = len(all_rows)
        expect(n_rows == result["rows"], f"the printed row count matches the files ({n_rows:,})")
        expect(len(days_with_twice) == 1, "exactly one day has duplicate appointment ids")
        if days_with_twice:
            position, base, repeated, rows = days_with_twice[0]
            copies = [r for r in rows if r["appointment_id"] in repeated]
            identical = all(sum(r == c for c in copies) == 2 for r in copies)
            expect(10 <= position <= 25 and len(repeated) == 4 and identical and 300 <= base <= 450,
                   f"that day is day {position} of 30, with 4 rows sent twice, identical")
        ids = Counter(r["appointment_id"] for r in all_rows)
        expect(all(re.fullmatch(r"A\d{8}", i) for i in ids) and sum(c > 1 for c in ids.values()) == 4,
               "appointment ids are A and 8 digits, unique across days except those 4")
        for name, low, high in [("unknown patient", 0.001, 0.006), ("fee ten times", 0.0005, 0.005),
                                ("late booking", 0.002, 0.01), ("personal data", 0.012, 0.03)]:
            expect(low <= flaws[name] / n_rows <= high, f"{name}: {flaws[name]} rows ({flaws[name] / n_rows:.2%})")
        for name in ["wrong date", "booked too early", "fee too low", "unknown doctor", "bad value",
                     "10 digits or @ outside reason", "empty value"]:
            expect(flaws[name] == 0, f"no {name} ({flaws[name]})")

        good = read_csv(a / "sample" / "appointments_good.csv")
        bad = read_csv(a / "sample" / "appointments_bad.csv")
        expect(len(good) == len(bad) == SAMPLE_ROWS, "both samples have 150 rows")
        expect(len({r["appointment_date"] for r in good}) == 1
               and len({r["appointment_id"] for r in good}) == SAMPLE_ROWS
               and all(r["patient_id"] in known and r["doctor_id"] in doctor_ids for r in good)
               and all(LOWEST_FEE <= int(r["fee_rupees"]) <= HIGHEST_FEE and r["status"] in STATUSES for r in good)
               and not any(re.search(r"[0-9]{10}|@", r["reason"]) for r in good),
               "the good sample is one clean day with no personal data in reason")
        first_day = read_csv(day_files[0])
        expect(all(r in first_day for r in good), "the good sample's rows are rows of the first day's file")
        changed = [(g, b_) for g, b_ in zip(good, bad) if g != b_]
        expect(len(changed) == 4
               and len({r["appointment_id"] for r in bad}) == SAMPLE_ROWS - 1
               and sum(r["patient_id"] == "" for r in bad) == 1
               and sum(r["fee_rupees"].startswith("-") for r in bad) == 1
               and sum(r["status"] == "DONE" for r in bad) == 1,
               "the bad sample has exactly the four planted faults")

        # --resend: a corrected file for the duplicate day, and a file a drill deleted.
        if days_with_twice:
            dup_day = date.fromisoformat(day_file_name_day(day_files[days_with_twice[0][0] - 1]))
            other_day = end
            before = day_file(a, other_day).read_bytes()
            day_file(a, other_day).unlink()
            main(["--student", "CHECK-0001", "--out", str(a), "--resend", dup_day.isoformat()])
            main(["--student", "CHECK-0001", "--out", str(a), "--resend", other_day.isoformat()])
            fixed = read_csv(day_file(a, dup_day))
            expect(len({r["appointment_id"] for r in fixed}) == len(fixed) == days_with_twice[0][1],
                   "--resend on the duplicate day writes it without the 4 copies")
            expect(day_file(a, other_day).read_bytes() == before, "--resend restores a deleted day file exactly")

        # Running again with a later --end leaves exactly --days files and still one duplicate day.
        generate("CHECK-0001", 30, end + timedelta(days=3), a)
        files_now = sorted((a / "appointments").glob("*.csv"))
        dups = sum(len(read_csv(p)) != len({r["appointment_id"] for r in read_csv(p)}) for p in files_now)
        expect(len(files_now) == 30 and dups == 1, "a second run with a later --end leaves 30 files and one duplicate day")

        # --days other than 30.
        small = generate("CHECK-0003", 7, end, folder / "c")
        expect(small["day_files"] == 7 and len(list((folder / "c" / "appointments").glob("*.csv"))) == 7,
               "--days 7 writes 7 files")

        check_notes(folder / "notes-check", end, expect)
    finally:
        shutil.rmtree(folder, ignore_errors=True)

    print()
    if problems:
        print(f"check FAILED: {len(problems)} problem(s)")
        return 1
    print("check passed")
    return 0


def day_file_name_day(path: Path) -> str:
    return path.stem.split("_")[1]


# The patterns P15 task 7 gives in full: P13's widened phone pattern, the email pattern, and names
# as whole words in any case. --check uses them to prove the planted count and the masking rule.
PHONE_PATTERN = r"[0-9]{5}[ -]?[0-9]{5}"
EMAIL_PATTERN = r"[\w.+-]+@[\w-]+(\.[\w-]+)+"


def names_pattern(names) -> re.Pattern:
    return re.compile(r"\b(" + "|".join(map(re.escape, sorted(set(names), key=len, reverse=True))) + r")\b",
                      re.IGNORECASE)


def has_personal(text: str, names: re.Pattern) -> bool:
    return bool(re.search(PHONE_PATTERN, text) or "@" in text or names.search(text))


def masked(text: str, names: re.Pattern) -> str:
    text = re.sub(EMAIL_PATTERN, "[EMAIL]", text)
    text = re.sub(PHONE_PATTERN, "[PHONE]", text)
    return names.sub("[NAME]", text)


def check_notes(folder: Path, end: date, expect) -> None:
    """--check for --notes: every promise of the README's "Visit notes (P15)" section."""
    import contextlib
    import io

    students = ["CHECK-0001", "CHECK-0002", "CHECK-0003"]
    every_name = names_pattern(FIRST_NAMES_F + FIRST_NAMES_M + FIRST_NAMES_X + LAST_NAMES)
    stats = {}
    for student in students:
        plain, out = folder / student / "plain", folder / student / "with-notes"
        generate(student, 30, end, plain)
        result = generate(student, 30, end, out, notes=True)
        p13_files = sorted(p.relative_to(plain).as_posix() for p in plain.rglob("*.csv"))
        out_files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*.csv") if p.parent.name != "notes")
        patients, unknown_ids = make_patients(student)
        doctors = make_doctors(student)
        window = [end - timedelta(days=29 - n) for n in range(30)]
        notes = make_notes(student, window, patients, unknown_ids, doctors)          # the generator's own view
        visits = {r["appointment_id"]: r for day in window for r in read_csv(day_file(out, day))}
        rows, texts_match, header_ok = [], True, True
        for day in window:
            path = notes_file(out, day)
            raw = path.read_bytes()
            day_rows = read_csv(path)
            header_ok &= raw.startswith((",".join(NOTE_COLUMNS) + "\n").encode()) and b"\r\n" not in raw
            texts_match &= [r["note_text"] for r in day_rows] == [note_text(n) for n in notes[day]]
            for row, note in zip(day_rows, notes[day]):
                rows.append((day, row, note))
        names = names_pattern(word for p in read_csv(out / "patients.csv") + read_csv(out / "doctors.csv")
                              for word in p["full_name"].split(" "))
        stats[student] = {"result": result, "p13_same": p13_files == out_files and all(
            (plain / f).read_bytes() == (out / f).read_bytes() for f in p13_files),
            "rows": rows, "visits": visits, "names": names, "header_ok": header_ok, "texts_match": texts_match,
            "known": {p["patient_id"] for p in patients}}

    expect(all(s["p13_same"] for s in stats.values()),
           "--notes: every P13 file is the same bytes with and without --notes (3 ids)")
    printed = {}
    for flag in ([], ["--notes"]):                             # the same folder, so the printed paths are the same
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            main(["--student", "CHECK-0001", "--end", end.isoformat(), "--out", str(folder / "printed")] + flag)
        printed[bool(flag)] = buffer.getvalue().splitlines()
    added = [line for line in printed[True] if line not in printed[False]]
    expect([line for line in printed[True] if line not in added] == printed[False] and len(added) == 2
           and added[0].startswith("notes:      30 files in ") and added[1].startswith("notes with planted personal data: "),
           "--notes prints P13's lines unchanged, plus two notes lines after the samples line")
    expect(all(s["header_ok"] and s["texts_match"] for s in stats.values())
           and all(len(list((folder / st / "with-notes" / "notes").glob("*.csv"))) == 30 for st in students),
           "notes files: one per day, the README's columns in order, \\n line endings")

    def numbers(fn) -> str:
        return ", ".join(str(fn(s)) for s in stats.values())

    def only(rows, version=None, note_type=None):
        return [(d, r, n) for d, r, n in rows if (version is None or r["version"] == str(version))
                and (note_type is None or r["note_type"] == note_type)]

    pilot_ok = True
    for s in stats.values():
        firsts = only(s["rows"], 1)
        consultations = Counter(r["appointment_id"] for _, r, _ in firsts if r["note_type"] == "consultation")
        wanted = {i for i, v in s["visits"].items() if v["doctor_id"] in PILOT_DOCTORS and v["status"] == "completed"}
        pilot_ok &= set(consultations) == wanted and max(consultations.values()) == 1
        types = {}
        for _, r, _ in firsts:
            types.setdefault(r["appointment_id"], {})[r["note_type"]] = r["note_id"]
        for appointment_id, ids in types.items():
            number = f"N{appointment_id[1:]}"
            pilot_ok &= ids == ({"triage": f"{number}-1", "consultation": f"{number}-2"} if "triage" in ids
                                else {"consultation": f"{number}-1"})
        for _, r, _ in firsts:
            visit = s["visits"][r["appointment_id"]]
            stamp = datetime.fromisoformat(r["written_at"])
            slot = datetime.fromisoformat(f"{visit['appointment_date']}T{visit['slot_time']}:00{IST}")
            minutes = (stamp - slot) / timedelta(minutes=1)
            pilot_ok &= (-20 <= minutes <= -5) if r["note_type"] == "triage" else (10 <= minutes <= 25)
    expect(pilot_ok, "notes only for completed visits of D033 and D037: one consultation each, triage 5 to 20 "
                     "minutes before the slot, consultation 10 to 25 minutes after")
    for s in stats.values():
        firsts = only(s["rows"], 1)
        s["notes"] = len(firsts)
        s["per_day"] = Counter(d for d, _, _ in s["rows"])
        s["triage"] = len(only(firsts, note_type="triage")) / len(firsts)
        newest = {}
        for _, r, _ in s["rows"]:
            newest[r["note_id"]] = r["note_text"]
        s["words"] = sum(len(t.split()) for t in newest.values())
        s["two_chunks"] = sum(len(t.split()) > 60 for t in newest.values()) / len(newest)
        s["longest"] = max(len(t.split()) for t in newest.values())
        s["consultation_words"] = [len(r["note_text"].split()) for _, r, _ in only(firsts, note_type="consultation")]
        s["triage_words"] = [len(r["note_text"].split()) for _, r, _ in only(firsts, note_type="triage")]
        split = re.compile(r"(?<=[.!?])\s+")
        s["consultation_sentences"] = [len(split.split(r["note_text"])) for _, r, _ in only(firsts, note_type="consultation")]
        s["triage_sentences"] = [len(split.split(r["note_text"])) for _, r, _ in only(firsts, note_type="triage")]
    expect(all(500 <= s["notes"] <= 680 and 8 <= min(s["per_day"].values()) and max(s["per_day"].values()) <= 45
               for s in stats.values()),
           f"notes in 30 days: {numbers(lambda s: s['notes'])}; rows a day {numbers(lambda s: min(s['per_day'].values()))} "
           f"to {numbers(lambda s: max(s['per_day'].values()))} (they follow P13's visits)")
    triage = numbers(lambda s: format(s["triage"], ".0%"))
    expect(all(0.2 <= s["triage"] <= 0.3 for s in stats.values()), f"about 25% triage notes ({triage})")
    words = numbers(lambda s: format(s["words"], ","))
    expect(all(25_000 <= s["words"] <= 33_000 and 46 <= s["words"] / s["notes"] <= 53 for s in stats.values()),
           f"words in the newest version of each note: {words} (46 to 53 a note)")
    expect(all(45 <= min(s["consultation_words"]) and max(s["consultation_words"]) <= 85
               and 15 <= min(s["triage_words"]) and max(s["triage_words"]) <= 35 for s in stats.values()),
           "consultation notes have 45 to 85 words, triage notes 15 to 35")
    expect(all(9 <= min(s["consultation_sentences"]) and max(s["consultation_sentences"]) <= 13
               and set(s["triage_sentences"]) <= {2, 3} for s in stats.values()),
           "consultation notes have 9 to 13 sentences, triage notes 2 or 3")
    two_chunks = numbers(lambda s: format(s["two_chunks"], ".0%"))
    expect(all(0.22 <= s["two_chunks"] <= 0.38 and s["longest"] <= 200 for s in stats.values()),
           f"about 30% of notes have more than 60 words, so two chunks at 60 words ({two_chunks}); "
           f"none has more than 200")

    clean_text = True
    for s in stats.values():
        for _, r, n in s["rows"]:
            for kind, text in n["parts"]:
                if kind == "planted":
                    continue
                clean_text &= not has_personal(text, every_name)
                clean_text &= ("It started" in text) == (kind == "story")
                clean_text &= bool(re.search(r"urgent|emergency", text, re.IGNORECASE)) == (
                    kind == "urgency" and text in URGENCY_SENTENCES["urgent"])
                clean_text &= n["side"] is not None or not re.search(r"\b(left|right)\b", text)
            clean_text &= n["planted"] is None or s["visits"][r["appointment_id"]]["patient_id"] in s["known"]
    expect(clean_text, "outside planted sentences: no name, 10 digits or @; 'It started' only in stories; "
                       "'urgent' and 'emergency' only in urgent sentences; left and right only as a side")

    long_window = [end + timedelta(days=2) - timedelta(days=31 - n) for n in range(32)]
    patients, unknown_ids = make_patients("CHECK-0001")
    doctors = make_doctors("CHECK-0001")
    long_notes = make_notes("CHECK-0001", long_window, patients, unknown_ids, doctors)
    stories = [n["story"] for day in long_window for n in long_notes[day] if n["version"] == 1 and n["story"]]
    story_texts = [text for day in long_window for n in long_notes[day] if n["version"] == 1
                   for kind, text in n["parts"] if kind == "story"]
    per_day = Counter(n["day"] for day in long_window for n in long_notes[day] if n["version"] == 1 and n["story"])
    expect(len(stories) == 64 and len(set(stories)) == 64 and set(per_day.values()) == {2}
           and all(text.startswith("It started") for text in story_texts),
           "32 days hold 64 different stories, two a day (D033 and D037), each starting 'It started'")

    corrections_ok, contact, other_changed = True, [], True
    for s in stats.values():
        firsts = {r["note_id"]: (d, r, n) for d, r, n in only(s["rows"], 1)}
        seconds = only(s["rows"], 2)
        by_day = Counter(d for d, _, _ in seconds)
        corrections_ok &= all(by_day.get(day, 0) == (0 if i < 2 else 2) for i, day in enumerate(window))
        corrections_ok &= len({r["note_id"] for _, r, _ in seconds}) == len(seconds)
        for day, r, n in seconds:
            first_day, first, _ = firsts[r["note_id"]]
            corrections_ok &= (first_day == day - timedelta(days=2) and first["appointment_id"] == r["appointment_id"]
                               and first["note_type"] == r["note_type"] and first["note_text"] != r["note_text"]
                               and r["written_at"][11:16] >= "09:00" and r["written_at"][11:16] <= "19:00")
            same_masked = masked(first["note_text"], s["names"]) == masked(r["note_text"], s["names"])
            if n["correction"] == "contact":
                contact.append(same_masked)
            else:
                other_changed &= not same_masked
    expect(corrections_ok, "2 corrections a day from the third day: version 2 of a note written two days "
                           "before, same ids and type, new text, at most one per note")
    expect(contact and all(contact) and other_changed,
           f"a contact correction ({len(contact)} in 3 ids) leaves the masked text unchanged; every other correction changes it")

    planted_ok, masked_ok = True, True
    for s in stats.values():
        found = [has_personal(r["note_text"], s["names"]) for _, r, _ in s["rows"]]
        planted = [n["planted"] is not None for _, _, n in s["rows"]]
        planted_ok &= found == planted and s["result"]["notes"]["planted"] == sum(planted)
        masked_ok &= not any(has_personal(masked(r["note_text"], s["names"]), s["names"]) for _, r, _ in s["rows"])
        s["planted"] = sum(planted) / len(planted)
    expect(planted_ok and all(0.10 <= s["planted"] <= 0.20 for s in stats.values()),
           f"P13's phone pattern, @ and names in any case find exactly the planted rows, no miss and no false "
           f"positive, about 15% of rows ({numbers(lambda s: s['result']['notes']['planted'])})")
    expect(masked_ok, "after masking emails, then phones, then names, the scan finds nothing")

    first30 = folder / "CHECK-0001" / "with-notes"
    longer = folder / "CHECK-0001" / "longer"
    generate("CHECK-0001", 32, end + timedelta(days=2), longer, notes=True)
    expect(all(notes_file(first30, day).read_bytes() == notes_file(longer, day).read_bytes()
               and day_file(first30, day).read_bytes() == day_file(longer, day).read_bytes() for day in window)
           and len(list((longer / "notes").glob("*.csv"))) == 32,
           "--days 32 --end E+2 leaves the first 30 notes and appointments files the same bytes as --days 30 --end E")
    one = generate("CHECK-0002", 1, end, folder / "one-day", notes=True)["notes"]
    expect(one["files"] == 1 and one["corrections"] == 0, "--days 1 --notes writes one notes file with no corrections")


if __name__ == "__main__":
    sys.exit(main())
