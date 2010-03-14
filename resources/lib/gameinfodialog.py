
import os, sys
import xbmc, xbmcgui
import dbupdate, importsettings
from gamedatabase import *


ACTION_EXIT_SCRIPT = ( 10, )
ACTION_CANCEL_DIALOG = ACTION_EXIT_SCRIPT + ( 9, )
ACTION_MOVEMENT_LEFT = ( 1, )
ACTION_MOVEMENT_RIGHT = ( 2, )
ACTION_MOVEMENT_UP = ( 3, )
ACTION_MOVEMENT_DOWN = ( 4, )
ACTION_MOVEMENT = ( 1, 2, 3, 4, )

CONTROL_LABEL_MSG = 4000

CONTROL_LABEL_GAME = 6000
CONTROL_LABEL_GENRE = 6100
CONTROL_LABEL_YEAR = 6200
CONTROL_LABEL_PUBLISHER = 6300
CONTROL_LABEL_DEVELOPER = 6400
CONTROL_LABEL_REGION = 6500
CONTROL_LABEL_MEDIA = 6600
CONTROL_LABEL_CONTROLLER = 6700
CONTROL_LABEL_RATING = 6800
CONTROL_LABEL_VOTES = 6900
CONTROL_LABEL_PLAYERS = 7000
CONTROL_LABEL_PERSPECTIVE = 7100
CONTROL_LABEL_REVIEWER = 7200
CONTROL_LABEL_URL = 7300
CONTROL_LABEL_LAUNCHCOUNT = 7400

CONTROL_GAME_LIST = 1000
CONTROL_IMG_BACK = 10000
CONTROL_IMG_CARTRIDGE = 8000
CONTROL_LABEL_DESC = 8100
CONTROL_IMG_INGAMEVIDEO = 9000

RCBHOME = os.getcwd()


class UIGameInfoView(xbmcgui.WindowXMLDialog):
	def __init__(self, *args, **kwargs):		
		xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )		
		
		self.gdb = kwargs[ "gdb" ]
		self.selectedGameId = kwargs[ "gameId" ]
		self.selectedConsoleId = kwargs[ "consoleId" ]
		self.selectedGenreId = kwargs[ "genreId" ]		
		self.selectedYearId = kwargs[ "yearId" ]		
		self.selectedPublisherId = kwargs[ "publisherId" ]		
		
		self.doModal()
		
		
	def onInit(self):
		self.showGameList()
		self.showGameInfo()
		self.setFocus(self.getControl(CONTROL_GAME_LIST))
		self.selectedControlId = CONTROL_GAME_LIST
		
		
		
	def onClick( self, controlId ):
		return		

	def onFocus( self, controlId ):
		self.selectedControlId = controlId

	def onAction( self, action ):		
		if(action.getId() in ACTION_CANCEL_DIALOG):
			self.close()
		elif(action.getId() in ACTION_MOVEMENT_LEFT or action.getId() in ACTION_MOVEMENT_RIGHT):
			if(self.selectedControlId == CONTROL_GAME_LIST):
				selectedGame = self.getControl(CONTROL_GAME_LIST).getSelectedItem()
		
				if(selectedGame == None):
					return
			
				self.selectedGameId = selectedGame.getLabel2()
				self.showGameInfo()
	
	
	def showGameList(self):
		games = Game(self.gdb).getFilteredGames(self.selectedConsoleId, self.selectedGenreId, self.selectedYearId, self.selectedPublisherId)
		
		self.getControl(CONTROL_GAME_LIST).setVisible(1)
		self.getControl(CONTROL_GAME_LIST).reset()
		
		self.writeMsg("loading games...")
		
		items = []
		for game in games:			
			coverFile = File(self.gdb).getCoverByGameId(game[0])
			items.append(xbmcgui.ListItem(str(game[1]), str(game[0]), coverFile, ''))
				
		self.getControl(CONTROL_GAME_LIST).addItems(items)
		self.writeMsg("")
	
		
	def showGameInfo(self):			
		gameRow = Game(self.gdb).getObjectById(self.selectedGameId)
		if(gameRow == None):
			self.writeMsg('Selected game could not be read from database.')
			return
		
		genreString = ""
		genres = Genre(self.gdb).getGenresByGameId(gameRow[0])
		if (genres != None):
			for i in range(0, len(genres)):
				genre = genres[i]
				genreString += genre[1]
				if(i < len(genres) -1):
					genreString += ", "
				
		year = self.getItemName(Year(self.gdb), gameRow[9])
		publisher = self.getItemName(Publisher(self.gdb), gameRow[6])
		developer = self.getItemName(Developer(self.gdb), gameRow[7])
		reviewer = self.getItemName(Reviewer(self.gdb), gameRow[8])
		
		#self.setLabel(CONTROL_LABEL_GAME, gameRow[1])
		self.setLabel(CONTROL_LABEL_GENRE, genreString)
		self.setLabel(CONTROL_LABEL_YEAR, year)
		self.setLabel(CONTROL_LABEL_PUBLISHER, publisher)
		self.setLabel(CONTROL_LABEL_DEVELOPER, developer)
		self.setLabel(CONTROL_LABEL_REGION, gameRow[14])
		self.setLabel(CONTROL_LABEL_MEDIA, gameRow[15])
		self.setLabel(CONTROL_LABEL_CONTROLLER, gameRow[17])
		self.setLabel(CONTROL_LABEL_RATING, gameRow[11])
		self.setLabel(CONTROL_LABEL_VOTES, gameRow[12])
		self.setLabel(CONTROL_LABEL_PLAYERS, gameRow[10])
		self.setLabel(CONTROL_LABEL_PERSPECTIVE, gameRow[16])
		self.setLabel(CONTROL_LABEL_REVIEWER, reviewer)
		self.setLabel(CONTROL_LABEL_URL, gameRow[13])			
		
		self.setLabel(CONTROL_LABEL_LAUNCHCOUNT, gameRow[19])
		
		description = gameRow[2]
		if(description == None):
			description = ""		
		self.getControl(CONTROL_LABEL_DESC).setText(description)
		
		#TODO more than one?
		titleScreenshots = File(self.gdb).getTitleScreenshotsByGameId(self.selectedGameId)		
		if(titleScreenshots != None and len(titleScreenshots) != 0):
			titleScreenshot = titleScreenshots[0]			
			self.getControl(CONTROL_IMG_BACK).setImage(titleScreenshot[0])
		else:
			#TODO setVisible?
			background = os.path.join(RCBHOME, 'resources', 'skins', 'Default', 'media', 'background.png')			
			self.getControl(CONTROL_IMG_BACK).setImage(background)
			
		cartridges = File(self.gdb).getCartridgesByGameId(self.selectedGameId)
		if(cartridges != None and len(cartridges) != 0):
			cartridge = cartridges[0]
			self.getControl(CONTROL_IMG_CARTRIDGE).setImage(cartridge[0])
			self.getControl(CONTROL_IMG_CARTRIDGE).setVisible(1)
		else:
			self.getControl(CONTROL_IMG_CARTRIDGE).setVisible(0)
			
		ingameVideos = File(self.gdb).getIngameVideosByGameId(self.selectedGameId)
		if(ingameVideos != None and len(ingameVideos) != 0):
			ingameVideo = ingameVideos[0]			
			
			""" TODO Play Video embedded
			playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			listitem = xbmcgui.ListItem( gameRow[0], thumbnailImage=titleScreenshot[0] )
			listitem.setInfo( "video", { "Title": gameRow[0]} )
			playlist.add( ingameVideo[0], listitem )
			xbmc.Player().play( playlist )
			"""
		
		
	def getItemName(self, object, itemId):
		itemRow = object.getObjectById(itemId)
		if(itemRow == None):
			return ""
		else:
			return itemRow[1]
			
	
	def setLabel(self, controlId, value):
		if(value == None):
			value = ""		
		self.getControl(controlId).setLabel(str(value))
	
		
		
	def writeMsg(self, msg):
		print "writeMsg: " +msg
		self.getControl(CONTROL_LABEL_MSG).setLabel(msg)
		