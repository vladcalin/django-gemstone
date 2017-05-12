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

    def check_for_jsonrpc_error(self, resp_dict, expected_response_dict):
        self.assertDictEqual(resp_dict, expected_response_dict)

    def test_single_method_call(self):
        # keyword arguments
        post_data = json.dumps(self.get_jsonrpc_request_dict(1, "say_hello", {"name": "world"}))
        resp = self.client.post("/api", post_data, content_type="application/json")

        resp_dict = json.loads(resp.content.decode())

        self.assertDictEqual(resp_dict,
                             {"jsonrpc": "2.0", "id": 1, "result": "Hello world", "error": None})

        # positional arguments
        post_data = json.dumps(self.get_jsonrpc_request_dict(1, "say_hello", ["world"]))
        resp = self.client.post("/api", post_data, content_type="application/json")

        resp_dict = json.loads(resp.content.decode())
        self.assertDictEqual(resp_dict,
                             {"jsonrpc": "2.0", "id": 1, "result": "Hello world", "error": None})

    def test_single_method_call_method_not_found(self):
        post_data = json.dumps(self.get_jsonrpc_request_dict(1, "not_found", [1, 2, 3]))
        resp = self.client.post("/api", post_data, content_type="application/json")
        resp_dict = json.loads(resp.content.decode())

        self.assertDictEqual(resp_dict,
                             {
                                 "jsonrpc": "2.0",
                                 "id": 1,  # id must be returned
                                 "result": None,
                                 "error": {
                                     "code": -32601, "message": "Method not found"
                                 }
                             })

    def test_single_method_call_parse_error(self):
        data = '{"jsonrpc": "2.0", "id": 1, "method": "hello'
        resp = self.client.post("/api", data=data, content_type="application/json")
        resp_dict = json.loads(resp.content.decode())

        self.assertDictEqual(resp_dict,
                             {
                                 # no id must be returned
                                 "jsonrpc": "2.0",
                                 "result": None,
                                 "error": {
                                     "code": -32700, "message": "Parse error"
                                 }
                             })

    def test_single_method_call_invalid_request(self):
        expected_resp = {
            "jsonrpc": "2.0",
            "result": None,
            "error": {
                "code": -32600, "message": "Invalid request"
            }
        }

        # wrong content type1
        post_data = json.dumps(self.get_jsonrpc_request_dict(1, "say_hello", ["world"]))
        resp = self.client.post("/api", post_data, content_type="application/x-www-form-urlencoded")

        resp_dict = json.loads(resp.content.decode())

        self.assertDictEqual(resp_dict, expected_resp)

        # invalid jsonrpc request body
        # no 'jsonrpc' field
        post_dict = self.get_jsonrpc_request_dict(1, "say_hello", ["world"])
        del post_dict["jsonrpc"]
        post_data = json.dumps(post_data)

        resp = self.client.post("/api", post_data, content_type="application/x-www-form-urlencoded")
        resp_dict = json.loads(resp.content.decode())

        self.assertDictEqual(resp_dict, expected_resp)

        # no 'method' field
        post_dict = self.get_jsonrpc_request_dict(1, "say_hello", ["world"])
        del post_dict["method"]
        post_data = json.dumps(post_data)

        resp = self.client.post("/api", post_data, content_type="application/x-www-form-urlencoded")
        resp_dict = json.loads(resp.content.decode())

        self.assertDictEqual(resp_dict, expected_resp)
