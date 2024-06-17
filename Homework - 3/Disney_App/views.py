from django.db import connection
from django.shortcuts import render
from .models import Movies, Actorsinmovies
from .models import Actorsinmovies

# Create your views here.
def dictfetchall(cursor):
    # Returns all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def index(request):
    return render(request, 'index.html')


def left(request):
    return render(request, 'left.html')


def Home(request):
    return render(request, 'Home.html')


def Query_Results(request):
    with connection.cursor() as cursor:
        cursor.execute("""  select c.genre, number_of_movies, max_gross, max_length, movieTitle
                            from    (   select G.genre, ISNULL(NM.num_movies, 0) as number_of_movies
                                        from    (select DISTINCT genre FROM Movies) G
                                        left join
                                                (select M.genre, Count(M.genre) as num_movies
                                                from (  select Distinct M1.genre, YEAR(M1.releaseDate) as year
                                                        from Movies M1, Movies M2
                                                        where M1.genre = M2.genre and YEAR(M1.releaseDate) = YEAR(M2.releaseDate) and M1.movieTitle <> M2.movieTitle
                                                     ) M
                                                GROUP BY M.genre) NM
                                        ON G.genre = NM.genre
                                        where G.genre is not NULL) c
                            inner join (select M1.genre, MIN(M1.movieTitle) as max_length
                                        from Movies M1, (select genre ,MAX(LEN(movieTitle)) as max_len
                                                                    from Movies
                                                                    group by genre) max
                                        where LEN(M1.movieTitle) = max.max_len and M1.genre = max.genre
                                        group by M1.genre) b
                            on c.genre = b.genre
                            inner join (select M.genre, M.movieTitle, max.max_gross
                                        from Movies M, (select genre ,MAX(gross) as max_gross
                                                        from Movies
                                                        group by genre) max
                                        where M.genre = max.genre and M.gross = max.max_gross) a
                            on a.genre = b.genre
                            ORDER BY c.genre""")
        sql_a = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("""  select DISTINCT movie, COUNT(movie) as num_actors
                            from   (select actor, Count(actor) as num_movies
                                    from (select DISTINCT actor, movie, rating
                                          from Movies M inner join ActorsInMovies AIM on M.movieTitle = AIM.movie
                                          where rating <> 'R') M
                                    where rating = 'G'
                                    group by actor) G
                            inner join (select DISTINCT actor, movie from ActorsInMovies) A
                            on G.actor = A.actor
                            where num_movies >= 4
                            group by movie
                            order by num_actors DESC , movie ASC
                                """)
        sql_c = dictfetchall(cursor)[:5]

        sql_b = [{}]
        if request.method == 'POST' and request.POST:
            limiter = request.POST['num_input']
            with connection.cursor() as cursor:
                cursor.execute(f"""     select DISTINCT RD.actor, M.movieTitle
                                        from       (select actor, MIN(releaseDate) as min_date
                                                    from Movies M inner join ActorsInMovies AIM on M.movieTitle = AIM.movie
                                                    group by actor) RD
                                        inner join (select Distinct actor, count(actor) as num_movies
                                                    from (select DISTINCT actor, movie From ActorsInMovies) DM
                                                    group by actor) num
                                        on RD.actor = num.actor
                                        inner join Movies M on M.releaseDate = RD.min_date
                                        where num.num_movies > {limiter}
                                        """)
                sql_b = dictfetchall(cursor)

    return render(request, 'Query_Results.html', {'sql_a': sql_a,
                                                  'sql_b': sql_b,
                                                  'sql_c': sql_c})


def Add_a_Movie(request):
    if request.method == 'POST' and request.POST:
        Movie_Title = request.POST["Movie_Title"]
        Release_Date = request.POST["Release_Date"]
        Genre = request.POST["Genre"]
        Gross = request.POST["Gross"]
        Rating = request.POST["Rating"]
        new_Movie = Movies(movietitle=Movie_Title, rating=Rating,
                           releasedate=Release_Date, genre=Genre, gross=Gross)

        new_Movie.save()
    return render(request, 'Add_a_Movie.html')
