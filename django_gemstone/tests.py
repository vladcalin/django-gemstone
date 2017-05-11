import json

from django.test import TestCase


class JsonRpcSpecsTestCase(TestCase):
    @staticmethod
    def get_jsonrpc_request_dict(id, method, params):
        to_return = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        if id:
            to_return["id"] = id
        return to_return

    def test_single_method_call(self):
        post_data = json.dumps(self.get_jsonrpc_request_dict(1, "say_hello", {"name": "world"}))
        resp = self.client.post("/api", post_data, content_type="application/json")

        resp_dict = json.loads(resp.content.decode())
        self.assertEqual(resp_dict["id"], 1)
        self.assertEqual(resp_dict["jsonrpc"], "2.0")
        self.assertIs(resp_dict["error"], None)
        self.assertEqual(resp_dict["result"], "Hello world")
