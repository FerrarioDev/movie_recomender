from django.core.management import BaseCommand
from ...models import Movie


# Check if genres are valid
def check_valid_genres(genres: str) -> bool:
    if bool(genres and not genres.isspace()) and genres != 'na':
        return True
    else:
        return False

# Method to calculate Jaccard Similarity
def jaccard_similarity(list1: list, list2: list) -> float:
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

# Calculate the similarity between two movies
def similarity_between_movies(movie1: Movie, movie2: Movie) -> float:
    if check_valid_genres(movie1.genres) and check_valid_genres(movie2.genres):
        m1_generes = movie1.genres.split()
        m2_generes = movie2.genres.split()
        return jaccard_similarity(m1_generes, m2_generes)
    else:
        return 0


class Command(BaseCommand):
    help = 'Recommend movies'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        THRESHOLD = 0.8

        watched_movies = Movie.objects.filter(watched = True)
        unwatched_movies = Movie.objects.filter(watched = False)
        
        for unwatched in unwatched_movies:
            max_similarity = 0
            will_recommend = False
            for watched in watched_movies:
                similarity = similarity_between_movies(unwatched_movies, watched)
                if similarity >= max_similarity:
                    max_similarity = similarity
                
                if max_similarity >= THRESHOLD:
                    break
        
            if max_similarity > THRESHOLD:
                will_recommend = True
                print(f"Find a movie recommendation: {unwatched.original_title}")
            
            unwatched.recommended = will_recommend
            unwatched.save()