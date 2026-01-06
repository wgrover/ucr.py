import requests
import json
import cmd
from rich.console import Console
console = Console()

BASE_URL = "https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb"

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

term_code = 202610
url = f"{BASE_URL}/term/search?mode=search"
data = {'term': term_code, 'studyPath': '', 'startDatepicker': '','endDatepicker': ''}
response = session.post(url, data=data)
response.raise_for_status()
url = f"{BASE_URL}/searchResults/searchResults"
params = {
    'txt_subject': "BIEN",
    'txt_term': term_code,
    'txt_courseNumber': "",
    'startDatepicker': '',
    'endDatepicker': '',
    'pageOffset': '0',
    'pageMaxSize': '50',
    'sortColumn': 'subjectDescription',
    'sortDirection': 'asc'
}
response = session.get(url, params=params)
response.raise_for_status()
data = response.json()
# print(json.dumps(data, indent=1))



class UCR(cmd.Cmd):
    intro = "ucr.py"
    prompt = "> "
    show_special_sections = False
    show_discussions = False
    def do_l(self, arg):
        for c in data["data"]:
            if not self.show_special_sections and c["courseNumber"] in ["190", "197"]:
                pass
            elif not self.show_discussions and c["scheduleTypeDescription"] == "Discussion":
                pass
            else:
                console.print(f"[bold cyan]{c['courseNumber']}[/bold cyan]\t{c['courseTitle']} [red]{c['scheduleTypeDescription']}[/red]", end=" ")
                for f in c["faculty"]:
                    print(f["displayName"], end=" ")
                print()
    def do_q(self, arg):
        print('GTFO')
        return True
    def do_s(self, arg):
        "Show or hide special sections 190 and 197 (toggle)"
        if self.show_special_sections:
            print("\tshow special sections OFF")
            self.show_special_sections = False
        else:
            print("\tshow special sections ON")
            self.show_special_sections = True
        self.do_l(self)
    def do_d(self, arg):
        if self.show_discussions:
            print("\tshow discussions OFF")
            self.show_discussions = False
        else:
            print("\tshow discussions ON")
            self.show_discussions = True
        self.do_l(self)
    def default(self, arg):
        for c in data["data"]:
            if c["courseNumber"] == arg:
                console.print(f"{c['courseNumber']} {c['courseTitle']} {c['scheduleTypeDescription']} {c['enrollment']}/{c['maximumEnrollment']}", end=" ")
                for f in c["faculty"]:
                    console.print(f"{f['displayName'].split(',')[0]}", end=" ")
                for m in c["meetingsFaculty"]:
                    for d, day in (("M", "monday"), ("T", "tuesday"), ("W", "wednesday"), ("R", "thursday"), ("F", "friday")):
                        if m['meetingTime'][day]:
                            console.print(d, end="")
                    console.print(" ", end="")
                    console.print(f"{m['meetingTime']['beginTime']}-{m['meetingTime']['endTime']}", end=" ")
                    console.print(f"{m['meetingTime']['building']} {m['meetingTime']['room']}")

def parse(self, arg):
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
    UCR().cmdloop()