import json
import math
import tempfile
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
import app
import audit
import config
import detector
import scoring
import stylometry

TEXT = "A working service records each request. A writer can ask for review. The original decision stays available. " * 3

def model_result(score=0.60, truncated=False):
    return {"model_score": score, "perplexity": 35.0, "tokens_total": 600 if truncated else 90,
            "tokens_scored": 400 if truncated else 90, "truncated": truncated,
            "model": "test-double", "model_revision": "test-only", "device": "test"}

class ScoringTests(unittest.TestCase):
    def test_complete_bands_and_boundaries(self):
        for i in range(1001):
            score = i / 1000
            expected = "human" if score <= .25 else "ai" if score >= .8 else "unsure"
            self.assertEqual(scoring.score_to_label(score), (expected, scoring.LABELS[expected]))
        self.assertEqual(scoring.score_to_label(.51)[0], "unsure")
        self.assertEqual(scoring.score_to_label(.95)[0], "ai")

    def test_disagreement_and_weak_evidence(self):
        self.assertAlmostEqual(scoring.combine_signals(.9, .1), .58)
        self.assertAlmostEqual(scoring.combine_signals(.8, .7), .77)
        for m in [0, .1, .5, .9, 1]:
            for s in [0, .1, .5, .9, 1]:
                score = scoring.decision_score(m, s, weak_evidence=True)
                self.assertEqual(scoring.score_to_label(score)[0], "unsure")

    def test_bad_scores_fail_instead_of_clipping(self):
        for score in [float("nan"), float("inf"), -.01, 1.01, "0.5", True, None]:
            with self.subTest(score=score), self.assertRaises(ValueError):
                scoring.combine_signals(score, .5)
            with self.subTest(score=score), self.assertRaises(ValueError):
                scoring.score_to_label(score)

    def test_style_neutral_on_sparse_evidence(self):
        for text in ["", "!!!", "One sentence with enough words.", "猫 猫 猫"]:
            self.assertEqual(stylometry.style_signal(text), .5)
        self.assertEqual(stylometry.words("Café naïve résumé"), ["café", "naïve", "résumé"])
        self.assertEqual(stylometry.sentence_length_spread("One two. Three four."), 0)
        self.assertEqual(stylometry.type_token_ratio("one one two"), 2/3)

    def test_style_varies_and_stays_bounded(self):
        repeated = "The service works well and is easy to use. " * 8
        varied = ("Go! " + " ".join("unusual" + str(i) for i in range(60)) + ". "
                  + "Wait, really? Six fresh ideas; perhaps seven—eventually.")
        self.assertGreater(stylometry.style_signal(repeated), stylometry.style_signal(varied))
        for text in [TEXT, repeated, varied, "hi " * 500]:
            self.assertTrue(0 <= stylometry.style_signal(text) <= 1)

class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = Path(self.tmp.name) / "audit.jsonl"
        self.path_patch = patch.object(config, "AUDIT_LOG", self.log)
        self.path_patch.start()
        app.app.config["TESTING"] = True
        self.client = app.app.test_client()
        self.model = patch("detector.signal_details", return_value=model_result()).start()

    def tearDown(self):
        patch.stopall()
        self.tmp.cleanup()

    def submit(self, text=TEXT):
        result = self.client.post("/submit", json={"text": text, "creator_id": "test_writer"})
        self.assertEqual(result.status_code, 201, result.get_json())
        return result.get_json()

    def test_response_and_durable_decision(self):
        result = self.submit()
        self.assertTrue(uuid.UUID(result["content_id"]))
        for key in ["model_score", "style_score", "confidence", "combined_score"]:
            self.assertTrue(math.isfinite(result[key]) and 0 <= result[key] <= 1)
        entries = audit.read_entries()
        self.assertEqual(len(entries), 1)
        self.assertNotIn("text", entries[0])
        self.assertEqual(entries[0]["combined_score"], result["confidence"])
        self.assertEqual(entries[0]["evidence"], result["evidence"])

    def test_invalid_requests_never_infer(self):
        cases = [
            ({"data": "hello", "content_type": "text/plain"}, 415),
            ({"data": "{", "content_type": "application/json"}, 400),
            ({"data": "null", "content_type": "application/json"}, 400),
            ({"json": []}, 400), ({"json": "text"}, 400), ({"json": 12}, 400),
            ({"json": {}}, 400),
        ]
        for value in [None, True, 7, [], {}, "", " \n ", "\ud800"]:
            cases.append(({"json": {"text": value, "creator_id": "x"}}, 400))
        for value in [None, True, [], "", " ", "bad creator", "bad\ncreator"]:
            cases.append(({"json": {"text": TEXT, "creator_id": value}}, 400))
        cases += [
            ({"json": {"text": "one two", "creator_id": "x"}}, 422),
            ({"json": {"text": "!" * 20, "creator_id": "x"}}, 422),
            ({"json": {"text": "x" * 10001, "creator_id": "x"}}, 413),
            ({"json": {"text": TEXT, "creator_id": "x" * 129}}, 413),
            ({"data": "x" * 65537, "content_type": "application/json"}, 413),
        ]
        for request_args, expected in cases:
            with self.subTest(request_args=str(request_args)[:100]):
                result = self.client.post("/submit", **request_args)
                self.assertEqual(result.status_code, expected, result.get_json())
                self.assertIsInstance(result.get_json()["error"], str)
        self.model.assert_not_called()
        self.assertTrue(all(e["event"] == "rejected" for e in audit.read_entries()))

    def test_short_and_truncated_text_are_unsure(self):
        self.model.return_value = model_result(.99)
        short = self.submit("An ordinary short sentence.")
        self.assertEqual(short["guess"], "unsure")
        self.assertIn("fewer_than_40_words", short["evidence"]["limitations"])
        self.model.return_value = model_result(.99, truncated=True)
        long = self.submit()
        self.assertEqual(long["guess"], "unsure")
        self.assertIn("only_first_400_tokens_scored", long["evidence"]["limitations"])

    def test_appeal_preserves_original_and_exact_reason(self):
        decision = self.submit()
        original = self.log.read_text().splitlines()[0]
        reason = "  My drafts exist.\nPlease check the history.  "
        response = self.client.post("/appeal", json={"content_id": decision["content_id"], "reasoning": reason, "creator_id": "spoof"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "under_review")
        self.assertEqual(self.log.read_text().splitlines()[0], original)
        records = audit.read_entries()
        self.assertEqual(records[1]["reasoning"], reason)
        self.assertEqual(records[1]["creator_id"], "test_writer")
        current = self.client.get("/content/" + decision["content_id"]).get_json()
        self.assertEqual(current["status"], "under_review")
        self.assertEqual(current["original_decision"], records[0])

    def test_unknown_and_invalid_appeals(self):
        identifier = self.submit()["content_id"]
        cases = [
            ({"content_id": str(uuid.uuid4()), "reasoning": "Review please"}, 404),
            ({"content_id": "bad", "reasoning": "Review please"}, 400),
            ({"content_id": None, "reasoning": "Review please"}, 400),
            ({"content_id": identifier, "reasoning": ""}, 400),
            ({"content_id": identifier, "reasoning": []}, 400),
            ({"content_id": identifier, "reasoning": "x" * 2001}, 413),
        ]
        for body, code in cases:
            self.assertEqual(self.client.post("/appeal", json=body).status_code, code)
        self.assertFalse(any(e.get("event") == "appeal" for e in audit.read_entries()))
        self.assertEqual(self.client.get("/content/bad").status_code, 400)

    def test_detector_failure_does_not_create_decision(self):
        self.model.side_effect = detector.DetectorUnavailable("local diagnostic")
        response = self.client.post("/submit", json={"text": TEXT, "creator_id": "x"})
        self.assertEqual(response.status_code, 503)
        self.assertNotIn("local diagnostic", response.get_data(as_text=True))
        self.assertEqual(audit.read_entries(), [])

    def test_nonfinite_model_result_does_not_create_decision(self):
        self.model.return_value = model_result(float("nan"))
        response = self.client.post("/submit", json={"text": TEXT, "creator_id": "x"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(audit.read_entries(), [])

    def test_busy_detector_is_explicit(self):
        app._inference_slot.acquire()
        try:
            response = self.client.post("/submit", json={"text": TEXT, "creator_id": "x"})
            self.assertEqual(response.status_code, 503)
            self.model.assert_not_called()
        finally:
            app._inference_slot.release()

    def test_write_failures_do_not_claim_success(self):
        decision = self.submit()
        with patch("audit._append", side_effect=OSError("disk full")):
            self.assertEqual(self.client.post("/submit", json={"text": TEXT, "creator_id": "x"}).status_code, 503)
            self.assertEqual(self.client.post("/appeal", json={"content_id": decision["content_id"], "reasoning": "Review"}).status_code, 503)
        self.assertEqual(len(audit.read_entries()), 1)

    def test_corrupt_history_is_visible(self):
        self.log.write_text('{"broken":\n')
        self.assertEqual(self.client.get("/log").status_code, 503)
        self.assertEqual(self.client.get("/health").status_code, 503)
        self.assertEqual(self.client.post("/submit", json={"text": TEXT, "creator_id": "x"}).status_code, 503)
        self.model.assert_not_called()

    def test_log_limit_and_concurrent_append(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda i: audit.log_rejection("test", str(i)), range(40)))
        self.assertEqual(len(audit.read_entries()), 40)
        self.assertEqual(self.client.get("/log?limit=0").get_json()["count"], 0)
        self.assertEqual(self.client.get("/log?limit=3").get_json()["count"], 3)
        for value in ["-1", "abc", "1.2", "999999999999999999", "²", "1000001"]:
            self.assertEqual(self.client.get("/log", query_string={"limit": value}).status_code, 400)

    def test_non_utf8_history_is_reported_as_storage_failure(self):
        self.log.write_bytes(b"\xff\xfe")
        self.assertEqual(self.client.get("/log").status_code, 503)
        self.assertEqual(self.client.post("/submit", json={"text": TEXT, "creator_id": "x"}).status_code, 503)
        self.model.assert_not_called()

if __name__ == "__main__":
    unittest.main()
