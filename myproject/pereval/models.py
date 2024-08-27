from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        return f"Coordinates: {self.latitude}, {self.longitude}, {self.height}"


class Pereval(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beautyTitle = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, null=True, blank=True)
    connect = models.TextField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)  # Поле заполняется автоматически при создании
    coord = models.ForeignKey(Coords, on_delete=models.CASCADE)
    winter_level = models.CharField(max_length=50, null=True, blank=True)
    summer_level = models.CharField(max_length=50, null=True, blank=True)
    autumn_level = models.CharField(max_length=50, null=True, blank=True)
    spring_level = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Используем choices

    def __str__(self):
        return f"{self.title} ({self.status})"


class PerevalImage(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()  # Используем URLField для хранения ссылок на изображения

    def __str__(self):
        return f"Image for {self.pereval.title}"
