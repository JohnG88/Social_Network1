from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
#from django.template.defaultfilters import slugify
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="No bio...", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    # Install pillow
    # Create media_root
    # find avatar.png
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created}"
    
    # Creating first profile with name and last name in slug, the following profiles, if they have the same name will have a number by them, prob how red eyed coder did with implementing the time to slug(maybe it was pyplane?)
    def save(self, *args, **kwargs):
        # Set ex to false
        ex = False
        # If first name and last name
        if self.first_name and self.last_name:
            # slugify first name and last name
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            # filter profile slugs and see if it exists, assign it to ex variable
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                # I'm guessing if ex is not false, meaning if it is carrying some data, then slugify the get_random_code from utils.py and use that as slug.(If has same first name and last name, first person to put John G, will have John G. Second person will have John Gdd37a50a )
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                # Check to see if it exists
                ex = Profile.objects.filter(slug=to_slug).exists()

        else:
            # Set user to slug
            to_slug = str(self.user)
        # Assign slug to to_slug
        self.slug = to_slug
        super().save(*args, **kwargs)


class Relationship(models.Model):
    