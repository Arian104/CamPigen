# Enterprise Email Platform

A multi-tenant email marketing and delivery platform built with **Django**, **Django REST Framework**, **Celery**, **Redis**, SMTP routing, and **Next.js**.

The platform supports organizations, contacts, contact lists, campaign templates, scheduled campaigns, instant sending, SMTP pools, tracked links, webhooks, and analytics foundations.

---

## 1. Tech Stack

### Backend

* Django
* Django REST Framework
* Simple JWT
* Celery
* Redis
* SQLite for local development

### Frontend

* Next.js
* React
* TypeScript
* Lucide React
* Recharts

---

## 2. Project Structure

```txt
email_platform/
├── accounts/
├── analytics/
├── campaigns/
├── contacts/
├── core/
├── email_engine/
├── events/
├── frontend/
├── links/
├── organizations/
├── webhooks/
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## 3. Main Features

### Organization Management

* Multi-tenant organization support
* Organization branding
* Campaign default sender settings
* Compliance settings
* Social links
* Plan and feature limits

### Contact Management

* Contacts
* Tags
* Contact lists
* Contact list memberships
* Custom contact fields

### Campaign Management

* Campaign creation
* Campaign editing
* Template selection
* Contact list targeting
* Scheduled sending
* Local time to UTC conversion
* Campaign status tracking

### Email Engine

* Email job queue
* SMTP routing
* SMTP health checks
* Daily, hourly, and minute sending limits
* Retry logic
* Delivery status tracking

### SMTP Management

* Multiple SMTP configurations
* Active/inactive SMTP status
* Sender name and sender email
* TLS/SSL options
* SMTP health monitoring

### Links

* Tracked redirect links
* Click recording
* Campaign/contact/email-job relationship
* Analytics support

### Webhooks

* Webhook configuration
* Event delivery
* Retry tracking
* CRM, Zapier, Make, Slack, ERP, and dashboard integration support

### Analytics

* Campaign analytics foundation
* Daily organization analytics foundation
* Link analytics foundation

---

## 4. Backend Setup

Go to the project root:

```bash
cd email_platform
```

Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Start backend:

```bash
python manage.py runserver
```

Backend URL:

```txt
http://127.0.0.1:8000
```

API base URL:

```txt
http://127.0.0.1:8000/api
```

---

## 5. Frontend Setup

Go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create `.env.local`:

```bash
cat > .env.local <<'ENV'
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
ENV
```

Start frontend:

```bash
npm run dev
```

Frontend URL:

```txt
http://localhost:3000
```

---

## 6. Redis Setup

Celery uses Redis as the message broker.

Start Redis:

```bash
redis-server
```

Check Redis:

```bash
redis-cli ping
```

Expected output:

```txt
PONG
```

If Redis says the port is already in use, Redis is already running.

---

## 7. Celery Worker

Open a new terminal from the Django project root:

```bash
cd email_platform
source venv/bin/activate
celery -A core worker -l info -Q high_priority,default,low_priority
```

The worker should show tasks such as:

```txt
campaigns.tasks.process_pending_campaigns
campaigns.tasks.process_campaign
email_engine.tasks.process_due_email_jobs
email_engine.tasks.process_email_job
email_engine.tasks.check_smtp_health
webhooks.tasks.deliver_webhook
```

---

## 8. Celery Beat

Open another terminal from the Django project root:

```bash
cd email_platform
source venv/bin/activate
celery -A core beat -l info
```

Celery beat runs scheduled tasks such as:

```txt
process-pending-campaigns
process-due-email-jobs-every-minute
reset-smtp-minute-counters
check-smtp-health
retry-failed-jobs
```

If beat does not detect updated schedules, stop beat and clear old schedule files:

```bash
rm -f celerybeat-schedule
rm -f celerybeat-schedule.db
rm -f celerybeat-schedule.dat
rm -f celerybeat-schedule.dir
```

Then restart beat.

---

## 9. Required Running Terminals

For full local development, keep these running:

### Terminal 1: Django Backend

```bash
cd email_platform
source venv/bin/activate
python manage.py runserver
```

### Terminal 2: Redis

```bash
redis-server
```

### Terminal 3: Celery Worker

```bash
cd email_platform
source venv/bin/activate
celery -A core worker -l info -Q high_priority,default,low_priority
```

### Terminal 4: Celery Beat

```bash
cd email_platform
source venv/bin/activate
celery -A core beat -l info
```

### Terminal 5: Frontend

```bash
cd email_platform/frontend
npm run dev
```

---

## 10. Campaign Sending Flow

```txt
Campaign created from frontend
→ User selects template
→ User selects contact list
→ Frontend converts local schedule time to UTC
→ Campaign saved as scheduled
→ Celery beat runs process_pending_campaigns
→ Campaign processor creates EmailJob rows
→ Email engine processes EmailJob rows
→ SMTP sends the email
→ EmailJob becomes done
→ Campaign becomes completed
```

Campaigns currently send through contact lists:

```txt
Campaign.target_lists
→ ContactListMembership
→ Contact
→ EmailJob
```

A campaign will not send if:

* no contact list is selected
* selected contact list has no contacts
* Celery beat is not running
* Celery worker is not running
* SMTP is inactive or invalid

---

## 11. Timezone Logic

Frontend uses local time.

Backend stores UTC.

Correct frontend conversion:

```ts
scheduled_at: new Date(scheduledAt).toISOString()
```

Example:

```txt
10:10 PM Bangladesh time
= 4:10 PM UTC
```

Frontend displays stored UTC back as local time:

```ts
new Date(value).toLocaleString()
```

---

## 12. SMTP Notes

For Brevo:

```txt
SMTP username is not the sender email.
```

Example Brevo setup:

```txt
Host: smtp-relay.brevo.com
Port: 587
Username: Brevo SMTP username
Password: Brevo SMTP key
TLS: enabled
SSL: disabled
From Email: verified sender email
```

Brevo will reject emails if the sender email or domain is not verified.

---

## 13. Useful Debug Commands

Open Django shell:

```bash
python manage.py shell
```

### Check Campaigns

```python
from campaigns.models import Campaign
from django.utils import timezone

now = timezone.now()

for c in Campaign.objects.order_by("-scheduled_at")[:10]:
    print(c.id, c.name, c.status, c.scheduled_at, c.scheduled_at <= now, c.total_sent)
```

### Check Email Jobs

```python
from email_engine.models import EmailJob

for job in EmailJob.objects.order_by("-scheduled_at")[:10]:
    print(job.id, job.recipient_email, job.subject_snapshot, job.status, job.error_message, job.sent_at)
```

### Check Contact Lists

```python
from contacts.models import ContactList, ContactListMembership

for item in ContactList.objects.all():
    count = ContactListMembership.objects.filter(contact_list=item).count()
    print(item.id, item.name, count)
```

### Manually Process Pending Campaigns

```python
from campaigns.tasks import process_pending_campaigns

print(process_pending_campaigns())
```

### Manually Process One Campaign

```python
from campaigns.models import Campaign
from campaigns.tasks import process_campaign

campaign = Campaign.objects.order_by("-created_at").first()
print(process_campaign(campaign.id))
```

### Manually Process One Email Job

```python
from email_engine.models import EmailJob
from email_engine.tasks import process_email_job

job = EmailJob.objects.filter(status="queued").first()
process_email_job.delay(job.id)
```

---

## 14. Common Problems

### Campaign Scheduled but No Email Sent

Check:

* Is Celery beat running?
* Is Celery worker running?
* Does the campaign have selected contact lists?
* Do selected lists contain contacts?
* Did `EmailJob` rows get created?
* Is SMTP active and healthy?

### EmailJob Stuck Queued

Make sure Celery worker is running:

```bash
celery -A core worker -l info -Q high_priority,default,low_priority
```

### Celery Beat Not Running Campaign Scheduler

Make sure `core/celery.py` contains:

```txt
campaigns.tasks.process_pending_campaigns
```

Then clear beat schedule files and restart beat.

### Redis Port Already in Use

Redis is already running.

Check:

```bash
redis-cli ping
```

Expected output:

```txt
PONG
```

### Brevo Sender Rejected

Use a verified sender email or authenticate the sender domain in Brevo.

---

## 15. Current Frontend Pages

| Route                    | Purpose                                 |
| ------------------------ | --------------------------------------- |
| `/`                      | Dashboard                               |
| `/campaigns`             | Campaign studio and template management |
| `/instant-send`          | Immediate email sending                 |
| `/smtp`                  | SMTP management                         |
| `/email-history`         | Email job history                       |
| `/contacts`              | Contacts, tags, and lists               |
| `/links`                 | Tracked links                           |
| `/webhooks`              | Webhook management                      |
| `/settings/organization` | Organization settings                   |

---

## 16. Future Improvements

### Backend

* Add `target_contacts` for one-off campaign recipients
* Add campaign error message field
* Add campaign activity logs
* Add campaign detail endpoint
* Add open tracking pixel
* Add unsubscribe tracking
* Add bounce and complaint handling
* Add webhook event emitters
* Improve analytics aggregation
* Improve SMTP credential encryption

### Frontend

* Add campaign detail page
* Add campaign resend/retry action
* Add contact list builder UI
* Add email job detail drawer
* Add webhook payload preview
* Add link analytics charts
* Add onboarding checklist

---

## 17. Production Notes

Before production deployment, configure:

* PostgreSQL
* Redis service
* Celery worker service
* Celery beat service
* Environment variables
* HTTPS
* CORS allowed origins
* Domain authentication for email
* Static/media storage
* Logging and monitoring
* Database backups

Recommended production stack:

```txt
Django + Gunicorn/Uvicorn
Next.js
PostgreSQL
Redis
Celery
Celery Beat
Nginx
systemd / supervisor / Docker Compose
```

---

## 18. Quick Start Summary

### Backend

```bash
source venv/bin/activate
python manage.py runserver
```

### Redis

```bash
redis-server
```

### Celery Worker

```bash
source venv/bin/activate
celery -A core worker -l info -Q high_priority,default,low_priority
```

### Celery Beat

```bash
source venv/bin/activate
celery -A core beat -l info
```

### Frontend

```bash
cd frontend
npm run dev
```
