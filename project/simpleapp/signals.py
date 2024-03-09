from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from .models import Post,PostCategory
from django.core.exceptions import ValidationError

#@receiver(post_save, sender=Post)
#def post_limit(sender, instance, **kwargs):
    #today = datetime.date.today()
    #post_limit = Post.objects.filter(author=instance.author , time_create__date=today).count()
    #if post_limit >= 3:
        #raise ValidationError("Нельзя публиковать больше 3 постов в сутки!!!")