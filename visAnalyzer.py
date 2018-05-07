"""
The script containing the main gui for the visualizer. All other graphs will
be called from here.
"""
import wx
import wx.lib.newevent
import wx.lib.scrolledpanel as scp
import oglCanvas as oglC

# Plots
import scatterplot_2D as sc2
import histogramplot as hp
import osciloscopeplot as op
import pieplot as pp
import gauge as gg
import lineplot as lp
import parallelcoord as pc
import splom as spm

import random as r

class mainGUI(wx.Frame):
    """
    Handles the widgets for the gui.
    """
    def __init__(self, parent, title=""):
        super(mainGUI, self).__init__(parent, title=title)

        self.selectedDB = False
        self.data = None
        self.labels = None
        self.category = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #https://stackoverflow.com/questions/30797443/add-a-vertical-scrollbar-to-a-wxframe-accross-multiple-wxpanels
        # Create a scrolled panel
        self.panel = scp.ScrolledPanel(self, -1, style=wx.SIMPLE_BORDER, size=(400, 200))
        self.panel.SetupScrolling()
        self.panel.SetBackgroundColour((255, 255, 255))
        self.panel.SetSizer(self.mainSizer)

        self.initMenus()

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
        # Add to menu bar
        menubar.Append(loadDB, "Databases")

        # Select a graph
        selectGraph = wx.Menu()
        self.registerMenuAction(selectGraph, -1, self.OnPCSelected, "Parallel Coordinates")
        self.registerMenuAction(selectGraph, -1, self.OnSPLOMSelected, "SPLOM")
        self.registerMenuAction(selectGraph, -1, self.OnLPSelected, "Line plot")
        self.registerMenuAction(selectGraph, -1, self.OnGPSelected, "Gauge")
        self.registerMenuAction(selectGraph, -1, self.OnPPSelected, "Pie plot")
        self.registerMenuAction(selectGraph, -1, self.OnOSCSelected, "Osciloscope")
        self.registerMenuAction(selectGraph, -1, self.OnHGSelected, "Histogram")
        self.registerMenuAction(selectGraph, -1, self.OnSCPSelected, "Scatterplot")
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
            self.Close()
        else:
            # Let it propagate
            event.Skip()

    def OnDBSelected(self, event):
        """ Displays the available mysql databases and loads the selected one """
        pass

    def OnLoadCSVFile(self, event):
        """ Loads a csv file """
        # The admitted files formats
        wildcard = "CSV files (*.csv)|*.csv"
        dlg = wx.FileDialog(self, "Open File", wildcard=wildcard, style=wx.FD_OPEN)
        # Show dialog, if the "ok" button is pressed, open the file
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.data = []
            self.labels = []
            self.category = []
            LabelsandCategoryLoaded = 0
            with open(path, "r") as dataFile:
                for line in dataFile:
                    row = line.split(",")
                    # Load category
                    if LabelsandCategoryLoaded == 0:
                        self.labels = row.copy()
                        LabelsandCategoryLoaded = 1
                        continue
                    if LabelsandCategoryLoaded == 1:
                        # Copy as integer
                        for r in row:
                            self.category.append(int(r))
                        LabelsandCategoryLoaded = 2
                        continue
                    incomplete = False
                    nRow = []
                    for r in row:
                        if r != '?':
                            nRow.append(float(r))
                        else:
                            incomplete = True
                            break
                    if not incomplete:
                        self.data.append(nRow)
            self.selectedDB = True
        dlg.Destroy()

    def getSelectionableAxes(self):
        """ Returns a list of all the axes suitable for the histogram """
        selectionable = []
        for i in range(len(self.category)):
            # 0 -> Numerical variables
            if self.category[i] == 0:
                selectionable.append(self.labels[i])
        return selectionable
    
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
        # Create pc widget
        self.pc = pc.PCWidget(self.panel, self.data, self.labels)
        self.mainSizer.Add(self.pc, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        # Force layout update
        self.mainSizer.Layout()
        self.panel.Layout()
        self.Fit()

    def OnSPLOMSelected(self, event):
        """ When the SPLOM is selected """
        pass

    def OnLPSelected(self, event):
        """ When the line plot is selected"""
        pass

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
            self.pp = pp.PPWidget(self.panel, self.data, self.labels, axis)
            self.mainSizer.Add(self.pp, 0, wx.SHAPED | wx.ALIGN_CENTER | wx.ALL, 5)
            # Force layout update
            self.mainSizer.Layout()
            self.panel.Layout()
            self.Fit()

    def OnOSCSelected(self, event):
        """ When the osciloscope is selected """
        pass

    def OnHGSelected(self, event):
        """ When the histogram is selected """
        # Verify that a database is selected
        if not self.SelectedDB():
            return
        # Get the selectionable axes
        selectionable = self.getSelectionableAxes()
        axis = self.GetSelectedAxis(selectionable, title="Axes suitable for histogram", text="Select an axis")
        if axis > -1:
            # Set it to the histogram
            self.hist = hp.HistogramWidget(self.panel, self.data, axis)
            self.mainSizer.Add(self.hist, 0, wx.LEFT | wx.SHAPED | wx.ALL, 5)
            # Force layout update
            self.mainSizer.Layout()
            self.panel.Layout()
            self.Fit()

    def OnSCPSelected(self, event):
        """ When the scatterplot is selected """
        pass

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
