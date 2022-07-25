# # # # Selenium_PAA - v1.5 # # # # #
import time
from constants import FF_PROFILE, GECKOPATH, URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Any, Optional, Generator

from bs4 import BeautifulSoup
from people_aa.parser import (
    extract_related_questions,
    get_featured_snippet_parser,
)
from people_aa.exceptions import (
    RelatedQuestionParserError,
    FeaturedSnippetParserError,
)

def load_ff():
    service = Service(GECKOPATH)
    profile_path = FF_PROFILE
    options = Options()
    options.headless = False
    # options.add_argument('--ignore-certificate-errors')
    set_driver = webdriver.Firefox(firefox_profile=profile_path, options=options, service=service)
    return set_driver


class GSearch:

    search_tag_selector = '//input[@aria-label="Search"]'
    results_selector = '//div[contains(@id, "result-stats")]'
    item_tag_selector = "//div[contains(@class, 'related-question-pair')]"

    def __init__(self, question):
        self.driver = load_ff()
        self.driver.get(URL)
        # self.driver.fullscreen_window()
        self.question = question

    def search(self, query):

        # command to remove css images
        # self.driver.execute_script("document.head.parentNode.removeChild(document.head)")
        try:
            self.driver.find_element(By.XPATH, self.search_tag_selector).send_keys(query + Keys.RETURN)
        except Exception:
            self.driver.find_element(By.ID, 'recaptcha')
            print("Captcha Page - Enter within 60s")
            WebDriverWait(self.driver, timeout=60).until(EC.visibility_of_element_located((
                By.XPATH, self.search_tag_selector)))
            self.driver.find_element(By.XPATH, self.search_tag_selector).send_keys(query + Keys.RETURN)

        # Added WebDriverWait to check results page before continuing, otherwise fails by going too fast
        WebDriverWait(self.driver, timeout=10).until(EC.visibility_of_element_located((
            By.XPATH, self.results_selector)))

        paa = self.driver.find_elements(By.XPATH, self.item_tag_selector)

        # MANUALLY SET PAA SCRAPING LEVEL (length)
        length = 7

        if not paa or len(paa) == 0:
            print(f" ! No PAAs found for {query}")
            time.sleep(0.5)
            self.driver.close()
            time.sleep(0.5)

        else:
            size = 0
            while size < length:
                paa[-1].click()
                time.sleep(0.5)
                paa = self.driver.find_elements(By.XPATH, self.item_tag_selector)
                size += 1

        document = BeautifulSoup(self.driver.page_source, 'html.parser')
        return document

    def get_answer(self) -> Dict[str, Any]:
        """
        return a dictionary as answer for a question.

        :param str question: asked question
        """
        document = self.search(self.question)
        related_questions = extract_related_questions(document)
        # related_questions = get_related_questions(question)
        featured_snippet = get_featured_snippet_parser(
            self.question, document)
        if not featured_snippet:
            res = dict(
                has_answer=False,
                question=self.question,
                related_questions=related_questions,
            )
        else:
            res = dict(
                has_answer=True,
                question=self.question,
                related_questions=related_questions,
            )
            try:
                res.update(featured_snippet.to_dict())
            except Exception:
                raise FeaturedSnippetParserError(self.question)
        return res

    def _get_related_questions(self, text: str) -> List[str]:
        """
        return a list of questions related to text.
        These questions are from search result of text

        :param str text: text to search
        """
        document = self.search(text)

        if not document:
            return []
        try:
            return extract_related_questions(document)
        except Exception:
            raise RelatedQuestionParserError(text)

    def generate_related_questions(self, text: str) -> Generator[str, None, None]:
        """
        generate the questions related to text,
        these questions are found recursively

        :param str text: text to search
        """
        questions = set(self._get_related_questions(text))
        searched_text = set(text)
        while questions:
            text = questions.pop()
            yield text
            searched_text.add(text)
            questions |= set(self._get_related_questions(text))
            questions -= searched_text

    def get_related_questions(self, text: str, max_nb_questions: Optional[int] = None):
        """
        return a number of questions related to text.
        These questions are found recursively.

        :param str text: text to search
        """
        if max_nb_questions is None:
            return self._get_related_questions(text)
        nb_question_regenerated = 0
        questions = set()
        for question in self.generate_related_questions(text):
            if nb_question_regenerated > max_nb_questions:
                break
            questions.add(question)
            nb_question_regenerated += 1
        return list(questions)

    def generate_answer(self, text: str) -> Generator[dict, None, None]:
        """
        generate answers of questions related to text

        :param str text: text to search
        """

        answer = self.get_answer(text)

        questions = set(answer["related_questions"])
        searched_text = set(text)
        if answer["has_answer"]:
            yield answer
        while questions:
            # text = questions.pop()
            answer = self.get_answer(text)
            if answer["has_answer"]:
                yield answer
            searched_text.add(text)
            questions |= set(self.get_answer(text)["related_questions"])
            questions -= searched_text

    def get_simple_answer(self, question: str, depth: bool = False) -> str:
        """
        return a text as summary answer for the question

        :param str question: asked question
        :param bool depth: return the answer of first related question
            if no answer found for question
        """
        document = self.search(question)
        featured_snippet = get_featured_snippet_parser(
                question, document)
        if featured_snippet:
            return featured_snippet.response
        if depth:
            related_questions = self.get_related_questions(question, 10)
            if not related_questions:
                return ""
            return self.get_simple_answer(related_questions[0])
        return ""

    def __del__(self):
        try:
            self.driver.close()
            # print("driver successfully closed.")
        except Exception:
            print("driver already closed.")


# if __name__ == "__main__":
#     from pprint import pprint as print
#     print(get_answer(sys.argv[1]))
