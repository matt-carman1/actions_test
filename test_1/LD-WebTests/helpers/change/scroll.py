from library import dom
from selenium.webdriver.common.keys import Keys


def scroll_to_right(driver, keystrokes):
    """
    Scrolls the LR to the right, using right navigation key
    For this method to work, grid cells should be unselected
    :param driver: selenium webdriver
    :param keystrokes: int, number of strokes of right navigation key
    """
    dom.press_keys(driver, Keys.RIGHT * keystrokes)


def scroll_to_left(driver, keystrokes):
    """
    Scrolls the LR to the left, using left navigation key
    For this method to work, grid cells should be unselected
    :param driver: selenium webdriver
    :param keystrokes: int, number of strokes of left navigation key
    """
    dom.press_keys(driver, Keys.LEFT * keystrokes)


def scroll_to_up(driver, keystrokes):
    """
    Scrolls the LR to up, using up navigation key
    For this method to work, grid cells should be unselected
    :param driver: selenium webdriver
    :param keystrokes: int, number of strokes of up navigation key
    """
    dom.press_keys(driver, Keys.UP * keystrokes)


def scroll_to_down(driver, keystrokes):
    """
    Scrolls the LR to down, using down navigation key
    For this method to work, grid cells should be unselected
    :param driver: selenium webdriver
    :param keystrokes: int, number of strokes of down navigation key
    """
    dom.press_keys(driver, Keys.DOWN * keystrokes)


def scroll_to_rightmost(driver):
    """
    Scrolls to and selects the rightmost cell of the grid by pressing END key
    :param driver: selenium webdriver
    """
    dom.press_keys(driver, Keys.END)
