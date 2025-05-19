import unittest
from unittest.mock import patch
from data.models import Topic, TopicCreate
import services.topics_service as service

def fake_topic(id=1, title="T", content="C", category_id=1, user_id=2, is_locked=0, best_reply_id=None, created_at=None):
    return Topic(id=id, title=title, content=content, category_id=category_id, user_id=user_id,
                 is_locked=is_locked, best_reply_id=best_reply_id, created_at=created_at)

class TopicsService_Should(unittest.TestCase):

    def test_all_returnsTopicList(self):
        with patch('services.topics_service.read_query') as mock_query:
            mock_query.return_value = [
                (1, "T1", "C1", 5, 2, 0, None, None),
                (2, "T2", "C2", 7, 3, 1, 4, None)
            ]
            result = list(service.all())
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].title, "T1")
            self.assertEqual(result[1].category_id, 7)

    def test_all_with_search_and_pagination(self):
        with patch('services.topics_service.read_query') as mock_query:
            mock_query.return_value = [
                (2, "T2", "C2", 7, 3, 1, 4, None)
            ]
            result = list(service.all(search="T2", limit=1, offset=0))
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].title, "T2")

    def test_sort_by_title_and_content(self):
        A = fake_topic(1, "B", "z", 1, 2)
        B = fake_topic(2, "A", "y", 1, 2)
        C = fake_topic(3, "C", "x", 1, 2)
        by_title = service.sort([A, B, C], attribute="title")
        self.assertEqual([B, A, C], by_title)
        by_content = service.sort([A, B, C], attribute="content")
        self.assertEqual([C, B, A], by_content)
        by_id = service.sort([A, B, C], attribute="id", reverse=True)
        self.assertEqual([C, B, A], by_id)

    def test_get_by_id_found_and_none(self):
        with patch('services.topics_service.read_query') as mock_query:
            mock_query.return_value = [(1, "T", "C", 1, 2, 0, None, None)]
            topic = service.get_by_id(1)
            self.assertIsInstance(topic, Topic)
            mock_query.return_value = []
            self.assertIsNone(service.get_by_id(999))

    def test_create_returnsTopic(self):
        with patch('services.topics_service.insert_query') as mock_insert:
            mock_insert.return_value = 7
            topic_data = TopicCreate(title="T", content="C", category_id=1)
            result = service.create(topic_data, user_id=3)
            self.assertIsInstance(result, Topic)
            self.assertEqual(result.id, 7)
            self.assertEqual(result.title, "T")
            self.assertEqual(result.user_id, 3)

    def test_create_returnsNone_whenInsertFails(self):
        with patch('services.topics_service.insert_query') as mock_insert:
            mock_insert.return_value = None
            topic_data = TopicCreate(title="T", content="C", category_id=1)
            result = service.create(topic_data, user_id=3)
            self.assertIsNone(result)

    def test_select_best_reply(self):
        with patch('services.topics_service.update_query') as mock_update:
            mock_update.return_value = 1
            self.assertTrue(service.select_best_reply(2, 9))
            mock_update.return_value = 0
            self.assertFalse(service.select_best_reply(2, 9))

    def test_set_locked(self):
        with patch('services.topics_service.update_query') as mock_update:
            mock_update.return_value = 1
            self.assertTrue(service.set_locked(1, True))
            mock_update.return_value = 0
            self.assertFalse(service.set_locked(1, False))

    def test_toggle_lock_true(self):
        with patch('services.topics_service.read_query') as mock_read, \
             patch('services.topics_service.update_query') as mock_update:
            mock_read.return_value = [(0,)]
            mock_update.return_value = 1
            self.assertTrue(service.toggle_lock(5))

    def test_toggle_lock_false_when_no_topic(self):
        with patch('services.topics_service.read_query') as mock_read:
            mock_read.return_value = []
            self.assertFalse(service.toggle_lock(5))

if __name__ == '__main__':
    unittest.main()
