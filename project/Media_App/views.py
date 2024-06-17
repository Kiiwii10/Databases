from django.shortcuts import render
from django.db import connection
from django.shortcuts import render
from .models import *

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
        cursor.execute("""  select P.genre, MIN(P.title) as title, P.duration
                            from Programs P
                            inner join
                            longest_duration ld
                            on P.duration = ld.duration and P.genre = ld.genre
                            inner join
                            returned_shows rs on P.title = rs.title
                            group by P.genre, P.duration
                            order by p.genre asc
                                                        """)
        query_1 = dictfetchall(cursor)

    with connection.cursor() as cursor:
        cursor.execute("""  select PR.title, ROUND(AVG(CAST(PR.rank as float)), 2) as avg_rank
                            from ProgramRanks PR, valid_3 V
                            where PR.title = V.title and V.num_ratings >= 3
                            group by PR.title
                            order by avg_rank desc, PR.title asc
                            """)
        query_2 = dictfetchall(cursor)

    with connection.cursor() as cursor:
        cursor.execute("""  select title
                            from shows
                            except
                            select title
                            from low_shows
                            order by title asc
                            """)
        query_3 = dictfetchall(cursor)


    return render(request, 'Query_Results.html', {'query_1': query_1,
                                                  'query_2': query_2,
                                                  'query_3': query_3})

def Rankings(request):
    # print('##################################')
    # print('##################################')

    with connection.cursor() as cursor:
        cursor.execute("""  select DISTINCT hID
                            from Households
                            order by hID asc
                            """)
        hIDs = dictfetchall(cursor)

    with connection.cursor() as cursor:
        cursor.execute("""  select Distinct title
                            from Programs
                            order by title asc
                            """)
        titles = dictfetchall(cursor)


    with connection.cursor() as cursor:
        cursor.execute("""  select genre
                            from   (Select genre, COUNT(genre) as count
                                    FROM Programs
                                    GROUP BY genre) G
                            where genre is not null and count >= 5
                            order by genre asc
                            """)
        genre_scroll = dictfetchall(cursor)

    pop_shows = []
    if request.method == 'POST' and request.POST:
        if 'hID' in request.POST:
            hID = int(request.POST['hID'])
            Title = request.POST['Title']
            Rating = int(request.POST['Rating'])


            program = Programs.objects.get(title=Title)
            household = Households.objects.get(hid=hID)

            try:
                Programranks.objects.filter(hid=hID, title=Title).delete()
            except Exception:
                pass

            rank, created = Programranks.objects.update_or_create(
                hid=household, title=program, rank=Rating
            )
            # print(created)
            # print(rank)
            # print(rank.hid)
            if not created:
                rank.save()


        elif 'min_ranks' in request.POST:
            Genre = request.POST.get('Genre')
            min_ranks = int(request.POST['min_ranks'])
            # print(Genre)
            # print(min_ranks)

            with connection.cursor() as cursor:
                cursor.execute(f""" select PTA.title, average
                                    from (      select P.title, genre, average, counter
                                                from Programs P
                                                left join (select title, ROUND(AVG(CAST(rank as float)), 2) as average, COUNT(title) as counter
                                                            from ProgramRanks
                                                            group by title) TA
                                                on P.title = TA.title) PTA
                                    where PTA.genre = '{Genre}' and counter >= {min_ranks}
                                    order by average desc, PTA.title asc
                                    """)
                pop_shows = dictfetchall(cursor)
            # print(pop_shows)

            if len(pop_shows) < 5:
                with connection.cursor() as cursor:
                    cursor.execute(f""" select title
                                        from Programs
                                        where genre = '{Genre}'
                                        except
                                        
                                        select PTA.title
                                        from (      select P.title, genre, average, counter
                                                    from Programs P
                                                    left join (select title, AVG(rank) as average, COUNT(title) as counter
                                                                from ProgramRanks
                                                                group by title) TA
                                                    on P.title = TA.title) PTA
                                        where PTA.genre = '{Genre}' and counter >= {min_ranks}
                                        
                                        order by title
                                                   """)
                    temp = dictfetchall(cursor)
                for dic in temp:
                    if len(pop_shows) >= 5:
                        break
                    dic['average'] = 0
                    pop_shows.append(dic)

            # print(pop_shows)

    return render(request, 'Rankings.html', {'genre_scroll': genre_scroll,
                                             'hIDs': hIDs,
                                             'titles': titles,
                                             'pop_shows': pop_shows[:5]})

def Records_Management(request):
    with connection.cursor() as cursor:
        cursor.execute("""  select A.hID, COUNT(A.hID) as num_returns
                            from
                            (select title, hID
                             from RecordReturns
                             UNION ALL
                             select title, hID
                             from RecordOrders) A
                            group by A.hID
                            order by num_returns desc, A.hID asc
                            """)
        most_returns = dictfetchall(cursor)[:3]

    order_error = ''
    placed = ''
    return_error = ''
    returned = ''
    if request.method == 'POST' and request.POST:
        # print('###############################################')
        # print('hID_order' in request.POST)
        # print('hID_return' in request.POST)
        if 'hID_order' in request.POST:
            hID = request.POST.get('hID_order')
            title = request.POST.get('title')
            # print('###############################################')
            # print(hID)
            # print(title)
            # print('###############################################')

            if check_hID(hID):
                order_error = 'Error: hID Doesnt Exist'
            elif check_title(title):
                order_error = 'Error: Title Doesnt Exist'
            elif check_3_copies(hID):
                order_error = 'Error: Family owns 3 copies'
            else:
                order = title_available(title)
                if len(order) != 0:
                    if order[0]['hID'] == int(hID):
                        order_error = 'Error: Title already owned by family'
                    else:
                        order_error = 'Error: Title not available, another family owns it'

                elif was_owned(hID, title):
                    order_error = 'Error: Title was owned by family before'
                elif pg_18(hID, title):
                    order_error = 'Error: Title is not suited for children'

            if len(order_error) == 0:
                program = Programs.objects.get(title=title)
                household = Households.objects.get(hid=hID)
                recordorder = Recordorders(title=program, hid=household)
                recordorder.save()
                placed = 'Success: Order is placed'

        elif 'hID_return' in request.POST:
            hID = request.POST.get('hID_return')
            title = request.POST.get('title')
            if check_hID(hID):
                return_error = 'Error: hID Doesnt Exist'
            elif check_title(title):
                return_error = 'Error: Title Doesnt Exist'
            else:
                order = title_available(title)
                if len(order) == 0 or order[0]['hID'] != int(hID):
                    return_error = 'Error: Title is not owned by family'

            if len(return_error) == 0:
                program = Programs.objects.get(title=title)
                household = Households.objects.get(hid=hID)

                Recordorders.objects.filter(hid=household, title=program).delete()

                return_record, created = Recordreturns.objects.update_or_create(
                    hid=household, title=program
                )
                if not created:
                    return_record.save()

                # return_record = Recordreturns(hid=household, title=program)
                # return_record.save()
                returned = 'Success: Record was returned'

    return render(request, 'Records_Management.html', {'order_error': order_error,
                                                       'placed': placed,
                                                       'return_error': return_error,
                                                       'returned': returned,
                                                       'most_returns': most_returns})


def check_hID(hID):
    with connection.cursor() as cursor:
        cursor.execute(f""" select hID
                            from Households
                            where hID = '{hID}'
                                       """)
        temp = dictfetchall(cursor)
        return len(temp) == 0

def check_title(title):
    with connection.cursor() as cursor:
        cursor.execute(f""" select title
                            from Programs
                            where title = '{title}'
                                       """)
        temp = dictfetchall(cursor)
        return len(temp) == 0

def check_3_copies(hID):
    with connection.cursor() as cursor:
        cursor.execute(f""" select hID, COUNT(hID) as num_records
                            from RecordOrders
                            where hID = '{hID}'
                            group by hID
                                       """)
        temp = dictfetchall(cursor)
        if (len(temp) == 0):
            return False
        return temp[0]['num_records'] >= 3

def title_available(title):
    with connection.cursor() as cursor:
        cursor.execute(f""" select title, hID
                            from RecordOrders
                            where title = '{title}'
                                       """)
        temp = dictfetchall(cursor)
        # print(temp)
        return temp

def was_owned(hID, title):
    with connection.cursor() as cursor:
        cursor.execute(f""" select hID
                            from RecordReturns
                            where title = '{title}' and hID = '{hID}'
                                       """)
        temp = dictfetchall(cursor)
        return len(temp) != 0

def pg_18(hID, title):
    with connection.cursor() as cursor:
        cursor.execute(f""" select genre
                            from Programs
                            where title = '{title}'
                                       """)
        genre = dictfetchall(cursor)


    if genre[0]['genre'] != 'Adults only' and genre[0]['genre'] != 'Reality':
        return False

    with connection.cursor() as cursor:
        cursor.execute(f""" select hID
                            from Households
                            where hID = '{hID}' and ChildrenNum > 0
                                       """)
        temp = dictfetchall(cursor)


    return len(temp) != 0

