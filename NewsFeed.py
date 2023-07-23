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

