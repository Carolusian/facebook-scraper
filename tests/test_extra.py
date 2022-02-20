import pytest

from facebook_scraper.extra import *


class TestExtra:
    def test_get_likes(self):
        doc_id = 5052894721405548
        target_id = 5137284522973096
        reaction_id = "1635855486666999"
        resp = get_likes(doc_id, target_id, reaction_id)
        assert "feedback" in resp["data"]
        assert "reactors" in resp["data"]["feedback"]

        # incorrect parameters will return errors
        doc_id = 4907607215989892
        target_id = 5201889779845903
        resp = get_likes(doc_id, target_id, str(doc_id))
        assert "errors" in resp

    def test_get_comments(self):
        doc_id = 4907607215989892
        target_id = 5201889779845903
        resp = get_comments(doc_id, target_id)
        assert "node" in resp["data"]
        assert resp["data"]["node"]["__typename"] == "Feedback"

    def test_get_reshares(self):
        doc_id = 3733849556714301
        target_id = 5137284522973096
        resp = get_reshares(doc_id, target_id)
        assert "feedback" in resp["data"]
        assert "reshares" in resp["data"]["feedback"]
