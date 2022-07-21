# # # # Selenium_PAA - v1.3 # # # # #
import sys
import time
from constants import FF_PROFILE, GECKOPATH, URL
from seleniumwire import webdriver  # testing selenium-wire to intercept image requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Any, Optional, Generator

from bs4 import BeautifulSoup
from people_also_ask.parser import (
    extract_related_questions,
    get_featured_snippet_parser,
)
from people_also_ask.exceptions import (
    RelatedQuestionParserError,
    FeaturedSnippetParserError,
)

# def interceptor(request):
#     # Block PNG, JPEG and GIF images
#     if request.path.endswith(('.png', '.jpg', '.gif')):
#         request.abort()
# Requests for PNG, JPEG and GIF images will result in a 403 Forbidden


def search(query):

    service = Service(GECKOPATH)
    profile_path = FF_PROFILE
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(
        firefox_profile=profile_path,  # deprecated method
        options=options,
        service=service)

    # block images requests with selenium-wire
    # driver.request_interceptor = interceptor
    driver.get(URL)

    search_tag_selector = '//input[@aria-label="Search"]'
    results_selector = '//div[contains(@id, "result-stats")]'
    item_tag_selector = "//div[contains(@class, 'related-question-pair')]"

    driver.execute_script("document.head.parentNode.removeChild(document.head)")
    driver.find_element(By.XPATH, search_tag_selector).send_keys(query + Keys.RETURN)

    # Added WebDriverWait to check results page before continuing, otherwise fails by going too fast
    WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((
        By.XPATH, results_selector)))

    paa = driver.find_elements(By.XPATH, item_tag_selector)

    # MANUALLY SET PAA SCRAPING LEVEL (length)
    length = 10

    if not paa or len(paa) == 0:
        print(f" ! No PAAs found for {query}")
        time.sleep(0.5)
        driver.close()
        time.sleep(0.5)

    else:
        size = 0
        while size < length:
            paa[-1].click()
            time.sleep(0.5)
            paa = driver.find_elements(By.XPATH, item_tag_selector)
            size += 1

    document = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return document


def _get_related_questions(text: str) -> List[str]:
    """
    return a list of questions related to text.
    These questions are from search result of text

    :param str text: text to search
    """
    document = search(text)

    if not document:
        return []
    try:
        return extract_related_questions(document)
    except Exception:
        raise RelatedQuestionParserError(text)


def generate_related_questions(text: str) -> Generator[str, None, None]:
    """
    generate the questions related to text,
    these questions are found recursively

    :param str text: text to search
    """
    questions = set(_get_related_questions(text))
    searched_text = set(text)
    while questions:
        text = questions.pop()
        yield text
        searched_text.add(text)
        questions |= set(_get_related_questions(text))
        questions -= searched_text


def get_related_questions(text: str, max_nb_questions: Optional[int] = None):
    """
    return a number of questions related to text.
    These questions are found recursively.

    :param str text: text to search
    """
    if max_nb_questions is None:
        return _get_related_questions(text)
    nb_question_regenerated = 0
    questions = set()
    for question in generate_related_questions(text):
        if nb_question_regenerated > max_nb_questions:
            break
        questions.add(question)
        nb_question_regenerated += 1
    return list(questions)


def get_answer(question: str) -> Dict[str, Any]:
    """
    return a dictionary as answer for a question.

    :param str question: asked question
    """
    document = search(question)
    related_questions = extract_related_questions(document)
    # related_questions = get_related_questions(question)
    featured_snippet = get_featured_snippet_parser(
            question, document)
    if not featured_snippet:
        res = dict(
            has_answer=False,
            question=question,
            related_questions=related_questions,
        )
    else:
        res = dict(
            has_answer=True,
            question=question,
            related_questions=related_questions,
        )
        try:
            res.update(featured_snippet.to_dict())
        except Exception:
            raise FeaturedSnippetParserError(question)
    return res


def generate_answer(text: str) -> Generator[dict, None, None]:
    """
    generate answers of questions related to text

    :param str text: text to search
    """

    answer = get_answer(text)

    questions = set(answer["related_questions"])
    searched_text = set(text)
    if answer["has_answer"]:
        yield answer
    while questions:
        # text = questions.pop()
        answer = get_answer(text)
        if answer["has_answer"]:
            yield answer
        searched_text.add(text)
        questions |= set(get_answer(text)["related_questions"])
        questions -= searched_text


def get_simple_answer(question: str, depth: bool = False) -> str:
    """
    return a text as summary answer for the question

    :param str question: asked question
    :param bool depth: return the answer of first related question
        if no answer found for question
    """
    document = search(question)
    featured_snippet = get_featured_snippet_parser(
            question, document)
    if featured_snippet:
        return featured_snippet.response
    if depth:
        related_questions = get_related_questions(question, 10)
        if not related_questions:
            return ""
        return get_simple_answer(related_questions[0])
    return ""


# def answer_then_related(question: str, depth: bool = False) -> str:
#     """
#     return a text as summary answer for the question
#
#     :param str question: asked question
#     :param bool depth: return the answer of first related question
#         if no answer found for question
#     """
#     document = search(question)
#     text = question
#
#     def answer():
#         featured_snippet = get_featured_snippet_parser(
#             question, document)
#         if featured_snippet:
#             return featured_snippet.response
#         if depth:
#             related_questions = get_related_questions(question)
#             if not related_questions:
#                 return ""
#             return get_simple_answer(related_questions[0])
#         return ""
#
#     def _getrelated_questions(text: str) -> List[str]:
#         if not document:
#             return []
#         try:
#             return extract_related_questions(document)
#         except Exception:
#             raise RelatedQuestionParserError(text)
#
#     def generate_related(text: str) -> Generator[str, None, None]:
#         """
#         generate the questions related to text,
#         these questions are found recursively
#
#         :param str text: text to search
#         """
#         questions = set(_getrelated_questions(text))
#         searched_text = set(text)
#         while questions:
#             text = questions.pop()
#             yield text
#             searched_text.add(text)
#             questions |= set(_getrelated_questions(text))
#             questions -= searched_text
#
#     def related(text: str) -> Generator[str, None, None]:
#         max_nb_questions = 5
#         nb_question_regenerated = 0
#         questions = set()
#         for question in generate_related(text):
#             if nb_question_regenerated > max_nb_questions:
#                 break
#             questions.add(question)
#             nb_question_regenerated += 1
#         return list(questions)
#
#     # Need to output these to a list or whatever
#     print('ANSWER:', answer())
#     print('RELATED QUESTIONS:')
#     print(related(question))


if __name__ == "__main__":
    from pprint import pprint as print
    print(get_answer(sys.argv[1]))
