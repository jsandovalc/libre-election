# Libre-election
Simple site to perform elections.

# Requirements

- Python 3.x (tested on 3.7. Proably works on 3.6 --I want to use
  f-strings--).
- Django.
- PostgreSQL (Probably others, but not tested).

# Development

1. Create a virtualenv for local testing.
2. Copy local_settings.py.example to local_settings.py.
3. Create a PostgreSQL database for testing.
4. Configure database.
5. Run migrations (insert code snippet).
6. Create a django superuser.

# Quickstart

1. Go to django admin and create an election.
2. Create a polling station.
3. Create a voting jury.
4. Create a voting user.

## To vote

Go to / and login as a voting jury. Now users can vote with their
document number.
