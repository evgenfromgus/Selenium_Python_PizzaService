import logging

import allure
from selenium.webdriver.support import expected_conditions as ec

from final.base.base_page import BasePage
from final.configuration.links import Links

logger = logging.getLogger(__name__)


class DesertsPage(BasePage):
    PAGE_URL = Links.DESERT_URL

    def add_desert_to_cart(self, desert_name):
        with allure.step(f"Добавление десерта {desert_name} в корзину"):
            desert_name_locator = (
                "xpath",
                f"//a[contains(@aria-label, '{desert_name}')]",
            )
            self.wait.until(ec.element_to_be_clickable(desert_name_locator)).click()
            logger.info(f"Добавлен {desert_name} в корзину")
