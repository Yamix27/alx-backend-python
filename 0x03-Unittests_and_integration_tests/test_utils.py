#!/usr/bin/env python3
"""
Unit tests for utility functions.
"""

from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Any, Tuple, Dict
import unittest
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
    test case for the `access_nested_map` function.
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: Tuple[str], expected: Any
    ) -> None:
        """
        test `access_nested_map` with valid inputs.
        Args:
            nested_map (Dict[str, Any]): The nested dictionary to access.
            path (Tuple[str]): The path of keys to follow.
            expected (Any): The expected value at the end of the path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: Tuple[str]
    ) -> None:
        """
        test `access_nested_map` raises KeyError for invalid paths.
        Args:
            nested_map (Dict[str, Any]): The nested dictionary to access.
            path (Tuple[str]): The path of keys to follow.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    test case for the `get_json` function.
    """

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(
        self, test_url: str, test_payload: Dict[str, Any], mock_get: Mock
    ) -> None:
        """
        test `get_json` function with mocked `requests.get`.
        Args:
            test_url (str): The URL to fetch JSON from.
            test_payload (Dict[str, Any]): The expected JSON payload.
            mock_get (Mock): The mocked `requests.get` method.
        """
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    test case for the `memoize` decorator.
    """

    def test_memoize(self) -> None:
        """
        test `memoize` decorator to ensure it caches method results.
        """

        class TestClass:
            """
            test class with a method and a memoized property.
            """

            def a_method(self) -> int:
                """
                method that returns 42.
                Returns:
                    int: The number 42.
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """
                memoized property that calls `a_method`.
                Returns:
                    int: The result of `a_method`.
                """
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            test_class = TestClass()
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mocked.assert_called_once()
