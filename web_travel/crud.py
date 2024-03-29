import random

from web_travel.db import db
from web_travel.country.models import Country
from web_travel.city.models import City
from web_travel.place.models import Place, Photo


def get_random_place():
    places = Place.query.order_by(Place.place_name).limit(1000).all()
    return random.choice(places).place_name


def get_description_by_place(place_name):
    place = Place.query.filter_by(place_name=place_name).first()
    return place.description


def get_photo_by_place(place_name):
    place = Place.query.filter_by(place_name=place_name).first()
    photo = Photo.query.filter_by(place_id=place.id).first()
    return photo.photo_link


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
            new_place = Place(place_name=place_name, description=description,
                              country_id=country.id, city_id=city.id)
        else:
            new_place = Place(place_name=place_name, description=description, country_id=country.id)
        db.session.add(new_place)
        db.session.commit()


def save_photo(photo_link, related_place):
    place = Place.query.filter(Place.place_name == related_place).first()
    new_photo = Photo(photo_link=photo_link, place_id=place.id)
    db.session.add(new_photo)
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
