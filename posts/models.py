from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from likes.models import Like
# from dislikes.models import Dislike
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
import PIL
# from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill
# Create your models here.



class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.CharField(max_length = 1000, null = True, blank = True)
    pub_date = models.DateTimeField()
    likes_quanity = models.IntegerField(default = 0)
    repost = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'reposted', null = True, blank = True)
    is_repost = models.BooleanField(default = False)
    comments_quanity = models.IntegerField(default = 0)
    reposts_quanity = models.IntegerField(default = 0)
    likes = GenericRelation(Like, related_query_name='posts')
    class Meta:
        ordering = ['-pub_date']


    def __str__(self):
        return '%s %s' % (self.author, self.pub_date)


    def all_comments(self):
        comments = Comment.objects.filter(post = self)
        return comments


    def who_liked(self):
        likes = self.likes.all()
        who_liked = []
        for l in likes:
            who_liked.append(l.liker)
        return who_liked

    def image_box(self):
        image_box = ImagePost.objects.filter(post = self)
        return image_box

    def short_text(self):
        if self.text:
            splitted_text = self.text.split(' ')
            if len(splitted_text) > 5:
                short = splitted_text[:5]
                short_text = ' '.join(short) + '...'
                return short_text
            else:
                return self.text
        else:
            return None

    def get_absolute_url(self):
        return "/post/%i/" % self.id

    def already_reposted(self, user):
        reposts = Post.objects.filter(repost = self)
        post = reposts.filter(author = user)
        if post.exists():
            return True
        else:
            return False

    def user_can_likes(self, user):
        posttype = ContentType.objects.get_for_model(self)
        likes = Like.objects.filter(content_type__pk = posttype.id, object_id = self.id, liker = user)
        num_qs = likes.count()
        if num_qs>0:
            return False
        else:
            return True

    def user_delete_likes(self, user):
        posttype = ContentType.objects.get_for_model(self)
        likes = Like.objects.filter(content_type__pk = posttype.id, object_id = self.id, liker = user)
        num_qs = likes.count()
        if num_qs==0:
            return False
        else:
            return True


    def user_can_dislikes(self, user):
        posttype = ContentType.objects.get_for_model(self)
        dislikes = Like.objects.filter(content_type__pk = posttype.id, object_id = self.id, disliker = user)
        num_qs = dislikes.count()
        if num_qs>0:
            return False
        else:
            return True

    def user_delete_dislikes(self, user):
        posttype = ContentType.objects.get_for_model(self)
        dislikes = Like.objects.filter(content_type__pk = posttype.id, object_id = self.id, disliker = user)
        num_qs = dislikes.count()
        if num_qs==0:
            return False
        else:
            return True

class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.CharField(max_length = 500, null = True, blank = True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    answer_to = models.ForeignKey('Comment', on_delete = models.CASCADE, null = True, blank = True)
    com_date = models.DateTimeField()

    def __str__(self):
        return self.commentator.username

    def is_to_comment(self):
        if self.answer_to:
            return True
        else:
            return False

    def short_text(self):
        splitted_text = self.text.split(' ')
        if len(splitted_text) > 7:
            short = splitted_text[:7]
            short_text = ' '.join(short) + '...'
            return short_text
        else:
            return self.text

class ImagePost(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="images/")
    image_small = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    image_ultra = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})

    def __str__(self):
        return self.post.author.username
