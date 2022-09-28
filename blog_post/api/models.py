from email.policy import default
from djongo import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import jwt
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    # id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=30, unique=True,default="")
    username = models.CharField(max_length=10, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def __str__(self):
        return self.username


class Tags(models.Model):
    tags = models.CharField(max_length=15)

    def __str__(self):
        return self.tags 


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.CharField(max_length=50, null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='tag')
    category = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, related_name='post_tag')
    category = models.CharField(max_length=15)

