from pdb import post_mortem
from django.test import TestCase
from .models import User, Post, Comment

# Create your tests here.


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('test', 'test')

    def test_user_id(self):
        user = User.objects.get(user_id='test')
        expected_object_name = f"{user.user_id}"
        self.assertEqual(expected_object_name, 'test')


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('test', 'test')
        Post.objects.create(topic='Test topic',
                            user=user, content='Test content')

    def test_post(self):
        post = Post.objects.get(topic='Test topic')
        expected_post_topic = f"{post.topic}"
        expected_post_content = f"{post.content}"
        self.assertEqual(expected_post_topic, 'Test topic')
        self.assertEqual(expected_post_content, 'Test content')


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('test', 'test')
        post = Post.objects.create(topic='Test topic',
                                   user=user, content='Test content')
        Comment.objects.create(comment='Test comment',
                               user=user, post=post)

    def test_comment(self):
        comment = Comment.objects.get(comment='Test comment')
        expected_comment = f"{comment.comment}"
        expected_comment_user = f"{comment.user}"
        expected_comment_post = f"{comment.post}"
        self.assertEqual(expected_comment, 'Test comment')
        self.assertEqual(expected_comment_post, 'Test topic')
        self.assertEqual(expected_comment_user, 'test')
