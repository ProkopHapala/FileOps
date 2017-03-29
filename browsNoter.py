#!/usr/bin/python

import os
import wx
import sys
#import shutil
import pyFileOps.file as fops

# developed by help of : https://wiki.wxpython.org/AnotherTutorial

class MyTextDropTarget(wx.TextDropTarget):

    def __init__(self, object):
        wx.TextDropTarget.__init__(self)
        self.object = object

    def OnDropText(self, x, y, data):
        self.object.InsertStringItem(0, data)

class MyPopupMenu(wx.Menu):
    def __init__(self, app):
        wx.Menu.__init__(self)
        self.app = app
        item1 = wx.MenuItem(self, wx.NewId(), "open external")
        self.AppendItem(item1)
        self.Bind(wx.EVT_MENU, self.OnItem1, item1)

    def OnItem1(self, event):
        print "external open i : ", self.app.i_select
        item = self.app.found_items[self.app.i_select];    # print "external open   : ", item
        abspath   = os.path.join(self.app.search_path, item[1])
        full_path = os.path.join(abspath, item[0]);        # print full_path
        if sys.platform == 'linux2':
            os.system('xdg-open %s' %full_path) 
        else:
            os.system('start %s' %full_path)

class MyFrame(wx.Frame):
    root_path   = "/home/prokop/Dropbox/MyDevSW"
    includes=['.c','.cpp','.h','.cl','.py']
    excludes=['.png','.bmp','.jpg','.jpeg','.tif','.tiff','.gif']
    search_str = 'virtual'
    

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(640, 480))
        splitter1 = wx.SplitterWindow(self     , -1, style=wx.SP_3D, size=(100,100))
        splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D, size=(100,100))
        splitter3 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D, size=(100,100))
        
        self.dir  = wx.GenericDirCtrl(splitter3, -1, dir=self.root_path, size=(100,100), style=wx.DIRCTRL_DIR_ONLY)
        self.lc1  = wx.ListCtrl(splitter2, -1, size=(100,100), style=wx.LC_LIST)
        self.text = wx.TextCtrl(splitter2, 1000, '', size=(100, 100), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.text.SetFocus()
        
        panel = wx.Panel(splitter3, -1, size=(100,100) )
        box = wx.BoxSizer(wx.VERTICAL)
        self.txtExt = wx.TextCtrl(panel, -1); self.txtExt.SetValue('.c;.cpp;.h;.cl;.py')
        self.txtStr = wx.TextCtrl(panel, -1); self.txtStr.SetValue('virtual')
        box.Add(self.txtExt, 1, wx.EXPAND | wx.ALL, 3)
        box.Add(self.txtStr, 1, wx.EXPAND | wx.ALL, 3)
        #box.Add(wx.Button(panel, -1, 'Button1'), 1, wx.EXPAND | wx.ALL, 3)
        #box.Add(wx.Button(panel, -1, 'Button2'), 1, wx.EXPAND | wx.ALL, 3)
        #box.Add(wx.Button(panel, -1, 'Button3'), 1, wx.EXPAND | wx.ALL, 3)
        panel.SetSizer(box)

        wx.EVT_LIST_BEGIN_DRAG   (self, self.lc1.GetId(), self.OnDragInit)
        wx.EVT_LIST_ITEM_SELECTED(self, self.lc1.GetId(), self.OnFileSelect )
        #wx.EVT_RIGHT_DOWN        (self, self.lc1.GetId(), self.OnRightDown )
        tree = self.dir.GetTreeCtrl()
        splitter2.SplitHorizontally(self.lc1, self.text)
        splitter3.SplitHorizontally(panel, self.dir)
        splitter1.SplitVertically  (splitter3, splitter2)
        wx.EVT_TREE_SEL_CHANGED(self, tree.GetId(), self.OnFolderSelect )
        self.Centre()
        
        self.lc1.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.popup = MyPopupMenu(self)
        
    def OnRightDown(self,event):
        self.PopupMenu(MyPopupMenu(self), event.GetPosition())
        #self.popup

    def OnFileSelect(self, event ):
        i = len(self.found_items) - event.GetIndex() -1 # why like that? - probably list filled last-on-top; numbered from 1
        self.i_select = i
        item = self.found_items[i]
        #print i," ",item
        abspath   = os.path.join(self.search_path, item[1])
        full_path = os.path.join(abspath, item[0])
        print full_path
        self.text.LoadFile( full_path )

    def OnFolderSelect(self, event):
        self.includes   = self.txtExt.GetValue().split(";"); #print  self.includes
        self.search_str = self.txtStr.GetValue();            #print  self.includes
        path = self.dir.GetPath();  #print path
        self.search_path = path
        items    = fops.path2list_filter( path, include=self.includes, echoPerNFiles=100 ) 
        found_is = fops.searchInFiles( items, path, self.search_str )
        self.lc1.ClearAll()
        #print "found %i items" %len(found_is)
        found_items = []
        for i in found_is:
            print items[i][0]
            self.lc1.InsertStringItem(0, items[i][0] )
            found_items.append( items[i] ) 
        self.found_items = found_items

    def OnDragInit(self, event):
        text = self.lc1.GetItemText(event.GetIndex())
        tdo = wx.PyTextDataObject(text)
        tds = wx.DropSource(self.lc1)
        tds.SetData(tdo)
        tds.DoDragDrop(True)

class MyApp(wx.App):

    def OnInit(self):
        frame = MyFrame(None, -1, "dragdrop.py")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
