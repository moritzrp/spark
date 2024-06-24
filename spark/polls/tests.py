import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


def create_question(question_text: str, days: int) -> Question:
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexTests(TestCase):
    def test_no_questions(self) -> None:
        """
        If no question exists, an appropriate
        message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        assert response.context
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self) -> None:
        """
        Questions with a pub_date in the past are displayed
        on the index page.
        """
        question = create_question("Past question", -30)
        response = self.client.get(reverse("polls:index"))
        assert response.context
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self) -> None:
        """
        Questions with a pub_date in the future are not displayed
        on the index page.
        """
        create_question("Past question", 30)
        response = self.client.get(reverse("polls:index"))
        assert response.context
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_question(self) -> None:
        """
        Even if both past and future questions exist, only past
        questions are displayed.
        """
        question = create_question("Past question", -30)
        create_question("Past question", 30)
        response = self.client.get(reverse("polls:index"))
        assert response.context
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self) -> None:
        """
        The questions index may return multiple questions.
        """
        question1 = create_question("Past question", -30)
        question2 = create_question("Past question", -5)
        response = self.client.get(reverse("polls:index"))
        assert response.context
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question2, question1]
        )


class QuestionDetailView(TestCase):
    def test_future_question(self) -> None:
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question("Future question", 5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self) -> None:
        """
        The detail view of a question with a pub_date in the past
        displays the questions text.
        """
        past_question = create_question("Past question", -5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self) -> None:
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self) -> None:
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
