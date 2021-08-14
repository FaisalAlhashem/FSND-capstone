import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.db_UserAndPass = os.getenv(
            'DB_USER_AND_PASS', 'postgres:postgres')
        self.db_host = os.getenv('DB_HOST', 'localhost:5432')
        self.db_name = os.getenv('DB_NAME', "capstone_test")
        self.db_path = "postgresql://{}@{}/{}".format(
            self.db_UserAndPass, self.db_host, self.db_name)
        setup_db(self.app, self.db_path)

        self.new_Movie = {
            "title": "The Godfather",
            "release date": "1972",
            "id": 2
        }

        self.new_Actor = {
            "name": "nick cage",
            "age": 54,
            "gender": "male",
            "id": 2
        }

        self.assistant_JWT = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZhU1FSdGktb3ZWdXVIWVR1UktKNCJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbDcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMTY4YzBhODFkOTliMDA3MGVmMzNhOCIsImF1ZCI6IkFnZW5jeSIsImlhdCI6MTYyODk3MDE2MSwiZXhwIjoxNjI5MDQyMTYxLCJhenAiOiJHN09RNGcwOEs5UDh5aUtIdFFDNHJjYUpod1kydU15RSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.HJvYFsnPe3qfcFIKboufNIKRdBYamJc1ENvckiSV-OjdpuMn7OIDqyCC6JJ_yiReXEQY3Zu4-33ehZCTxt0RTRdcw32sGCBgKnmY_FNpDGrB_d6dw46ph-NZbS5iIi83QyPqMXCEcOAJgOoYWBKMmkxWA08DvsB9psvepOJ5bIJfjgAs3PB7gVbeng7MrCpbYtAR8saXug9siJ4eGlY93q5DsMVQZm9Oo5SqBJ6aAOyJ8rU555dysIKiwGLwX5I6ZVofc2rM2gFAtalk2TpEUFxvsjWqbtX2R3iiYDJZ8zzOIlEyaDnwPDUYfig6j7i7ZqUFbbKqZIrRQUbF5-nJow"

        self.director_JWT = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZhU1FSdGktb3ZWdXVIWVR1UktKNCJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbDcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZWM1MjZmNTMwODA5MDA2ODAwNDc4YiIsImF1ZCI6IkFnZW5jeSIsImlhdCI6MTYyODk3MDI1NCwiZXhwIjoxNjI5MDQyMjU0LCJhenAiOiJHN09RNGcwOEs5UDh5aUtIdFFDNHJjYUpod1kydU15RSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.QZoS1NgH2nYKAXwxZQ7oHGC0TrXn4VoiOmGWj9rwU7uCp_i-PKz9TX_OnZQuU4-kRAIBkO7aXAWMpaUvvNNXBTfUEpbv15bNwujSs37OJv6ofHYQqrfuP0G8fDT8zzizJwrYMd1WUCWOlRVxHF0lKXyl1axY1_jG9ODq6Ey0PIAv1yD1k5kUcAyjvwGT40NoQlvXQNVo3L3dkOl2AZVHj61VHqfGydf0mBB8hjNPoAmsQ-VNYhYxzl-ERJR5cnXoqKET8EpjsboM2NJ5IAQ0hwi_LAKzEHV5qszV85hXdKjdYQKcBjCgYxfT1pftdInp7yW6aobu2uEkS_-FheuYAw"

        self.producer_JWT = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZhU1FSdGktb3ZWdXVIWVR1UktKNCJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbDcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZWM1MmFhNTMwODA5MDA2ODAwNDdhNSIsImF1ZCI6IkFnZW5jeSIsImlhdCI6MTYyODk3MDMyNiwiZXhwIjoxNjI5MDQyMzI2LCJhenAiOiJHN09RNGcwOEs5UDh5aUtIdFFDNHJjYUpod1kydU15RSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.hgcYJCypmGAIcsXeUV--aLi_7bjm-1MeQI1-qAXFWvJj1TD6QC5flfbNAWWE2JUnnFzDIsmOMTDQauYOJp9_n3rpanz4i5rPRiu-0nyLZIOqu0CGX-1Qs0_tDeLFU9iNKYa4JPYbIThqoJ6IeBm6wPQg2VEd1ve7iFehb3sVemXgBoDgE5XEBONXDwwUr3p3DV9jbs4vbvZn_Vmax_RsmM9sWo7A20p4BNSgJpO89U3wnxwamJqYOuDJxk91BqmNhW589RPBC0avvjMgL5p6OcPiTVIb_v21e4ZBlP63B5Z7OQqQjyLyhgKT3BJCGSpZXqq3C8G2siNcidyZTWlWiw"

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    endpoint tests: success:True
    """

    'Movies'

    def test_get_Movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": self.assistant_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['movies']))
        self.assertTrue(data['total movies'])

    def test_create_Movie(self):
        res = self.client().post('/movies', headers={
            "Authorization": self.producer_JWT
        }, json=self.new_Movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['movieID'])

    def test_patch_Movie(self):
        res = self.client().patch('/movies/1', headers={
            "Authorization": self.director_JWT
        }, json={
            "release date": "date test"
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['updated'])

    def test_delete_Movie(self):
        movie = Movie.query.filter(
            Movie.title == 'The Godfather').one_or_none()
        Mid = Movie.query.filter(Movie.title == 'The Godfather').first().id
        Mid = movie.id
        res = self.client().delete('/movies/{}'.format(Mid), headers={
            "Authorization": self.producer_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], Mid)

    'Actors'

    def test_get_Actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": self.assistant_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total actors'])

    def test_create_Actor(self):
        res = self.client().post('/actors', headers={
            "Authorization": self.director_JWT
        }, json=self.new_Actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['actor'])
        self.assertTrue(data['actorID'])

    def test_patch_Actor(self):
        res = self.client().patch('/actors/1', headers={
            "Authorization": self.director_JWT
        }, json={
            "name": "name test"
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['updated'])

    def test_delete_Actor(self):
        actor = Actor.query.filter(
            Actor.name == 'nick cage').one_or_none()
        Mid = actor.id
        res = self.client().delete('/actors/{}'.format(Mid), headers={
            "Authorization": self.producer_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], Mid)

    """
    endpoint tests: success:False
    """

    'Movies'

    def test_get_Movies_405(self):
        res = self.client().get('/movies/1', headers={
            "Authorization": self.assistant_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_Movie_422(self):
        res = self.client().post('/movies', headers={
            "Authorization": self.producer_JWT
        }, json={
            'title': "The Godfather"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_patch_Movie_400(self):
        res = self.client().patch('/movies/1', headers={
            "Authorization": self.director_JWT
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

        self.assertEqual(data['message'], "bad request")

    def test_delete_Movie_404(self):
        res = self.client().delete('/movies/999', headers={
            "Authorization": self.producer_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    'Actor'

    def test_get_Actors_405(self):
        res = self.client().get('/actors/1', headers={
            "Authorization": self.assistant_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_Actor_422(self):
        res = self.client().post('/actors', headers={
            "Authorization": self.producer_JWT
        }, json={
            'title': "The Godfather"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_patch_Actor_400(self):
        res = self.client().patch('/actors/1', headers={
            "Authorization": self.director_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_Actor_404(self):
        res = self.client().delete('/actors/999', headers={
            "Authorization": self.director_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    'authorization tests'

    def test_assistant_allowed(self):
        res = self.client().get('/actors', headers={
            "Authorization": self.assistant_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total actors'])

    def test_assistant_not_allowed(self):
        res = self.client().patch('/movies/1', headers={
            "Authorization": self.assistant_JWT
        }, json=self.new_Actor)

        data = json.loads(res.data)
        message = data['message']
        message = message['code']

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(message, "unauthorized")

    def test_director_allowed(self):
        res = self.client().post('/actors', headers={
            "Authorization": self.director_JWT
        }, json=self.new_Actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['actor'])
        self.assertTrue(data['actorID'])
        self.test_delete_Actor()

    def test_director_not_allowed(self):
        res = self.client().post('/movies', headers={
            "Authorization": self.director_JWT
        }, json=self.new_Movie)
        data = json.loads(res.data)
        message = data['message']
        message = message['code']

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(message, "unauthorized")

    def test_producer_create_movie(self):
        res = self.client().post('/movies', headers={
            "Authorization": self.producer_JWT
        }, json=self.new_Movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['movieID'])

    def test_producer_delete_Movie(self):
        movie = Movie.query.filter(
            Movie.title == 'The Godfather').one_or_none()
        Mid = Movie.query.filter(Movie.title == 'The Godfather').first().id
        Mid = movie.id
        res = self.client().delete('/movies/{}'.format(Mid), headers={
            "Authorization": self.producer_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], Mid)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
