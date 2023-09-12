from project import yes_no_prompt, get_recipes, get_recipe_details, user_ingredients
import pytest
from unittest.mock import patch


def test_yes_no_prompt():
    question = "Do you want to continue? Yes/No: "
    valid_answers = ["yes", "no"]

    with patch('builtins.input', return_value='yes'):
        user_response = yes_no_prompt(question, valid_answers)
        assert user_response == 'yes'

    with patch('builtins.input', side_effect=['invalid_input', 'yes']):
        user_response = yes_no_prompt(question, valid_answers)
        assert user_response == 'yes'


def test_get_recipes():
    recipes = get_recipes('bacon')
    assert recipes is not None
    assert isinstance(recipes, list)


def test_get_recipe_details():
    dict = {
        'recipe': {
            'label': 'Title',
            'url': 'anyurl',
            'ingredientLines': ['one', 'two', 'three'],
            'images': {
                'REGULAR': {
                    'url': 'img_url'}}
        }
    }
    assert get_recipe_details(dict) == ('Title', 'anyurl', ['one', 'two', 'three'], 'img_url')
    
    dict = {
        'recipe': 'no recipe'
    }
    assert get_recipe_details(dict) == (None, None, None, None)

    with pytest.raises(TypeError):
        get_recipe_details()


def test_user_ingredients():
    with patch('builtins.input', return_value='Tomatoes'):
        user_response = user_ingredients()
        assert user_response == 'tomatoes'
    
    with patch('builtins.input', return_value='1'):
        user_response = user_ingredients()
        assert user_response == '1'