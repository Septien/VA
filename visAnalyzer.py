"""
The script containing the main gui for the visualizer. All other graphs will
be called from here.
"""
import wx
import wx.lib.newevent
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

# Create custom events for the graphs
# Parallel coordinates
PCEvent, EVT_PC_EVENT = wx.lib.newevent.NewEvent()
PCCommandEvent, EVT_PC_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
# Scatterplot matrix
SPLOMEvent, EVT_SPLOM_EVENT = wx.lib.newevent.NewEvent()
SPLOMCommandEvent, EVT_SPLOM_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
# Lineplot
LPvent, EVT_LP_EVENT = wx.lib.newevent.NewEvent()
LPCommandEvent, EVT_LP_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
# Gauge
GPEvent, EVT_GP_EVENT = wx.lib.newevent.NewEvent()
GPCommandEvent, EVT_GP_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
# Pieplot
PPEvent, EVT_PP_EVENT = wx.lib.newevent.NewEvent()
PPCommandEvent, EVT_PP_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
# Osciloscope
OSCEvent, EVT_OSC_EVENT = wx.lib.newevent.NewEvent()
OSCCommandEvent, EVT_OSC_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
# Histogram
HGEvent, EVT_HG_EVENT = wx.lib.newevent.NewEvent()
HGCommandEvent, EVT_HG_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
# Scatterplot
SCPEvent, EVT_SCP_EVENT = wx.lib.newevent.NewEvent()
SCPCommandEvent, EVT_SCP_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()

class mainGUI(wx.Frame):
    """
    Handles the widgets for the gui.
    """
    def __init__(self, parent, title=""):
        super(mainGUI, self).__init__(parent, title=title)

        self.selectedDB = False
        self.data = None
        
        # Set the panel
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour((255, 255, 255))

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
            with open(path, "r") as dataFile:
                for line in dataFile:
                    row = line.split(",")
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
        print(self.selectedDB)


    def OnPCSelected(self, event):
        """ When the ||-coord is selected """
        pass

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
        pass

    def OnOSCSelected(self, event):
        """ When the osciloscope is selected """
        pass

    def OnHGSelected(self, event):
        """ When the histogram is selected """
        pass

    def OnSCPSelected(self, event):
        """ When the scatterplot is selected """
        pass

#---------------------------------------------------------------------------------------------

class visAnalyzer(wx.App):
    def OnInit(self):
        self.frame = mainGUI(None, title="Visual Analyzer")
        self.frame.Show()
        # Maximize
        self.frame.Maximize(True)
        return True

#---------------------------------------------------------------------------------------------

# "Main" function
if __name__ == '__main__':
    app = visAnalyzer(False)
    app.MainLoop()
