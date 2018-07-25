from django.db import models
from django.utils.translation import ugettext_lazy
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date=models.DateTimeField(default=timezone.now)
    Topic = models.ForeignKey('Topic',related_name='questions',on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('auth.User', verbose_name=('created by'),
                                   null=True, related_name="+",on_delete=models.CASCADE)
    updated_by = models.ForeignKey('auth.User', verbose_name=('updated by'),
                                   null=True, related_name="+",on_delete=models.CASCADE)
    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question_text = models.ForeignKey('Question',on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('auth.User', verbose_name=('created by'),
                                   null=True, related_name="+", on_delete=models.CASCADE)
    updated_by = models.ForeignKey('auth.User', verbose_name=('updated by'),
                                   null=True, related_name="+", on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

class Comment(models.Model):
    comments_text = models.CharField(max_length=200)
    answer_text = models.ForeignKey('Answer',on_delete=models.CASCADE)
    invites_text= models.CharField(max_length=200)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('auth.User', verbose_name=('created by'),
                                   null=True, related_name="+", on_delete=models.CASCADE)
    updated_by = models.ForeignKey('auth.User', verbose_name=('updated by'),
                                   null=True, related_name="+", on_delete=models.CASCADE)

    def __str__(self):
        return self.comments_text

class Topic(models.Model):
    topics_text=models.CharField(max_length=200)
    description = models.TextField(max_length=10000, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    closed = models.BooleanField(blank=True, default=False)
    question_text=models.CharField(max_length=200)

def num_posts(self):
    return self.post_set.count()


def num_replies(self):
    return max(0, self.post_set.count() - 1)


def last_post(self):
    if self.post_set.count():
        return self.post_set.order_by("created")[0]


def __unicode__(self):
    return __unicode__(self.creator) + " - " + self.title

class Discussion(models.Model):
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.ForeignKey(Answer, on_delete=models.CASCADE)
    topics_text = models.ForeignKey(Topic, on_delete=models.CASCADE)
    discussion_text=models.CharField(max_length=200)

class Vote(models.Model):
    vote_up=+1
    vote_down=-1
    vote_choices=(
        (vote_up, u'up'),
        (vote_down, u'down')
    )
    user = models.ForeignKey('auth.User', related_name='forum_votes',on_delete=models.CASCADE)


    Vote = models.SmallIntegerField(choices=vote_choices)
    voted_at = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    message_text= models.TextField(ugettext_lazy('message'))
    created = models.DateTimeField(default=timezone.now)
    is_visible = models.BooleanField(default=True)
    thread = models.ForeignKey('Thread', related_name='messages',on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user',on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.message_text

class Thread(models.Model):
    title=models.CharField(max_length=250)
    view_count = models.PositiveIntegerField(default=0)
    favourite_count = models.PositiveIntegerField(default=0)
    answer_count = models.PositiveIntegerField(default=0)
    last_activity_at = models.DateTimeField(default=timezone.now)
    last_activity_by = models.ForeignKey('auth.User', related_name='unused_last_active_in_threads',on_delete=models.CASCADE)

class Tag(models.Model):
    name= models.CharField(max_length=255, unique=True)
    created_by= models.ForeignKey('auth.User', related_name='created_tags',on_delete=models.CASCADE)
    created_at= models.DateTimeField(blank=True, default=timezone.now)
    used_count = models.PositiveIntegerField(default=0)
    marked_by = models.ManyToManyField('auth.User', related_name="marked_tags", through="MarkedTag")

class MarkedTag(models.Model):
    TAG_MARK_REASONS =('good','interesting','bad', 'ignored')
    tag = models.ForeignKey('Tag', related_name='user_selections',on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='tag_selections',on_delete=models.CASCADE)

class Search(models.Model):
    POST_SEARCH  = 'P'
    TOPIC_SEARCH = 'T'
    TYPE_CHOICES = (
        (POST_SEARCH, 'Posts'),
        (TOPIC_SEARCH, 'Topics'),
    )

    type= models.CharField(max_length=1, choices=TYPE_CHOICES)
    user= models.ForeignKey('auth.User', related_name='searches',on_delete=models.CASCADE)
    searched_at= models.DateTimeField(default=timezone.now)

    def is_post_search(self):
        return self.type == self.POST_SEARCH

    def is_topic_search(self):
        return self.type == self.TOPIC_SEARCH

class Category(models.Model):
    name = models.CharField(("Name"), max_length=255, unique=True)
    position = models.IntegerField(("Position"), default=0)

    def __str__(self):
        return self.name


class Post(models.Model):
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    bodytext=models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user

class NotificationEmail(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

REPLY_ACTION_CHOICES = (
    ('post_answer', 'Post an answer'),
    ('post_comment', 'Post a comment'),
    ('replace_content', 'Edit post'),
    ('auto_answer_or_comment', 'Answer or comment, depending on the size of post'),
)


class ReplyAddress(models.Model):
    address = models.CharField(max_length=25, unique=True)
    post = models.ForeignKey(Post, null=True, related_name='reply_addresses',on_delete=models.CASCADE)
    reply_action = models.CharField(max_length=32, choices=REPLY_ACTION_CHOICES,
                                    default='auto_answer_or_comment')
    response_post = models.ForeignKey(Post, null=True,
                                      related_name='edit_addresses',on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    allowed_from_email = models.EmailField(max_length=150)
    used_at = models.DateTimeField(default=timezone.now)




