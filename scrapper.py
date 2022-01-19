import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("div", {"class": "fl1"}).find("a")['title']
    company, location = html.find("h3", {
        "class": "mb4"
    }).find_all("span", recursive=False)
    job_id = html['data-jobid']

    return {
        'title': title,
        'company': company.get_text(strip=True),
        'location': location.get_text(strip=True),
        'apply link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{url}{page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&pg="
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page,url)
    return jobs


"""
def get_jobs():
  soup = BeautifulSoup(HTML.text,'html.parser')

  page = soup.find("div",{"class":"s-pagination"})

  return page
"""
