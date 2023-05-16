import praw
import os
import schedule
import time
import random
import functools
from response_generation import generate_response

def comment_exists_under_post(post):
    username = os.environ["reddit_username"]

    for comment in post.comments:
        if comment.author == username:
            return True
    
    return False

def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

@catch_exceptions()
def reply_to_post(r):
    subreddit_names = ["cats"]
    subreddit_name = random.choice(subreddit_names)
    subreddit = r.subreddit(subreddit_name)

    for post in subreddit.new(limit=1):
        if not comment_exists_under_post(post):
            post_content = post.title + ' ' + post.selftext
            response = generate_response(subreddit_name, post_content)

            if response is not None:
                if response[0] == "\"":
                    index = response[1:].index("\"")

                    if index == len(response) - 2:
                        response = response[1:-1]

                if (response[0].isalpha() or response[0] == '\"') and response[-1] in ['.', '!', '?', '\"']:
                    comment = post.reply(response)
                    print("Posted comment:", comment.permalink)
        else:
            print("Comment already exists under post")
        
def run():
    reddit = praw.Reddit(
        client_id=os.environ["reddit_client_id"],
        client_secret=os.environ["reddit_client_secret"],
        username=os.environ["reddit_username"],
        password=os.environ["reddit_password"],
        user_agent=os.environ["reddit_user_agent"],
    )

    print("Starting...")

    schedule.every(5).hours.do(reply_to_post, r=reddit)

    while True:
        schedule.run_pending()
        time.sleep(1)