# Fix: Login, Register, and Payment Not Working

## Root Cause

The error **"no such table: auth_user"** occurs because:

1. The database configuration in `settings.py` previously had `NAME: "insta"` hardcoded (instead of using `db.sqlite3`), creating/wrongly referencing a database called `insta` that doesn't have the auth tables.
2. The development server was running with stale/cached code and hasn't been restarted after the settings fix.

## Steps to Fix

### 1. Restart the Development Server

Stop the running server (Ctrl+C) and restart it so it picks up the fixed `settings.py`:

```powershell
python manage.py runserver 127.0.0.1:8000
```

### 2. Run Migrations

Ensure all database tables are created (including `auth_user`):

```powershell
python manage.py migrate
```

### 3. Create a Superuser (for admin access)

```powershell
python manage.py createsuperuser
```

### 4. Verify Login/Register/Payment

After the server is running with the fixed code:

- **Login**: Go to `http://127.0.0.1:8000/accounts/login/` — should work now that `auth_user` table exists
- **Register**: Go to `http://127.0.0.1:8000/accounts/register/` — creates a user and logs them in
- **Payment**: After logging in, validate a URL, then proceed to payment. The Razorpay test mode keys are already configured in `.env`.

## Code Changes Already Made

The following fixes are already in place:

| File | Fix |
|------|-----|
| `config/settings.py` | Fixed database `NAME` from hardcoded `"insta"` to `BASE_DIR / "db.sqlite3"`; fixed env var names (`DB_USER`, `DB_PASSWORD`, etc.) |
| `config/settings.py` | Removed duplicate `INSTAGRAM_PROVIDER` code at bottom of file |
| `downloader/views.py` | Added `@login_required` to `validate_url_view` so URL validation requires authentication |
| `static/js/app.js` | Added auth redirect to `/accounts/login/?next=<path>` on 401/403/redirect responses; added download status polling after payment verification |
| `downloader/tests/test_views.py` | Updated `test_invalid_url_validation_anonymous` to expect 302 redirect (login required) |

## Verification

All 26 tests pass:
```
Ran 26 tests in ~15s
OK
```

And `python manage.py check` reports no issues.

## If You Still See "no such table: auth_user"

Delete any stray `insta` database file in the project root, then:
1. Stop the server
2. Run `python manage.py migrate`
3. Restart the server