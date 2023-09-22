import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://online.pace.edu/graduate-programs/ms-in-computer-science/faculty/"

try:
    page = requests.get(url)
    page.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(page.content, 'html.parser')
    faculty_members = soup.find_all('div', class_="faculty-member-expanded")

    names = []
    titles = []
    departments = []
    bios = []
    courses = []

    for member in faculty_members:
        name = member.find('h3', class_="name").text.strip()
        title = member.find('div', class_="title").text.strip()
        department = member.find('div', class_="dept").text.strip()
        bio = member.find('div', class_="bio").text.strip().replace('\n', ' ')
        ul_no_class = member.find('ul', class_=False)
        li = ul_no_class.find_all('li')
        interests = [item.get_text() for item in li]

        names.append(name)
        titles.append(title)
        departments.append(department)
        bios.append(bio)
        courses.append(interests[0] if interests else '')

    df = pd.DataFrame({'Names': names, 'Titles': titles, 'Department': departments, 'Bio': bios, 'Courses': courses})

    df.to_csv("Faculty_dataset.csv", index=False)
    print("Data successfully scraped and saved to Faculty_dataset.csv")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
