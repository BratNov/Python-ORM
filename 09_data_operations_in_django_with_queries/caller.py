import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
from populate_db import populate_model_with_data
from django.db.models import F


# Create queries within functions
def create_pet(name: str, species: str):
    pet = Pet.objects.create(name=name, species=species)
    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    return '\n'.join(str(loc) for loc in Location.objects.all().order_by('-id'))


def new_capital():
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    first_location = Location.objects.first()
    if first_location:
        first_location.delete()


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        car_price = float(car.price)
        discount_percentage = sum([int(ch) for ch in str(car.year)]) / 100
        discount = car_price * discount_percentage
        car.price_with_discount = car_price - discount
        car.save()


def get_recent_cars():
    recent_cars = Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')
    return recent_cars


def delete_last_car():
    last_car = Car.objects.all().order_by('-id').first()
    if last_car:
        last_car.delete()


def show_unfinished_tasks():
    return '\n'.join(str(t) for t in Task.objects.filter(is_finished=False))


def complete_odd_tasks():
    (Task.objects.filter(is_finished=False)
     .extra(where=["MOD(id, 2) != 0"])
     .update(is_finished=True))


def encode_and_replace(text: str, task_title: str):
    description = ''.join([chr(ord(ch) - 3) for ch in text])
    (Task.objects.filter(title=task_title)
     .update(description=description))


def get_deluxe_rooms():
    rooms = (HotelRoom.objects.filter(room_type="Deluxe")
             .extra(where=["MOD(id, 2) = 0"]))
    return '\n'.join(str(r) for r in rooms)


def increase_room_capacity():
    rooms = HotelRoom.objects.order_by('id')
    previous_capacity = 0
    for index, room in enumerate(rooms):
        if room.is_reserved:
            if index == 0:
                room.capacity += room.id
            else:
                room.capacity += previous_capacity
            room.save()
        previous_capacity = room.capacity


def reserve_first_room():
    first_room = HotelRoom.objects.filter(is_reserved=False).order_by('id').first()
    if first_room:
        first_room.is_reserved = True
        first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.order_by('-id').first()
    if last_room and not last_room.is_reserved:
        last_room.delete()


def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )
    warriors = Character.objects.filter(class_name='Warrior')
    for warrior in warriors:
        warrior.hit_points = warrior.hit_points // 2
        warrior.dexterity += 4
        warrior.save()
    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character):
    new_name = f"{first_character.name} {second_character.name}"
    new_class_name = "Fusion"
    new_level = (first_character.level + second_character.level) // 2
    new_strength = int((first_character.strength + second_character.strength) * 1.2)
    new_dexterity = int((first_character.dexterity + second_character.dexterity) * 1.4)
    new_intelligence = int((first_character.intelligence + second_character.intelligence) * 1.5)
    new_hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ['Mage', 'Scout']:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        new_inventory = "Dragon Scale Armor, Excalibur"

    new_character = Character.objects.create(
        name=new_name,
        class_name=new_class_name,
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory
    )

    first_character.delete()
    second_character.delete()

    return new_character


def grand_dexterity():
    Character.objects.all().update(dexterity=30)


def grand_intelligence():
    Character.objects.all().update(intelligence=40)


def grand_strength():
    Character.objects.all().update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()
