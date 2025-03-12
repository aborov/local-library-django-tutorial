import os
import django
from faker import Faker
import random
from django.db.models.functions import Lower

# Configure settings for project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')

# Load the Django project's settings
django.setup()

# Import models
from catalog.models import Genre, Book, BookInstance, Author, Language

# Initialize Faker instance
fake = Faker()
Faker.seed(1)  # Generate consistent sample data

# Reset database
Language.objects.all().delete()
BookInstance.objects.all().delete()
Genre.objects.all().delete()
Book.objects.all().delete()
Author.objects.all().delete()


def create_language():
    """Create sample languages."""
    languages = ["English", "French", "Spanish", "German", "Japanese", "Chinese", "Russian", "Italian"]
    for lang in languages:
        Language.objects.create(name=lang)


def create_genre(num_genres):
    genres = ["Science Fiction", "Fantasy", "Mystery", "Romance", "Horror", "Historical Fiction", "Thriller", "Biography"]
    
    for _ in range(num_genres):
        genre_name = random.choice(genres)
        if not Genre.objects.annotate(lower_name=Lower('name')).filter(lower_name=genre_name.lower()).exists():
            Genre.objects.create(name=genre_name)
        else:
            print(f"Genre '{genre_name}' already exists. Skipping.")

def create_author(n):
    """Create n sample authors."""
    for _ in range(n):
        Author.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=20, maximum_age=90),
            date_of_death=fake.date_of_birth(minimum_age=40, maximum_age=100) if random.random() < 0.3 else None
        )


def create_book(n):
    """Create n sample books, each with a random author, genre, and language."""
    genres = list(Genre.objects.all())
    authors = list(Author.objects.all())
    languages = list(Language.objects.all())

    if not genres or not authors or not languages:
        print("Error: Ensure genres, authors, and languages exist before creating books.")
        return

    for _ in range(n):
        book = Book.objects.create(
            title=fake.sentence(nb_words=3),
            summary=fake.text(),
            isbn=fake.isbn13(),
            author=random.choice(authors),
            language=random.choice(languages)
        )
        book.genre.set(random.sample(genres, k=random.randint(1, 3)))  # Assign random genres


def create_book_instance(n):
    """Create n sample book instances, each assigned to a book."""
    books = list(Book.objects.all())

    if not books:
        print("Error: Ensure books exist before creating book instances.")
        return

    status_choices = ["m", "o", "a", "r"]  # Maintenance, On Loan, Available, Reserved

    for _ in range(n):
        BookInstance.objects.create(
            book=random.choice(books),
            imprint=fake.company(),
            due_back=fake.future_date(end_date="+30d") if random.random() < 0.7 else None,  # 70% chance of having a due date
            status=random.choice(status_choices)
        )


# Create sample data
create_language()
create_genre(5)
create_author(10)
create_book(30)
create_book_instance(60)

print("\nSample data generated\n")