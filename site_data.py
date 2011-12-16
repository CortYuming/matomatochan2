#!/usr/bin/env python
# *-# -*- coding: utf-8 -*-

site_dict_arr = [
  {"title":u"ろぼ速VIP","link":"http://dariusnews.blog11.fc2.com/","feed_url":"http://dariusnews.blog11.fc2.com/?xml"},
  # {"title":u"【2ch】ニュー速クオリティ","link":"http://news4vip.livedoor.biz/","feed_url":"http://news4vip.livedoor.biz/index.rdf"},
  {"title":u"ワラ速","link":"http://warasoku.blog18.fc2.com/","feed_url":"http://warasoku.blog18.fc2.com/?xml"},
  {"title":u"アルファルファモザイク","link":"http://alfalfalfa.com/","feed_url":"http://alfalfalfa.com/index.rdf"},
  {"title":u"まめ速","link":"http://mamesoku.com/","feed_url":"http://mamesoku.com/atom.xml"},
  # {"title":u"VIPワイドガイド","link":"http://news4wide.livedoor.biz/","feed_url":"http://news4wide.livedoor.biz/index.rdf"},
  {"title":u"もみあげチャ～シュ～","link":"http://michaelsan.livedoor.biz/","feed_url":"http://michaelsan.livedoor.biz/index.rdf"},
  {"title":u"VIPPERな俺","link":"http://blog.livedoor.jp/news23vip/","feed_url":"http://blog.livedoor.jp/news23vip/index.rdf"},
  # {"title":u"イミフｗｗｗうはｗｗｗｗおｋｗｗｗｗ","link":"http://imihu.blog30.fc2.com/","feed_url":"http://imihu.blog30.fc2.com/?xml"},
  {"title":u"おはようｗｗｗお前らｗｗｗｗｗｗｗｗ","link":"http://kaisun1192.blog121.fc2.com/","feed_url":"http://kaisun1192.blog121.fc2.com/?xml"},
  # {"title":u"スチーム速報　ＶＩＰ","link":"http://newsteam.livedoor.biz/","feed_url":"http://newsteam.livedoor.biz/index.rdf"},
  # {"title":u"ワラノート","link":"http://waranote.livedoor.biz/","feed_url":"http://waranote.livedoor.biz/index.rdf"},
  {"title":u"働くモノニュース : 人生VIP職人ブログwww","link":"http://workingnews.blog117.fc2.com/","feed_url":"http://workingnews.blog117.fc2.com/?xml"},
  # {"title":u"ニュー速VIPブログ(`･ω･´)","link":"http://blog.livedoor.jp/insidears/","feed_url":"http://blog.livedoor.jp/insidears/index.rdf"},
  {"title":u"ワロタニッキ","link":"http://blog.livedoor.jp/hisabisaniwarota/","feed_url":"http://blog.livedoor.jp/hisabisaniwarota/index.rdf"},
  {"title":u"無題のドキュメント","link":"http://mudainodqnment.ldblog.jp/","feed_url":"http://mudainodqnment.ldblog.jp/index.rdf"},
  {"title":u"ベア速","link":"http://vipvipblogblog.blog119.fc2.com/","feed_url":"http://vipvipblogblog.blog119.fc2.com/?xml"},
  {"title":u"痛いニュース(ﾉ∀`)","link":"http://blog.livedoor.jp/dqnplus/","feed_url":"http://blog.livedoor.jp/dqnplus/index.rdf"},
  {"title":u"ハムスター速報","link":"http://hamusoku.com/","feed_url":"http://hamusoku.com/index.rdf"},
  {"title":u"社会生活VIP","link":"http://minisoku.blog97.fc2.com/","feed_url":"http://minisoku.blog97.fc2.com/?xml"},
  {"title":u"ほんわか2ちゃんねる","link":"http://honwaka2ch.blog90.fc2.com/","feed_url":"http://honwaka2ch.blog90.fc2.com/?xml"},
  {"title":u"暇人＼(＾o＾)／速報","link":"http://blog.livedoor.jp/himasoku123/","feed_url":"http://blog.livedoor.jp/himasoku123/index.rdf"},
  {"title":u"妹はVIPPER", "link":"http://blog.livedoor.jp/vipsister23/", "feed_url":"http://blog.livedoor.jp/vipsister23/index.rdf"},
  {"title":u"にくろぐ。", "link":"http://nikuch.blog42.fc2.com/", "feed_url":"http://nikuch.blog42.fc2.com/?xml"},
  {"title":u"ライフハックちゃんねる弐式", "link":"http://lifehack2ch.livedoor.biz/", "feed_url":"http://lifehack2ch.livedoor.biz/index.rdf"},
  ]

def get_site_link(arr):
  return sorted([dict(
    site_link_name = d["title"],
    site_link_url = d["link"])
                 for d in arr
                 ])

def get_feed_url_arr(arr):
    return [d["feed_url"] for d in arr]

feed_url_arr = get_feed_url_arr(site_dict_arr)
site_link_arr = get_site_link(site_dict_arr)


# if __name__ == '__main__':
#   import urllib2
#   for d in site_dict_arr:
#     try:
#       html = urllib2.urlopen(d["feed_url"])
#       print html.info()
#     except:
#       print "error"
