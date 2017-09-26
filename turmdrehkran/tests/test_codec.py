from unittest import TestCase
from turmdrehkran.higherlevelcontrol.protocol import codec

from turmdrehkran.exceptions import *


class CodecTest(TestCase):

    def setUp(self):
        pass

    def test_request_decode_valid_all(self):
        decoder = codec.DecodeRequest(
            "TESTMETH abc\nParam1: Value1\n\n"
        )

        self.assertEqual("TESTMETH",decoder.method,)
        self.assertEqual("abc", decoder.method_args[0])
        self.assertEqual("Value1", decoder.params["Param1"])

    def test_request_decode_valid_many_args(self):
        decoder = codec.DecodeRequest(
            "TESTMETH arg1 arg2 arg3 arg4 arg5 arg6 arg7 arg8 arg9 arg10 arg11 arg12\n" +
            "Param1: Param1\n" +
            "Param2: Param2\n" +
            "Param3: Param3\n" +
            "Param4: Param4\n" +
            "Param5: Param5\n" +
            "Param6: Param6\n\n"
        )

        self.assertEqual(6, len(decoder.params))
        self.assertEqual(12, len(decoder.method_args))

        self.assertEqual("TESTMETH", decoder.method)

        for num in range(1, 12):
            self.assertEqual("arg" + str(num), decoder.method_args[num-1])

        for param in decoder.params:
            self.assertEqual(param, decoder.params[param])

    def test_request_decode_valid_minimal(self):
            codec.DecodeRequest(
                "TESTMETH\n\n"
            )

    def test_request_decode_invalid_line_endings_missing(self):

        with self.assertRaises(CodecDecodeException):
            codec.DecodeRequest(
                "TESTMETH\n"
            )

    def test_response_decode_valid_all(self):
        decoder = codec.DecodeResponse(
            "200 Blah Blah Blah\nParam: Value\n\n"
        )

        self.assertEqual(200, decoder.status_code)
        self.assertEqual("Blah Blah Blah", decoder.status_message)

    def test_response_decode_no_message(self):
        decoder = codec.DecodeResponse(
            "200\nParam: Value\n\n"
        )

        self.assertEqual(200, decoder.status_code)
        self.assertEqual("", decoder.status_message)

    def test_response_encode_valid_all(self):
        encoder = codec.EncodeResponse()
        encoder.status_code = 200
        encoder.status_message = "OK"
        encoder.params = {
            "a": "123",
            "b": "345"
        }

        self.assertEqual("200 OK\na: 123\nb: 345\n\n", str(encoder))

    def test_request_encode_1(self):
        encoder = codec.EncodeRequest()

        encoder.method = "METHOD"
        encoder.method_args = ["1","2","3","4","5","6"]
        encoder.params = {
            "a": "12",
            "b": "abc"
        }

        self.assertEqual("METHOD 1 2 3 4 5 6\na: 12\nb: abc\n\n", str(encoder))

    def test_request_interop(self):
        encoder = codec.EncodeRequest()

        encoder.method = "METHOD"
        encoder.method_args = ["1","2","3","4","5","6"]
        encoder.params = {
            "a": "12",
            "b": "abc"
        }

        decoder = codec.DecodeRequest(str(encoder))

        self.assertEqual(decoder.params, encoder.params)
        self.assertEqual(decoder.method, encoder.method)
        self.assertEqual(decoder.method_args, encoder.method_args)