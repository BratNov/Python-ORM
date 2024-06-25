import os
from typing import List

import django
from django.db.models import Case, When, Value, F, TextField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout


# Create and check models
def show_highest_rated_art():
    hig_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return (f"{hig_art.art_name} is the highest-rated art"
            f" with a {hig_art.rating} rating!")


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create(
        [first_art, second_art]
    )


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop():
    expensive = Laptop.objects.order_by('-price', '-id').first()
    return (f"{expensive.brand} is the most expensive "
            f"laptop available for {expensive.price}$!")


def bulk_create_laptops(args):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    (Laptop.objects
     .filter(brand__in=["Asus", "Lenovo"])
     .update(storage=512))


def update_to_16_GB_memory():
    (Laptop.objects
     .filter(brand__in=["Apple", "Dell", "Acer"])
     .update(memory=16))


def update_operation_systems():
    Laptop.objects.update(
        operation_system=Case(
            When(brand='Asus', then=Value('Windows')),
            When(brand='Apple', then=Value('MacOS')),
            When(brand__in=['Dell', 'Acer'], then=Value('Linux')),
            When(brand='Lenovo', then=Value('Chrome OS')),
            default=F('operation_system')
        )
    )


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(args: List[ChessPlayer]):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title="no title").delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title="GM").update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.all().update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title="IM")


def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=(2200, 2299)).update(title="FM")


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title="regular player")


def set_new_chefs():
    Meal.objects.update(chef=Case(
        When(meal_type="Breakfast", then=Value("Gordon Ramsay")),
        When(meal_type="Lunch", then=Value("Julia Child")),
        When(meal_type="Dinner", then=Value("Jamie Oliver")),
        When(meal_type="Snack", then=Value("Thomas Keller")),
        default=F('chef')
    ))


def set_new_preparation_times():
    Meal.objects.update(preparation_time=Case(
        When(meal_type="Breakfast", then=Value("10 minutes")),
        When(meal_type="Lunch", then=Value("12 minutes")),
        When(meal_type="Dinner", then=Value("15 minutes")),
        When(meal_type="Snack", then=Value("5 minutes")),
        default=F('preparation_time')
    ))


def update_low_calorie_meals():
    (Meal.objects
     .filter(meal_type__in=["Breakfast", "Dinner"])
     .update(calories=400))


def update_high_calorie_meals():
    (Meal.objects
     .filter(meal_type__in=["Lunch", "Snack"])
     .update(calories=700))


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=["Lunch", "Snack"]).delete()


def show_hard_dungeons():
    hard_dungeons = Dungeon.objects.filter(difficulty="Hard").order_by('-location')
    return '\n'.join(
        f"{dungeon.name} is guarded by {dungeon.boss_name} "
        f"who has {dungeon.boss_health} health points!"
        for dungeon in hard_dungeons
    )


def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
            When(difficulty='Easy', then=Value("The Erased Thombs")),
            When(difficulty='Medium', then=Value("The Coral Labyrinth")),
            When(difficulty='Hard', then=Value("The Lost Haunt")),
            default=F('name')
        ))


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty="Easy").update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.filter(difficulty='Easy').update(recommended_level=25)
    Dungeon.objects.filter(difficulty='Medium').update(recommended_level=50)
    Dungeon.objects.filter(difficulty='Hard').update(recommended_level=75)


def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health=500).update(reward="1000 Gold")
    Dungeon.objects.filter(location__startswith="E").update(reward="New dungeon unlocked")
    Dungeon.objects.filter(location__endswith="s").update(reward="Dragonheart Amulet")


def set_new_locations():
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
        )
    )


def show_workouts():
    workouts = Workout.objects.filter(workout_type__in=["Calisthenics", "CrossFit"]).order_by('id')
    return '\n'.join(
        f'{w.name} from {w.workout_type} type has {w.difficulty} difficulty!'
        for w in workouts
    )


def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(workout_type="Cardio", difficulty="High").order_by('instructor')


def set_new_instructors():
    Workout.objects.update(instructor=Case(
        When(workout_type='Cardio', then=Value('John Smith')),
        When(workout_type='Strength', then=Value('Michael Williams')),
        When(workout_type='Yoga', then=Value('Emily Johnson')),
        When(workout_type='CrossFit', then=Value('Sarah Davis')),
        When(workout_type='Calisthenics', then=Value('Chris Heria')),
        default=F('instructor')
    ))


def set_new_duration_times():
    Workout.objects.update(duration=Case(
        When(instructor='John Smith', then=Value('15 minutes')),
        When(instructor='Sarah Davis', then=Value('30 minutes')),
        When(instructor='Chris Heria', then=Value('45 minutes')),
        When(instructor='Michael Williams', then=Value('1 hour')),
        When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
        default=F('duration')
    ))


def delete_workouts():
    Workout.objects.exclude(workout_type__in=["Strength", "Calisthenics"]).delete()
