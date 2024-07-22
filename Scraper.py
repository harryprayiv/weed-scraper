#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time

def scrape_position_data(url, driver):
    driver.get(url)
    time.sleep(5)  # Adjust the sleep time as needed for page load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    rows = soup.find_all('tr', class_='TableBase-bodyTr')
    position_data = []

    for row in rows:
        player_data = {}

        # Extracting player name, position, and team
        player_name_tag = row.find('a')
        if player_name_tag:
            player_data['player_name'] = player_name_tag.get_text(strip=True)

        position_tag = row.find('span', class_='CellPlayerName-position')
        if position_tag:
            player_data['position'] = position_tag.get_text(strip=True)

        team_tag = row.find('span', class_='CellPlayerName-team')
        if team_tag:
            player_data['team'] = team_tag.get_text(strip=True)

        # Extracting statistics from each row
        stat_tags = row.find_all('td', class_='TableBase-bodyTd--number')
        stats = [tag.get_text(strip=True) for tag in stat_tags]

        # Assuming a fixed number and order of stats, assign them to named fields
        if len(stats) >= 20:  # Modify this condition based on the actual number of stats
            player_data.update({
                'stat1': stats[0],  # Replace 'stat1', 'stat2', etc. with actual stat names
                'stat2': stats[1],
                # Continue for all other stats...
                'stat20': stats[19]
            })

        position_data.append(player_data)

    return position_data

def get_cbs_sports_data():
    base_url = "https://www.cbssports.com/fantasy/baseball/stats/"
    positions = ["C", "1B", "2B", "SS", "3B", "OF", "U", "SP", "RP"]
    year = "2023"
    all_data = []

    driver = webdriver.Firefox()  # or use webdriver.Chrome()

    for position in positions:
        url = f"{base_url}{position}/{year}/season/stats/"
        position_data = scrape_position_data(url, driver)
        all_data.extend(position_data)

    driver.quit()

    # Save the data to a JSON file
    with open('player_stats_2023.json', 'w') as file:
        json.dump(all_data, file, indent=4)

if __name__ == "__main__":
    get_cbs_sports_data()
