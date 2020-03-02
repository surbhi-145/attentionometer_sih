# run 'pip install wxpython' before running this code. This will take time to complete, don't panic.
import wx
import wx.html2
from screeninfo import get_monitors
m = get_monitors()[0]
HEIGHT = m.height
WIDTH = m.width


def printUrl(event):
  print("Navigated")


class MyBrowser(wx.Frame):
  def __init__(self, *args, **kwds):
    wx.Frame.__init__(self, *args, **kwds)
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.browser = wx.html2.WebView.New(self)
    sizer.Add(self.browser, 1, wx.EXPAND, 10)
    self.SetSizer(sizer)
    self.SetSize((WIDTH/2, HEIGHT/2))
    self.Bind(wx.EVT_MOTION, printUrl)

if __name__ == '__main__':
  app = wx.App()
  dialog = MyBrowser(None, -1)
  dialog.browser.LoadURL("https://www.greatlearning.in/")
  dialog.Show()
  app.MainLoop()