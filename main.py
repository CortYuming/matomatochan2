#!/usr/bin/env python
# *-# -*- coding: utf-8 -*-

import os

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import cgi
import datetime

import advertising
import site_data


NUM_OF_FETCH = 320 #high limit 500
PAGESIZE = 20

SITE_TITLE = "mato-mato-chan2 [2ch速報まとめのまとめ] まとまとちゃん２"
SITE_DESCRIPTION = "2ちゃんねる速報まとめサイトのそのまたまとめ"
SITE_KEYWORDS_CONTENT = "2ch,2ちゃんねる,まとめ,まとめのまとめ,速報,最新ニュース"
SITE_INFO_MAIL = "matomatochan2dev@gmail.com"


class Feed(db.Model):
  site_name = db.StringProperty()
  link = db.URLProperty()
  title = db.StringProperty()
  updated_parsed = db.DateTimeProperty()


def conv_struct_to_datetime(struct_time):
    return datetime.datetime(*struct_time[:6])

def get_strftime(time):
    return datetime.strftime("%Y-%m-%d %H:%M",struct_time)

def parse_feed(feed_url):
  import feedparser
  from google.appengine.api import urlfetch

  result = urlfetch.fetch(feed_url)
  if result.status_code == 200:
    d = feedparser.parse(result.content)
  else:
    raise Exception("Can not retyieve given URL.")
  if d.bozo == 1:
    raise Exception("Can not parse givin URL.")
  return d

def is_even(num):
  return False if num % 2 else True

def get_single_figure(num):
  return num % 10


class Crawl(webapp.RequestHandler):
  def get(self):
    fetch_get_num = NUM_OF_FETCH * 2

    query = Feed.all().order("-updated_parsed").fetch(fetch_get_num)
    check_query_title_arr = [q.title for q in query]

    self.crawl(check_query_title_arr)
    self.response.out.write("This is cron job on GAE - dev.")

  def crawl(self, check_query_title_arr, crawl_days_to_date=3):
    FEED_URL_SEQ = site_data.feed_url_arr
    feed_list = []

    now_time = datetime.datetime.now()
    now_minute = now_time.minute
    crawl_day = now_time - datetime.timedelta(days = crawl_days_to_date)

    # cron 取得時間を必ず奇数に設定する
    # 巡回フィードリストを半々づつ読み込む（現在時刻（分）一桁が奇数偶数で分ける）
    len_feed_url = len(FEED_URL_SEQ)
    separate_p = len_feed_url / 2
    if is_even(get_single_figure(now_minute)):
      partial_feed_url_seq = FEED_URL_SEQ[:separate_p]
    else:
      partial_feed_url_seq = FEED_URL_SEQ[separate_p:]

    for feed_url in partial_feed_url_seq:
      try:
        d = parse_feed(feed_url)

        tmp_site_name = d.feed.title
        for entry  in d.entries:
          updated_parsed_time = conv_struct_to_datetime(entry.updated_parsed)
          if not entry.title in check_query_title_arr:
            if crawl_day < updated_parsed_time:
              feed = Feed(
                site_name = tmp_site_name,
                link = entry.link,
                title = entry.title,
                updated_parsed = updated_parsed_time\
                + datetime.timedelta(hours=9) #日本時間only
                )

              feed_list.append(feed)
      except:
        pass
    db.put(feed_list)

    delete_old_data()


class ViewRSS(webapp.RequestHandler):
  def get(self):
    from django.utils import feedgenerator
    query = Feed.all().order("-updated_parsed").fetch(PAGESIZE)
    feed = feedgenerator.Rss201rev2Feed(
      title = "mato-mato-chan2",
      link = "http://matomatochan2.appspot.com/",
      description = SITE_DESCRIPTION,
      language = u"ja")

    for article in query:
      feed.add_item(
        title = article.title,
        link = article.link,
        description = "",
        )

    rss = feed.writeString("utf-8")

    self.response.out.write(rss)


class ViewFeed(webapp.RequestHandler):
  def get(self, current_page_arg=""):
    SITE_LINK_SEQ = site_data.site_link_arr

    query = Feed.all().order("-updated_parsed").fetch(NUM_OF_FETCH)
    check_query_title_arr = [q.title for q in query]
    len_all_query = len(query)

    if len_all_query < 1:
      c = Crawl()
      c.crawl(check_query_title_arr, crawl_days_to_date = 14)

    if current_page_arg == "" or current_page_arg == "1":
      current_page_int = 1
    else:
      current_page_int = int(current_page_arg)

    if current_page_int:
      query = query[
        PAGESIZE * current_page_int - PAGESIZE:PAGESIZE * current_page_int
        ]
    else:
      query = query[:PAGESIZE]

    all_article_seq = []
    for article in query:
      all_article_seq.append(dict(
        link = cgi.escape(article.link),
        title = cgi.escape(article.title),
        updated_parsed = article.updated_parsed,
        site_name = article.site_name,
        ))

    pagination_seq = []
    page_max = len_all_query/PAGESIZE

    for number in range(1, page_max+1):
      if number == current_page_int:
        pagination_num_str = "<font>%d</font>" % number
      else:
        pagination_num_str = str(number)

      pagination_seq.append(dict(
        page = number,
        page_str = pagination_num_str
        ))

    next_page_int = current_page_int + 1
    if page_max < next_page_int:
      next_page_int = page_max

    if current_page_int == 1:
      title = SITE_TITLE
    else:
      title = "(%d) %s" % (current_page_int, SITE_TITLE)

    template_values = dict(
      title = title,
      description  = SITE_DESCRIPTION,
      keywords_content = SITE_KEYWORDS_CONTENT,
      info_mail = SITE_INFO_MAIL,
      contents = all_article_seq,
      site_link = SITE_LINK_SEQ,
      advertising = advertising.get_random(),
      next_page = str(next_page_int),
      pagination = pagination_seq,
      )
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))


def delete_old_data():
  # query = Feed.all().order("updated_parsed").fetch()
  query = Feed.all().order("updated_parsed").fetch(NUM_OF_FETCH *2)
  all_query_count = len(query)

#   if NUM_OF_FETCH <= all_query_count:
  if NUM_OF_FETCH < all_query_count:
    db.delete(query[:all_query_count - NUM_OF_FETCH])


#メンテ用
class ViewDeleteData(webapp.RequestHandler):
  def get(self, do_del_avg=""):
    if do_del_avg == "t":
      delete_old_data()
      self.response.out.write("deleted<br />")

    query = Feed.all().order("updated_parsed").fetch(NUM_OF_FETCH * 2)
    self.response.out.write(u"%d<br /><br />" % len(query))
    self.response.out.write("\n<br />".join(
      ["%s (%s) %s" % (d.title, d.updated_parsed, d.site_name) for d in query]))


class RedirectToHome(webapp.RequestHandler):
  def get(self):
    self.redirect("/")

def is_dev():
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


def main():
  application = webapp.WSGIApplication([
    ('/index.rdf', ViewRSS),
    ('/cron/crowl', Crawl),
    ('/(\d*)', ViewFeed),
#     ('/maintenance/delete/(\w)*', ViewDeleteData),
    ('/.*', RedirectToHome),
    ], debug = is_dev() and True)
  run_wsgi_app(application)


if __name__ == '__main__':
    main()

    """
    ver1_10_1
    todo debag 開発サーバか判定
    fix SITENAME_URL_FEED_DICT のサイト名のあたまに u を追加

    ver1_10_2
    add amazon アフェ 大型画像

    ver1_10_3
    fix css

    ver1_10_4
    fix url処理 (?next=) なしで数字飲みでいけるように

    ver1_10_5
    fix 変数名
    fix template

    ver1_11
    todo rss フィード
    todo 無料Google Adsence で サイトの宣伝

    ver1_12
    todo Link site のリスト順を固定（site_link_seq に sorted() 追加）
    fix Link site 定数にして関数の外に
    fix base.css
    add info e-mail
    fix info に 移動 「このサイトはリンクフリーです」

    ver1_12_1
    add robots.txt

    ver1_13_0
    fix put -> db.put (大量に put() してたのを一回で処理)

    ver1_13_1
    fix
    add POWERED by google app engine 画像

    ver1_13_3
    fix SITENAME_URL_FEED_DICT を SITENAME_URL_FEED_LIST に変更（単純化）

    ver1_13_4
    todo amアフェ広告ランダムに
    fix site data 別ファイルに移動
    fix advertising まわり
    fix データ削除の応急処置
    fix 設定していないアドレスをhomeにリダイレクト

    ver1_13_5
    fix template を分割
    fix template 分割しない仕様に戻した
    fix html

    ver1_13_6
    fix main.py ViewFeed の変数を解りやすく、余分なコード削除。

    ver1_13_7
    fix タイトル説明まわり main.py, index.html
    fix main.py 重複コードを削除。あと若干修正。

    ver1_13_8
    fix main.py の crawl feed まわり 古いfeed 取得しない仕様に変更（重複データ）

    ver1_13_9
    todo ViewDeleteData の 削除部分を分割して汎用defにする。
    todo cron の crawl で データが必要以上に増えてたら削除する
    fix crawl.get の 『NUM_OF_FETCH * 2』-> 『NUM_OF_FETCH』にしてテストして戻した

    ver1_14_1
    fix crawl 読み込み先 ランダムで半分読み込む
    fix cron.yaml (8 min)
    fix cron.yaml (13 min) 戻した
    fix delete_old_data

    ver1_14_2
    del リンク外した maintenance/delete/
    fix index.html description, keywords 変数に
    fix parse_feed の中でモジュール読み込み
    fix advertising.py 広告<a>タグまわり短く
    fix common.css leftside <a> タグ色変更
    fix リンク外す maintenance/delete

    ver1_14_3
    fix delete_old_data

    ver1_14_4
    fix crawl で cron処理を分一桁で偶数 奇数に分けて巡回フィードリストを半々づつ読込む
    fix 一部定数を使用している関数内に移動
    webで検索 SELECT * FROM Feed ORDER BY updated_parsed DESC

    ver1_14_4
    fix タイトルにページ数を表示

    TODO
    memcach 調べて必要なら実装
    task queue を使う
    アクセスアップをどうするか？
    汎用性を持たせクローンサイトを簡単に造れるようにする。
    設計見直す
    check 2010-10-08 08:45 /cron/crowl ERROR 2

    """
