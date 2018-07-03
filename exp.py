def __init__(self, parent, title=""):
        super(mainGUI, self).__init__(parent, title=title)

        self.selectedDB = False
        self.streamSelected = False
        self.data = None
        self.labels = None
        self.category = None
        self.description = None
        self.units = None
        self.timer = None
        self.infBar = None
        self.Sizer = wx.GridBagSizer()#rows=1, cols=2, vgap=1, hgap=1)
        # self.Sizer.SetFlexibleDirection(wx.BOTH)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        #https://stackoverflow.com/questions/30797443/add-a-vertical-scrollbar-to-a-wxframe-accross-multiple-wxpanels
        # Create a scrolled panel
        self.panel = scp.ScrolledPanel(self, -1, style=wx.SIMPLE_BORDER,)
        self.panel.SetupScrolling()
        self.panel.SetAutoLayout(1)
        self.panel.ShowScrollbars(horz=wx.SHOW_SB_DEFAULT, vert=wx.SHOW_SB_ALWAYS)
        self.panel.SetBackgroundColour((255, 255, 255))
        self.panel.SetScrollRate(20, 20)

        self.panel2 = wx.Panel(self, -1)
        self.infBar = infoBar.InfoBar(self)

        self.initGraphs()
        self.Sizer.Add(self.infBar, wx.GBPosition(0, 0), wx.DefaultSpan, flag=wx.ALIGN_LEFT)
        self.panel.SetSizer(self.mainSizer)
        self.Sizer.Add(self.panel, wx.GBPosition(0, 1), span=wx.DefaultSpan, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.panel2.SetSizer(self.Sizer)

        self.initMenus()


self.Sizer = wx.FlexGridSizer(rows=1, cols=2, vgap=0, hgap=0)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        #https://stackoverflow.com/questions/30797443/add-a-vertical-scrollbar-to-a-wxframe-accross-multiple-wxpanels
        # Create a scrolled panel
        self.panel = scp.ScrolledPanel(self, -1, style=wx.SIMPLE_BORDER)
        self.panel.SetupScrolling()
        self.panel.SetAutoLayout(1)
        self.panel.ShowScrollbars(horz=wx.SHOW_SB_DEFAULT, vert=wx.SHOW_SB_ALWAYS)
        self.panel.SetBackgroundColour((255, 255, 255))
        self.panel.SetScrollRate(20, 20)

        self.panel2 = wx.Panel(self, -1)
        self.infBar = infoBar.InfoBar(self)

        self.initGraphs()
        self.Sizer.Add(self.infBar, 0, wx.ALIGN_LEFT)
        self.panel.SetSizer(self.mainSizer)
        self.Sizer.Add(self.panel, 1, wx.EXPAND | wx.ALIGN_RIGHT)
        self.panel2.SetSizer(self.Sizer)

        self.initMenus()
