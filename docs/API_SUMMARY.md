# Email Platform API Summary

Base URL (local): `http://127.0.0.1:8000`

## Authentication and Platform

- `GET /api/health/` - Health check
- `POST /api/auth/login/` - Get JWT access/refresh token pair
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/verify/` - Verify access token
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc UI

## Versioned DRF Router Endpoints

All routes below are under `/api/v1/`:

- `/contacts/`
- `/contact-lists/`
- `/tags/`
- `/campaigns/`
- `/templates/`
- `/email-jobs/`
- `/smtp-configs/`
- `/webhooks/`
- `/webhook-deliveries/`
- `POST /api/v1/send-template-to-contact/`

## Other API Endpoints

- `POST /api/send-email/`
- `POST /api/otp/request/`
- `POST /api/otp/verify/`

## Legacy App Endpoints

### Contacts (`/api/contacts/`)

- `GET /simple-create/`
- `GET /list/`
- `GET /global/`
- `GET /all/`
- `GET /organizations/`

### Campaigns (`/api/campaigns/`)

- `GET /`
- `GET /<pk>/`
- `POST /create/`
- `POST /<pk>/edit/`
- `POST /<pk>/delete/`
- `POST /<pk>/send/`
- `POST /<pk>/duplicate/`
- `GET /templates/`
- `GET /templates/<pk>/`

### Email Engine (`/api/email-engine/`)

- `GET /jobs/`
- `GET /jobs/<pk>/`
- `GET /configs/`

## Command Samples (curl)

### 1) Health check

```bash
curl -X GET "http://127.0.0.1:8000/api/health/"
```

### 2) Login and capture tokens

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"YOUR_USERNAME","password":"YOUR_PASSWORD"}'
```

### 3) Refresh token

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/refresh/" \
  -H "Content-Type: application/json" \
  -d '{"refresh":"YOUR_REFRESH_TOKEN"}'
```

### 4) List contacts (v1)

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/contacts/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5) Create a contact (v1)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/contacts/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 6) Create campaign (v1)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/campaigns/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "April Promo",
    "subject": "Special offer this week"
  }'
```

### 7) Send direct email

```bash
curl -X POST "http://127.0.0.1:8000/api/send-email/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "recipient@example.com",
    "subject": "Hello",
    "body": "Testing from API"
  }'
```

### 8) Send template to a contact

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/send-template-to-contact/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": 1,
    "contact_id": 1
  }'
```

### 9) Request OTP

```bash
curl -X POST "http://127.0.0.1:8000/api/otp/request/" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "user@example.com",
    "channel": "email"
  }'
```

### 10) Verify OTP

```bash
curl -X POST "http://127.0.0.1:8000/api/otp/verify/" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "user@example.com",
    "code": "123456"
  }'
```

## Notes

- Some payload fields differ by serializer/model constraints; use `/api/docs/` for exact schema.
- Most `/api/v1/` endpoints require JWT authentication.
