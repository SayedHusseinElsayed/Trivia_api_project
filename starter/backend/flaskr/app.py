import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import random
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10
CATEGORIES_PER_PAGE = 10

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
  db.init_app(app)
  migrate = Migrate(app , db)
  with app.app_context():
       db.create_all()

  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''

  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  
  '''

  @app.route('/categories/add', methods=['GET'])
  def retrieve_categories():
    categories = Category.query.all()
    cate = {}
    for category in categories:
        cate[category.id] = category.type
    result = {
      "success": True,
      "categories": cate
          }
    return jsonify(result)



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
# reterive all questions based on pagination
  @app.route('/questions', methods =['GET'])
  def retrieve_questions():
    selection = Question.query.all()
    categories = Category.query.filter(Question.category==Category.type)

    # because of there are no relations between tables we will assgin categ id to be same as categ type 
    cate = {}
    for category in categories:
        cate[category.id] = category.type
    #formatted_cat = [category.format() for category in categories] 
    current_questions =   paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    result = {
      "success": True,
      "questions": current_questions,
      "total_questions": len(Question.query.all()),
      "categories": cate,
      "current_category" : cate[category.id]
     
    }
    return jsonify(result)


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id==question_id).one_or_none()
    

    if question is None:
      abort(404)

    question.delete()

    return jsonify({
      'success': True
    })
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions/add', methods=['POST'])
  def add_question():
  
    try:
      data = {
        'question': request.get_json()['question'],
        'answer': request.get_json()['answer'],
        'category': request.get_json()['category'],
        'difficulty': request.get_json()['difficulty']
      }

      question = Question(**data)
      question.insert()
  
      result = {
        'success': True,
      }
      return jsonify(result)

    except:

     return abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    
    form = request.get_json()
    search_term = form.get('searchTerm', None)
    #searched_question = Question.query.filter(Question.question.ilike('%{}'.format(search_term))).all()
    searched_question = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

    #formatted_cat = [category.format() for category in categories] 
    current_questions =   paginate_questions(request, searched_question)

    if len(current_questions) == 0:
      abort(404)
    result = {
      "success": True,
      "questions": current_questions,
      "total_questions": len(searched_question),
      "current_category": None
    }
    return jsonify(result)

 
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_question_by_category(category_id):
      current_category = Category.query.filter(Category.id == category_id).one_or_none()
      selection = Question.query.filter(Question.category == current_category.type) 
      current_questions = paginate_questions(request, selection) 

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection.all()),
        'current_category': current_category.id
      })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
# reterive all categories

  @app.route('/categories', methods=['GET'])
  def retrieve_categories_play():
    categories = Category.query.all()
    cate = {}
    for category in categories:
        cate[category.id] = category.type
    result = {
      "success": True,
      "categories": cate
          }
    return jsonify(result)


  @app.route('/quizzes', methods=['POST'])
  def quizzes():
      """route to quizzes, play"""      
      try:
        data = request.get_json()
        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']
        
        questions = None        
        if quiz_category['type'] == "click":
          questions = Question.query.all()
          print(f"LOG ALL cat questions {questions}")     
        else:
          questions=Question.query.filter_by(category =(quiz_category['id'])).all()
          print(f"LOG Other cat questions {questions}")        
        formatted_questions = [ q.format() for q in questions]   
        possible_questions = []      
        for q in formatted_questions:
          if q['id'] not in previous_questions:
            possible_questions.append(q)
                
        # get a random question from possible quest
        question_sel = None
        if len(possible_questions) > 0:
          question_sel = random.choice(possible_questions)        
          
          return jsonify({
              'success': True,
              'question':question_sel,
              'previous_questions': previous_questions,
              'quizCategory':quiz_category
          })
      except Exception as ex:
        abort(422)
        print("***PLAY Quiz err: *** ", ex)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  return app

    