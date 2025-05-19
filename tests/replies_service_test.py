import unittest
from unittest.mock import patch
from data.models import Reply, ReplyCreate
import services.replies_service as service

def fake_reply(id=1, text="Reply", topic_id=1, user_id=2, created_at=None, username="U", avatar_url=None):

    return Reply(
        id=id,
        text=text,
        topic_id=topic_id,
        user_id=user_id,
        created_at=created_at,
        username=username,
        avatar_url=avatar_url
    )

class RepliesService_Should(unittest.TestCase):

    def test_get_by_topic_returnsReplyList(self):
        with patch('services.replies_service.read_query') as mock_query:
            mock_query.return_value = [
                (1, "A", 2, 3, "2024-01-01", "U1", None),
                (2, "B", 2, 4, "2024-01-02", "U2", "pic.png"),
            ]
            result = service.get_by_topic(2)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[1].text, "B")
            self.assertEqual(result[0].username, "U1")

    def test_create_returnsTrueOnInsert(self):
        with patch('services.replies_service.insert_query') as mock_insert:
            mock_insert.return_value = 11
            data = ReplyCreate(text="hi")
            result = service.create(data, user_id=5, topic_id=3)
            self.assertTrue(result)

    def test_create_returnsFalseOnFail(self):
        with patch('services.replies_service.insert_query') as mock_insert:
            mock_insert.return_value = None
            data = ReplyCreate(text="hi")
            result = service.create(data, user_id=5, topic_id=3)
            self.assertFalse(result)

    def test_exists_true_and_false(self):
        with patch('services.replies_service.read_query') as mock_query:
            mock_query.return_value = [(1,)]
            self.assertTrue(service.exists(5))
            mock_query.return_value = []
            self.assertFalse(service.exists(6))

    def test_get_by_id_found_and_none(self):
        with patch('services.replies_service.read_query') as mock_query:
            mock_query.return_value = [(1, "A", 2, 3, "2024-01-01")]
            reply = service.get_by_id(1)
            self.assertIsInstance(reply, Reply)
            mock_query.return_value = []
            self.assertIsNone(service.get_by_id(22))

if __name__ == '__main__':
    unittest.main()
