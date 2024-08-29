from django.test import SimpleTestCase

from products.forms import ReviewForm


class TestReviewForm(SimpleTestCase):
    def test_review_valid_form(self):
        form1 = ReviewForm(
            data={
                "review": "Good product",
                "rating": 4.5,
            }
        )

        form2 = ReviewForm(
            data={
                "rating": 2.5,
            }
        )

        self.assertTrue(form1.is_valid())
        self.assertTrue(form2.is_valid())

    def test_review_invalid_form(self):
        form = ReviewForm(data={"review": "Poor Quality"})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
