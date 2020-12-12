import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db

test_database_path = os.getenv("TEST_DATABASE_PATH").replace("\r", "")
castingAssistant_BearerToken = os.getenv("CASTING_ASSISTANT_TOKEN").replace("\r", "")
castingDirector_BearerToken = os.getenv("CASTING_DIRECTOR_TOKEN").replace("\r", "")
executiveProducer_BearerToken = os.getenv("EXECUTIVE_PRODUCER_TOKEN").replace("\r", "")


class CastingAgencyTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = test_database_path
        self.castingAssistant = castingAssistant_BearerToken
        self.castingDirector = castingDirector_BearerToken
        self.executiveProducer = executiveProducer_BearerToken

        setup_db(self.app, self.database_path)

        self.new_movie = {"title": "Mad Max", "release_date": "2016-01-10"}
        self.edit_movie = {"title": "Mad Max 2", "release_date": "2020-01-10"}

        self.new_actor = {
            "name": "Denzel Washington",
            "age": "65",
            "gender": "Male",
        }

        self.edit_actor = {"name": "Denzel Washington", "age": 66, "gender": "Male"}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    """
    Executed after each test
    """

    def tearDown(self):
        pass

    """
    Test GetMovies Role: Casting Assistant
    """

    def test_getMovies_castingAssistant(self):
        res = self.client().get("/movies", headers={"Authorization": "Bearer {}".format(self.castingAssistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    """
    Test GetMovies Role:Public
    """

    def test_getMovies_public(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "No Authorization header")

    """
    Test GetActor Role: Casting Director
    """

    def test_getActors_castingDirector(self):
        res = self.client().get("/actors", headers={"Authorization": "Bearer {}".format(self.castingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    """
    Test GetActor Role:Public
    """

    def test_getActors_public(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "No Authorization header")

    """
    Test CreateMovie Role:Executive Producer
    """

    def test_createMovie_executiveProducer(self):
        res = self.client().post(
            "/movies", json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["id"])

    """
    Test CreateMovie Role:Casting Director
    """

    def test_createMovie_castingDirector(self):
        res = self.client().post(
            "/movies", json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.castingDirector)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Permission not found")

    """
    Test CreateActor Role: Casting Director
    """

    def test_createActor_castinDirector(self):
        res = self.client().post(
            "/actors", json=self.new_actor, headers={"Authorization": "Bearer {}".format(self.castingDirector)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["id"])

    """
    Test CreateActor Role: Casting Assistant
    """

    def test_createActor_castingAssistant(self):
        res = self.client().post(
            "/actors", json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.castingAssistant)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Permission not found")

    """
    Test DeleteMovie Role: Executive Producer
    """

    def test_deleteMovie_executiveProducer1(self):
        res1 = self.client().post(
            "/movies", json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )

        id = json.loads(res1.data)["id"]

        res = self.client().delete(
            "/movies/{}".format(id), headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(int(data["delete"]), id)

    """
    Test DeleteMovie Role:Executive Producer
    """

    def test_deleteMovie_executiveProducer2(self):
        res1 = self.client().post(
            "/movies", json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )

        id = json.loads(res1.data)["id"]

        res = self.client().delete(
            "/movies/{}".format(id + 1), headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    """
    Test DeleteActor Role:Casting Director
    """

    def test_deleteActor_castingDirector(self):
        res1 = self.client().post(
            "/actors", json=self.new_actor, headers={"Authorization": "Bearer {}".format(self.castingDirector)}
        )

        id = json.loads(res1.data)["id"]

        res = self.client().delete(
            "/actors/{}".format(id), headers={"Authorization": "Bearer {}".format(self.castingDirector)}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(int(data["delete"]), id)

    """
    Test DeleteActor Role:Casting Assistant
    """

    def test_deleteActor_castingAssistant(self):
        res1 = self.client().post(
            "/actors", json=self.new_actor, headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )

        id = json.loads(res1.data)["id"]

        res = self.client().delete(
            "/actors/{}".format(id), headers={"Authorization": "Bearer {}".format(self.castingAssistant)}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Permission not found")

    """
    Test EditMovie Role: Executive Producer
    """

    def test_editMovie_executiveProducer(self):
        res1 = self.client().post(
            "/movies", json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )
        id = json.loads(res1.data)["id"]

        res2 = self.client().patch(
            "/movies/{}".format(id),
            json=self.edit_movie,
            headers={"Authorization": "Bearer {}".format(self.executiveProducer)},
        )

        data = json.loads(res2.data)

        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data["movie"])

    """
    Test EditMovie Role: Casting Director
    """

    def test_editMovie_castingDirector(self):
        res1 = self.client().post(
            "/movies", json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.executiveProducer)}
        )

        id = json.loads(res1.data)["id"]

        res2 = self.client().patch(
            "/movies/{}".format(id),
            headers={"Authorization": "Bearer {}".format(self.castingDirector)},
        )

        data = json.loads(res2.data)

        self.assertEqual(res2.status_code, 400)
        self.assertTrue(data["message"], "Bad Request")

    """
    Test EditActor Role: Casting Director
    """

    def test_editActor_castingDirector(self):
        res1 = self.client().post(
            "/actors", json=self.new_actor, headers={"Authorization": "Bearer {}".format(self.castingDirector)}
        )
        id = json.loads(res1.data)["id"]

        res2 = self.client().patch(
            "/actors/{}".format(id),
            json=self.edit_actor,
            headers={"Authorization": "Bearer {}".format(self.castingDirector)},
        )

        data = json.loads(res2.data)

        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data["actor"]["age"], 66)

    """
    Test EditActor 
    """

    def test_editActor_castingAssistant(self):
        res1 = self.client().post(
            "/actors", json=self.new_actor, headers={"Authorization": "Bearer {}".format(self.castingDirector)}
        )
        id = json.loads(res1.data)["id"]

        res2 = self.client().patch(
            "/actors/{}".format(id),
            json=self.edit_actor,
            headers={"Authorization": "Bearer {}".format(self.castingAssistant)},
        )

        data = json.loads(res2.data)

        self.assertEqual(res2.status_code, 403)
        self.assertEqual(data["message"], "Permission not found")


if __name__ == "__main__":
    unittest.main()
