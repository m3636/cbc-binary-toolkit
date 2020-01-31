# -*- coding: utf-8 -*-

"""Unit tests for input functions"""

from parameterized import parameterized
from cb_binary_analysis.input import read_csv, read_json
from typing import List, Dict
from json import JSONDecodeError
import unittest

from tests.unit.input_fixtures.file_path_constants import (
    BASIC_INPUT_FILE,
    LARGE_INPUT_FILE,
    BASIC_JSON_INPUT_FILE,
    LARGE_JSON_INPUT_FILE,
    BASIC_INPUT_ANSWER_PATH,
    LARGE_INPUT_ANSWER_PATH,
    BASIC_JSON_ANSWER_PATH,
    LARGE_JSON_ANSWER_PATH,
    BASIC_JSON_WRONG_HASHLEN,
    BASIC_JSON_MALFORMED_FILE,
    BASIC_INPUT_CSV_WRONG_HASHLEN,
    DOES_NOT_EXIST_FILE,
    EMPTY_CSV,
    WRONG_KEY_JSON,
    EMPTY_HASHES_DICT_JSON
)


class TestInputFunctions(unittest.TestCase):
    """
    Unit tests for input.py functions
    """
    @parameterized.expand([
        (BASIC_INPUT_FILE, BASIC_INPUT_ANSWER_PATH)
        #(LARGE_INPUT_FILE, LARGE_INPUT_ANSWER_PATH)
    ])

    def test_csv(self, input_file_path: str, answer_file_path: List[Dict]):
        """
        Unit testing read_csv function
        """

        with open(answer_file_path, 'r') as answer_file:
            self.assertEqual(str(read_csv(input_file_path)), answer_file.read().strip())

    @parameterized.expand([
        (BASIC_JSON_INPUT_FILE, BASIC_JSON_ANSWER_PATH)
        #(LARGE_JSON_INPUT_FILE, LARGE_JSON_ANSWER_PATH)
    ])

    def test_json(self, input_file_path: str, answer_file_path: List[Dict]):
        """
        Unit testing read_json function
        """
        with open(input_file_path, 'r') as input_file:
            with open(answer_file_path, 'r') as answer_file:
                self.assertEqual(str(read_json(input_file.read().strip())), answer_file.read().strip())

    @parameterized.expand([
        (AssertionError, BASIC_INPUT_CSV_WRONG_HASHLEN, f'Hash should be 64 chars, instead is 63 chars: qqtrqoetfdomjjqnyatgmmbomhtnzqchzqzhxggmxqzgoabcnzysikrmunjgrup'),
        (OSError, DOES_NOT_EXIST_FILE, f"[Errno 2] No such file or directory: '{DOES_NOT_EXIST_FILE}'"),
        (AssertionError, EMPTY_CSV, f'There are no hashes in File {EMPTY_CSV}')
    ])

    def test_csv_exceptions(self, error, input_file_path: str, msg: str):
        """
        Unit testing read_csv function exceptions
        """
        with self.assertRaises(error) as context:
            read_csv(input_file_path)
        self.assertEqual(str(context.exception), msg)

    @parameterized.expand([
        (KeyError, WRONG_KEY_JSON, "'There is no sha256 array in JSON object received from command line'"),
        (AssertionError, EMPTY_HASHES_DICT_JSON, "Hashes array contains no hashes"),
        (AssertionError, BASIC_JSON_WRONG_HASHLEN, "Found hash with 63 chars instead of 64 chars for hash: zhfsxqdiovvniajycvnnluubnsgdrqdczzarsxjoozfdbolnovnqacbtelxcnve"),
        (JSONDecodeError, BASIC_JSON_MALFORMED_FILE, "Expecting ':' delimiter: line 1 column 13 (char 12)")
    ])

    def test_json_exceptions(self, error, input_file_path: str, msg: str):
        """
        Unit testing read_json exceptions
        """
        with self.assertRaises(error) as context:
            with open(input_file_path, 'r') as input_file:
                str(read_json(input_file.read()))
        self.assertEqual(str(context.exception), msg)
