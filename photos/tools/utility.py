import mimetypes
import os
import sqlite3
from collections import namedtuple
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse


def namedtuplefetchall(cursor, name):
    desc = cursor.description
    nt_result = namedtuple(name, [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def getTableData(tableName):
    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM {tableName}")
        result = namedtuplefetchall(cursor, f"{tableName}")
    con.close()
    return result


def getValues(tableName, allSelectParams):
    conditionalQuery = "WHERE"
    conditionExist = False
    sort = ""
    conditionSort = False

    if 'camera' in allSelectParams:
        if len(allSelectParams['camera']) == 1:
            conditionalQuery += f" camera_id={allSelectParams['camera'][0]}"
        else:
            conditionalQuery += f" camera_id IN {str(allSelectParams['camera'])}"
        conditionExist = True

    if 'event' in allSelectParams:
        if conditionExist:
            conditionalQuery += " AND"
        if len(allSelectParams['event']) == 1:
            conditionalQuery += f" event_id={allSelectParams['event'][0]}"
        else:
            conditionalQuery += f" event_id IN {str(allSelectParams['event'])}"
        conditionExist = True

    if 'film' in allSelectParams:
        if conditionExist:
            conditionalQuery += " AND"
        if len(allSelectParams['film']) == 1:
            conditionalQuery += f" film_id={allSelectParams['film'][0]}"
        else:
            conditionalQuery += f" film_id IN {str(allSelectParams['film'])}"
        conditionExist = True

    if not conditionExist:
        conditionalQuery = ""

    if 'sort' in allSelectParams:
        sort += "ORDER BY"
        if "date" in allSelectParams["sort"]:
            sort += " timestamp"
            conditionSort = True

        if "film" in allSelectParams["sort"]:
            if conditionSort:
                sort += ","
            sort += " film_id"
            conditionSort = True

        if "camera" in allSelectParams["sort"]:
            if conditionSort:
                sort += ","
            sort += " camera_id"
            conditionSort = True

        if "atoz" in allSelectParams["sort"]:
            if conditionSort:
                sort += ","
            sort += " fileName"

    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM {tableName} {conditionalQuery} {sort}")
        result = namedtuplefetchall(cursor, f"{tableName}")
    con.close()
    return result


def deletePhotoById(deleteId, timestamp):
    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT fileName FROM photos_photos WHERE id={deleteId};")
        result = namedtuplefetchall(cursor, "photos_photos")
        filename = Path("photos/static/photos/pictures/" + timestamp + "/" + result[0].fileName)
        if filename.is_file():
            os.remove(filename)
        cursor.execute(f"DELETE FROM photos_photos WHERE id={deleteId};")


def modifyPhotoById(values):
    saveId = values["save"]
    filename = values["filename"]
    camera = values["camera"]
    if values["event"] == "none":
        event = {'null': None}
    else:
        event = values["event"]
    if values["film"] == "none":
        film = {'null': None}
    else:
        film = values["film"]
    timestamp = values["timestamp"]
    filmEnd = values["filmEnd"]

    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT fileName FROM photos_photos WHERE id={saveId};")
        oldFilename = namedtuplefetchall(cursor, "photos_photos")
        os.rename("photos/static/photos/pictures/" + timestamp + "/" + oldFilename[0].fileName,
                  "photos/static/photos/pictures/" + timestamp + "/" + filename)
        cursor.execute(
            f"update photos_photos SET "
            f"filename='{filename}', "
            f"camera_id='{camera}', "
            f"event_id='{event}', "
            f"film_id='{film}', "
            f"timestamp='{timestamp}', "
            f"filmEnd='{filmEnd}' "
            f"WHERE "
            f"id={saveId};")

def downloadPhotoById(filename, timestamp):
    path = Path("photos/static/photos/pictures/" + timestamp + "/" + filename)

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

def addPhotoById(values):
    filename = values["filename"]
    camera = values["camera"]
    if values["event"] == "none":
        event = ''
    else:
        event = values["event"]
    if values["film"] == "none":
        film = ''
    else:
        film = values["film"]
    timestamp = values["timestamp"]
    filmEnd = values["filmEnd"]

    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO photos_photos(filename, camera_id, event_id, film_id, timestamp, filmEnd) VALUES ('{filename}', '{camera}', '{event}', '{film}', '{timestamp}', '{filmEnd}');")

