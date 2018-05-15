"""
Module implementing the dialog for getting the name of the database.
"""
import wx

class GetDBDialog(wx.Dialog):
    """
    Implements a dialog for getting the proper parameters for connect to the database.
    Get the following fields:
        -Username.
        -Password.
        -Name of the database.
    """
    def __init__(self, parent, title=""):
        super(GetDBDialog, self).__init__(parent, title=title)

        #self.panel = wx.Panel(self)
        self.initCtrls()
        self.bindEvents()

    def initCtrls(self):
        """ Creates the controls for the widget """
        # Labels
        usernameLabel = wx.StaticText(self, -1, "Username:")
        passwordLabel = wx.StaticText(self, -1, "Password:")
        dbLabel = wx.StaticText(self, -1, "Database:")
        # Textbox
        self.userNameTbx = wx.TextCtrl(self, -1)
        self.passwordTbx = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        self.dbTbx = wx.TextCtrl(self, -1)
        # Buttons
        self.okBtn = wx.Button(self, wx.OK, label="Ok")
        self.okBtn.SetDefault()
        self.cancelBtn = wx.Button(self, wx.CANCEL, label="Cancel")
        
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(usernameLabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer1.Add(self.userNameTbx, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(passwordLabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer2.Add(self.passwordTbx, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(dbLabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer3.Add(self.dbTbx, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(self.okBtn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer4.Add(self.cancelBtn, 0, wx.ALIGN_CENTER_HORIZONTAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(sizer4, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(sizer)
        self.DoLayoutAdaptation()

    def bindEvents(self):
        """ Bind the events to the buttons """
        self.okBtn.Bind(wx.EVT_BUTTON, self.onOkButton)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelButton)

    def getUserData(self):
        """ Returns the data on the text fields """
        name = self.userNameTbx.GetLineText(0)
        passw = self.passwordTbx.GetLineText(0)
        db = self.dbTbx.GetLineText(0)

        return name, passw, db

    def onOkButton(self, event):
        """ When the Ok button is pressed """
        self.EndModal(wx.ID_OK)

    def onCancelButton(self, event):
        """ When the Cancel button is pressed """
        self.EndModal(wx.ID_CANCEL)
