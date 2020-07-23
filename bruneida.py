from bs4 import BeautifulSoup

import requests

jobLink = "https://www.bruneida.com/index3.php?n={}&ca=&n2=&t_d=0&page=1"

class Bruneida:

    def scrape(self, keyword):
        # format the url before sending a request
        url = jobLink.format(keyword)

        # init divs
        divs = []
        
        # get the soup object based on the keyword passed to the argument
        soup = self.getSoup(url)

        # find all divs with the class az-ext-detail
        divs = divs + soup.find_all("div", class_="az-ext-detail")

        # init jobs array
        jobs = []

        # loop the divs and get the company and job details in each div
        # and put it into a dictionary variable
        for div in divs:
            myLink = div.find('a', class_="h-elips", href=True)
            link = myLink['href']

            linkSoup = self.getSoup(link)

            linkDiv = linkSoup.find(id="contact-xs")
            company = linkDiv.find('b', text=True).string # Get Company Name
            applyLink = linkDiv.find_all('li')[5].find('a', href=True)['href'] # Get Apply Now Link

            title = myLink.contents[0]

            salary = div.find('div', class_="az-price").find(text=True)
            salary = salary[2:]

            # put them into a dictionary
            job = {
                'company' : company,
                'title' : title,
                'salary' : "B$ {}".format(salary),
                'link' : link,
                'applyLink' : applyLink
            }

            # append the job dictionary
            jobs.append(job)
        return jobs


    def getSoup(self, url):

        # send a get request to the url
        resp = requests.get(url)

        # get the page content of the requested page (html, css, js)
        text = resp.text

        # convert to a BeautifulSoup object
        soup = BeautifulSoup(text, "html.parser")

        # duhh
        return soup 
