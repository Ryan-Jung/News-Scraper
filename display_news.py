import news_scraper
import wx
import webbrowser
#Define GUI
class NewsWindow(wx.Frame):


	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size=(600,300))

		self.data = self.loadData()

		self.mainsizer = wx.BoxSizer(wx.VERTICAL)

		#Handles article display
		self.updateListBox()

		#Add widgets to be displayed
		self.refresh_button = wx.Button(self, label ="Refresh")
		self.mainsizer.AddStretchSpacer()
		self.mainsizer.Add(self.refresh_button, flag=wx.RIGHT)
		self.mainsizer.Add(self.listbox)
		self.view_button = wx.Button(self, label = "View")
		self.mainsizer.AddStretchSpacer()
		self.mainsizer.Add(self.view_button, flag=wx.CENTER)
		self.mainsizer.AddStretchSpacer()	
		
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
		if data:
			return data
		else:
			return None

	def onClick(self, event):
		"""Opens default browser to display URL of the user's selected article
		"""
		index = self.currentSelection
		urls = self.data["urls"]
		webbrowser.open(urls[index], 0, autoraise=True)

	def saveCurrentSelection(self, listbox_event):
		"""Keeps track of the user's selection
		"""
		self.currentSelection = listbox_event.GetSelection()
	
	def onRefresh(self,event):
		self.data = self.loadData()
		self.updateListBox()

		

	def updateListBox(self):
		self.listbox = wx.ListBox(self)
		self.data = self.loadData()
		if self.data:
			self.listbox.Set(self.data["articles"])
		else:
			self.listBox.Set(["No Articles to display"])	

		self.listbox.SetMinSize(self.GetSize())

	
	


       
app = wx.App(False)
frame = NewsWindow(None, "SfGate Latest News")
app.MainLoop()
