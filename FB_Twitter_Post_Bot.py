import sys
from PyQt4 import QtGui, QtCore
import facebook
from imgurpython import ImgurClient
import pyimgur
import tweepy

global myTextData
global imageExists
imageExists = False 
myTextData = 'Hello'


######################### Facebook Credentials #################################
FacebookAppID = "Facebook APP ID Goes Here Goes Here"

ShortLivedUserToken = "Short Lived User Token Goes Here"

LongLivedUserToken = "Long Lived User Token Goes Here"

ShortPageAccessToken = "Short Page Access Token Goes Here"

LongPageAccessToken = "Long Page Access Toke Goes Here"

UserId = "User ID # Goes Here"
TestPageID = "Test Page ID Goes Here"

status = "Waiting..."

AppToken = "App Token Goes Here"
AppSecret = "App Secret Goes Here"

graph = facebook.GraphAPI(access_token=LongPageAccessToken)
################################################################################

############################ Imgur Credentials #################################
CLIENT_ID = 'Imgur Client ID Goes Here'
clientSecret = 'Imgur Client Secret Goes Here'

im = pyimgur.Imgur(CLIENT_ID)
client = ImgurClient(CLIENT_ID, clientSecret)

print("Number of credits left: %s" % client.credits["UserRemaining"])
################################################################################


############################ Twitter Credentials ###############################
TwitterConsumerAPIKey = "Twitter API Key Goes Here"
TwitterConsumerAPISecret = "Twitter API Secret Goes Here"
TwitterOwner = "Twitter Owner Name Goes Here"
TwitterOwnerID = "Twitter Owner ID Goes Here"
TwitterAccessToken = "Twitter Access Token Goes Here"
TwitterAccessTokenSecret = "Twitter Access Token Secret Goes Here"
TwitterAuth = tweepy.OAuthHandler(TwitterConsumerAPIKey, 
	TwitterConsumerAPISecret)
TwitterAuth.set_access_token(TwitterAccessToken, TwitterAccessTokenSecret)
TwitterAPI = tweepy.API(TwitterAuth)
################################################################################

def postTwitter(imageName="none"):
	if imageExists:
		TwitterAPI.update_with_media(filename=imageName, status=myTextData)
	else:
		TwitterAPI.update_status(status=myTextData)


def uploadImgur(imageName):
	print("Uploading image %s" % imageName)
	uploaded_image = im.upload_image(imageName, title=imageName)
	global imgurPhotoUrl
	imgurPhotoUrl = uploaded_image.link
	print("Image link is: %s" % imgurPhotoUrl)

def postComment(imageName="none"):
	if imageExists:
		print("Trying to upload a photo")
		uploadImgur(imageName)
		graph.put_object(parent_object=UserId + "_" + TestPageID,
			attachment_url=imgurPhotoUrl, connection_name='comments',
			message=myTextData)
	else:
		graph.put_object(parent_object=UserId + "_" + TestPageID,
			connection_name='comments', message=myTextData)

class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()

		self.setWindowTitle("Facebook & Twitter Bot")
		self.setGeometry(1500, 300, 700, 265)
		self.setWindowIcon(QtGui.QIcon('pepe.png'))

		self.textEdit = QtGui.QTextEdit(self)
		self.textEdit.move(5, 60)
		self.textEdit.resize(350, 200)

		self.home()

	def home(self):
		post_status_header = QtGui.QLabel("Post Status:", self).move(240,5)
		self.post_status = QtGui.QLabel("Waiting...", self)
		self.post_status.move(240,30)

		self.iconLabel = QtGui.QLabel(self)
		self.setImage("photoIcon.png")
		
		openBtn = QtGui.QPushButton("Open\n File", self)
		openBtn.clicked.connect(self.openImage)
		openBtn.resize(110,50)
		openBtn.move(120,5)

		btn = QtGui.QPushButton("Post Media", self)
		btn.clicked.connect(self.post)
		btn.resize(110,50)
		btn.move(5,5)
		
		self.show()

	def setImage(self, imageName):
		pixmap = QtGui.QPixmap(imageName)
		pixmap2 = pixmap.scaledToHeight(200)
		self.iconLabel.setPixmap(pixmap2)
		self.iconLabel.move(430, 10)
		self.iconLabel.resize(300,300)
		
	def openImage(self):
		self.imageName = QtGui.QFileDialog.getOpenFileName()
		self.setImage(self.imageName)
		global imageExists
		imageExists = True

	def getText(self):
		global myTextData
		myTextData = self.textEdit.toPlainText()

	def post(self):
		self.getText()
		if imageExists:
			postComment(self.imageName)
			postTwitter(self.imageName)
		else:
			postComment()
			postTwitter()
		self.post_status.setText("Complete!")

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	app.exec_()
run()
