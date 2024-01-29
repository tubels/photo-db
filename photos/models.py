from django.db import models

class Camera(models.Model):
    id = models.IntegerField(primary_key=True)
    model = models.CharField(max_length=200)
    isFilm = models.IntegerField()
    dateOfPurchase = models.DateTimeField(blank=True, null=True, default='')
    isWorking = models.IntegerField()

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    place = models.CharField(max_length=200, blank=True, null=True, default='')
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(blank=True, null=True, default='')

class Film(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    iso = models.IntegerField()
    numOfImg = models.IntegerField()
class Photos(models.Model):
    id = models.IntegerField(primary_key=True)
    fileName = models.CharField(max_length=200)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, default='')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, blank=True, null=True, default='')
    timestamp = models.DateField()
    filmEnd = models.DateField(blank=True, null=True, default='')

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/static/photos/pictures')

    def __str__(self):
        return self.title