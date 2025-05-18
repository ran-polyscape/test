import sqlite3
import argparse
from datetime import datetime

DB_NAME = 'cases.db'

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    created_at TEXT NOT NULL
)
'''


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()


def add_case(title, description=None, status='open'):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cases (title, description, status, created_at) VALUES (?, ?, ?, ?)',
        (title, description, status, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def list_cases():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT id, title, description, status, created_at FROM cases')
    rows = cur.fetchall()
    conn.close()
    return rows


def update_case(case_id, title=None, description=None, status=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    updates = []
    params = []
    if title is not None:
        updates.append('title = ?')
        params.append(title)
    if description is not None:
        updates.append('description = ?')
        params.append(description)
    if status is not None:
        updates.append('status = ?')
        params.append(status)
    params.append(case_id)
    if updates:
        sql = 'UPDATE cases SET ' + ', '.join(updates) + ' WHERE id = ?'
        cur.execute(sql, params)
        conn.commit()
    conn.close()


def delete_case(case_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('DELETE FROM cases WHERE id = ?', (case_id,))
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='Case Management System')
    subparsers = parser.add_subparsers(dest='command')

    parser_init = subparsers.add_parser('initdb', help='Initialize database')

    parser_add = subparsers.add_parser('add', help='Add new case')
    parser_add.add_argument('--title', required=True, help='Case title')
    parser_add.add_argument('--description', help='Case description')
    parser_add.add_argument('--status', default='open', help='Case status')

    parser_list = subparsers.add_parser('list', help='List cases')

    parser_update = subparsers.add_parser('update', help='Update case')
    parser_update.add_argument('id', type=int, help='Case ID')
    parser_update.add_argument('--title', help='New title')
    parser_update.add_argument('--description', help='New description')
    parser_update.add_argument('--status', help='New status')

    parser_delete = subparsers.add_parser('delete', help='Delete case')
    parser_delete.add_argument('id', type=int, help='Case ID')

    args = parser.parse_args()

    if args.command == 'initdb':
        init_db()
        print('Database initialized.')
    elif args.command == 'add':
        add_case(args.title, args.description, args.status)
        print('Case added.')
    elif args.command == 'list':
        cases = list_cases()
        for case in cases:
            print(f"{case[0]} | {case[1]} | {case[2]} | {case[3]} | {case[4]}")
    elif args.command == 'update':
        update_case(args.id, args.title, args.description, args.status)
        print('Case updated.')
    elif args.command == 'delete':
        delete_case(args.id)
        print('Case deleted.')
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
