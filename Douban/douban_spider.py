#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
A simple python spider to gather top 100 movies from Douban

Author: Zeng Ming
Version: 0.0.1
Date: 2015-01-04
Language: Python2.7
"""
__author__ = 'mizeng'

import re
import requests


class DoubanSpider(object):
    """This class is to get top 100 movies' name and link

    :param page_num: The web page number which will be gathered
    :param cur_url: The current url which will be gathered
    :param movie_names: The movie names after process
    :param _top_num: The current movie number


    """

    def __init__(self):
        self.page_num = 1
        self.cur_url = "http://movie.douban.com/top250?start={0}&filter=&type="
        self._top_num = 1
        self.movie_names = []
        print "Preparation finished, Start to spider data..."

    def get_page(self, cur_page_num):
        """Spider HTML according to current page, one page have 25 items

        :param cur_page_num: Current page
        :return: Current page's HTML
        """

        url = self.cur_url.format(cur_page_num)
        return requests.get(url).content

    def find_title(self, cur_page):
        """Matching top 100 movie names according to the whole page html

        :param cur_page: The HTML context wait for Regular Expression Process
        """
        # pattern is like <span class="title">这个杀手不太冷</span>
        #                 <span class="title">&nbsp;/&nbsp;Léon</span>
        # one movie may have a alias such as "Leon"
        titles = []
        links = []
        entrys = []
        pattern_grid_view = re.compile(r'<ol class="grid_view">(.|\n)+</ol>')
        match_grid = pattern_grid_view.search(cur_page)
        li_contents = match_grid.group().split(r'<li>')
        li_contents.pop(0)
        for content in li_contents:
            link = re.findall(r'<a href="(.*)" class="">', content)[0]
            title = re.findall(r'<span class="title">(.*)</span>',
                               content)[0]
            titles.append(title)
            links.append(link)
        for i in range(0, len(titles)):
            number = str(self._top_num) \
                if self._top_num > 9 else "0"+str(self._top_num)
            entry = "Top{0} : {1} ({2})".format(number, titles[i], links[i])
            entrys.append(entry)
            self._top_num += 1
        self.movie_names.extend(entrys)

    def start_spider(self):
        """Spider entrance

        """

        while self.page_num <= 4:
            cur_page = self.get_page(self._top_num - 1)
            self.find_title(cur_page)
            self.page_num += 1

        for item in self.movie_names:
            print item

        print "Spider process complete!"

if __name__ == '__main__':
    my_spider = DoubanSpider()
    my_spider.start_spider()