"""
Module for an infoBar. This bar will be located on the left side of the window, and will
display information about the data, such as type, units, and values.
"""

import wx

class InfoBar(wx.Panel):
    """
    For the infobar.
    """
    def __init__(self, parent):
        super(InfoBar, self).__init__(parent, style=wx.SUNKEN_BORDER)

        self.dbName = ''
        # Pane for the information
        self.variables = wx.CollapsiblePane(self)
        self.graphs = wx.CollapsiblePane(self)

        self.lvVariables = wx.ListView(self)
        self.lvGraphs = wx.ListView(self)

        self.lvVariables.InsertColumn(0, "Name")
        self.lvVariables.InsertColumn(1, "Type/Description")

        self.lvGraphs.InsertColumn(0, " ")
        self.lvGraphs.InsertColumn(1, " ")
        self.lvGraphs.InsertColumn(2, " ")
        self.SetBackgroundColour((255, 255, 255))

        self.groupCtrls()

    def groupCtrls(self):
        """ """
        name = wx.StaticText(self, -1, self.dbName)
        varDescr = wx.StaticText(self, -1, "Variables description.")
        graphs = wx.StaticText(self, -1, " ")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(name, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.Add(varDescr, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.Add(self.lvVariables, 4, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        self.sizer.Add(graphs, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.Add(self.lvGraphs, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)

        self.SetSizer(self.sizer)

    def create(self, labels, category, description, units):
        """ Inserts the name of the variable along with their description. """
        name = ''
        cat = ''
        n = len(labels)
        j, k = 0, 0
        for i in range(n):
            if category[i] == 0:
                name = labels[i] + ' (' + units[i] + ')'
                cat = 'Numerical'
            else:
                name = labels[i]
                cat = 'Categorical'
            
            pos = self.lvVariables.InsertItem(k, name)
            self.lvVariables.SetItem(pos, 1, cat)
            if category[i] == 1:
                j = k + 1
                descr = [d[i] for d in description]
                for c in descr:
                    if c == '':
                        break
                    pos = self.lvVariables.InsertItem(j, ' ')
                    self.lvVariables.SetItem(pos, 1, c)
                    j += 1
                del descr
            k = j + 1
        self.lvVariables.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.lvVariables.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)

    def setNDBame(self, name):
        """ Sets the name of the variable. """
        assert type(name) is str

        self.dbName = name

    # def AddGraph(self, )