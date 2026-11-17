# ReelPay

ReelPay is a Django application for authorized Instagram Reel downloads at ₹1 per download.

## Architecture and assumptions

- Django 5.2, Python 3.12+.
- SQLite for local development, PostgreSQL for production.
- Razorpay test mode by default.
- Demo media provider uses a licensed sample file and does not retrieve real Instagram content.
- Real Instagram retrieval requires configuring an authorized provider and enabling `AUTHORIZED_MEDIA_PROVIDER_ENABLED`.
- Monetary values are stored as integer paise.
- Background processing uses a database-backed queue and management commands. Production can replace it with Celery and Redis.

## Project structure

See the required structure in the repository root.

## Windows installation

```powershell
mkdir ReelPay
cd ReelPay
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```cmd
venv\Scripts\activate.bat
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the project has not already been generated:

```powershell
django-admin startproject config .
python manage.py startapp downloader
```

This repository already contains the complete project, so do not run `startproject` or `startapp` again. Instead run:

```powershell
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and admin at `http://127.0.0.1:8000/admin/`.

## Environment variables

Copy `.env.example` to `.env` and update values. Never commit `.env`.

## AI help chat

A floating ReelPay help chat is available on every page. It works without an
external provider: pricing, payment, download, status, refund, account, privacy,
and demo-mode questions are answered from a built-in ReelPay knowledge base.

To use an OpenAI-compatible chat completions provider, set:

```dotenv
AI_CHAT_ENABLED=True
AI_CHAT_API_URL=https://api.openai.com/v1/chat/completions
AI_CHAT_API_KEY=your-provider-key
AI_CHAT_MODEL=gpt-4o-mini
AI_CHAT_TIMEOUT=15
```

If the key is empty, the provider is disabled, or the provider request fails,
ReelPay automatically falls back to the local answers. With a provider
configured, chat messages are sent to that provider. Set
`AI_CHAT_ENABLED=False` to hide the widget and disable the endpoint.

The chat endpoint is `POST /api/ai-chat/` with JSON
`{"message": "...", "history": [...]}` and returns
`{"answer": "...", "suggestions": [...], "source": "ai|local"}`. The endpoint is
CSRF-protected and rate limited. Never put a provider key in client-side code.

## Razorpay test setup

1. Create a Razorpay account.
2. Enable test mode.
3. Obtain test API key ID and secret.
4. Set `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, and `RAZORPAY_WEBHOOK_SECRET`.
5. Run the app and create a download request.
6. Use Razorpay test cards/UPI to test success, failure, and cancellation.
7. Configure webhook URL `https://your-domain/webhooks/razorpay/`.
8. Verify webhook signatures in the dashboard and server logs.
9. Test duplicate events by replaying a webhook.
10. Switch to live mode only after verification and business approval.

## Background processing

Development:

```powershell
python manage.py process_downloads --once
python manage.py cleanup_artifacts
```

Production: run `python manage.py process_downloads --loop` as a worker, or replace with Celery/Redis.

## Production deployment

- Set `DEBUG=False`.
- Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- Use PostgreSQL via `DATABASE_URL`.
- Configure persistent/object storage for private artifacts.
- Run `python manage.py collectstatic`.
- Run migrations during deploy.
- Configure HTTPS and HSTS.
- Configure Razorpay production webhook.
- Schedule `cleanup_artifacts`.
- Back up PostgreSQL regularly.

Ephemeral hosting filesystems may lose generated files during redeployment. Do not rely on SQLite or local disk for production financial records or downloads.

## Troubleshooting

- Payment not verified: check Razorpay keys and signature.
- Download stuck in PAID: run `process_downloads`.
- Expired download: request a new download; do not reuse expired links.
- Webhook duplicates: idempotency keys prevent duplicate processing.
- Missing demo sample: ensure `media/demo/sample_reel.mp4` exists.
- Missing home phone preview: ensure `media/demo/reelpay_how_to.mp4` exists (the generated ReelPay how-to reel shown in the phone mockup).
- Help chat uses local answers: set `AI_CHAT_API_KEY` and check `AI_CHAT_API_URL`/`AI_CHAT_MODEL`.
- Rate limiting: wait and retry.

## Tests

```powershell
python manage.py test
```
