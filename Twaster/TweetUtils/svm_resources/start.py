import os

def startTweets():
    os.system("SET HTTPS_PROXY=194.138.0.6:9400")
    os.system("python tweets.py")
    # os.system("start /wait cmd /c python tweets.py")