import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_profile_path(self, filename):
        """
        Generate the user profile path for a given filename.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The path of the user's profile file.
        """
        username = self.user.username
        ext = filename.split('.')[-1]
    

        return os.path.join('users', username, 'profile', f'{filename}')


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
    )
    designation = models.CharField(max_length=100)

    profile_picture = models.ImageField(
        upload_to = user_profile_path, blank=True, null=True)