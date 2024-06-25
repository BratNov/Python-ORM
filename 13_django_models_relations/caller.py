import os
from datetime import timedelta, date

import django
from django.db.models import Sum, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import (Author, Book, Song, Artist, Product,
                             Review, Driver, DrivingLicense, Owner,
                             Car, Registration)


# Create queries within functions
def show_all_authors_with_their_books():
    authors = Author.objects.all().order_by('id')
    authors_with_books = []

    for author in authors:
        books = Book.objects.filter(author=author)
        if books:
            book_titles = ', '.join(b.title for b in books)
            authors_with_books.append(f"{author.name} has written - {book_titles}!")

    return '\n'.join(authors_with_books)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    return Artist.objects.filter(name=artist_name).first().songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).get(name=product_name)
    return product.avg_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    expiration_dates = []

    for l in licenses:
        expiration_date = l.issue_date + timedelta(days=365)
        expiration_dates.append(f"License with number: {l.license_number} expires on {expiration_date}!")
    return '\n'.join(expiration_dates)


def get_drivers_with_expired_licenses(due_date: date):
    start_date = due_date - timedelta(days=365)
    return Driver.objects.filter(license__issue_date__gt=start_date)


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()
    car.owner = owner
    car.registration = registration
    car.save()
    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return (f'Successfully registered {car.model} '
            f'to {owner.name} with registration number '
            f'{registration.registration_number}.')
