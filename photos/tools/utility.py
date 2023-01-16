import os
import sqlite3
from collections import namedtuple


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


def deletePhotoById(deleteId):
    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT fileName FROM photos_photos WHERE id={deleteId};")
        result = namedtuplefetchall(cursor, "photos_photos")
        os.remove("photos/static/photos/pictures/" + result[0].fileName)
        cursor.execute(f"DELETE FROM photos_photos WHERE id={deleteId};")


def modifyPhotoById(values):
    saveId = values["save"]
    filename = values["filename"]
    camera = values["camera"]
    event = values["event"]
    film = values["film"]
    timestamp = values["timestamp"]
    filmEnd = values["filmEnd"]

    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT fileName FROM photos_photos WHERE id={saveId};")
        oldFilename = namedtuplefetchall(cursor, "photos_photos")
        os.rename("photos/static/photos/pictures/" + oldFilename[0].fileName,
                  "photos/static/photos/pictures/" + filename)
        cursor.execute(
            f"update photos_photos SET filename='{filename}', camera_id='{camera}', event_id='{event}', film_id='{film}', timestamp='{timestamp}', filmEnd='{filmEnd}' WHERE id={saveId};")


def addPhotoById(values):
    filename = values["filename"]
    camera = values["camera"]
    event = values["event"]
    film = values["film"]
    timestamp = values["timestamp"]
    filmEnd = values["filmEnd"]

    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        cursor.execute(
            f"INSERT INTO photos_photos(filename, camera_id, event_id, film_id, timestamp, filmEnd) VALUES ('{filename}', '{camera}', '{event}', '{film}', '{timestamp}', '{filmEnd}');")


def addFilm(deleteId):
    with sqlite3.connect('./db.sqlite3') as con:
        cursor = con.cursor()
        result = namedtuplefetchall(cursor, "photos_film")
        os.remove("photos/static/photos/pictures/" + result[0].fileName)
        cursor.execute(f"DELETE FROM photos_photos WHERE id={deleteId};")
