from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='417d347326df453f9007fa5d2a8091ab')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='Hong Kong',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

print(top_headlines)



