from flask.ext.restless import APIManager
import dbconfig


api_manager = APIManager(dbconfig.app, flask_sqlalchemy_db=dbconfig.db)

api_manager.create_api(
    dbconfig.Member, methods=['GET', 'POST', 'PUT', 'DELETE'],
    exclude_columns=['meals', 'funds'],
    include_methods=['total_funds', 'total_meal']
)

api_manager.create_api(
    dbconfig.Meal, methods=['GET', 'POST', 'PUT', 'DELETE'],
    # exclude_columns=['by']
)

api_manager.create_api(
    dbconfig.Funds, methods=['GET', 'POST', 'PUT', 'DELETE']
)
api_manager.create_api(
    dbconfig.Invoice, methods=['GET', 'POST', 'PUT', 'DELETE']
)

api_manager.create_api(
    dbconfig.Manager, methods=['GET'],
    exclude_columns=['expenses', 'funds', 'meals'],
    include_methods=['total_funds', 'total_expense', 'total_meal', 'meal_rate']
)
api_manager.create_api(
    dbconfig.Manager,
    methods=['GET'],
    collection_name='journal'
)