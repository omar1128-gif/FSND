import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    @app.route('/categories',methods=['GET'])
    def show_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)

        categories_format = {}
        for category in categories:
            categories_format[category.id] = category.type

        return jsonify({
        'success': True,
        'categories': categories_format,
        'total_catagories': len(categories)
        })


    @app.route('/questions',methods=['GET'])
    def show_all_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        cate_types = [category.type for category in categories]

        return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions),
        'current_category': None,
        'categories': cate_types,
        })



    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            else:
                question.delete()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                'success': True,
                'deleted': question_id,
                'books': current_questions,
                'total_books': len(Question.query.all())
                })
        except:
            abort(422)



    @app.route('/questions', methods=['POST'])
    def add_search_question():

        body = request.get_json()
        if body is None:
            abort(422)
        search_term = body.get('searchTerm', None)
        n_question = body.get('question', None)
        n_answer = body.get('answer', None)
        n_difficulty = body.get('difficulty', None)
        n_category = body.get('category', None)

        try:
            if search_term:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search_term}%')).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': None
                })
            else:
                if n_question and n_answer and n_category and n_difficulty:

                    new_question = Question(
                    question = n_question,
                    answer = n_answer,
                    category = n_category,
                    difficulty = n_difficulty
                    )

                    new_question.insert()

                    selection = Question.query.order_by(Question.id).all()
                    current_questions = paginate_questions(request, selection)

                    return jsonify({
                        'success': True,
                        'created': new_question.id,
                        'questions': current_questions,
                        'total_questions': len(Question.query.all())
                        })
                else:
                    abort(422)
        except:
            abort(422)



    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def show_questions_by_category(category_id):
        try:
            category_id = str(category_id)
            questions = Question.query.filter(Question.category == category_id).all()
            formated_questions = [question.format() for question in questions]

            return jsonify({
            'success': True,
            'questions': formated_questions,
            'total_questions': len(questions),
            'current_category': category_id
            })

        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        body = request.get_json()
        if body is None:
            abort(400)

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category')
        category_id = quiz_category.get('id')

        if category_id == 0:
            if previous_questions:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.all()
        else:
            if previous_questions:
                questions = Question.query.filter(Question.category == category_id).filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.category == category_id).all()

        questions = [question.format() for question in questions]
        if len(questions) == 0:
            abort(404)

        next_question = random.choice(questions)

        if next_question is None:
            next_question = False
            abort(404)

        return jsonify({
        'success': True,
        'question': next_question
        })


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
        }),500



    return app
