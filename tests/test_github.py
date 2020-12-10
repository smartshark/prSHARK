"""Tests for the github backend"""

import pprint
import unittest
import json
import mongoengine

from unittest.mock import patch
from argparse import Namespace

from pycoshark.mongomodels import Project, PullRequestSystem, PullRequest, People, PullRequestReview, PullRequestReviewComment, PullRequestComment, PullRequestEvent
from prSHARK.backends.github import Github

# load simple fixtures (taken from the github api examples)
with open('tests/fixtures/user.json') as f:
    person = json.loads(f.read())

with open('tests/fixtures/pr_list.json', 'r') as f:
    pr_list = json.loads(f.read())

with open('tests/fixtures/pr_reviews.json', 'r') as f:
    review_list = json.loads(f.read())

with open('tests/fixtures/pr_review_comments.json', 'r') as f:
    review_comment_list = json.loads(f.read())

with open('tests/fixtures/issue_comments.json', 'r') as f:
    issue_comment_list = json.loads(f.read())

with open('tests/fixtures/issue_events.json', 'r') as f:
    issue_event_list = json.loads(f.read())


def mock_return(*args, **kwargs):
    url = args[0].split('?')[0]
    if 'user' in url:
        return person

    if url.endswith('/pulls'):
        return pr_list
    if '/pulls/' in url and url.endswith('/reviews'):
        return review_list
    if '/pulls/' in url and url.endswith('/comments'):
        return review_comment_list
    if '/issues/' in url and url.endswith('/comments'):
        return issue_comment_list
    if '/issues/' in url and url.endswith('/events'):
        return issue_event_list


class TestGithubBackend(unittest.TestCase):
    """Test Github Backend."""

    def setUp(self):
        """Setup the mongomock connection."""
        mongoengine.connection.disconnect()
        mongoengine.connect('testdb', host='mongomock://localhost')
        p = Project(name='test')
        p.save()

        pr_system = PullRequestSystem(project_id=p.id, url='https://localhost/repos/smartshark/test/pulls')
        pr_system.save()

    def tearDown(self):
        """Tear down the mongomock connection."""
        mongoengine.connection.disconnect()

    @patch('prSHARK.backends.github.Github._send_request', side_effect=mock_return)
    def test_pr_list(self, mock_request):
        """Test Github Parser pull request list response parsing."""

        cfg = Namespace(tracking_url='https://localhost/repos/smartshark/test/pulls')

        project = Project.objects.get(name='test')
        pr_system = PullRequestSystem.objects.get(project_id=project.id)

        with open('tests/fixtures/pr_list.json', 'r') as fi:
            data = json.loads(fi.read())

        pr1 = data[0]
        gp = Github(cfg, project, pr_system)
        gp.parse_pr_list(data)

        pr = PullRequest.objects.get(external_id='1347')
        p = People.objects.get(id=pr.assignee_id)
        prr = PullRequestReview.objects.get(pull_request_id=pr.id)
        prrc = PullRequestReviewComment.objects.get(pull_request_review_id=prr.id, external_id='10')

        prc = PullRequestComment.objects.get(pull_request_id=pr.id)
        pre = PullRequestEvent.objects.get(pull_request_id=pr.id)

        self.assertEqual(pr.title, pr1['title'])
        self.assertEqual(p.name, 'monalisa octocat')
        self.assertEqual(prr.state, 'APPROVED')
        self.assertEqual(prrc.comment, 'Great stuff!')
        self.assertEqual(prc.comment, 'Me too')
        self.assertEqual(pre.event_type, 'closed')
