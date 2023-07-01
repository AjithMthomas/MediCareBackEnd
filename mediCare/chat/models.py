from django.db import models
from accounts.models import User 


class Room(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.author} - {self.content}'
