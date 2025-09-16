import csv
from django.db import connection
from django.http import HttpResponse
from io import StringIO


def export_player_levels_to_csv():
    """
    Выгружает данные в CSV: id игрока, название уровня, пройден ли уровень, полученный приз за уровень
    Оптимизировано для 100k+ записей
    """
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['player_id', 'level_title', 'is_completed', 'prize_title'])

    query = """
            SELECT p.player_id, \
                   l.title  as level_title, \
                   pl.is_completed, \
                   pr.title as prize_title
            FROM PlayerLevel pl \
                     INNER JOIN \
                 Player p ON pl.player_id = p.id \
                     INNER JOIN \
                 Level l ON pl.level_id = l.id \
                     LEFT JOIN \
                 LevelPrize lp ON l.id = lp.level_id \
                     LEFT JOIN \
                 Prize pr ON lp.prize_id = pr.id
            ORDER BY p.player_id, l.order \
            """

    with connection.cursor() as cursor:
        cursor.execute(query)

        batch_size = 5000
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            writer.writerows(rows)

    response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="player_levels_report.csv"'
    response['Content-Length'] = len(output.getvalue())
