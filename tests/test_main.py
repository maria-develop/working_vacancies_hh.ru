from unittest.mock import MagicMock, patch

import pytest

from main import user_interaction


@patch("main.JSONSaver")
@patch("builtins.input", side_effect=["2", "1", "5"])
def test_user_interaction_top_vacancies(mock_input, MockJSONSaver):
    mock_json_saver = MockJSONSaver.return_value
    mock_json_saver.load_vacancies.return_value = [
        MagicMock(name="vacancy", salary=2000),
        MagicMock(name="vacancy", salary=1000),
    ]

    with pytest.raises(SystemExit):
        user_interaction()

    assert mock_json_saver.load_vacancies.call_count >= 1


@patch("main.JSONSaver")
@patch("builtins.input", side_effect=["3", "python", "5"])
def test_user_interaction_filter_keyword(mock_input, MockJSONSaver):
    mock_json_saver = MockJSONSaver.return_value
    mock_json_saver.load_vacancies.return_value = [
        MagicMock(
            name="vacancy",
            description="Test description",
            snippet={"requirement": "Python", "responsibility": "Developing applications"},
        ),
        MagicMock(
            name="vacancy",
            description="Another description",
            snippet={"requirement": "Java", "responsibility": "Developing Java applications"},
        ),
    ]

    with pytest.raises(SystemExit):
        user_interaction()

    assert mock_json_saver.load_vacancies.call_count >= 1
