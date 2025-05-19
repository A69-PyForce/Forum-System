import unittest
from unittest.mock import patch
from data.models import Vote
import services.votes_service as service

def fake_vote(id=1, reply_id=2, user_id=3, type_vote='up'):
    return Vote(id=id, reply_id=reply_id, user_id=user_id, type_vote=type_vote)

class VotesService_Should(unittest.TestCase):

    def test_vote_creates_new_vote(self):
        with patch('services.votes_service.read_query') as mock_read, \
             patch('services.votes_service.insert_query') as mock_insert:
            mock_read.return_value = []
            mock_insert.return_value = 11
            result = service.vote(reply_id=2, user_id=5, type_vote="down")
            self.assertIsInstance(result, Vote)
            self.assertEqual(result.id, 11)
            self.assertEqual(result.type_vote, "down")

    def test_vote_returns_existing_vote_if_type_is_same(self):
        with patch('services.votes_service.read_query') as mock_read:
            mock_read.return_value = [(7, "up")]
            result = service.vote(reply_id=1, user_id=3, type_vote="up")
            self.assertIsInstance(result, Vote)
            self.assertEqual(result.id, 7)
            self.assertEqual(result.type_vote, "up")

    def test_vote_updates_existing_vote_if_type_is_different(self):
        with patch('services.votes_service.read_query') as mock_read, \
             patch('services.votes_service.update_query') as mock_update:
            mock_read.return_value = [(8, "up")]
            mock_update.return_value = 1  # just so it doesn't crash
            result = service.vote(reply_id=2, user_id=3, type_vote="down")
            self.assertIsInstance(result, Vote)
            self.assertEqual(result.id, 8)
            self.assertEqual(result.type_vote, "down")

    def test_count_votes_for_replies(self):
        with patch('services.votes_service.read_query') as mock_read:
            mock_read.return_value = [
                (17, 5, 2),
                (18, 3, 0)
            ]
            result = service.count_votes_for_replies(topic_id=123)
            self.assertEqual(result, {17: {'up': 5, 'down': 2}, 18: {'up': 3, 'down': 0}})

if __name__ == '__main__':
    unittest.main()
