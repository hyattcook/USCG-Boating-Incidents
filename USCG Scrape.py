import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import product

from selenium import webdriver


def combo():
    request = requests.get('https://bard.knightpoint.systems/PublicInterface/Report1.aspx')
    content = request.content

    soup = BeautifulSoup(content, 'html.parser')

    criteria = soup.find('select', {'id': 'dlist_criteria'}).find_all('option')
    state = soup.find('select', {'id': 'dlist_state'}).find_all('option')
    year = soup.find('select', {'id': 'dlist_year'}).find_all('option')

    criteria_list = [c.text for c in criteria]
    state_list = [s.text for s in state[1:]]
    year_list = [y.text for y in year[1:]]

    combinations = list(product(criteria_list, state_list, year_list))

    return combinations, criteria_list, state_list, year_list

combinations, criteria_list, state_list, year_list = combo()

def scrape():
    criteria_number = {
        'Year': 1,
        'Month': 2,
        'Body of Water': 3,
        'Vessel Type': 4,
        'Accident Type': 5,
        'Accident Cause': 6,
        'Operator Experience': 7,
        'Operator Education': 8,
        'Cause of Death': 9,
        'Primary Injury': 10,
        'Vessel Length Category': 11,
        'Operator Age Category': 12,
        'Injured Age Category': 13,
        'Deceased Age Category': 14,
        'Time Of Day': 15    
    }
    
    

    # Create a dataframe to house all the data.
    dataframe = pd.DataFrame(columns=['State', 'Year', 'Dimension', 'Dimension Detail',
                                      'Accidents', 'Vessels', 'Injuries', 'Deaths'])

    # Create a dataframe for the parameters that have no data.
    empty = pd.DataFrame(columns=['State', 'Year', 'Dimension'])

    sequence = 1
    for c, s, y in combinations[:1000]:
        #Measure progress
        print(f'Completing Sequence {sequence}')
        sequence += 1

        # Set the search parameters.
        dimension = criteria_number[c]
        state = s
        year = y

        
        try:
            # Assign the base url a variable.
            url = 'https://bard.knightpoint.systems/PublicInterface/Report1.aspx'
            # Create dictionary of all the search requirements.
            payload = {'dlist_criteria': dimension, 'dlist_state': state, 'dlist_year': year, 'btnsubmit': 'Search',
                       '__VIEWSTATEGENERATOR': '86A19E47',
                      '__VIEWSTATE': '/wEPDwULLTE3MjkxMzYyOTIPFgIeE1ZhbGlkYXRlUmVxdWVzdE1vZGUCARYCAgMPZBYWZg8WAh4JaW5uZXJodG1sBQsyMDA1IC0gMjAxN2QCAQ8QZGQWAQIBZAICDxAPFgYeDURhdGFUZXh0RmllbGQFBXN0YXRlHg5EYXRhVmFsdWVGaWVsZAUFc3RhdGUeC18hRGF0YUJvdW5kZ2QQFT0DQUxMAkFLAkFMAkFSAkFUAkFaAkNBAkNPAkNUAkRDAkRFAkZFAkZMAkdBAkdMAkdNAkdVAkhJAklBAklEAklMAklOAktTAktZAkxBAk1BAk1EAk1FAk1JAk1OAk1PAk1QAk1TAk1UAk5DAk5EAk5FAk5IAk5KAk5NAk5WAk5ZAk9IAk9LAk9SAlBBAlBDAlBSAlJJAlNDAlNEAlROAlRYAlVUAlZBAlZJAlZUAldBAldJAldWAldZFT0DQUxMAkFLAkFMAkFSAkFUAkFaAkNBAkNPAkNUAkRDAkRFAkZFAkZMAkdBAkdMAkdNAkdVAkhJAklBAklEAklMAklOAktTAktZAkxBAk1BAk1EAk1FAk1JAk1OAk1PAk1QAk1TAk1UAk5DAk5EAk5FAk5IAk5KAk5NAk5WAk5ZAk9IAk9LAk9SAlBBAlBDAlBSAlJJAlNDAlNEAlROAlRYAlVUAlZBAlZJAlZUAldBAldJAldWAldZFCsDPWdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIDDxAPFgYfAgUEeWVhch8DBQR5ZWFyHwRnZBAVDgNBTEwEMjAwNQQyMDA2BDIwMDcEMjAwOAQyMDA5BDIwMTAEMjAxMQQyMDEyBDIwMTMEMjAxNAQyMDE1BDIwMTYEMjAxNxUOA0FMTAQyMDA1BDIwMDYEMjAwNwQyMDA4BDIwMDkEMjAxMAQyMDExBDIwMTIEMjAxMwQyMDE0BDIwMTUEMjAxNgQyMDE3FCsDDmdnZ2dnZ2dnZ2dnZ2dnZGQCBQ8PFgIeBFRleHQFI1Jlc3VsdHM6ICZuYnNwOzEmbmJzcDtSZWNvcmRzIEZvdW5kZGQCCA8PFgQeB1Zpc2libGVnHghJbWFnZVVybAUSSW1hZ2VzL2V4Y2VsLTQuanBnZGQCCQ8PFgQfBmcfBwUSSW1hZ2VzL2NoYXJ0LTMuanBnZGQCCg8PFgQfBmcfBwUSSW1hZ2VzL2NoYXJ0LTIuanBnZGQCCw88KwARAgAPFgQfBGceC18hSXRlbUNvdW50AgFkDBQrAAUWCB4ETmFtZQUEWWVhch4KSXNSZWFkT25seWgeBFR5cGUZKwIeCURhdGFGaWVsZAUEWWVhchYIHwkFCUFjY2lkZW50cx8KaB8LGSsBHwwFCUFjY2lkZW50cxYIHwkFB1Zlc3NlbHMfCmgfCxkrAR8MBQdWZXNzZWxzFggfCQUISW5qdXJpZXMfCmgfCxkrAR8MBQhJbmp1cmllcxYIHwkFBkRlYXRocx8KaB8LGSsBHwwFBkRlYXRocxYCZg9kFgYCAQ9kFgpmDw8WAh8FBQQyMDA3ZGQCAQ8PFgIfBQUCODFkZAICDw8WAh8FBQMxMDFkZAIDDw8WAh8FBQI1NWRkAgQPDxYCHwUFAjE4ZGQCAg8PFgIfBmhkZAIDDw8WAh8GaGRkAgwPPCsAEQEMFCsAAGQCDQ8PFgIfBWVkZBgDBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAwUJSW1nX2V4Y2VsBQxJbWdfYmFyY2hhcnQFDEltZ19waXJjaGFydAUKZXhwb3J0Z3JpZA9nZAUKZ3JpZHJlc3VsdA88KwAMAQgCAWS00wCRDSROR+T9Hc2rU6JHPEfeF0SVWN036B7+MJJyQA=='}
            # Post the search request to the url.
            page = requests.post(url, data=payload)

            # Soupify the page so to parse through the data.
            content = page.content
            soup = BeautifulSoup(content, 'html.parser')
            # Find the table.
            table = soup.find('table', {'class': 'gridcontent', 'id': 'gridresult'})
            #Find the header and body rows.
            header_row = table.find('tr')
            body_rows = table.find_all('tr')[1:]
            #Find the columns of the header and their corresponding names.
            header_row_columns = header_row.find_all('th')
            header_row_names = header_row.find_all('th')[1:]

            # Create a list of all the column header names. The first one is always the 'Dimension Detial'.
            names = ['Dimension Detail']
            for name in header_row_names:
                names.append(name.text)
            
            
            # For each row in the table, append it to the dataframe.
            if len(body_rows) != 22:
                for row in body_rows:
                    detail = row.find_all('td')[0].text

                    try:
                        deaths = int(row.find_all('td')[names.index('Deaths')].text)
                    except:
                        deaths = None

                    try:
                        accidents = row.find_all('td')[names.index('Accidents')].text
                    except:
                        accidents = None

                    try:
                        vessels = row.find_all('td')[names.index('Vessels')].text
                    except:
                        vessels = None

                    try:
                        injuries = row.find_all('td')[names.index('Injuries')].text
                    except:
                        injuries = None

                    entry = {
                        'State': state,
                        'Year': year,
                        'Dimension': c,
                        'Dimension Detail': detail,
                        'Accidents': accidents,
                        'Vessels': vessels,
                        'Injuries': injuries,
                        'Deaths': deaths
                    }

                    dataframe = dataframe.append(entry, ignore_index=True)

                    
            elif len(body_rows) == 22:
                # Scrape the first page.
                for row in body_rows[:-2]:
                    detail = row.find_all('td')[0].text

                    try:
                        deaths = int(row.find_all('td')[names.index('Deaths')].text)
                    except:
                        deaths = None

                    try:
                        accidents = row.find_all('td')[names.index('Accidents')].text
                    except:
                        accidents = None

                    try:
                        vessels = row.find_all('td')[names.index('Vessels')].text
                    except:
                        vessels = None

                    try:
                        injuries = row.find_all('td')[names.index('Injuries')].text
                    except:
                        injuries = None

                    entry = {
                        'State': state,
                        'Year': year,
                        'Dimension': c,
                        'Dimension Detail': detail,
                        'Accidents': accidents,
                        'Vessels': vessels,
                        'Injuries': injuries,
                        'Deaths': deaths
                    }

                    dataframe = dataframe.append(entry, ignore_index=True)
                    
                # Open Selenium driver to extract the page source for the other pages.
                driver = webdriver.Chrome('C:\\Users\\Hyatt Cook\\Desktop\Web Scraping\\chromedriver.exe')
                driver.get('https://bard.knightpoint.systems/PublicInterface/Report1.aspx')

                # Define all the parameter options.
                sel_criteria = driver.find_element_by_xpath('//*[@id="dlist_criteria"]').find_elements_by_tag_name('option')
                sel_state = driver.find_element_by_xpath('//*[@id="dlist_state"]').find_elements_by_tag_name('option')
                sel_year = driver.find_element_by_xpath('//*[@id="dlist_year"]').find_elements_by_tag_name('option')
                sel_submit = driver.find_element_by_xpath('//*[@id="btnsubmit"]')

                # Click on the required parameters.
                sel_criteria[criteria_list.index(c)].click()
                sel_state[state_list.index(s) + 1].click()
                sel_year[year_list.index(y) + 1].click()
                sel_submit.click()
                
                # Go to each page.
                sel_pagination = driver.find_element_by_xpath('//*[@id="gridresult"]/tbody/tr[22]/td/table').find_elements_by_tag_name('td')
                for i in range(1, len(sel_pagination)):
                    page_pagination = driver.find_element_by_xpath('//*[@id="gridresult"]/tbody/tr[22]/td/table').find_elements_by_tag_name('td')
                    # Click on the next page
                    page_pagination[i].click()
                    # Extract the source code.
                    source_code = driver.page_source
                    
                    # Parse through the source code.
                    soup = BeautifulSoup(source_code, 'html.parser')
                    # Find the table.
                    table = soup.find('table', {'class': 'gridcontent', 'id': 'gridresult'})
                    #Find the header and body rows.
                    header_row = table.find('tr')
                    body_rows = table.find_all('tr')[1:]
                    #Find the columns of the header and their corresponding names.
                    header_row_columns = header_row.find_all('th')
                    header_row_names = header_row.find_all('th')[1:]

                    # Create a list of all the column header names. The first one is always the 'Dimension Detial'.
                    names = ['Dimension Detail']
                    for name in header_row_names:
                        names.append(name.text)
                    
                    for row in body_rows[:-2]:
                        detail = row.find_all('td')[0].text

                        try:
                            deaths = int(row.find_all('td')[names.index('Deaths')].text)
                        except:
                            deaths = None

                        try:
                            accidents = row.find_all('td')[names.index('Accidents')].text
                        except:
                            accidents = None

                        try:
                            vessels = row.find_all('td')[names.index('Vessels')].text
                        except:
                            vessels = None

                        try:
                            injuries = row.find_all('td')[names.index('Injuries')].text
                        except:
                            injuries = None

                        entry = {
                            'State': state,
                            'Year': year,
                            'Dimension': c,
                            'Dimension Detail': detail,
                            'Accidents': accidents,
                            'Vessels': vessels,
                            'Injuries': injuries,
                            'Deaths': deaths
                        }

                        dataframe = dataframe.append(entry, ignore_index=True)
                                            
                                      
        except:
            entry = {
                'State': state,
                'Year': year,
                'Dimension': c,
            }

            empty = empty.append(entry, ignore_index=True)
            
    return dataframe, empty

get_ipython().magic('time dataframe, empty = scrape()')

dataframe.to_csv('USCG.csv')
empty.to_csv('Empty.csv')

