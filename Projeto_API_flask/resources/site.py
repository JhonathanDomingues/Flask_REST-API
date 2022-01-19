from flask_restful import Resource
from models.site import SiteModel
from flask_jwt_extended import jwt_required

class Sites(Resource):
	def get(self):
		return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
	def get(self,url):
		site = SiteModel.find_site(url)
		if site:
			return site.json()
		return {'message': 'Site not found.'}, 404
	

	@jwt_required()
	def post(self, url):
		site = SiteModel.find_site(url)
		if site:
			return {"message": "The site '{site}' already exists."},400
		site = SiteModel(url)
		try:
			site.save_site()
			return {'message': 'Site created successfully!'}, 200
		except:
			return {'message': 'An internal error ocurred trying to create a new site.'},500

	@jwt_required()
	def delete(self, url):
		site = SiteModel.find_site(url)
		if site:
			site.delete_site()
			return {'message': 'Site deleted.'}, 200
		return {"message": "Site not found."}, 404