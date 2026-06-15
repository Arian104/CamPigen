from django.test import TestCase


class ApiSmokeTests(TestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_auth_login_endpoint_exists(self):
        response = self.client.post(
            "/api/auth/login/",
            data={"username": "missing", "password": "missing"},
            content_type="application/json",
        )
        # Invalid credentials are expected, but endpoint should exist.
        self.assertIn(response.status_code, {400, 401})

    def test_v1_router_is_reachable(self):
        response = self.client.get("/api/v1/")
        self.assertIn(response.status_code, {200, 401, 403})
