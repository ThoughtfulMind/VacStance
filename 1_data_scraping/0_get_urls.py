#!/usr/bin/env python

import argparse
import re
import pickle
import os
import pandas as pd
import numpy as np
import glob
import datetime
import json
from dateutil import parser
from collections import defaultdict
import shutil
from requests.exceptions import SSLError
import time

config = json.load(open('../config.json', 'r'))
MC_API_KEY = config['MC_API_KEY']
SERP_API_KEY = config['SERP_API_KEY']

def do_serpapi(domain,keyword):
    """
    Wrapper script for running a SerpAPI query.
    :param domain: str website name, beginning with "www", e.g. "www.foxnews.com".
    :param keyword: str keyword for doing Google search.
    :return: list of dictionaries
    """
    keyword = keyword.replace('_',' ').replace('+',' ').replace('-',' ')
    client.params_dict["q"] = "site:{} {}".format(domain,keyword) # Update query to restrict to particular site
    print('Searching w/ query: {}...'.format(client.params_dict["q"]))
    client.params_dict["num"] = 100
    page_no = 1
    client.params_dict["start"] = (page_no-1)*10                  # Update pagination

    dict_list = []

    while True:
        try:
            api_req = client.get_dict()
        except SSLError:
            print('Max requests reached--sleeping for 5 min')
            time.sleep(300)
        else:
            print('Enough sleeping!')
            break

    while 'error' not in api_req: # Get results as long as more pages exist
        dict_list.append(api_req)
        page_no += 10
        client.params_dict["start"] = (page_no-1)*10
        while True:
            try:
                api_req = client.get_dict()
            except SSLError:
                print('Max requests reached--sleeping for 5 min')
                time.sleep(300)
            else:
                print('Enough sleeping!')
                break

    return dict_list


def parse_serpapi_results(d_list):
    """
    Script for parsing results returned from do_serpapi().
    :param d_list: list of dictionaries returned by do_serpapi().
    :return: list of URLs with meta information (title, publish date)
    """
    meta = []
    for d in d_list:
        if 'error' in d:
            print(d['error'])
        elif d['search_metadata']['status'] == 'Success':
            res = d['organic_results']
            page_no = d['search_information']['page_number'] if 'page_number' in d['search_information'] else 1
            print('Number of results on page {}: {}'.format(page_no,len(res)))
            meta.extend([(x['title'],x['link'],x['date']) if 'date' in x
                        else (x['title'],x['link']) for x in res])
        else:
            print("API get failure")
    return meta


def get_serp_urls(l_domains,r_domains):
    """
    """
    if not os.path.exists('./serp_api'):
        os.mkdir('./serp_api')

    # Query each domain for each keyword
    for DOMAIN in l_domains + r_domains:
        for KW in CC_KEYWORDS:
            dl = do_serpapi(DOMAIN,KW)
            results = parse_serpapi_results(dl)
            pickle.dump(results,open(os.path.join('serp_api','{}_{}.pkl'.format(DOMAIN,KW)),'wb'))


def merge_serp_urls():
    """
    Generates `google_search_res_covid19_vaccine_<current date>.pkl`, a dictionary with outer keys for domains and inner keys for search terms,
    where <current date> records the date of the API call.
    """
    # Initialize default nested dict with outer keys for each media domain and inner keys for each keyword.
    URLS_PER_DOMAIN = defaultdict(dict)

    # Merge serp API results into a single nested dict.
    for filename in glob.glob('serp_api/*.pkl'):
        res = pickle.load(open(filename,'rb'))
        domain_kw = filename.split('/')[-1][:-4]
        domain,kw = domain_kw.split('_')[0],domain_kw.split('_')[1]
        URLS_PER_DOMAIN[domain][kw] = res

    # Save nested dict
    curr_date = datetime.date.today()
    str_curr_date = curr_date.strftime("%m_%d_%Y")
    save_name = 'google_search_res_covid19_vaccine_{}.pkl'.format(str_curr_date)
    print('Saving search results to {}...'.format(save_name))
    pickle.dump(URLS_PER_DOMAIN,open(save_name,'wb'))
    print('Done!')


def get_mc_urls(start_year=2020,start_mo=1,start_day=1,end_year=2021,end_mo=5,end_day=1):
    """
    Generates `mediacloud_df.pkl`, a dataframe w/ output from MediaCloud.
    :param int start_year: Year to begin collecting stories.
    :param int start_mo: Month to begin collecting stories.
    :param int start_day: Day to begin collecting stories.
    :param int end_year: Year to end story collection.
    :param int end_mo: Month to end story collection.
    :param int end_day: Day to end story collection.
    """

    print("debug 1")
    if not os.path.exists('./mediacloud'):
        os.mkdir('./mediacloud')

    date_range_str = '{}_{}_{}_to_{}_{}_{}'.format(start_year,start_mo,start_day,end_year,end_mo,end_day)
    print ("date range:" + date_range_str)
    if not os.path.exists(os.path.join('mediacloud',date_range_str)):
        os.mkdir(os.path.join('mediacloud',date_range_str))
        for curr_outlet_ix in mc_ids.index:
            curr_outlet_id = mc_ids.iloc[curr_outlet_ix]['media_id']
            print(mc_ids.iloc[curr_outlet_ix])
            curr_outlet_stance = mc_ids.iloc[curr_outlet_ix]['leaning']
            fetch_size = 5000
            stories = []
            last_processed_stories_id = 0
            print("start year = ", start_year, "end year = ", end_year)
            for start_year in range(start_year,end_year,5): # Start collecting stories from Jan. 1, 2020 by default
                print("start year = ", start_year)
                while len(stories) < 10000:
                    print("Going to get stories")
                   #This is the modified original paper code that did not work:
                    #fetched_stories = mc.storyList('(covid-19 AND vaccin*) OR (coronavirus AND vaccine) OR (vaccine AND pandemic) OR (vaccine AND side-effect*) AND media_id:{}'.format(curr_outlet_id),
                                                   #solr_filter=mc.publish_date_query(datetime.date(start_year,start_mo,start_day), datetime.date(start_year+4,end_mo,end_day)),
                                                   #last_processed_stories_id=last_processed_stories_id, rows= fetch_size)
                    #This is my modified code that works:
                    fetched_stories = mc.storyList('(covid-19 AND vaccine) OR (coronavirus AND vaccine) OR (vaccine AND side-effects) AND media_id:{}'.format(curr_outlet_id),
                        solr_filter=mc.publish_date_query(datetime.date(start_year, start_mo, start_day),datetime.date(start_year + 4, end_mo, end_day)),
                        last_processed_stories_id=last_processed_stories_id, rows=fetch_size)

                    #stories.extend(fetched_stories)
                    print("I got these stories", (len(fetched_stories)))
                    stories.extend(fetched_stories)
                    if len(fetched_stories) < fetch_size:
                        break
                    last_processed_stories_id = stories[-1]['processed_stories_id']
            if len(stories) > 0:
                df = pd.DataFrame({key: [s[key] for s in stories] for key in mc_metadata})
                df['topic'] = ['cc']*len(df)
                df['stance'] = curr_outlet_stance
                df.sort_values(by='publish_date')

                OUTLET_NAME = df['media_name'].iloc[0].lower().replace(' ','_')
                df.to_pickle(os.path.join('mediacloud',date_range_str,'{}_df.pkl'.format(OUTLET_NAME)))
                print('Done fetching stories from {} (outlet id = {}).'.format(OUTLET_NAME,curr_outlet_id))

        # Merge into a single df; filter out stories not in English; clean titles.
        dfs = []
        for filename in glob.glob('mediacloud/{}/*.pkl'.format(date_range_str)):
            df = pd.read_pickle(filename)
            dfs.append(df)
        if len(dfs) > 0:
            df_all = pd.concat(dfs,ignore_index=True)
            df_all = df_all[df_all.language == 'en']
            df_all['clean_title'] = df_all.title.apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x.lower()))
            df_all.to_pickle('output/mediacloud_df_{}.pkl'.format(date_range_str))
        else:
            print('No MediaCloud stories found in selected date range.')
        shutil.rmtree(os.path.join('mediacloud',date_range_str))


def create_filtered_df(l_domains=None,r_domains=None,mc_date_range_str=None):
    """Creates intermediate df for collected URLs, applying filtering, regularization, and deduplication."""

    BLACKLIST_URL_INIT_STRS = set(['rss.','feeds.','rssfeeds.'])
    def is_rss(url):
        """Determine if URL is from an RSS feed."""
        for xx in BLACKLIST_URL_INIT_STRS:
            if url[:len(xx)] == xx:
                return True
        return False

    with open('blacklist_url_tags.txt','r') as f:
        TAGS_TO_REMOVE = f.read().splitlines()

    def is_blacklist(url):
        """Helper function to determine if URL should be filtered out"""
        for xx in TAGS_TO_REMOVE:
            if xx in url:
                return True
        return False

    def is_pdf(url):
        return url[-4:] == '.pdf'

    from urllib.parse import urlparse
    def get_hostname(url, uri_type='both'):
        """Get the host name from the url"""
        parsed_uri = urlparse(url)
        if uri_type == 'both':
            return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        elif uri_type == 'netloc_only':
            return '{uri.netloc}'.format(uri=parsed_uri)

    def strip_url(url):
        """Strip leading 'http(s)://(www.) from URL'"""
        if url.startswith('http'):
            url = re.sub(r'https?://', '', url)
        if url.startswith('www.'):
            url = re.sub(r'www.', '', url)
        return url

    def standardize_domain(x):
        if x == 'Guardian US':
            return 'guardian_us'
        elif 'washingtonpost.com' in x:
            return 'wapo'
        elif 'vox.com' in x:
            return 'vox'
        elif 'breitbart.com' in x:
            return 'breitbart'
        elif 'nytimes.com' in x:
            return 'nyt'
        elif 'motherjones.com' in x:
            return 'mj'
        elif x == 'democracy_now':
            return 'dem_now'
        elif 'foxnews.com' in x:
            return 'fox'
        elif 'buzzfeednews.com' in x or 'www.buzzfeed' in x:
            return 'buzzfeed'
        elif 'https://childrenshealthdefense.org/' in x:
            return 'chd'
        elif x == 'Daily Caller' or 'www.dailycaller' in x:
            return 'daily_caller'
        elif 'www.dailysignal' in x:
            return 'daily_signal'
        elif x == 'Washington Post':
            return 'wapo'
        elif 'theblaze.com' in x or x == 'the_blaze':
            return 'blaze'
        elif 'democracynow.org' in x:
            return 'dem_now'
        elif x == 'Grist':
            return 'grist'
        elif x == 'New York Times':
            return 'nyt'
        elif 'nationalreview.com' in x:
            return 'nat_review'
        elif 'thenation.com' in x:
            return 'nation'
        elif x == 'Breitbart':
            return 'breitbart'
        elif x == 'Christian Science Monitor':
            return 'cs_monitor'
        elif 'https://www.csmonitor/' in x:
            return 'cs_monitor'
        elif x == 'buzzfeed_news':
            return 'buzzfeed'
        elif x == 'washington_post':
            return 'wapo'
        elif x == 'FOX News':
            return 'fox'
        elif x == 'USA Today':
            return 'usa_today'
        elif x == 'Mother Jones':
            return 'mj'
        elif x == 'NBC News' or 'nbcnews.com' in x:
            return 'nbc'
        elif x == 'Democracy Now!':
            return 'dem_now'
        elif x == 'National Review':
            return 'nat_review'
        elif x == 'CNS News':
            return 'cns'
        elif x == 'Buzzfeed':
            return 'buzzfeed'
        elif x == 'The Nation':
            return 'nation'
        elif 'pjmedia.com' in x:
            return 'pj'
        elif 'pajamas_media' in x:
            return 'pj'
        elif x == 'pj' or x == 'pjmedia':
            return 'pj'
        elif 'www.americanthinker' in x:
            return 'american_thinker'
        elif 'www.redstate' in x:
            return 'redstate'
        elif 'www.infowars' in x:
            return 'infowars'
        elif 'www.wnd' in x:
            return 'wnd'
        elif 'www.nysun' in x:
            return 'new_york_sun'
        elif 'www.cnsnews' in x:
            return 'cns'
        elif 'www.realclearpolitics' in x:
            return 'real_clear_politics'
        elif 'www.newsmax' in x:
            return 'newsmax'
        elif 'www.newsbusters.org' in x:
            return 'newsbusters'
        elif 'www.unionleader' in x:
            return 'unionleader'
        elif 'www.townhall' in x:
            return 'townhall'
        elif 'www.hotair' in x:
            return 'hot_air'
        elif 'www.wsj' in x:
            return 'wsj'
        else:
            return x.lower().strip().replace(' ', '_').replace('.com', '')

    def standardize_date(x):
        if x is not None:
            if type(x) == str:
                x = x.replace('·','').strip()
                try:
                    return parser.parse(x)
                except ValueError:
                    return None
            elif type(x) == datetime.datetime:
                return x
            else:
                return x.to_pydatetime()

    # Create a dataframe combining all data structures with urls, that filters according to above criteria.
    filtered_urls = []
    filtered_titles = []
    filtered_dates = []
    filtered_domains = []
    filtered_stances = []
    filtered_topics = []
    filtered_is_AP = []

    if args.do_serp:
        google_pkl = glob.glob("google_search_res_covid19_vaccin_*")
        for g_pkl in google_pkl:
            google_cc_urls = pickle.load(open(g_pkl,'rb'))

            for key in google_cc_urls:
                for keyword in google_cc_urls[key]:
                    for item in google_cc_urls[key][keyword]:
                        url = strip_url(item[1])
                        if not is_rss(url) and not is_blacklist(url) and not is_pdf(url):
                            title = item[0]
                            date = item[2] if len(item) > 2 else None
                            stance = 'pro' if key in l_domains else 'anti'
                            topic = 'cc'
                            is_AP = None

                            if ' | ' not in title:
                                filtered_urls.append(url)
                                filtered_titles.append(title)
                                filtered_dates.append(date)
                                filtered_domains.append(key)
                                filtered_stances.append(stance)
                                filtered_topics.append(topic)
                                filtered_is_AP.append(is_AP)

    if args.do_mediacloud and os.path.exists('output/mediacloud_df_{}.pkl'.format(mc_date_range_str)):
        mediacloud_cc_urls = pd.read_pickle('output/mediacloud_df_{}.pkl'.format(mc_date_range_str))

        for ix in mediacloud_cc_urls.index:
            row = mediacloud_cc_urls.loc[ix]
            url = strip_url(row['url']) if 'http' in row['url'] else strip_url(row['guid'])
            if not is_rss(url) and not is_blacklist(url):
                title = row['clean_title']
                date = row['publish_date']
                domain = row['media_name']
                stance = row['stance']
                topic = row['topic']
                is_AP = row['ap_syndicated']

                if ' | ' not in title:
                    filtered_urls.append(url)
                    filtered_titles.append(title)
                    filtered_dates.append(date)
                    filtered_domains.append(domain)
                    filtered_stances.append(stance)
                    filtered_topics.append(topic)
                    filtered_is_AP.append(is_AP)

    combined_df = pd.DataFrame({'url':filtered_urls,
                              'title':filtered_titles,
                              'date':filtered_dates,
                              'domain':filtered_domains,
                              'stance':filtered_stances,
                              'topic':filtered_topics,
                              'is_AP':filtered_is_AP})

    combined_df['domain'] = combined_df.domain.apply(standardize_domain)
    combined_df.title = combined_df.title.apply(lambda x: x.strip().lower() if x
                                           is not None else x)
    stance_reg_dict = {'l':'pro','r':'anti','c':'between','pro':'pro','anti':'anti','between':'between'}
    combined_df = combined_df.loc[~pd.isnull(combined_df.stance)]
    combined_df['stance'] = combined_df.stance.apply(lambda x: stance_reg_dict[x])
    combined_df['date'] = combined_df['date'].apply(standardize_date)

    # We sort combined_df by title and date so that when we drop duplicate URLs,
    # we keep the one that doesn't have a null value for these fields.
    combined_df = combined_df.sort_values(['title'],axis=0)
    combined_df = combined_df.drop_duplicates(subset='url',keep='first')
    print('Intermediate df shape:',combined_df.shape)
    print('Saving intermediate df to "output/temp_combined_df_{}.pkl"...'.format(mc_date_range_str))
    combined_df.to_pickle('output/temp_combined_df_{}.pkl'.format(mc_date_range_str))


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--google_domains', type=str, default=None,
                      help='/path/to/txt/file/with/domains')
    arg_parser.add_argument('--do_serp', action="store_true", help='whether to run SerpAPI URL retrieval')
    arg_parser.add_argument('--do_mediacloud', action="store_true", help='whether to run MediaCloud URL retrieval')
    arg_parser.add_argument('--mediacloud_start_year', type=int, default=2000, help='Start year threshold for stories')
    arg_parser.add_argument('--mediacloud_start_month', type=int, default=1, help='Start month threshold for stories')
    arg_parser.add_argument('--mediacloud_start_day', type=int, default=1, help='Start day threshold for stories')
    arg_parser.add_argument('--mediacloud_end_year', type=int, default=2020, help='End year threshold for stories')
    arg_parser.add_argument('--mediacloud_end_month', type=int, default=12, help='End month threshold for stories')
    arg_parser.add_argument('--mediacloud_end_day', type=int, default=31, help='End day threshold for stories')
    args = arg_parser.parse_args()

    L_DOMAINS,R_DOMAINS = None,None

    print('Getting URLs...')
    if not os.path.exists('output'):
        os.mkdir('output')
    if args.do_serp:
        # Set up SerpAPI
        from serpapi import GoogleSearch

        if os.path.exists('./SERP_API_KEY.txt'):
            with open('SERP_API_KEY.txt','r') as f:
                SERP_API_KEY = f.read().strip()

        query_params = {"location":"United States", "device":"desktop", "hl":"en", "gl":"us", "serp_api_key":SERP_API_KEY}
        CC_KEYWORDS = ['covid_vaccine']#,'coronavirus_vaccine']#,'vaccine_safe','vaccine_side-effects','vaccination']
        client = GoogleSearch(query_params)

        # Read in list of domains and political leanings for SerpAPI
        print("Reading in political leanings of domains for SerpAPI...")
        fname = "google_domains.txt" if args.google_domains is None else args.google_domains

        L_DOMAINS,R_DOMAINS = [],[]
        with open(fname,'r') as f:
            lines = f.read().splitlines()
            for line in lines[1:]:
                split_line = line.split('\t')
                R_DOMAINS.append(split_line[0]) if split_line[1] == 'R' else L_DOMAINS.append(split_line[0])

        print('L_DOMAINS:',L_DOMAINS)
        print('R_DOMAINS:',R_DOMAINS)

        get_serp_urls(L_DOMAINS,R_DOMAINS)
        merge_serp_urls()

    mc_date_range_str = ''
    if args.do_mediacloud:

        # Set up MediaCloud API
        import mediacloud.api

        if os.path.exists('./MC_API_KEY.txt'):
            with open('MC_API_KEY.txt','r') as f:
                MC_API_KEY = f.read().strip()

        mc = mediacloud.api.MediaCloud(MC_API_KEY)
        mc_metadata = ['ap_syndicated','language','media_id','media_name','publish_date','title','guid','url','word_count']
        mc_ids = pd.read_csv('./mediacloud_ids.txt',sep='\t',header=0)
        mc_ids.reset_index(drop=True, inplace=True)
        print(mc_ids)

        mc_date_range_str = '{}_{}_{}_to_{}_{}_{}'.format(args.mediacloud_start_year,args.mediacloud_start_month,
        args.mediacloud_start_day,args.mediacloud_end_year,args.mediacloud_end_month,args.mediacloud_end_day)
        print('Fetching stories from {}/{}/{} to {}/{}/{} from MediaCloud...'.format(args.mediacloud_start_year,args.mediacloud_start_month,
        args.mediacloud_start_day,args.mediacloud_end_year,args.mediacloud_end_month,args.mediacloud_end_day))
        get_mc_urls(start_year=args.mediacloud_start_year,start_mo=args.mediacloud_start_month,start_day=args.mediacloud_start_day,
        end_year=args.mediacloud_end_year,end_mo=args.mediacloud_end_month,end_day=args.mediacloud_end_day)
    print('Done retrieving URLs!')

    print('Creating intermediate dataframe...')
    create_filtered_df(set(L_DOMAINS),set(R_DOMAINS),mc_date_range_str) if L_DOMAINS is not None and R_DOMAINS is not None else create_filtered_df(mc_date_range_str=mc_date_range_str)
