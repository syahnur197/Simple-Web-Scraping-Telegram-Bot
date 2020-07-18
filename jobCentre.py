from bs4 import BeautifulSoup

import requests

jobLink = "https://www.jobcentrebrunei.gov.bn/web/guest/search-job?q={}"
class JobCentre:

    def scrape(self, keyword):
        # get the soup object based on the keyword passed to the argument
        soup = self.getSoup(keyword)

        # find all divs with the class of jp_job_post_main_wrapper
        divs = soup.find_all("div", class_="jp_job_post_main_wrapper")

        # init jobs array
        jobs = []

        # loop the divs and get the company and job details in each div
        # and put it into a dictionary variable
        for div in divs:
            # get the data
            company = div.find_all("div", class_="jp_job_post_right_cont")[0].find_all("p")[0].find_all("a")[0].text
            title = div.find_all("div", class_="jp_job_post_right_cont")[0].find_all("h4")[0].find_all("a")[0].text
            salary = div.find_all("li")[0].text
            link = div.find_all("div", class_="jp_job_post_right_cont")[0].find_all("h4")[0].find_all("a", href=True)[0]['href']
            URLlink = "http://www.jobcentrebrunei.gov.bn{}".format(link)
            applyLink = "http://www.jobcentrebrunei.gov.bn/c/portal/login?p_l_id=95?redirectURL={}".format(link)

            # put them into a dictionary
            job = {
                'company' : company,
                'title' : title,
                'salary' : "B$ {}".format(salary),
                'link' : URLlink,
                'applyLink' : applyLink
            }

            # append the job dictionary
            jobs.append(job)
        return jobs
        

    def getSoup(self, keyword):
        # format the url before sending a request
        url = jobLink.format(keyword)

        # send a get request to the url
        resp = requests.get(url)

        # get the page content of the requested page (html, css, js)
        text = resp.text

        # convert to a BeautifulSoup object
        soup = BeautifulSoup(text, "html.parser")

        # duhh
        return soup 
