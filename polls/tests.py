import datetime

from django.test import TestCase
from polls.models import Question
from django.utils import timezone
from django.core.urlresolvers import reverse


# Create your tests here.

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently should return False for questions whose pub_date is in the future
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=3)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently should return True for questions whose pub_date is within the last days
        :return:
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)



def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_create_question_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains( response, 'there is no question')
        self.assertEqual(response.status_code, 200)

    def test_create_question_with_only_future_questions(self):
        create_question(question_text='future_question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
        self.assertContains(response,'there is no question', status_code=200 )

    def test_create_question_with_only_past_question(self):
        create_question(question_text='past_question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past_question>'])

    def test_create_question_with_past_question_and_future_question(self):
        create_question(question_text='past question', days=-30)
        create_question(question_text='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past question>'])


class QuestionDetailViewTests(TestCase):
    def test_detail_view_with_future_question(self):
        future_question = create_question(question_text='Future Question', days=30)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_withe_past_question(self):
        past_question = create_question(question_text='Past Question', days=-30)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)
