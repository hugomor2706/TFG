from django.db import models


class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Estudiante'),
        ('teacher', 'Profesor'),
        ('staff', 'Personal'),
    ]

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Card(models.Model):
    uid = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='card'
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.uid


class Door(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Lunes'),
        ('TUE', 'Martes'),
        ('WED', 'Miércoles'),
        ('THU', 'Jueves'),
        ('FRI', 'Viernes'),
        ('SAT', 'Sábado'),
        ('SUN', 'Domingo'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    door = models.ForeignKey(
        Door,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.door}"


class Device(models.Model):
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, unique=True)
    door = models.OneToOneField(
        Door,
        on_delete=models.CASCADE,
        related_name='device'
    )
    active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class AccessLog(models.Model):
    RESULT_CHOICES = [
        ('GRANTED', 'Autorizado'),
        ('DENIED', 'Denegado'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    card = models.ForeignKey(
        Card,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    door = models.ForeignKey(
        Door,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES
    )

    reason = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.timestamp} - {self.result}"