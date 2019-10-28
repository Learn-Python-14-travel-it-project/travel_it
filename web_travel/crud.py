import json

from web_travel.models import db, User
from web_travel.country.models import Country
from web_travel.city.models import City
from web_travel.place.models import Place


def save_user(username, password, email):
    user_exists = User.query.filter(User.email == email).count()
    if not user_exists:
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()


def save_country(country_name):
    if not country_exists(country_name):
        new_country = Country(country_name=country_name)
        db.session.add(new_country)
        db.session.commit()


def country_exists(country):
    if Country.query.filter(Country.country_name == country).count():
        return True
    else:
        return False


def save_city(city_name, related_country):
    if country_exists and not city_exists(city_name, related_country):
        country = Country.query.filter(Country.country_name == related_country).first()
        new_city = City(city_name=city_name, country_id=country.id)
        db.session.add(new_city)
        db.session.commit()


def city_exists(city_name, related_country):
    same_cities_objects = City.query.filter(City.city_name == city_name).all()
    for city_object in same_cities_objects:
        country_object = Country.query.filter(Country.id == city_object.country_id)
        if country_object.count() and country_object.first().country_name == related_country:
            return True
    return False


def save_place(place_name, description, related_country, related_city=None):
    # TODO В случае страны не окажется, будет ошибка
    if not place_exists(place_name, related_country):
        country = Country.query.filter(Country.country_name == related_country).first()
        if related_city:
            city = City.query.filter(City.city_name == related_city).first()
            new_place = Place(place_name=place_name, description=description, country_id=country.id, city_id=city.id)
        else:
            new_place = Place(place_name=place_name, description=description, country_id=country.id)
        db.session.add(new_place)
        db.session.commit()


def place_exists(place_name, related_country):
    if not country_exists(related_country):
        return False
    same_places_objects = Place.query.filter(Place.place_name == place_name).all()
    for place_object in same_places_objects:
        country_object = Country.query.filter(Country.id == place_object.country_id)
        if country_object.count() and country_object.first().country_name == related_country:
            return True
    return False


def get_users():
    users = User.query.all()
    all_users = []
    for user in users:
        new_user = {
            'id': user.id,
            'name': user.username,
            'password': user.password,
            'email': user.email
        }
        all_users.append(new_user)
    return json.dumps(all_users)


def get_countries():
    countries = Country.query.all()
    all_countries = []
    for country in countries:
        new_country = {
            'id': country.id,
            'name': country.country_name
        }
        all_countries.append(new_country)
    return json.dumps(all_countries)


def get_cities():
    cities = City.query.all()
    all_cities = []
    for city in cities:
        new_city = {
            'id': city.id,
            'name': city.city_name,
            'country': city.country_id
        }
        all_cities.append(new_city)
    return json.dumps(all_cities)


def get_places():
    places = Place.query.all()
    all_places = []
    for place in places:
        new_place = {
            'id': place.id,
            'name': place.place_name,
            'description': place.description,
            'country': place.country_id,
            'city': place.city_id
        }
        all_places.append(new_place)
    return json.dumps(all_places)
