import requests
from bs4 import BeautifulSoup as bs
from fuzzywuzzy import process
from documents import documents_all
from subjects import all_subjects
import os
import datetime
import pandas as pd


class Core():
    def login(self, login, password):
        if login is None and password is None:
            return 0
        self.s = requests.Session()
        data = {"exceededAttempts": False, "ReturnUrl": "", "login": login, "password": password, "Captcha.Input": "", "Captcha.Id": "3c9b3f6d-a109-43cf-be5f-62661d5edfc3"}
        url = "https://login.kundelik.kz/login"
        self.s.post(url, data)
        if str(self.s.get(url).url) == str(url):
            return 0
        return 1

    def get_days(self, link):
        page = self.s.get(link)
        bs_page = bs(page.content, "html.parser")
        days = bs_page.find_all("tr", {"class": "wWeek", "id": True})
        return days

    def update_schedule(self, file):
        data = pd.read_excel(file)
        data = data.to_dict(orient="list")
        with open("dataframe.txt", "w", encoding="utf-8") as f:
            f.write("{")
            for key in data:
                f.write("{0}: {1}\n".format(key, data[key]))
            f.write("}")
        keys = ("Unnamed: 2", "Unnamed: 3", "Unnamed: 4", "Unnamed: 5", "Unnamed: 6")
        schedule_by_days = {"Monday": [],
                            "Tuesday": [],
                            "Wednesday": [],
                            "Thursday": [],
                            "Friday": [],
                            "Saturday": []}
        week_days = list(schedule_by_days.keys())
        for i in range(len(keys)):
            for j in range(len(data[keys[i]])):
                if data[keys[i]][j] != " " and not pd.isnull(data[keys[i]][j]) and data["Unnamed: 1"][j] not in {" ", "#"}:
                    subject_name = ""
                    for c in data[keys[i]][j]:
                        if c != "\n":
                            subject_name += c
                        else:
                            break
                    schedule_by_days[week_days[i]].append(subject_name)
                    all_subjects.add(subject_name)
        return schedule_by_days

    def match_subjects(self, folder, matched_subjects):
        subject = matched_subjects.get(folder)
        if not subject:
            all_subjects_list = list(all_subjects)
            exctracted = process.extractOne(folder, all_subjects_list)
            if exctracted[1] >= 80:
                subject = exctracted[0]
        return subject

    def get_folders(self, link):
        file_page = self.s.get(link)  # class files page
        bs_file_page = bs(file_page.content, "html.parser")  # parsing the file_page
        folders = bs_file_page.find_all("li", {"id": True})
        folders_name_id = []

        for folder in folders:
            try:
                folders_name_id.append((str(folder.div.a.span["title"]), folder["id"]))
            except AttributeError:
                continue
            except TypeError:
                continue

        return folders_name_id

    def get_subjects_for_today(self, schedule):
        week = datetime.datetime.now().strftime("%A")
        if week == "Sunday":
            return 0

        return set(schedule[week])

    def search_for_documents(self, folder_name, folder_id, matched_subjects, subjects_for_now, link):
        c = set(["\\", "/", "*", ":", "?", "\"", "<", ">", "|"])
        links = {}

        if matched_subjects.get(folder_name) not in subjects_for_now:
            return (0, 0)

        # Looking through the folder
        j = 1  # page number
        while True:
            folder_page = self.s.get("{0}&folder={1}&page={2}".format(link, folder_id[1:], j))  # current folder
            bs_folder_page = bs(folder_page.content, "html.parser")
            files = bs_folder_page.find_all("div", {"class": "name"})  # looking for files

            # if there are no files stop the loop
            if not files:
                break

            for file in files:
                if file.a.string not in documents_all:
                    links[str(file.a.string)] = file.a["href"]
            j += 1

        print(folder_name)

        # Creating a directory for current folder
        try:
            os.mkdir("Documents/{0}".format(folder_name))
        except FileExistsError:
            pass
        except OSError:
            for i in range(len(folder_name)):
                if folder_name[i] in c:
                    folder_name = folder_name[:i] + " " + folder_name[i + 1:]
            if folder_name[-1] == " ":
                folder_name = folder_name[:-1]
            try:
                os.mkdir("Documents/{0}".format(folder_name))
            except FileExistsError:
                pass
            except OSError as e:
                print(e)
                try:
                    folder_name = "Undefined"
                    os.mkdir("Documents/{}".format(folder_name))
                except FileExistsError:
                    pass

        return (links, folder_name)

    def download_files(self, new_file, file_link, folder_name):
        link = self.s.get(file_link)
        bs_link = bs(link.content, "html.parser")
        download_link = bs_link.find("a", {"class": "file link trackable", "data-category": "Download"})["href"]
        print(folder_name[-1])
        with open("Documents/{0}/{1}.docx".format(folder_name, new_file), "wb") as f:
            f.write(self.s.get(download_link).content)
        documents_all.add(new_file)

    def remember_files(self):
        with open("documents.py", "w", encoding="utf-8") as f:
            f.write("documents_all = {}".format(documents_all))
