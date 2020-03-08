from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import re

def getBeautifulSoupObject(url):
    url_str = str(url)
    html = request.urlopen(url_str)
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getHTMLContentsFromBeautifuleSoupObject(bs_object,
                                            html_class="div",
                                            attr_value="class",
                                            attr_class_name="p_local_senkyo_ttl_wrapp white column_ttl_wrapp"):
    return bs_obj.find(html_class, attrs={attr_value, attr_class_name})

def getFirstContentFromParsedHTML(parsed_html, html_class, attr_value, attr_class_name):
    try:
        return parsed_html.find(html_class, attrs={attr_value, attr_class_name}).contents[0]
    except AttributeError as e:
        print('AttributeError:', e)
        return ''

def getPrefectureNameFromElectionInformationHTML(parsed_html):
    return getFirstContentFromParsedHTML(parsed_html, html_class='p', attr_value='class',
                                         attr_class_name='column_ttl_small')

def getTownNameFromElectionInformationHTML(parsed_html):
    town_raw = getFirstContentFromParsedHTML(parsed_html, html_class='h1', attr_value='class',
                                             attr_class_name='p_local_senkyo_ttl column_ttl')
    return town_raw.strip()

def getElectionResultHTMLTableRegion(bs_object,
                                     html_class='table',
                                     attr_value='class',
                                     attr_class_name='m_senkyo_result_table'):
    """
    takes BeautifuleSoup object and returns HTML region where the election
    result is summarised.
    """
    tbl = bs_object.find(html_class, attrs={attr_value, attr_class_name})
    return tbl

def getElectionResultContents(bs_object, html_component='tr'):
    """
    From the parsed HTML region, collect only the contents that we are interested in.
    """
    return bs_object.find_all(html_component)

def getCandidateNameFromHTMLContents(parsed_html):
    """
    return the name of the candidate from the parsed HTML
    """
    name_area = parsed_html.find("a").contents[0]
    # The element looks like below, so remove the new line and the tabs.
    # \n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t神山 玄太
    name = name_area.replace('\t', '').replace('\n', '')
    return name

def getCandidatePartyNameFromHTMLContents(parsed_html):
    return getFirstContentFromParsedHTML(parsed_html, html_class='p', attr_value='class',
                                         attr_class_name='m_senkyo_result_data_circle')

def getCandidateAgeFromHTMLContents(parsed_html, delim='  '):
    age_gender_areas = getFirstContentFromParsedHTML(parsed_html,
                                                     html_class='p', attr_value='class',
                                                     attr_class_name='m_senkyo_result_data_para')
    age_gender_area = age_gender_areas.contents[0]
    age_raw, gender_raw = age_gender_area.split(delim)

    age_mat = re.compile(r'\d*')
    age_num = age_mat.match(age_raw).group()
    return age_num

def getCandidateGenderFromHTMLContents(parsed_html, delim='  '):
    age_gender_areas = getFirstContentFromParsedHTML(parsed_html,
                                                     html_class='p', attr_value='class',
                                                     attr_class_name='m_senkyo_result_data_para')
    age_gender_area = age_gender_areas.contents[0]
    age_raw, gender_raw = age_gender_area.split(delim)
    gender = gender_raw.replace('(', '').replace(')', '').replace(' ', '')
    return gender

def getCandidateElectionResultFromHTMLContents(parsed_html):
    """
    return 'Y' if the candidate won the election. 'N' otherwise.
    """
    election_result = parsed_html.find("td", attrs={"class", "left red"})
    is_elected = 'Y'
    if election_result is None:
        is_elected = 'N'
    return is_elected

def create_election_result_dictionary():
    election_results = dict()
    election_results['prefecture'] = []
    election_results['town'] = []
    election_results['name'] = []
    election_results['party'] = []
    election_results['age'] = []
    election_results['gender'] = []
    election_results['is_elected'] = []
    return election_results

if __name__ == '__main__':
    yamanashi_election_urls = ['https://go2senkyo.com/local/senkyo/18627',
                               'https://go2senkyo.com/local/senkyo/18628', 'https://go2senkyo.com/local/senkyo/18629',
                               'https://go2senkyo.com/local/senkyo/15494', 'https://go2senkyo.com/local/senkyo/19364',
                               'https://go2senkyo.com/local/senkyo/19499', 'https://go2senkyo.com/local/senkyo/15436',
                               'https://go2senkyo.com/local/senkyo/15424', 'https://go2senkyo.com/local/senkyo/16481',
                               'https://go2senkyo.com/local/senkyo/15368', 'https://go2senkyo.com/local/senkyo/17939',
                               'https://go2senkyo.com/local/senkyo/16190', 'https://go2senkyo.com/local/senkyo/17940',
                               'https://go2senkyo.com/local/senkyo/17916', 'https://go2senkyo.com/local/senkyo/16189',
                               'https://go2senkyo.com/local/senkyo/16151', 'https://go2senkyo.com/local/senkyo/19223',
                               'https://go2senkyo.com/local/senkyo/16530', 'https://go2senkyo.com/local/senkyo/18936',
                               'https://go2senkyo.com/local/senkyo/14956', 'https://go2senkyo.com/local/senkyo/15357',
                               'https://go2senkyo.com/local/senkyo/18937', 'https://go2senkyo.com/local/senkyo/18938',
                               'https://go2senkyo.com/local/senkyo/18939', 'https://go2senkyo.com/local/senkyo/16188',
                               'https://go2senkyo.com/local/senkyo/18940', 'https://go2senkyo.com/local/senkyo/18941']

    # data frame to save all the results
    election_results = create_election_result_dictionary()
    df_all = pd.DataFrame(election_results)

for url in yamanashi_election_urls:
    # download the data and parsed as BeautifulSoup
    # bs_obj = getBeautifulSoupObject(url='https://go2senkyo.com/local/senkyo/17916')
    bs_obj = getBeautifulSoupObject(url)
    print(url)
    # extract the election information
    senkyo_information = getHTMLContentsFromBeautifuleSoupObject(bs_obj,
                                                                 html_class='div',
                                                                 attr_value='class',
                                                                 attr_class_name='p_local_senkyo_ttl_wrapp white column_ttl_wrapp')
    # extract the election result part
    senkyo_result_table = getHTMLContentsFromBeautifuleSoupObject(bs_obj,
                                                                  html_class='table',
                                                                  attr_value='class',
                                                                  attr_class_name='m_senkyo_result_table')
    senkyo_result_values = getElectionResultContents(senkyo_result_table)
    # create a dictionary to store the election results
    election_results = create_election_result_dictionary()
    # store the result to the dictionary to create a pandas data frame
    for candidate in senkyo_result_values:
        election_results['prefecture'].append(getPrefectureNameFromElectionInformationHTML(senkyo_information))
        election_results['town'].append(getTownNameFromElectionInformationHTML(senkyo_information))
        election_results['name'].append(getCandidateNameFromHTMLContents(candidate))
        election_results['party'].append(getCandidatePartyNameFromHTMLContents(candidate))
        election_results['age'].append(getCandidateAgeFromHTMLContents(candidate))
        election_results['gender'].append(getCandidateGenderFromHTMLContents(candidate))
        election_results['is_elected'].append(getCandidateElectionResultFromHTMLContents(candidate))

    # save the output to a data frame
    df_election_results = pd.DataFrame(election_results)
    # append the data frame to the final data frame
    df_all = pd.concat([df_all, df_election_results], ignore_index=True)

    # create a column to indicate the town name only
    df_all['town_name'] = df_all.town.apply(lambda x: x.replace('議会議員選挙', ''))
    df_all['is_male'] = df_all.gender.apply(lambda x: 1 if x == '男' else 0)

    df_all.to_csv('./data/election_result_yamanashi.txt', sep='\t', index=False)
