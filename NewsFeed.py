from datetime import datetime

class User:
    def __init__(self, userId, username, password):
        self.userId = userId
        self.username = username
        self.password = password
        self.following = set()

class Session:
    def __init__(self, sessionId, userId):
        self.sessionId = sessionId
        self.userId = userId
        self.createdOn = datetime.now()

class FeedItem:
    def __init__(self, feedId, userId, text):
        self.feedId = feedId
        self.userId = userId
        self.feedText = text
        self.postTime = datetime.now()
        self.upvotes = 0
        self.downvotes = 0
        self.comments = []

class Comment:
    def __init__(self, commentId, userId, text):
        self.commentId = commentId
        self.userId = userId
        self.commentText = text
        self.commentTime = datetime.now()
        self.upvotes = 0
        self.downvotes = 0
        self.replies = []

class Feed:
    def __init__(self):
        self.feed_items = []

class NewsFeedManagement:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.feed = Feed()

    def signup(self, userId, username, password):
        if userId not in self.users:
            self.users[userId] = User(userId, username, password)
            return True
        return False

    def login(self, userId):
        if userId in self.users:
            sessionId = "session_{userId}"
            self.sessions[sessionId] = Session(sessionId, userId)
            return sessionId
        return None

    def post(self, sessionId, text):
        if sessionId in self.sessions:
            userId = self.sessions[sessionId].userId
            feed_item = FeedItem(feedId, userId, text)
            self.feed.feed_items.append(feed_item)
            return feedId
        return None

    def follow(self, sessionId, userId):
        if sessionId in self.sessions and userId in self.users:
            follower_id = self.sessions[sessionId].userId
            self.users[follower_id].following.add(userId)
            return True
        return False

    def upvote(self, sessionId, item_id, is_feed_item=True):
        if sessionId in self.sessions:
            userId = self.sessions[sessionId].userId
            target_list = self.feed.feed_items if is_feed_item else self._get_all_comments()
            for item in target_list:
                if item.feedId == item_id:
                    item.upvotes += 1
                    return True
        return False

    def downvote(self, sessionId, item_id, is_feed_item=True):
        if sessionId in self.sessions:
            userId = self.sessions[sessionId].userId
            feeds = self.feed.feed_items if is_feed_item else self._get_all_comments()
            for item in feeds:
                if item.feedId == item_id:
                    item.downvotes += 1
                    return True
        return False

    def comment(self, sessionId, feedId, text):
        if sessionId in self.sessions:
            userId = self.sessions[sessionId].userId
            for feed_item in self.feed.feed_items:
                if feed_item.feedId == feedId:
                    commentId = "comment_{userId}_{feedId}"
                    comment = Comment(commentId, userId, text)
                    feed_item.comments.append(comment)
                    return commentId
        return None

    def shownewsfeed(self, sessionId):
        if sessionId in self.sessions:
            userId = self.sessions[sessionId].userId
            followed_users = self.users[userId].following
            sorted_feed_items = sorted(self.feed.feed_items, key=lambda item: (
                item.userId in followed_users, 
                item.upvotes - item.downvotes, 
                len(item.comments), 
                item.post_time), 
                reverse=True
            )
            return sorted_feed_items
        return []

    def _get_all_comments(self):
        all_comments = []
        for feed_item in self.feed.feed_items:
            all_comments.extend(feed_item.comments)
            self._add_nested_comments(feed_item.comments, all_comments)
        return all_comments

    def _add_nested_comments(self, comments, all_comments):
        for comment in comments:
            all_comments.extend(comment.replies)
            self._add_nested_comments(comment.replies, all_comments)


if __name__ == "__main__":
    NFMObject = NewsFeedManagement()
    sessionId = None
    # Signin
    if NFMObject.signup("1", "Amar", "Password1"):
        sessionId = NFMObject.login("1")

        # Post
        feedId = NFMObject.post(sessionId, "This is a sample feed item.")

    # Follow
    if NFMObject.signup("2", "Kumar", "password2"):
        NFMObject.follow(sessionId, "2")

    # Post comment
    NFMObject.login("2")
    commentId = NFMObject.comment(sessionId, feedId, "Temp comment")

    # Upvote a feed item and a comment
    NFMObject.login("1")
    NFMObject.upvote(sessionId, feedId)
    NFMObject.upvote(sessionId, commentId, is_feed_item=False)

    # Print feed
    feed_items = NFMObject.shownewsfeed(sessionId)
    for item in feed_items:
        print(item.text)
