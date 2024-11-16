# - Constants 

language = 'en'


# - Language keywords

language_table = {
    "en": {
        "settings_section": "*** Settings ***",
        "variables_section": "*** Variables ***",
        "testcases_section": "*** Test Cases ***",
        "tasks_section": "*** Tasks ***",
        "keywords_section": "*** Keywords ***",
        "comments_section": "*** Comments ***",

        "library": "Library",
        "resource": "Resource",
        "variables": "Variables",
        "name": "Name",
        "documentation": "Documentation",
        "metadata": "Metadata",
        "testtags": "Test Tags",
        "tags": "Tags",
        "template": "Template",
        "arguments": "Arguments",

        "background": "Background",
        "scenario": "Scenario",
        "scenariooutline": "Scenario Outline",
        "Given ": "Given ",
        "When ": "When ",
        "Then ": "Then ",
        "And ": "And ",
        "But ": "But "
    },
    "nl":{
        "settings_section": "*** Instellingen ***",
        "variables_section": "*** Variabelen ***",
        "testcases_section": "*** Testgevallen ***",
        "tasks_section": "*** Taken ***",
        "keywords_section": "*** Sleutelwoorden ***",
        "comments_section": "*** Opmerkingen ***",

        "library": "Bibliotheek ",
        "resource": "Resource",
        "variables": "Variabele",
        "name": "Naam",
        "documentation": "Documentatie",
        "metadata": "Metadata",

  
# Suite Setup	Suite Preconditie
# Suite Teardown	Suite Postconditie
# Test Setup	Test Preconditie
# Task Setup	Taak Preconditie
# Test Teardown	Test Postconditie
# Task Teardown	Taak Postconditie
# Test Template	Test Sjabloon
# Task Template	Taak Sjabloon
# Test Timeout	Test Time-out
# Task Timeout	Taak Time-out
        "testtags": "Test Labels",
# Task Tags	Taak Labels
# Keyword Tags	Sleutelwoord Labels

        "tags": "Labels",
# Setup	Preconditie
# Teardown	Postconditie
# Template	Sjabloon
        "template": "Sjabloon",
# Timeout	Time-out
        "arguments": "Parameters",

        "background": "Achtergrond",
        "scenario": "Scenario,Voorbeeld",
        "scenariooutline": "Abstract Scenario",
        "Given ": "Gegeven ",
        "When ": "Als ",
        "Then ": "Dan ",
        "And ": "En ",
        "But ": "Maar ",
        "Wanneer ": "Als ",
    }
}

# - Functions -----------------------------------------------------------------

def set_language(new_language: str):
    global language
    language = new_language


def get_language() -> str:
    return language


def tr(text_id, default=None):
    text = language_table[language].get(text_id, None)
    if text is None:
        text = language_table["en"].get(text_id, None)
        if text is None and default is None:
            raise RuntimeWarning(f"No translation found for `{text_id}` in language: {language}")
        else:
            text = default
    return text

