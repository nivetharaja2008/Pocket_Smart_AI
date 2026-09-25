import os
import tempfile
import unittest

from pathlib import Path


TEST_DB = (
    Path(tempfile.gettempdir())
    / "pocketsmart_test.db"
)


os.environ[
    "SECRET_KEY"
] = "test-secret"


from app import config


config.DB_PATH = TEST_DB


from app.db import init_db

from fastapi.testclient import TestClient

from app.main import app


class PocketSmartTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(cls):

        if TEST_DB.exists():

            TEST_DB.unlink()

        init_db()

        cls.client = TestClient(
            app
        )


    @classmethod
    def tearDownClass(cls):

        if TEST_DB.exists():

            TEST_DB.unlink()


    def test_health(self):

        response = (
            self.client.get(
                "/health"
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["status"],
            "ok"
        )


    def test_register_login(self):

        response = (
            self.client.post(
                "/register",
                json={
                    "name":
                        "Test User",

                    "email":
                        "test@example.com",

                    "password":
                        "secret123"
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "access_token",
            response.json()
        )


        response = (
            self.client.post(
                "/login",
                json={
                    "email":
                        "test@example.com",

                    "password":
                        "secret123"
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_party_generation_without_api_key(
        self
    ):

        response = (
            self.client.post(
                "/generate-party",
                json={

                    "budget":
                        25000,

                    "guests":
                        30,

                    "event_type":
                        "Birthday",

                    "venue":
                        "Home",

                    "theme":
                        "Pastel",

                    "location":
                        "Chennai"
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["planner"],
            "party"
        )

        self.assertTrue(
            response.json()[
                "recommendations"
            ]
        )


if __name__ == "__main__":

    unittest.main()