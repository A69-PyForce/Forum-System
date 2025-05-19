import unittest
from unittest.mock import patch
from data.models import Category, Topic
import services.categories_service as service

def fake_category(id=1, name="General", is_private=0, is_locked=0, image_url=None):
    return Category(id=id, name=name, is_private=is_private, is_locked=is_locked, image_url=image_url)

def fake_topic(id=1, title="T", content="C", category_id=1, user_id=2, is_locked=0, best_reply_id=None, created_at=None):
    return Topic(id=id, title=title, content=content, category_id=category_id, user_id=user_id,
                 is_locked=is_locked, best_reply_id=best_reply_id, created_at=created_at)

class CategoriesService_Should(unittest.TestCase):

    def test_all_returnsCategoryList(self):
        with patch('services.categories_service.read_query') as mock_query:
            mock_query.return_value = [
                (1, "General", 0, 0, "img.png"),
                (2, "Secret", 1, 1, None)
            ]
            result = list(service.all())
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].name, "General")
            self.assertEqual(result[1].is_private, 1)

    def test_topics_by_category_returnsTopics(self):
        with patch('services.categories_service.read_query') as mock_query:
            mock_query.return_value = [
                (1, "T1", "Cont", 5, 2, 0, None, None),
                (2, "T2", "Cont2", 5, 3, 1, 6, None)
            ]
            result = list(service.topics_by_category(5))
            self.assertEqual(len(result), 2)
            self.assertEqual(result[1].title, "T2")

    def test_exists_true_and_false(self):
        with patch('services.categories_service.read_query') as mock_query:
            mock_query.return_value = [(1, "General", 0, 0)]
            self.assertTrue(service.exists(1))
            mock_query.return_value = []
            self.assertFalse(service.exists(2))

    def test_get_by_id_found_and_none(self):
        with patch('services.categories_service.read_query') as mock_query:
            mock_query.return_value = [(1, "General", 0, 0, None)]
            cat = service.get_by_id(1)
            self.assertIsInstance(cat, Category)
            mock_query.return_value = []
            self.assertIsNone(service.get_by_id(123))

    def test_create_returnsCategory(self):
        with patch('services.categories_service.insert_query') as mock_insert:
            mock_insert.return_value = 42
            cat = Category(id=None, name="Test", is_private=0, is_locked=0)
            result = service.create(cat)
            self.assertIsInstance(result, Category)
            self.assertEqual(result.id, 42)
            self.assertEqual(result.name, "Test")

    def test_set_privacy(self):
        with patch('services.categories_service.update_query') as mock_update:
            mock_update.return_value = 1
            self.assertTrue(service.set_privacy(1, True))
            mock_update.return_value = 0
            self.assertFalse(service.set_privacy(1, False))

    def test_set_locked(self):
        with patch('services.categories_service.update_query') as mock_update:
            mock_update.return_value = 1
            self.assertTrue(service.set_locked(1, True))
            mock_update.return_value = 0
            self.assertFalse(service.set_locked(1, False))

    def test_update_category_image_url(self):
        with patch('services.categories_service.update_query') as mock_update:
            mock_update.return_value = True
            self.assertTrue(service.update_category_image_url(1, "url"))
            mock_update.return_value = False
            self.assertFalse(service.update_category_image_url(2, "url2"))

if __name__ == '__main__':
    unittest.main()
