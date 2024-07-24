from typing import Tuple
from unittest.mock import Mock, patch
from enum import Enum

import pytest

from pebblo.entity_classifier.entity_classifier import EntityClassifier
from tests.entity_classifier.mock_response import (
    mock_input_text1_anonymize_snippet_true,
    mock_input_text2_anonymize_snippet_true,
)
from tests.entity_classifier.test_data import input_text1, input_text2, negative_data


class TestAnonymizerResult:
    def __init__(self, entity_type):
        self.entity_type = entity_type


# Constants
class Entities(Enum):
    PERSON = "person"
    GITHUB_TOKEN = "github-token"
    AWS_ACCESS_KEY = "aws-access-key"
    AWS_SECRET_KEY = "aws-secret-key"
    US_ITIN = "us-itin"
    US_SSN = "us-ssn"
    SLACK_TOKEN = "slack-token"
    IBAN_CODE = "iban-code"
    CREDIT_CARD = "credit-card"
    CREDIT_CARD_NUMBER = "credit-card-number"

@pytest.fixture
def mocked_objects():
    with (
        patch(
            "pebblo.entity_classifier.entity_classifier.AnalyzerEngine"
        ) as mock_analyzer,
        patch(
            "pebblo.entity_classifier.entity_classifier.AnalyzerEngine"
        ) as mock_anomyzer,
        patch(
            "pebblo.entity_classifier.utils.utils.add_custom_regex_analyzer_registry"
        ) as mock_custom_registry,
    ):
        yield mock_analyzer, mock_anomyzer, mock_custom_registry


@pytest.fixture
def mocked_entity_classifier_response(mocker):
    """
    Mocking entity classifier response
    """
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response",
        return_value=Mock(),
    )

    anonymize_response1: Tuple[list, str] = (
        [
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult(Entities.GITHUB_TOKEN.name),
            TestAnonymizerResult(Entities.AWS_ACCESS_KEY.name),
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult(Entities.US_ITIN.name),
            TestAnonymizerResult(Entities.US_SSN.name),
        ],
        input_text1,
    )

    anonymize_response2: Tuple[list, str] = (
        [
            TestAnonymizerResult(Entities.GITHUB_TOKEN.name),
            TestAnonymizerResult(Entities.AWS_ACCESS_KEY.name),
            TestAnonymizerResult(Entities.US_ITIN.name),
            TestAnonymizerResult(Entities.US_SSN.name),
        ],
        mock_input_text1_anonymize_snippet_true,
    )

    anonymize_response3: Tuple[list, str] = (
        [
            TestAnonymizerResult(Entities.SLACK_TOKEN.name),
            TestAnonymizerResult(Entities.SLACK_TOKEN.name),
            TestAnonymizerResult(Entities.GITHUB_TOKEN.name),
            TestAnonymizerResult(Entities.AWS_SECRET_KEY.name),
            TestAnonymizerResult(Entities.AWS_ACCESS_KEY.name),
            TestAnonymizerResult(Entities.US_ITIN.name),
            TestAnonymizerResult(Entities.IBAN_CODE.name),
            TestAnonymizerResult(Entities.CREDIT_CARD.name),
            TestAnonymizerResult(Entities.US_SSN.name),
        ],
        input_text2,
    )

    anonymize_response4: Tuple[list, str] = (
        [
            TestAnonymizerResult(Entities.SLACK_TOKEN.name),
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult(Entities.SLACK_TOKEN.name),
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult(Entities.GITHUB_TOKEN.name),
            TestAnonymizerResult(Entities.AWS_SECRET_KEY.name),
            TestAnonymizerResult(Entities.AWS_ACCESS_KEY.name),
            TestAnonymizerResult(Entities.US_ITIN.name),
            TestAnonymizerResult(Entities.IBAN_CODE.name),
            TestAnonymizerResult(Entities.CREDIT_CARD.name),
            TestAnonymizerResult("NRP"),
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult("NRP"),
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult(Entities.US_SSN.name),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult(Entities.PERSON.name),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult(Entities.PERSON.name),
        ],
        mock_input_text2_anonymize_snippet_true,
    )

    anonymize_negative_response1: Tuple[list, str] = (
        [],
        negative_data,
    )

    anonymize_negative_response2: Tuple[list, str] = (
        [],
        negative_data,
    )

    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.anonymize_response",
        side_effect=[
            anonymize_response1,
            anonymize_response2,
            anonymize_response3,
            anonymize_response4,
            anonymize_negative_response1,
            anonymize_negative_response2,
        ],
    )


@pytest.fixture
def entity_classifier(mocked_objects):
    """
    Create an instance of the EntityClassifier class
    """
    return EntityClassifier()


def test_entity_classifier_init(mocked_objects) -> None:
    """
    Initiated Entity Classifier
    """
    _ = EntityClassifier()


def test_presidio_entity_classifier_and_anonymizer(
    entity_classifier, mocked_entity_classifier_response
):
    """
    UTs for presidio_entity_classifier_and_anonymizer function
    """
    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text1)
    assert entities == {
        Entities.GITHUB_TOKEN.name: 1,
        Entities.AWS_ACCESS_KEY.value: 1,
        Entities.US_ITIN.value: 1,
        Entities.US_SSN.value: 1,
    }
    assert total_count == 4
    assert anonymized_text == input_text1

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        input_text1, anonymize_snippets=True
    )
    assert entities == {
        Entities.GITHUB_TOKEN.value: 1,
        Entities.AWS_ACCESS_KEY.value: 1,
        Entities.US_ITIN.value: 1,
        Entities.US_SSN.value: 1,
    }
    assert total_count == 4
    assert anonymized_text == mock_input_text1_anonymize_snippet_true

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text2)
    assert entities == {
        Entities.SLACK_TOKEN.value: 2,
        Entities.GITHUB_TOKEN.value: 1,
        Entities.AWS_ACCESS_KEY.value: 1,
        Entities.AWS_SECRET_KEY.value: 1,
        Entities.US_ITIN.value: 1,
        Entities.IBAN_CODE.value: 1,
        Entities.CREDIT_CARD_NUMBER.value: 1,
        Entities.US_SSN.value: 1,
    }

    assert total_count == 9
    assert anonymized_text == input_text2

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        input_text1, anonymize_snippets=True
    )
    assert entities == {
        Entities.SLACK_TOKEN.value: 2,
        Entities.GITHUB_TOKEN.value: 1,
        Entities.AWS_ACCESS_KEY.value: 1,
        Entities.AWS_SECRET_KEY.value: 1,
        Entities.US_ITIN.value: 1,
        Entities.IBAN_CODE.value: 1,
        Entities.CREDIT_CARD_NUMBER.value: 1,
        Entities.US_SSN.value: 1,
    }
    assert total_count == 9
    assert anonymized_text == mock_input_text2_anonymize_snippet_true

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(negative_data)
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == negative_data

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        negative_data, anonymize_snippets=True
    )
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == negative_data
