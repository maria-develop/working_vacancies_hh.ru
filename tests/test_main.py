from unittest.mock import MagicMock, patch

import pytest

from main import user_interaction


@patch("main.HeadHunterAPI")
@patch("main.JSONSaver")
@patch("builtins.input", side_effect=["1", "Python", "5"])
def test_user_interaction_search(mock_input, MockJSONSaver, MockHeadHunterAPI):
    mock_hh_api = MockHeadHunterAPI.return_value
    mock_hh_api.get_vacancies.return_value = [
        {
            "id": "1",
            "name": "Python Developer",
            "area": {"name": "Москва"},
            "url": "http://example.com",
            "salary": {"from": 1000},
            "description": "Test description",
            "snippet": {"requirement": "Python", "responsibility": "Developing applications"},
        }
    ]

    mock_json_saver = MockJSONSaver.return_value
    mock_json_saver.load_vacancies.return_value = []

    with pytest.raises(SystemExit):
        user_interaction()

    mock_hh_api.get_vacancies.assert_called_once_with("Python")
    mock_json_saver.add_vacancy.assert_called_once()


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
