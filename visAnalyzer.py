"""
The script containing the main gui for the visualizer. All other graphs will
be called from here.
"""
import wx
import wx.lib.newevent
import wx.lib.scrolledpanel as scp
import oglCanvas as oglC

# Plots
import parallelcoord as pc
import splom as spm
import lineplot as lp
import pieplot as pp
import histogramplot as hp
import scatterplot_2D as sc2
import gauge as gg
import osciloscopeplot as op

# For loading the db
import getdbDialog as dbD
import getStreamDialog as stD
import dataStreaming as dS
# Cursor
import dataIterator as dI

import random as r

class mainGUI(wx.Frame):
    """
    Handles the widgets for the gui.
    """
    def __init__(self, parent, title=""):
        super(mainGUI, self).__init__(parent, title=title)

        self.selectedDB = False
        self.streamSelected = False
        self.data = None
        self.labels = None
        self.category = None
        self.timer = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        # For the histogram and pieplot
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        # For the scatterplot (and another)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        #https://stackoverflow.com/questions/30797443/add-a-vertical-scrollbar-to-a-wxframe-accross-multiple-wxpanels
        # Create a scrolled panel
        self.panel = scp.ScrolledPanel(self, -1, style=wx.SIMPLE_BORDER, size=(400, 200))
        self.panel.SetupScrolling()
        self.panel.SetAutoLayout(1)
        self.panel.ShowScrollbars(horz=wx.SHOW_SB_DEFAULT, vert=wx.SHOW_SB_ALWAYS)
        self.panel.SetBackgroundColour((255, 255, 255))
        self.panel.SetScrollRate(20, 20)

        self.initGraphs()
        self.panel.SetSizer(self.mainSizer)

        self.initMenus()

    def initGraphs(self):
        """ Initialize the graphs to reserve area on client """
        self.pc = pc.PCWidget(self.panel)
        self.splom = spm.SPLOMWidget(self.panel)
        self.lp = lp.LinePlotWidget(self.panel)
        self.pp = pp.PPWidget(self.panel)
        self.hist = hp.HistogramWidget(self.panel)
        self.scp = sc2.ScatterplotWidget(self.panel)

        self.mainSizer.Add(self.pc, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        self.mainSizer.Add(self.splom, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        self.mainSizer.Add(self.lp, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)
        self.sizer1.Add(self.hist, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)
        self.sizer1.Add(self.pp, 0, wx.LEFT | wx.EXPAND | wx.ALL, 5)
        self.sizer2.Add(self.scp, 0, wx.LEFT | wx.SHAPED | wx.ALL, 5)
        self.mainSizer.Add(self.sizer1, 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.sizer2, 0, wx.ALIGN_CENTER)

        # Hide the graphs
        self.mainSizer.Show(self.pc, False)
        self.mainSizer.Show(self.splom, False)
        self.mainSizer.Show(self.lp, False)
        self.sizer1.Show(self.hist, False)
        self.sizer1.Show(self.pp, False)
        self.sizer2.Show(self.scp, False)
        self.mainSizer.Show(self.sizer1, False)
        self.mainSizer.Show(self.sizer1, False)

    def initMenus(self):
        """ Initialize the menus for the app """
        # Set up the menu bar
        menubar = wx.MenuBar()

        # For the file menu
        fileMenu = wx.Menu()
        self.registerMenuAction(fileMenu, wx.ID_EXIT, self.OnFile, "Exit\tCtrl+Q")
        menubar.Append(fileMenu, "File")

        # For loading files and db's menu
        loadDB = wx.Menu()
        self.registerMenuAction(loadDB, -1, self.OnDBSelected, "Select a database")
        self.registerMenuAction(loadDB, -1, self.OnLoadCSVFile, "Load a .csv file")
        self.registerMenuAction(loadDB, -1, self.onStreamSelected, "Recieve a stream of data")
        # Add to menu bar
        menubar.Append(loadDB, "Databases")

        # Select a graph
        selectGraph = wx.Menu()
        self.registerMenuAction(selectGraph, -1, self.OnPCSelected, "Parallel Coordinates")
        self.registerMenuAction(selectGraph, -1, self.OnSPLOMSelected, "SPLOM")
        self.registerMenuAction(selectGraph, -1, self.OnLPSelected, "Line plot")
        self.registerMenuAction(selectGraph, -1, self.OnPPSelected, "Pie plot")
        self.registerMenuAction(selectGraph, -1, self.OnHGSelected, "Histogram")
        self.registerMenuAction(selectGraph, -1, self.OnSCPSelected, "Scatterplot")
        self.registerMenuAction(selectGraph, -1, self.OnGPSelected, "Gauge")
        self.registerMenuAction(selectGraph, -1, self.OnOSCSelected, "Osciloscope")

        # Add to menu bar
        menubar.Append(selectGraph, "Graphs")

        # Append menu to frame
        self.SetMenuBar(menubar)

    def registerMenuAction(self, menu, id, handler, label=""):
        """ Add an item to the "menu" menu, and bind its event handler """
        item = wx.MenuItem(menu, id, label)
        menu.Append(item)
        self.Bind(wx.EVT_MENU, handler, item)

    def OnFile(self, event):
        """ For the file menu events """
        if event.Id == wx.ID_EXIT:
            if self.data:
                self.data.close()
            self.Close()
        else:
            # Let it propagate
            event.Skip()
    #--------------------------------------------------------------------------------------------------------------

    def OnDBSelected(self, event):
        """ Displays the available mysql databases and loads the selected one """
        if self.data:
            self.data.close()

        with dbD.GetDBDialog(self, "Connect to a database") as dlg:
            # Indicate the iterator to load a db
            self.data = dI.Data(0)
            # Get the data until a connection to the db is successfully established, or the user canceled
            while True:
                if dlg.ShowModal() == wx.ID_OK:
                    name, passw, db = dlg.getUserData()
                    result = self.data.loadDB(host="localhost", user=name, passwd=passw, dbName=db)
                    # If the connection was succesful
                    if result:
                        break
                else:
                    return
            self.labels, self.category = self.data.getDBDescription()
            self.selectedDB = True

    #--------------------------------------------------------------------------------------------------------------

    def OnLoadCSVFile(self, event):
        """ Loads a csv file """
        # The admitted files formats
        wildcard = "CSV files (*.csv)|*.csv"
        dlg = wx.FileDialog(self, "Open File", wildcard=wildcard, style=wx.FD_OPEN)
        # Show dialog, if the "ok" button is pressed, open the file
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if self.data:
                self.data.close()
            self.labels = []
            self.category = []
            self.data = dI.Data(1)
            self.data.loadCSV(path)
            self.labels, self.category = self.data.getDBDescription()
            self.selectedDB = True
        dlg.Destroy()

    #--------------------------------------------------------------------------------------------------------------

    def onStreamSelected(self, event):
        """ Recieve a data stream """
        # Connect
        dlg = stD.GetStreamDialog(self, title="Recieve stream")
        dlg.Show()
        self.labels = []
        self.category = []
        if self.data:
            self.data.close()
        self.data = dI.Data(2)
        self.data.connectToStream(('', 8080), 0)
        self.labels, self.category = self.data.getDBDescription()
        self.selectedDB = True
        self.streamSelected = True
        # Set timer for constant checking of new incoming values on the stream
        self.timer = wx.Timer(self, -1)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(1000)  # Check each second

    def OnTimer(self, event):
        """  """
        # Send an event for drawing
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))


    #--------------------------------------------------------------------------------------------------------------

    def fitLayout(self):
        """ Fit the layout of the window when a graph is added or deleted """
        w1,h1 = self.mainSizer.GetSize()
        w,h = self.mainSizer.GetMinSize()
        self.SetVirtualSize((w1, h))
        self.mainSizer.Layout()
        self.panel.Layout()
        # https://stackoverflow.com/questions/5912761/wxpython-scrolled-panel-not-updating-scroll-bars
        # The 'FitInside' function should be called from the panel, not the frame.
        self.panel.FitInside()
    
    def SelectedDB(self):
        """ Check if a database or csv file is selected. If not prompts the user. """
        if not self.selectedDB:
            wx.MessageBox("Select/load a database before proceeding", "No database selected")
            return False
        return True

    def GetSelectedAxis(self, selectionable, title="", text=""):
        """ Returns the index of the axis selected.
            -selectionable: List of selectionable axes.
            -title: Title of the dialog.
            -text: Text of the dialog.
        """
        axis = -1
        dlg = wx.SingleChoiceDialog(self, title, text, selectionable)
        if dlg.ShowModal() == wx.ID_OK:
            axisName = dlg.GetStringSelection()
            # Get the index
            for i in range(len(self.labels)):
                if self.labels[i] == axisName:
                    axis = i
        return axis


    def OnPCSelected(self, event):
        """ When the ||-coord is selected """
        if not self.SelectedDB():
            return
        if self.mainSizer.IsShown(self.pc):
            return

        # Create pc widget
        self.pc.create(self.data, self.labels)
        self.mainSizer.Show(self.pc, True)
        # Force layout update
        self.fitLayout()

    def OnSPLOMSelected(self, event):
        """ When the SPLOM is selected """
        if self.streamSelected:
            return
        if not self.SelectedDB():
            return
        if self.mainSizer.IsShown(self.splom):
            return

        self.splom.create(self.data, self.labels, self.category)
        self.mainSizer.Show(self.splom, True)
        # Force layout update
        self.fitLayout()

    def OnLPSelected(self, event):
        """ When the line plot is selected"""
        if self.streamSelected:
            return
        if not self.SelectedDB():
            return
        if self.mainSizer.IsShown(self.lp):
            return

        axis = self.GetSelectedAxis(self.labels, title="Axes", text="Select an axis")
        if axis > -1:
            self.lp.create(self.data, self.labels, axis)
            self.mainSizer.Show(self.lp, True)
            # Force layout update
            self.fitLayout()

    def OnGPSelected(self, event):
        """ When the Gauge is selected """
        pass

    def OnPPSelected(self, event):
        """ When the pieplot is selected """
        if not self.SelectedDB():
            return

        # Request the axis to draw
        axis = self.GetSelectedAxis(self.labels, title="Axes", text="Select an axis")
        if axis > -1:
            if not self.mainSizer.IsShown(self.sizer1):
                self.mainSizer.Show(self.sizer1, True)
            self.pp.create(self.data, self.labels, axis)
            self.sizer1.Show(self.pp, True)
            # Force layout update
            self.fitLayout()

    def OnOSCSelected(self, event):
        """ When the osciloscope is selected """
        pass

    def getSelectionableAxes(self):
        """ Returns a list of all the axes suitable for the histogram """
        selectionable = []
        for i in range(len(self.category)):
            # 0 -> Numerical variables
            if self.category[i] == 0:
                selectionable.append(self.labels[i])
        return selectionable

    def OnHGSelected(self, event):
        """ When the histogram is selected """
        # Verify that a database is selected
        if not self.SelectedDB():
            return

        # Get the selectionable axes
        selectionable = self.getSelectionableAxes()
        axis = self.GetSelectedAxis(selectionable, title="Axes suitable for histogram", text="Select an axis")
        if axis > -1:
            if not self.mainSizer.IsShown(self.sizer1):
                self.mainSizer.Show(self.sizer1, True, recursive=False)
            # Set it to the histogram
            self.hist.create(self.data, axis, self.labels[axis])
            self.sizer1.Show(self.hist, True)
            # Force layout update
            self.fitLayout()

    def OnSCPSelected(self, event):
        """ When the scatterplot is selected """
        if not self.SelectedDB():
            return
        #if self.mainSizer.IsShown(self.sizer2):
        if self.sizer2.IsShown(self.scp):
            return

        # Let the user select only the numerical variables
        choices = []
        for i in range(len(self.labels)):
            if self.category[i] == 0:
                choices.append(self.labels[i])

        dlg = wx.MultiChoiceDialog(self, "Pick two axes", "Select the axes to display", choices)
        options = 1
        while options != 2:
            if dlg.ShowModal() == wx.ID_OK:
                selections = dlg.GetSelections()
                if len(selections) != 2:
                    wx.MessageBox("Select only two axes", "")
                    continue
                else:
                    axis1 = choices[selections[0]]
                    axis2 = choices[selections[1]]
                    index1 = index2 = 0
                    for i in range(len(self.labels)):
                        if axis1 == self.labels[i]:
                            index1 = i
                        if axis2 == self.labels[i]:
                            index2 = i
                    if not self.mainSizer.IsShown(self.sizer2):
                        self.mainSizer.Show(self.sizer2, True)
                    self.scp.create(self.data, self.labels, self.category, index1, index2)
                    self.sizer2.Show(self.scp, True)
                    # Force layout update
                    self.fitLayout()
                    break
            else: # When cancel is pressed
                break

    def __del__(self):
        """ Destructor """
        if self.data:
            self.data.close()

#---------------------------------------------------------------------------------------------

class visAnalyzer(wx.App):
    def OnInit(self):
        self.frame = mainGUI(None, title="Visual Analyzer")
        self.frame.Fit()
        self.frame.Show()
        # Maximize
        self.frame.Maximize(True)
        return True

#---------------------------------------------------------------------------------------------

# "Main" function
if __name__ == '__main__':
    app = visAnalyzer(False)
    app.MainLoop()
