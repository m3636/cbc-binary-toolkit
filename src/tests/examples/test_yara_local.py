# -*- coding: utf-8 -*-

"""Test code local yara engine."""
import os
import pytest

from cbc_binary_toolkit.config import Config
from cbc_binary_toolkit.engine import LocalEngineManager


def attach_path(path):
    """Attaches local file path to location"""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


@pytest.fixture(scope="session")
def config():
    """Configuration for all the test cases in this module."""
    return Config.load(f"""
    id: cbc_binary_toolkit
    version: 0.0.1
    engine:
      name: Yara
      feed_id: example-feed-id
      local: True
      _provider: cbc_binary_toolkit_examples.engine.yara_local.yara_engine.YaraFactory
      rules_dir: {attach_path("yara_local_fixtures/test_rule.yara")}
    """)


@pytest.fixture(scope="session")
def engine(config):
    """Yara Engine"""
    manager = LocalEngineManager(config)
    return manager.engine


@pytest.mark.parametrize("file, expected_output", [
    ("yara_local_fixtures/matching_binary",
        {
            'iocs': [{
                     'id': 'UUID',
                     'match_type': 'equality',
                     'values': ['SHA256_HASH'],
                     'field': 'process_hash',
                     'severity': 2}],
            'engine_name': 'Yara',
            'binary_hash': 'SHA256_HASH',
            'success': True}),
    ("yara_local_fixtures/nonmatching_binary",
        {
            'iocs': [],
            'engine_name': 'Yara',
            'binary_hash': 'SHA256_HASH',
            'success': True})
])
def test_match(engine, file, expected_output):
    """Tests match and report generation logic"""
    result = engine._match("SHA256_HASH", open(attach_path(file), "r"))

    if len(result.get("iocs", [])) > 0:
        result["iocs"][0]["id"] = "UUID"
    assert result == expected_output
