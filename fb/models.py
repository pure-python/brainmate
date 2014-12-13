from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.conf import settings


class UserPost(models.Model):
    text = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, related_name='posts')
    likers = models.ManyToManyField(User, related_name='liked_posts')

    def __unicode__(self):
        return '{} @ {}'.format(self.author, self.date_added)

    class Meta:
        ordering = ['-date_added']


class UserPostComment(models.Model):
    text = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User)
    post = models.ForeignKey(UserPost)

    def __unicode__(self):
        return '{} @ {}'.format(self.author, self.date_added)

    class Meta:
        ordering = ['date_added']


class UserProfile(models.Model):
    GENDERS = (
        ('-', 'Unknown'),
        ('F', 'Female'),
        ('M', 'Male'),
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='-')
    avatar = models.ImageField(upload_to='images/', blank=False, null=True)

    user = models.OneToOneField(User, related_name='profile')

    def is_friendship(self,from_user_id,to_user_id):
        
        if(models.Friendship.filter(from_user_id=from_user_id, to_user_id=to_user_id).len()!=0):
            return True
        else:
            return False

    def del_friendship(self,from_user_id,to_user_id):
        models.Friendship.filter(from_user_id=from_user_id, to_user_id=to_user_id).delete()

    def make_friendship(self,from_user_id,to_user_id):
        Friendship(from_user_id,to_user_id)
    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar \
            else static(settings.AVATAR_DEFAULT)

class Friendship(models.Model):
    from_user_id = models.ForeignKey(User, related_name='from_user_id')
    to_user_id = models.ForeignKey(User, related_name='to_user_id')




@receiver(post_save, sender=User)
def callback(sender, instance, *args, **kwargs):
    if not hasattr(instance, 'profile'):
        instance.profile = UserProfile()
        instance.profile.save()
