#! /usr/bin/env/python

'''
esto me lo encontre  en stacckoverflow: http://stackoverflow.com/questions/8798043/adding-wxpython-in-pygame
'''

import wx, sys, os, pygame

class SDLThread:
    def __init__(self,screen):
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen
        self.color = (255,0,0)
        self.rect = (10,10,100,100)
    def Start(self):
        self.m_bKeepGoing = self.m_bRunning = True
        thread.start_new_thread(self.Run, ())
    def Stop(self):
        self.m_bKeepGoing = False
    def IsRunning(self):
        return self.m_bRunning
    def Run(self):
        while self.m_bKeepGoing:
            pass
##            GetInput()
##            Draw()
        self.m_bRunning = False;
class SDLPanel(wx.Panel):
    def __init__(self,parent,ID,tplSize):
        global pygame
        wx.Panel.__init__(self, parent, ID, size=tplSize)
        self.Fit()
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame
        pygame.init()
        icon = pygame.Surface((1,1));icon.set_alpha(0);pygame.display.set_icon(icon)
        global Surface
        Surface = pygame.display.set_mode(tplSize)
        self.thread = SDLThread(Surface)
        self.thread.Start()
    def __del__(self):
        self.thread.Stop()