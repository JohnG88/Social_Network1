from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.db.models import Q

# Create your models here.

class ProfileManager(models.Manager):
    
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        
        # When using set use .add instead of append
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

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

    objects = ProfileManager()

    # Get all the friends from the many to many fields
    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_post_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()
    
    # like_set is from Like model
    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked
    
    # liked is post model field
    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    
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


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)

class RelationshipManager(models.Manager):
    # receiver is ourself
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs

    # Writing something like, Relationship.objects.invitations_received(myprofile), will get all invitations from myprofile

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    #To connect it, make it all work, have to add line below
    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"