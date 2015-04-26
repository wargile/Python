# twitterstream.py

# Assignment 1, problem 1
# https://class.coursera.org/datasci-002/assignment/view?assignment_id=3

# TIPS: https://class.coursera.org/datasci-002/forum/thread?thread_id=156
# Twitter field spec: https://dev.twitter.com/docs/platform-objects/tweets

# LinkedIn page for class:
# http://www.linkedin.com/groups/University-Washington-Introduction-Data-Science-6724362?home=&trk=anet_ug_hm&gid=6724362

# App created: Terje_CourseraDataScience
# python twitterstream.py > output.txt -Encoding UTF8
# head -n 20 output.txt > problem_1_submission.txt

import oauth2 as oauth
import urllib2 as urllib

# See assignment1.html instructions or README for how to get these credentials

api_key = "hBuoyPq722GLoNpqcGyfdsIRb"
api_secret = "TuHjNnWfdUtBSrbErFJb1JkUXIwEDjPByoahTcLJ8lCVI2clmQ"
access_token_key = "2599813796-cv0nhAmZ1170iHMUNUdN6fOcb13q4Q649Wlk9xi"
access_token_secret = "mMmrynulIXH7QkUJK8AC8IbOa0eCVaYIlX47pB2Co21ZN"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print line.strip()

if __name__ == '__main__':
  fetchsamples()
