# LeetQuery
# Copyright (C) 2025 Yusuf Özçetin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import sqlite3
import sys
import os

DB_NAME = "problems.db"

def search_loop(db_path):
    print("\n-------------------------------------------------")
    print("LeetCode Company Search Engine")
    print(f"Database: {DB_NAME}")
    print("Type 'q' or 'exit' to quit.")
    print("-------------------------------------------------")

    try:
        db_uri = f'file:{db_path}?mode=ro'
        with sqlite3.connect(db_uri, uri=True) as conn:
            cursor = conn.cursor()

            while True:
                query = input("\nEnter problem title to search: ").strip()

                if query.lower() in ('q', 'exit'):
                    print("Exiting...")
                    break

                if not query:
                    continue

                search_key = query.lower()

                cursor.execute("SELECT company_list FROM problem_cache WHERE title_key = ?", (search_key,))

                result = cursor.fetchone()

                if result:
                    company_string = result[0]
                    companies = company_string.split(',')

                    print(f"\nCompanies asking for '{query}':")
                    for company in companies:
                        print(f"  - {company}")
                else:
                    print(f"\nProblem '{query}' not found in database.")
                    print("Hint: Check your spelling or try another problem.")

    except sqlite3.OperationalError as e:
        print(f"DATABASE ERROR: {e}", file=sys.stderr)
        print(f"Could not open '{db_path}'.", file=sys.stderr)
        print("Please make sure 'build_database.py' has been run successfully.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(script_dir, DB_NAME)

    if not os.path.exists(db_path):
        print(f"ERROR: Database file '{db_path}' not found.", file=sys.stderr)
        print("Please run 'build_database.py' one time to create the database.", file=sys.stderr)
        sys.exit(1)

    search_loop(db_path)

if __name__ == "__main__":
    main()
