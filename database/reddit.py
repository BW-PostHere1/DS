import praw
from database.queries import insert_post

reddit = praw.Reddit(client_id="8iZ0AOfNFEvXVw",
                     client_secret="-swryLd22biXYc2sxrE7p2c3En4",
                     username="notFatality",
                     password="myipadpassword1",
                     user_agent='u/notFatality')


def get_data(n_subs=1, n_posts=1):
    """
    n_subs - how many reddits to check
    n_posts - how many posts to grab per sub
    """
    for i in range(n_subs):
        sub = reddit.random_subreddit()
        hot = sub.hot(limit=n_posts)
        for post in hot:
            text = f"{post.title} {post.selftext}".replace("'", "")
            which_sub = str(post.subreddit)[:20]
            sub_id = str(post.subreddit_id)[:15]  # i think this length is wrong might be 15?
            num_comments = post.num_comments
            upvotes = post.ups
            downvotes = post.downs
            flair = str(post.link_flair_text)[:20]
            has_vid = post.is_video
            num_awards = post.total_awards_received
            insert_post(text, which_sub, sub_id,
                        num_comments, upvotes, downvotes,
                        flair, has_vid, num_awards)
            print('uploaded')
        print('Finished sub')
    return


if __name__ == "__main__":
    get_data()
