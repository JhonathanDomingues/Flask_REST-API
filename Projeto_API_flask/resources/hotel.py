from email import message
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
	def get(self):
		return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
	argumentos =  reqparse.RequestParser()
	argumentos.add_argument('nome')
	argumentos.add_argument('estrelas')
	argumentos.add_argument('diaria')
	argumentos.add_argument('cidade')

	def get(self, hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			return hotel.json()
		return {'message': 'Hotel note found.'}, 404
	
	def post(self, hotel_id):
		if HotelModel.find_hotel(hotel_id):
			return {"message":f"Hotel id '{hotel_id}' already exists"}, 400

		dados =  Hotel.argumentos.parse_args()
		hotel = HotelModel(hotel_id,**dados)
		hotel.save_hotel()
		return hotel.json()


	def put(self, hotel_id):

		dados =  Hotel.argumentos.parse_args()
		hotel_econtrado = HotelModel.find_hotel(hotel_id)
		if hotel_econtrado:
			hotel_econtrado.update_hotel(**dados)
			hotel_econtrado.save_hotel()
			return hotel_econtrado.json(), 200
		hotel = HotelModel(hotel_id,**dados)
		hotel.save_hotel()
		return hotel.json(), 201
		

	def delete(self, hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			hotel.delete_hotel()
			return {'message': 'Hotel deleted.'}
		return {'menssage': 'Hotel not found.'}