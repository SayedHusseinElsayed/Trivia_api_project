import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = 'postgresql://postgres@localhost:5432/trivia'
        setup_db(self.app, self.database_path)


        self.new_question = {
            'question': 'How old are you',
            'answer': '30 years old',
            'difficulty': 5,
            'category': 'Art'
        }

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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_question(self):
        res = self.client().delete('/questions/27')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 27).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_category_does_not_exist(self):
        res = self.client().delete('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_create_new_question(self):
        res = self.client().post('/questions/add', json=self.new_question)
        data = json.loads(res.data)

        pass
    
    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions/add', json=self.new_question)
        data = json.loads(res.data)

        pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()