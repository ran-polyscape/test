# Case Management System

This is a simple command-line case management system written in Python.
It uses SQLite for storage.

## Setup

Run the following command to initialize the database:

```bash
python3 case_manager.py initdb
```

## Usage

Add a case:

```bash
python3 case_manager.py add --title "Example" --description "Sample case" --status "open"
```

List all cases:

```bash
python3 case_manager.py list
```

Update a case:

```bash
python3 case_manager.py update <id> [--title NEW_TITLE] [--description NEW_DESC] [--status NEW_STATUS]
```

Delete a case:

```bash
python3 case_manager.py delete <id>
```

The database is stored in `cases.db` in the project directory.
