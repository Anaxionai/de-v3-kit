# Clinic data for CareLine (P13)

> **This data is made up.** No row belongs to a real person.
> Every name, phone number and email address comes from a generator.
> Even so, treat it as personal data: that is what CareLine practises.

CareLine reads the daily files of a clinic chain with 40 doctors in 5 branches.
`make_clinic.py` writes those files for you: a patient list, a doctor list, one appointments file for each day, and two small sample files.

## Make your data

Run it in Git Bash, from inside your `careline/` folder. Put your own student id after `--student`:

```bash
uv run python ~/de-kit/data/clinic/make_clinic.py --student <your-id> --days 30
```

It uses only the Python standard library, so it runs in any uv project, including CareLine's.
It writes into `data/`, which your `.gitignore` must ignore. If Git would commit `data/`, the script prints a warning.

At the end it prints what it wrote. With `--student DE-0042 --end 2026-11-12` it printed:

```text
Made-up clinic data for CareLine. No row belongs to a real person.
patients:   1,209 in data/patients.csv
doctors:    40 in data/doctors.csv
day files:  30 in data/appointments/ (2026-10-14 to 2026-11-12)
appointment rows: 12,070
samples:    150 rows each in data/sample/ (appointments_good.csv, appointments_bad.csv)
To make exactly these files again in another folder, add --end 2026-11-12 to the command.
```

Your numbers differ: every student id gives different data.
Thirty days are about 12,000 appointment rows and 1.7 MB on disk.

### The same data in every task

The same student id always gives exactly the same data, on any computer.
The days end on `--end`, which is **yesterday** unless you give it.

Each CareLine task copies your `careline/` folder **without** `data/`.
So in each new task folder, make the data again with the **same** `--end` as your first run (the script printed it):

```bash
uv run python ~/de-kit/data/clinic/make_clinic.py --student <your-id> --days 30 --end 2026-11-12
```

Without `--end`, a run on a later day moves all 30 days forward, and your notes about a day no longer match.

### Options

| Option | Meaning | Default |
|---|---|---|
| `--student` | Your student id. Capital and small letters count as the same. | (required) |
| `--days` | How many daily files to write, 1 to 90. | `30` |
| `--end` | The last day, as `YYYY-MM-DD`. | yesterday |
| `--out` | The folder to write to. | `data` |
| `--resend` | Write one day's appointments file again, as a corrected file from the clinic. Nothing else changes. | (none) |
| `--check` | Test the script itself in a temporary folder, then delete the folder. | (off) |

Running it again is safe. It writes the same files again, and it removes day files from an earlier run that fall outside the new days.

## The files

All files are UTF-8 CSV with one header row and `\n` line endings.
Dates look like `2026-11-12`. Times of day look like `14:30`. Timestamps are in India time, for example `2026-11-02T08:41:00+05:30`.
An empty value is an empty string. A text with a comma is in double quotes, so read the files with a CSV reader, never by splitting lines at commas.

| File | Rows | What it is |
|---|---|---|
| `data/patients.csv` | about 1,200 | Everyone registered with the clinic chain when the list was exported |
| `data/doctors.csv` | 40 | The doctors: one of each speciality in each branch |
| `data/appointments/appointments_YYYY-MM-DD.csv` | 300 to 450 a day | One file for each day: every appointment booked for that day and what happened |
| `data/sample/appointments_good.csv` | 150 | 150 rows of one day, with no faults and no personal data in `reason` |
| `data/sample/appointments_bad.csv` | 150 | The same 150 rows with four faults planted on purpose (below) |

The examples in the three tables below are real rows made with `--student DE-0042`. The phone number is hidden on purpose.

### `patients.csv`

| Column | Meaning | Example |
|---|---|---|
| `patient_id` | The patient's id: `P` and 6 digits | `P170513` |
| `full_name` | First name and surname | `Gauri Menon` |
| `phone` | Mobile number, as the front desk typed it | `9XXXXXXXXX` |
| `email` | Email address. Empty when the patient gave none, which is allowed | `gauri.menon60@example.com` |
| `date_of_birth` | Date of birth | `1994-10-04` |
| `gender` | `F`, `M` or `X` | `F` |
| `city` | One of 8 cities: Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad | `Kolkata` |
| `pin_code` | Postal PIN code, 6 digits | `700043` |
| `registered_on` | The day the patient registered | `2020-05-22` |

### `doctors.csv`

| Column | Meaning | Example |
|---|---|---|
| `doctor_id` | `D001` to `D040` | `D011` |
| `full_name` | The doctor's name | `Tarun Yadav` |
| `speciality` | `general`, `paediatrics`, `dermatology`, `cardiology`, `orthopaedics`, `gynaecology`, `ent` or `dental` | `dermatology` |
| `branch` | `north`, `south`, `east`, `west` or `central` | `south` |
| `joined_on` | The day the doctor joined the clinic | `2013-10-18` |

### `appointments_YYYY-MM-DD.csv`

The columns, in this order:

| Column | Meaning | Example |
|---|---|---|
| `appointment_id` | The booking's id: `A` and 8 digits, unique across all days | `A09783001` |
| `patient_id` | The patient, from `patients.csv` | `P170513` |
| `doctor_id` | The doctor, from `doctors.csv` | `D011` |
| `appointment_date` | The day of the appointment: always the file's day | `2026-10-14` |
| `slot_time` | Start of the 15-minute slot, from `09:00` to `19:45` | `13:15` |
| `booked_at` | When the booking was made: up to 14 days before the slot | `2026-09-30T07:46:00+05:30` |
| `status` | `booked`, `completed`, `cancelled` or `no_show` | `completed` |
| `fee_rupees` | The fee in whole rupees, from 300 to 1,500 depending on the speciality | `1300` |
| `payment_mode` | `cash`, `upi`, `card` or `insurance` | `insurance` |
| `reason_category` | `consultation`, `follow_up`, `test_results`, `vaccination` or `procedure` | `procedure` |
| `reason` | Short free text typed at the front desk | `chemical peel, first sitting` |

Revenue in CareLine counts only `completed` appointments.

### The two sample files

Both come from the first of your days. You may commit them in `careline/sample/`: they hold 150 generated rows, under the course's limit of 200.

`appointments_bad.csv` is `appointments_good.csv` with exactly four faults, each in a different row:

1. one `appointment_id` appears twice;
2. one `patient_id` is empty;
3. one `fee_rupees` is negative;
4. one `status` is `DONE`, which is not an allowed value.

Your tests use them: checks must pass on the good file and fail on the bad one.

## Which columns are personal data

| File | Personal data | Why |
|---|---|---|
| `patients.csv` | `patient_id`, `full_name`, `phone`, `email`, `date_of_birth`, `gender`, `pin_code` | Each one, alone or with the others, points to one person. |
| `patients.csv` | `city` (low risk) | Not personal alone, but it narrows the search when joined with other columns. |
| `doctors.csv` | `doctor_id`, `full_name` | The doctors are people too. |
| `appointments_*.csv` | `patient_id`, `doctor_id` | They link a visit to a person. |
| `appointments_*.csv` | `reason` | Free text: anyone at the desk can type anything into it, including contact details. |

`status`, `fee_rupees`, `payment_mode`, `reason_category`, the dates and the times are not personal data alone. Once they are joined to a patient, they are.

## What to expect

Real clinic exports are never perfect, and these files copy that.
The front desk, the booking system and late registrations all leave marks in the data.
This README does not list them: your profile in CareLine's first task finds them, with numbers.
Every student's data has the same kinds of problems, on different rows and days.

The values in `status`, `payment_mode` and `reason_category` always use exactly the spellings above.
`doctors.csv` has no faults.

## Reading the files

- pandas: `pandas.read_csv(path, dtype=str, keep_default_na=False)` keeps every value as text and keeps empty strings empty, as CareLine's `raw` tables expect.
- PostgreSQL: load every column as `TEXT` into `raw`, then convert types in `clean`.
- DuckDB, for a quick look: `SELECT * FROM read_csv('data/appointments/*.csv', all_varchar = true, filename = true);`

## How the data is made

- The script turns your student id into a seed (a starting number) for Python's random number generator. The same id always gives the same numbers, so the same files.
- Each day's file depends only on your id and that day. That is why `--resend` can write one day again exactly.
- Names are random pairs from short lists of first names and surnames. Any match with a real person is chance.
- Phone numbers are 10 random digits that start with 6, 7, 8 or 9, the way Indian mobile numbers do. They belong to nobody on purpose. **Never call or message one.**
- Email addresses end in `example.com`, `example.net` or `example.org`. These domains are reserved for examples, so no real mailbox has them.

There is no third-party data in these files, so there is no licence to follow and no credit line to give.

## Visit notes (P15)

In P15 (CareLine part 2) the clinic also sends the visit notes its doctors type.
Add `--notes` to your P13 command, with the **same** `--end` day:

```bash
uv run python ~/de-kit/data/clinic/make_clinic.py --student <your-id> --days 30 --end <your end day> --notes
```

`--notes` changes nothing in the P13 files: `patients.csv`, `doctors.csv`, the appointments files and the samples are the same bytes with or without it.
It adds the folder `data/notes/` and two lines after the samples line. With `--student DE-0042 --end 2026-11-12` it printed:

```text
notes:      30 files in data/notes/ (586 notes, 56 corrections, 29,405 words)
notes with planted personal data: 92 (task 7 must find them all, then mask them)
```

- **notes**: the notes in the files (each counted once), **corrections**: the rows that correct a note, **words**: the words in the newest version of every note.
- **planted personal data**: the note rows (originals and corrections) that hold a phone number, an email or a name. Task 7's scan of the raw notes must find exactly this number.

Your numbers differ: they follow your appointments. Most ids give 550 to 650 notes and 27,000 to 32,000 words in 30 days.
`--days`, `--end` and `--out` work as for P13. `--resend` writes only an appointments file, never notes.

### The notes files

`data/notes/notes_YYYY-MM-DD.csv`, one for each day: UTF-8, one header row, `\n` line endings, quotes only where a value needs them.
A file holds the notes **written** on that day, sorted by `written_at`. A day file outside your days is removed, as for appointments.
A later `--end` with the same first day only adds files: `--days 31 --end <your end day + 1>` leaves your 30 files the same bytes and adds one.

The columns, in this order:

| Column | Meaning | Example |
|---|---|---|
| `note_id` | `N`, the 8 digits of the appointment id, `-` and the note's number in that visit (1 or 2) | `N09812317-1` |
| `version` | `1` for the note as first written, `2` for a correction. A note is corrected at most once | `1` |
| `appointment_id` | The visit, from that day's appointments file | `A09812317` |
| `note_type` | `triage` (the nurse, before the visit) or `consultation` (the doctor) | `consultation` |
| `written_at` | When the note was saved, India time | `2026-11-12T09:44:00+05:30` |
| `note_text` | The note in plain English, on one line | below |

### Who writes notes

Only two pilot doctors type notes, both in the central branch: **`D033`** (general) and **`D037`** (orthopaedics).
Every one of their visits with status `completed` has a **consultation** note from the doctor, saved 10 to 25 minutes after the slot starts.
About 1 in 3 of those visits also has a **triage** note from the nurse, saved 5 to 20 minutes before the slot. Then the triage note is `-1` and the consultation `-2`; with no triage note, the consultation is `-1`.
Other doctors' visits have no notes, and the rows sent twice on the duplicate day give no extra notes.

### What a note says

A consultation note has these sentences, in this order (45 to 85 words, 9 to 13 sentences):

1. the complaint, with the side where it has one, and how long: "Pain in the left knee for three months.";
2. two details, and one sentence of history ("Has had asthma since childhood.");
3. sometimes a story sentence (below);
4. one or two findings ("Walks with a slight limp.", "Blood pressure 134/84, pulse 71.");
5. one urgency sentence, one or two plans, one piece of advice and a follow-up ("Follow up in a month.").

A real consultation note (`DE-0042`, version 1):

> Pain in the left knee for three months. Clicking when bending the knee. Cannot squat or sit on the floor. Has had asthma since childhood. Walks with a slight limp. No warning signs; routine care. X-ray of the left knee ordered. Ice pack on the knee twice a day. Follow up in a month.

A triage note has 2 or 3 sentences (15 to 35 words): the same complaint in lower case, then the vital signs.

> Came in with pain in the left wrist for two days. BP 139/73, pulse 84, temperature 37.1 C, oxygen 99 percent.

**Complaints and body areas.** Each complaint belongs to one doctor and one body area:

| Doctor | Complaint (as the note writes it) | Body area |
|---|---|---|
| `D033` | fever and body ache; feeling tired all the time | `whole body` |
| `D033` | dry cough; chest tightness when climbing stairs | `chest` |
| `D033` | sore throat | `throat` |
| `D033` | headache; dizziness when standing up | `head` |
| `D033` | stomach pain after meals; diarrhoea | `abdomen` |
| `D033` | itchy rash on both arms | `skin` |
| `D037` | pain in the left (or right) knee | `knee` |
| `D037` | lower back pain | `back` |
| `D037` | neck pain | `neck` |
| `D037` | stiffness in the left (or right) shoulder | `shoulder` |
| `D037` | swelling of the left (or right) ankle | `ankle` |
| `D037` | pain in the left (or right) wrist | `wrist` |
| `D037` | pain in the left (or right) hip | `hip` |

So the **13 body areas** are: `head`, `throat`, `chest`, `abdomen`, `skin`, `whole body`, `back`, `neck`, `shoulder`, `wrist`, `hip`, `knee`, `ankle`. Task 10 accepts exactly these.

How long: `since yesterday`, `for two days`, `for three days`, `for five days`, `for a week`, `for ten days`, `for two weeks`, `for a month`, `for three months`.

**Urgency.** Every consultation note has one urgency sentence, at one of three levels (about 60%, 30% and 10% of notes):

| Level | The sentence is one of |
|---|---|
| `routine` | "No warning signs; routine care." / "Routine follow-up only." |
| `soon` | "Review within a week if it is no better." / "Come back in three days if no better." |
| `urgent` | "Urgent: sent to the emergency department today." / "Urgent: go to the emergency department at once if it gets worse." / "Urgent referral to the specialist today." |

The words **urgent** and **emergency** appear only in the urgent sentences. Triage notes have no urgency sentence.

**Stories.** Each day, one consultation note of `D033` and one of `D037` hold a story sentence: how the problem began, with two details you can ask about in other words. A story always starts with **`It started`**, and nothing else in a note does:

> It started after he skipped breakfast and lunch on a busy moving day.

There are 32 general and 32 orthopaedic stories, and a day's stories depend on its date, so any 32 days in a row hold 64 different stories, each in exactly one note. That makes a story note the one right answer to a question about it: your test set in tasks 9 and 12 is built from them (`masked_text LIKE '%It started%'`).

### Corrections

On every day whose day-before-yesterday is among your days, two notes written two days earlier come back corrected. The first two files of your days hold no corrections; every later file holds two.
A correction is a new row with the same `note_id`, `appointment_id` and `note_type`, `version` `2`, and the **whole new text**. It is saved between 09:00 and 19:00 on the day it arrives. What it changes:

- the side, left and right swapped everywhere in the note;
- how long, in the first sentence;
- a line added at the end: "Added on review: Follow up in one week.";
- the urgency sentence, to another level;
- a contact detail: the phone number's digits or the email's number. Once masked, such a note reads exactly as before.

A real correction (`DE-0042`): `N09810202-2` was written on 2026-11-10 with "for five days"; the file of 2026-11-12 holds its version 2 with "for two weeks".
`clean.visit_notes` keeps the newest version of each note. Only a corrected note's chunks are rebuilt.

### Planted personal data

People type things into notes that should not be there, so about 15% of note rows hold **one** planted sentence with personal data, always about the visit's own patient (never for a patient missing from `patients.csv`). A correction keeps the planted sentence of its note.

| Kind | What appears |
|---|---|
| Phone number | The patient's mobile number, in one of five forms: `9876543210`, `98765 43210`, `98765-43210`, `+91 98765 43210`, `098765-43210` |
| Email | The patient's email from `patients.csv`, or `first.last@example.com` when it is empty |
| Full name | First name and surname, such as "Gauri Menon asked for a morning slot next time." |
| Full name in capitals | Triage notes only: "Name on the file: GAURI MENON." |
| First name | "Gauri says it is worse at night." |
| Title and surname | `Ms` or `Mr` and the surname. A patient with gender `X` gets the full name instead |
| A family member's first name | A first name from your `patients.csv`: "A family member, Ravi, will collect the report." |
| A doctor's surname | A surname from your `doctors.csv`: "Referred to Dr Yadav for a second opinion." |

Every name in a note comes from your `patients.csv` or `doctors.csv`. Outside the planted sentences, no note holds a first name or surname from those lists, ten digits in a row (or with one space or dash after the fifth), or an `@`.

### Only masked text goes to a model

The notes are made up, and you still treat them as real clinic notes: the course's rule is that **only masked text is ever sent to a model**.
Google's terms for the free Gemini API say: "Do not submit sensitive, confidential, or personal information to the Unpaid Services."

- Task 7 loads the notes into `raw.visit_notes` and writes the masked text into `clean.visit_notes`: emails first (`[\w.+-]+@[\w-]+(\.[\w-]+)+` becomes `[EMAIL]`), then phone numbers with P13's pattern (`[0-9]{5}[ -]?[0-9]{5}` becomes `[PHONE]`), then every first name and surname in `raw.patients` and `raw.doctors` as a whole word in any case (`[NAME]`). A scan proves it: raw finds the planted count, clean finds 0.
- From task 9, every call to a model (embedding, chat or extraction) goes through `assert_masked()`, which refuses text that still holds personal data.
- Chunks, embeddings, questions and anything you paste into `AI_LOG.md` come from `clean.visit_notes`, never from `raw`.
- The limit: masking by list finds only the names on the list. A name that is in neither file would slip through. The generator plants only names from your files, so you can prove your mask; real notes need more.

`note_text` is personal data, like `reason` in P13: free text that anyone can type anything into. `appointment_id` links a note to a patient. The model names and the calls are in [`models.md`](models.md).

`--check` (below) also tests every promise of this section.

## For mentors

- `--resend YYYY-MM-DD` writes that day's file again, as the clinic would send a corrected file. It removes rows that were sent twice, and it brings back a file that was deleted or broken. The incident drill uses it.
- `--check` generates data for three test ids in a temporary folder and checks every promise in this README. It ends with `check passed`. Run it after any change to the script:

```bash
uv run python ~/de-kit/data/clinic/make_clinic.py --check
```
