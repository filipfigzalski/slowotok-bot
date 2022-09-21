from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import os.path
import hickle

from trie import Trie
from board import Board
import credentials

# Load the dictionary
trie: Trie = None

if os.path.exists("trie.hickle"):
    print("Loading from pickle file!")
    trie = hickle.load("trie.hickle")
else:
    trie = Trie()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip().upper()
            trie.insert(word)

    hickle.dump(trie, "trie.hickle", mode="w")

print("Dictionary loaded!")
input("Press enter to continue...")

while True:
    # Creating the driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(2)

    # Opening the game.
    driver.get("https://slowotok.pl/play")

    # Logging in.
    email_box = driver.find_element(By.ID, "Email")
    password_box = driver.find_element(By.ID, "Password")

    email_box.send_keys(credentials.email)
    password_box.send_keys(credentials.password + "\n")

    # Reading the board.
    values = [["" for x in range(4)] for y in range(4)]
    elements = []

    for y in range(4):
        for x in range(4):
            num = x + 4 * y
            element = driver.find_element(By.ID, str(num))
            elements.append(element)
            values[x][y] = element.text
            print(values[x][y], end=" ")
        print("")


    board = Board(trie, values)
    board.generate_words()

    print("Words generated!")

    automate = True

    for word in board.get_words():
        print(word.get_word())
        if automate:
            chain = ActionChains(driver, duration=10)
            first = True
            for coords in word.get_combination():
                number = coords.x + coords.y * 4
                if first:
                    first = False
                    chain.click_and_hold(elements[number])
                else:
                    chain.move_to_element(elements[number])
            chain.release()
            chain.perform()

    input("Press enter to go again...")
