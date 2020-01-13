from datetime import datetime
from django.db.models import Q, Count, Avg
from db.models import User, Blog, Topic


def create():
    user_one = User.objects.create(first_name='u1', last_name='u1')
    user_two = User.objects.create(first_name='u2', last_name='u2')
    user_three = User.objects.create(first_name='u3', last_name='u3')

    b_one = Blog.objects.create(title='blog1', author=user_one)
    b_two = Blog.objects.create(title='blog2', author=user_one)

    b_one.subscribers.add(user_one, user_two)
    b_two.subscribers.add(user_two)

    topic_one = Topic.objects.create(title='topic1', blog=b_one, author=user_one)
    topic_two = Topic.objects.create(title='topic2_content', blog=b_one, author=user_three, created='2017-01-01')

    topic_one.likes.add(user_one, user_two, user_three)


def edit_all():
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    User.objects.filter(Q(first_name='u1') | Q(first_name='u2')).update(first_name='uu1')


def delete_u1():
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    u = User.objects.get(first_name='u2')
    u.subscriptions.clear()


def get_topic_created_grated():
    return Topic.objects.filter(created__gte='2018-01-01')


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.all().order_by('-id')[:2]


def get_topic_count():
    return Blog.objects.all().annotate(topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.all().annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    return Blog.objects.all().annotate(topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.all().filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.all().filter(blog__isnull=True).order_by('pk')


def get_topic_that_like_all_users():
    return Topic.objects.filter(likes=User.objects.all())


def get_topic_that_dont_have_like():
    return Topic.objects.exclude(likes=User.objects.all())

