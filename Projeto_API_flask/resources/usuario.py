from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):

	def get(self, user_id):
		user = UserModel.find_hotel(user_id)
		if user:
			return user.json()
		return {'message': 'User note found.'}, 404
	
	def delete(self, user_id):
		user = UserModel.find_hotel(user_id)
		if user:
			try:
				user.delete_hotel()
			except:
				return {'message': 'An internal error ocurred trying to save user.'}, 500
			return {'message': 'User deleted.'}
		return {'menssage': 'User not found.'}

class UserRegister(Resource):

	def post(self):
		atributos = reqparse.RequestParser()
		atributos.add_argument('login', type=str, required=True, help="The field 'nome' cannot be left blank")
		atributos.add_argument('senha', type=str, required=True, help="The field 'nome' cannot be left blank")
		dados = atributos.parse_args()

		if UserModel.find_by_login(dados['login']):
			return {'message': f"The login {dados['login']} already exists"}
		
		user = UserModel(**dados)
		user.save_user()
		return {'message': 'User cread successfully!'}, 201

	