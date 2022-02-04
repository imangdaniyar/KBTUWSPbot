import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from . import routes

day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
delay = 1


class WSPUser:
    def __init__(self, login, password):
        user_agent = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent.random}')
        options.add_argument('--log-level=3')
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.LOGIN = login
        self.PASSWORD = password
        self.logged = False
        self.main_window = None
        self.windows = []

    def login(self):
        try:
            self.driver.get(routes.URL)
            time.sleep(delay)

            login_page = self.driver.find_element(By.XPATH, routes.LOGIN_PAGE_PATH)
            ActionChains(self.driver).move_to_element(login_page).click().perform()
            time.sleep(delay)

            password_input = self.driver.find_element(By.ID, 'gwt-uid-6')
            password_input.clear()
            password_input.send_keys(self.PASSWORD)
            # time.sleep(delay)

            email_input = self.driver.find_element(By.ID, 'gwt-uid-4')
            email_input.clear()
            email_input.send_keys(self.LOGIN)
            time.sleep(delay)

            login_button = self.driver.find_element(By.XPATH, routes.LOGIN_BUTTON_PATH)
            ActionChains(self.driver).move_to_element(login_button).click().perform()
            time.sleep(delay)

            # home = self.driver.find_element(By.XPATH, routes.HOME_PATH)
            # ActionChains(self.driver).move_to_element(home).click().perform()

            self.logged = True
            self.main_window = self.driver.current_window_handle
            # time.sleep(2)
        except Exception as e:
            print(f'Exception = {e}')

    def is_logged(self):
        return self.logged

    def close_session(self):
        self.driver.close()
        self.driver.quit()

    def get_attestation_screenshot(self):
        if self.logged:
            self.driver.get(routes.ATTESTATION_URL)
            time.sleep(2)
            semesters = self.driver.find_elements(By.CSS_SELECTOR, "div[class='v-slot v-align-center']")
            attestation = {}
            n = 1
            for i in semesters:
                try:
                    semester = i.find_element(By.CLASS_NAME, "v-panel-caption").text
                    self.driver.execute_script("arguments[0].scrollIntoView();", i)
                    pic_name = f'img/{self.LOGIN}_{n}.png'
                    i.screenshot(pic_name)
                    attestation[semester] = pic_name
                    n += 1
                except:
                    print('No attestation description')
            return attestation

    def get_attestation(self):
        if self.logged:
            self.driver.get(routes.ATTESTATION_URL)
            time.sleep(2)
            semesters = self.driver.find_elements(By.CLASS_NAME, 'v-table-table')
            attestation = []
            for i in semesters:
                table = pd.read_html(i.get_attribute('outerHTML'))[0]
                # table = table.drop(columns=[3, 7])
                table = table.rename(
                    columns={0: 'Код курса',
                             1: 'Наименование курса',
                             2: 'Mid Term',
                             4: 'End Term',
                             5: 'Final Exam',
                             6: 'Итоговая буквенная оценка'})
                attestation.append(table)
            return attestation
        else:
            return 'Your are not logged'

    def get_schedule(self):
        if self.logged:
            self.driver.get(routes.SCHEDULE_URL)
            time.sleep(1)
            schedule = {}
            for i in day_names:
                schedule.update({i: []})
            days = self.driver.find_elements(By.XPATH,
                                             '/html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div/div[3]/div/div/div/div/div[31]/div/div/div')
            for i, n in zip(days, day_names):
                day = i.find_elements(By.CSS_SELECTOR,
                                      'div > div > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div')
                if day:
                    for course in day:
                        schedule[n].append(course.text)
            return schedule
        else:
            return {'error_message': 'Your are not logged'}

    def attend_lesson(self):
        self.driver.get(routes.ATTENDANCE_URL)
        time.sleep(1)
        attend_list = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div')
        attend_buttons = attend_list.find_elements(By.XPATH, 'div/div/div[3]/div')
        for i in attend_buttons:
            i.click()

    def get_news(self):
        if self.logged:
            self.driver.get(routes.NEWS_URL)
            time.sleep(1)
            news = self.driver.find_elements(By.XPATH,
                                             '/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div/div')
            news_list = []
            for i in news:
                date = i.find_element(By.XPATH, 'div/div/div/div[2]/div/div/div[1]/div').text
                description = 'No description'
                try:
                    description = i.find_element(By.XPATH, 'div/div/div/div[2]/div/div/div[2]/div/div/div/div').text
                except:
                    pass
                try:
                    description = i.find_element(By.XPATH, 'div/div/div/div[2]/div/div/div[3]/div/div/div/div').text
                except:
                    pass
                date = ' '.join(date.split()[:-2])
                description = description.replace('  ', '').replace('\t', '')
                news_list.append({'Date': date, 'Description': description})
            return news_list
        else:
            return 'Your are not logged'
