
import argparse
from crawler import crawl_page
from scraper import Post

def scrape():
    # the endpoint for the posts lookup
    ENDPOINT = "https://www.facebook.com/"

    # Setting up the arg parser to parse argument when the script called 
    parser = argparse.ArgumentParser(prog="FACEBOOK COLLECTOR",description='Collect facebook posts related to a specific subject.')
    parser.add_argument("-s","--subject",default="le décès du président Jacques Chirac") # for subject selection 
    
    args = parser.parse_args()
    print(f"Starting Crawling Process for topic = {args.subject}")
    url = f"{ENDPOINT}/search/posts/?q={args.subject}"

    page_source = crawl_page(url) 

    return page_source



if __name__ == "__main__":

    page_source = scrape()

    posts = Post.scrape_posts(page_source)
    print("Extracing and Saving data to DB ...", (posts))
    for post in posts:
        post.serialize() # serialize the object
        post.save_json() # save to the database DB

    print("Finished Successfully !")

