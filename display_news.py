import news_scraper
import wx
import webbrowser
import time
#Define GUI
class NewsWindow(wx.Frame):

	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size=(600,300))

		self.data = self.loadData()
		self.currentUserSelection = 0
		self.mainsizer = wx.BoxSizer(wx.VERTICAL)
		self.listbox = None
		
		self.refresh_button = wx.Button(self, label ="Refresh")
		self.view_button = wx.Button(self, label = "View")
		
		self.statusBar = self.CreateStatusBar()
		self.statusBar.SetStatusText("Waiting for your selection...")
		
		#Handles article display
		self.updateListBox()

		#Add widgets to be displayed
		self.mainsizer.AddStretchSpacer()
		self.mainsizer.Add(self.refresh_button)
		self.mainsizer.Add(self.listbox)
		self.mainsizer.AddStretchSpacer()
		self.mainsizer.Add(self.view_button, flag=wx.CENTER)

		#Event handling
		self.Bind(wx.EVT_LISTBOX, self.saveCurrentSelection)
		self.Bind(wx.EVT_BUTTON, self.onClick, self.view_button)
		self.Bind(wx.EVT_BUTTON, self.onRefresh, self.refresh_button)


		self.SetSizerAndFit(self.mainsizer)
		self.Center()

		self.Show(True)

		
	def loadData(self):
		"""Returns the scraped data from sfgate
		"""
		data = news_scraper.ScrapeNews().data
		if not data:
			data = None
		
		return data

			
	def onClick(self, event):
		"""Opens default browser to display URL of the user's selected article
		updates status bar to inform user of decision
		"""
		if self.data is not None:
			index = self.currentUserSelection
			urls = self.data["urls"]
			articles = self.data["articles"]
			self.statusBar.SetStatusText("Opening: " + articles[index] + " ...")
			webbrowser.open(urls[index], 0, autoraise=True)
			#Give time for browser to open
			time.sleep(5)
			self.statusBar.SetStatusText("Finished opening: " + articles[index])

			
	def saveCurrentSelection(self, listbox_event):
		"""Keeps track of the user's selection 
		"""
		self.currentUserSelection = listbox_event.GetSelection()

	
	def onRefresh(self,event):
		"""Displays the current news articles available on www.sfgate.com
		"""
		self.statusBar.SetStatusText("Gathering latest articles...")
		self.data = self.loadData()
		self.updateListBox()
		self.statusBar.SetStatusText("Finished!")
		#self.SetSizerAndFit(self.mainsizer)

		
	def updateListBox(self):
		"""Creates listbox that holds all the articles and allows user interaction with 
		items in the listbox. 
		"""
		if self.listbox is None:
			self.listbox = wx.ListBox(self)
			self.listbox.SetMinSize(self.GetSize())

		if self.data is not None:
			self.listbox.Set(self.data["articles"])
		else:
			self.statusBar.SetStatusText("No articles to display")

       
if __name__ == "__main__":	   
	app = wx.App(False)
	frame = NewsWindow(None, "SfGate Latest News")
	app.MainLoop()
