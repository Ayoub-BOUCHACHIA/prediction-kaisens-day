from bs4 import BeautifulSoup
import dateparser
from utils import convert_str_to_number
import pandas as pd


class Post(object):
    """
    Post class (model) that handles process, extracting and saving post data
    """
    COLLECTION_NAME = "posts" # the name of the collection where the data will be stored
    all_data =  {
        "publisher" : [],
        "text"      : [],
        "media"     : [],
        "publishDate":[],
        "shares"    : [],
        "comments"  : [],
        "reactions" : [],
    }
    def __init__(self,document):
        self.document = document
        self.data = {}
       
        
    @staticmethod
    def scrape_posts(document):
        """
        scrape all the posts from the document and return Post objects
        this is a static method bcz it contains generic class behavior and it's not linked to the object instances.
        """
        soup = BeautifulSoup(document,features="lxml")
        publications = soup.find_all("div",{"class":'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'})
        return map(lambda x: Post(x),publications)

    def get_publisher(self):
        anchor = self.document.find("h3", {"class":"x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz x1gslohp x1yc453h"})
        
        if not anchor:
            return None
        
        span = anchor.find("span", {"class":"x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x6prxxf xvq8zen xo1l8bm xi81zsa"}) or anchor.find("span", {"class":"xt0psk2"})        
        
        if span:
            list_a = span.find_all('a')
            publishers = []
            for a in list_a:
                href = a['href']
                publisherName =  a.find("span").get_text() 
                publishers.append({"publisherName":publisherName, "publisherAccount":href})
            
            return publishers
            
        return None

    def get_post_text(self):
        div = self.document.find("div", {"dir":"auto", "style" : "text-align: start;"})
        return div.get_text() if div else None


    def get_media(self):
        div_images = self.document.find_all("div", {"class" : "x6ikm8r x10wlt62 x10l6tqk"})
        imgs = []
        for div_img in div_images:
            img = div_img.find('img')
            src = img['src']
            imgs.append(src)

        return imgs

        
    def get_reactions(self):
        reactions = self.document.find("span", {"class" : "xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk"})
        if reactions:
            try:
                reactions_count = convert_str_to_number(reactions.get_text().replace(",","."))
                return reactions_count
            except:
                return None
            
            
    def get_comments(self):
        comments = self.document.find("span", {"class" : "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xi81zsa"})
        if comments:
            comments_str = comments.get_text()
            try:
                comments_count = convert_str_to_number(comments_str.replace(",","."))
                return comments_count
            except:
                return None
    
    def get_shares(self):

        spans = self.document.find_all('span', {"class" : "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xi81zsa"})
        span = None

        if len(spans) == 2:
            span = spans[1]
        elif len(spans) == 1:
            if 'partage' in spans[0]:
                span = spans[0]

        if span:
            shares_str = span.get_text().replace("partages", "").replace("s","").replace(" ","").replace(",",".")
            try:
                shares_count = convert_str_to_number(shares_str)
                return shares_count
            except:
                return None
            
        return None

    def get_publish_date(self):
        abbr = self.document.find("span",{"class":"x1rg5ohu x6ikm8r x10wlt62 x16dsc37 xt0b8zv"})
        date = None
        if abbr:
            text_date = abbr.get_text()
            date = dateparser.parse(text_date)
        return date


    def serialize(self):
        """
        extract and return a json like format of the post data
        """
        self.data = {
            "publisher" : self.get_publisher(),
            "text"      : self.get_post_text(),
            "media"     : self.get_media(),
            "publishDate":self.get_publish_date(),
            "shares"    : self.get_shares(),
            "comments"  : self.get_comments(),
            "reactions" : self.get_reactions()
        }
        return self.data
    
    def __str__(self) -> str:
        return "\n" + Post.COLLECTION_NAME + " --> "+ str(self.data) + "\n"

    def save_json(self):
        Post.all_data['publisher'].append(self.data['publisher'])
        Post.all_data['text'].append(self.data['text'])
        Post.all_data['media'].append(self.data['media'])
        Post.all_data['publishDate'].append(self.data['publishDate'])
        Post.all_data['shares'].append(self.data['shares'])
        Post.all_data['comments'].append(self.data['comments'])
        Post.all_data['reactions'].append(self.data['reactions'])
        df = pd.DataFrame(Post.all_data)         
        df.to_json('/data/data.json',index=False)
