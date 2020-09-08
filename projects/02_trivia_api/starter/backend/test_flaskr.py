import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://omar@:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        self.new_question = {
        'question': 'Where is Egypt located ?' ,
        'answer': 'Africa',
        'category': '3',
        'difficulty': 2
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

    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))



    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'rating': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_add_question(self):
        res = self.client().post('/questions', json= self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    def test_422_invalid_inputs_for_add_question(self):
        res = self.client().post('questions',)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_delete_question(self):
        insertion_response = self.client().post('/questions', json= self.new_question)
        insertion_data = json.loads(insertion_response.data)
        question_id = insertion_data['created']

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)



    def test_search_questions_with_results(self):
        res = self.client().post('/questions', json= {'searchTerm': 'Egyptians'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)



    def test_search_questions_without_results(self):
        res = self.client().post('/questions', json= {'searchTerm': 'carrot'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'],0)


    def test_get_questions_by_categories(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['current_category'], '6')


    def test_get_catagories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])


    def test_get_quiz_questions_by_specific_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],
                                                   'quiz_category':
                                                   {
                                                   'id': 4,
                                                   'type': 'History'
                                                   }
                                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])



    def test_get_quiz_questions_by_all_categories(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],
                                                   'quiz_category': {
                                                   'id': 0,
                                                   'type': 'All'
                                                   }
                                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    def test_400_missing_quiz_parameters(self):
        res = self.client().post('/quizzes',)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
