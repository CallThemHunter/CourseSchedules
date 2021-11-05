import requests
import requests.adapters
import json
import os
from requests.structures import CaseInsensitiveDict
import threading
import queue
import time
departments = [
    'AAS',
    'AHI',
    'AMS',
    'ARC',
    'ARI',
    'ART',
    'AS',
    'ASL',
    'BCH',
    'BE',
    'BIO',
    'BMI',
    'BMS',
    'CDA',
    'CDS',
    'CE',
    'CEP',
    'CHB',
    'CHE',
    'CHI',
    'CIE',
    'CL',
    'COL',
    'COM',
    'CPM',
    'CSE',
    'DAC',
    'DMS',
    'EAS',
    'ECO',
    'EE',
    'ELP',
    'END',
    'ENG',
    'ES',
    'ESL',
    'EVS',
    'FR',
    'GEO',
    'GER',
    'GGS',
    'GLY',
    'GR',
    'GRE',
    'HEB',
    'HIN',
    'HIS',
    'HON',
    'IE',
    'ITA',
    'JDS',
    'JPN',
    'KOR',
    'LAI',
    'LAT',
    'LAW',
    'LIN'
    'LIS',
    'LLS',
    'MAE',
    'MCH',
    'MDI',
    'MGA',
    'MGB',
    'MGE',
    'MGF',
    'MGG',
    'MGI',
    'MGM',
    'MGO',
    'MGQ',
    'MGS',
    'MGT',
    'MIC',
    'MLS',
    'MT',
    'MTH',
    'MTR',
    'MUS',
    'NBS',
    'NMD',
    'NRS',
    'NSG',
    'NTR',
    'OT',
    'PAS',
    'PGY',
    'PHC',
    'PHI',
    'PHM',
    'PHY',
    'PMY',
    'POL',
    'PS',
    'PSC',
    'PSY',
    'PUB',
    'REC',
    'RLL',
    'RUS',
    'SOC',
    'SPA',
    'SSC',
    'STA',
    'SW',
    'TH',
    'UE',
    'UGC',
    'ULC',
    'YID'
]

semester = 'fall'
authorization = 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiVGVzdGluZyBUb2tlbiIsImdyb3VwIjoiSU1DIiwidXNlciI6IjVmYzY3OTlmZjM0MzllMDAxMjBkMmUxNCIsImRvbWFpbiI6WyIqIl0sInBlcm1pc3Npb25zIjpbImNhdGFsb2ciLCJzY2hlZHVsZSIsImJ1aWxkaW5ncyIsIm5scCJdLCJ0b2tlbl9pZCI6IjVmYzY4MDQ3YWU0ODFjMDAxMmU5ZDA4NCIsImlhdCI6MTYwNjg0NDQ4N30.EWQyQ-4f32zmjCC0IuhnjPAniOAyQnoE52vcHrur1yY'
url = 'https://imc-apis.webapps.buffalo.edu/schedule/courses/' + semester

exitFlag = 0
threads = []
queueLock = threading.Lock()
workQueue = queue.Queue(120)
session = requests.session()
adapter = requests.adapters.HTTPAdapter(pool_connections=25, pool_maxsize=25)
session.mount('http://', adapter)

class MyThread (threading.Thread):
    def __init__(self, threadID, name, department):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = department

    def run(self):
        print("Starting " + self.name)
        with open('./departments/' + self.q + '.txt', 'w') as f:
            courses = self.get_department_courses(self.q)
            json.dump(courses, f)
        print("Exiting " + self.name)


    def get_department_courses(self, department):
        ret = []
        for course in range(100, 801):
            ret += get_department_course(department, str(course))
            # time.sleep(.5)
        return ret


def get_department_course(department, number):
    req = url + '?abbr=' + department + '&num=' + number

    headers = CaseInsensitiveDict()
    headers["Authorization"] = authorization

    resp = session.get(req, headers=headers)
    if resp.status_code == 200:
        if resp.text == '':
            return []
        try:
            json_out = resp.json()
        except Exception as err:
            print("what the fuck")
            return []
        if 'exam' in json_out:
            return [json_out]
        elif json_out['total'] == 0:
            return []
        else:
            return resp.json()['courses']
    else:
        return []


def get_all_courses():
    threadID = 1

    for department in departments:
        if not os.path.exists('./departments/'+department+'.txt'):
            thread = MyThread(threadID, department, department)
            thread.start()
            threads.append(thread)
            threadID += 1

    exitFlag = 1
    for t in threads:
        t.join()

    return


def load_all_courses():
    ret = []
    for department in departments:
        with open('./departments/'+department+'.txt', 'r') as f:
            courses = json.load(f)
        ret += courses
    pass


class Scheduler:
    coarse = {}


    def process_courses(self, courses):
        for course in courses:
            building, room = course['room'].split(' ')
            dates = course['dates']
            days = course['days']


    def add_course(self, building, room, dates, days):
        if building not in self.coarse:
            self.coarse[building] = {}
        if room not in self.coarse[building]:
            self.coarse[building][room] = {}
        self.coarse[building][room] += {'dates': dates, 'days': days}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_all_courses()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
