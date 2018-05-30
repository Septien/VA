"""
Dialog for requesting the data for the connecting to the stream
"""
import wx

class GetStreamDialog(wx.Dialog):
    """
    Implements a dialog for requesting the data (or displaying) necesary
    for the connection. Data:
        -ipaddr: IP address to connect from/to.
        -port: Port to connect from/to.
        -connectType: Type of connection
    """
    def __init__(self, parent, title=""):
        super(GetStreamDialog, self).__init__(parent, title=title)

        self.initCtrls()
        self.bindEvents()

    def initCtrls(self):
        # Labels
        iplabel = wx.StaticText(self, -1,   "IP:")
        portlabel = wx.StaticText(self, -1, "Port:")
        # Textbox
        self.ipTbx = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.portTbx = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        # Button
        self.cancelBtn = wx.Button(self, wx.OK, label="Ok")

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(iplabel, 0, wx.ALIGN_CENTER)
        sizer1.Add(self.ipTbx, 0, wx.ALIGN_CENTER)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(portlabel, 0, wx.ALIGN_CENTER)
        sizer2.Add(self.portTbx, 0, wx.ALIGN_CENTER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.cancelBtn, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(sizer)
        self.DoLayoutAdaptation()

    def bindEvents(self):
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.onOkButton)

    def onOkButton(self, event):
        """ When the Cancel button is pressed """
        self.Show(False)