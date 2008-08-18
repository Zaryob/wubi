from winui import ui
import os
import logging
log = logging.getLogger("WinuiPage")


class Page(ui.Page):
    '''
    Base Page class
    Adds some handy methods
    '''

    def on_init(self):
        x, y, width, height = self.parent.get_client_rect()
        self.resize(width, height)
        self.width = width
        self.height = height

    def insert_vertical_image(self, bmp_file):
        self.vertical_image = ui.Bitmap(
            self,
            0, 0, 164, 314)
        self.vertical_image.set_image(
            os.path.join(self.application.info.imagedir, bmp_file))
        self.vertical_image.width = 164

    def insert_header(self, title, subtitle, bmp_file):
        '''
        Inserts a header with image, title and subtitle
        '''
        hbh = 57
        hbw = 150
        self.header = ui.Panel(
            self,
            0, 0 , self.width, hbh+2)
        if bmp_file:
            self.header.image = ui.Bitmap(
                self.header,
                0, 0, hbw, hbh)
            self.header.image.set_image(
                os.path.join(self.application.info.imagedir, bmp_file))
        if title:
            self.header.title = ui.Label(
                self.header,
                hbw + 20, 10, self.width - 200, 20,
                text = title)
            self.header.title.set_font(bold=True)
            self.header.title.set_background_color(255,255,255)
        if subtitle:
            self.header.subtitle = ui.Label(
                self.header,
                hbw + 20, 30, self.width - 200, 20,
                text = subtitle)
            #~ self.header.subtitle.set_background_color(255,255,255)
        self.header.line = ui.EtchedRectangle(self.header,0, hbh,self.width, 2)
        self.header.height = hbh + 2
        self.header.set_background_color(255,255,255)

    def insert_main(self):
        '''
        Panel containing client widgets
        Inserts a control conatiner
        appropriately resized to take care of header and footer
        '''
        left=0
        top = 0
        width = self.width
        height = self.height
        if hasattr(self, "header"):
            top += self.header.height
            height -= self.header.height
        if hasattr(self, "navigation"):
            height -= self.navigation.height
        if hasattr(self, "vertical_image"):
            left = self.vertical_image.width
            width -= left
        self.main = ui.Panel(
            self,
            left, top, width, height)
        self.main.height = height
        self.main.width = width

    def insert_navigation(self, button1_text=None, button2_text=None, button3_text=None, default=None):
        '''
        Inserts navigation buttons starting from the leftmost button
        '''
        nbw = 90
        nbh = 24
        sep_top = 6
        sep_height = 2

        if hasattr(self, "vertical_image"):
            sep_top = 0

        self.navigation = ui.Panel(
            self,
            0, self.height - nbh - 20 -sep_top - sep_height, self.width, nbh + 20 + sep_top + sep_height)

        if not hasattr(self, "vertical_image"):
            self.revision_label = ui.Label(
                self.navigation,
                10, 0, 40, 20,
                "Rev %s" % self.application.info.revision)
            self.revision_label.disable()
            revision_label_width = 50
            self.line = ui.EtchedRectangle(
                self.navigation,
                50, sep_top,self.width - 60, sep_height)
        else:
            self.line = ui.EtchedRectangle(
                self.navigation,
                0, sep_top, self.width, sep_height)

        for i,text in enumerate((button1_text, button2_text, button3_text)):
            if not text: continue
            if default and i + 1 == default:
                Button = ui.DefaultButton
            else:
                Button = ui.Button
            n = 0
            for other in (button1_text, button2_text, button3_text)[i:]:
                if other:
                    n += 1
            button = Button(
                self.navigation,
                self.width -(nbw + 10) * n, 10 + sep_top + sep_height, nbw, nbh,
                text=text)
            setattr(self.navigation, "button%s" % ( i + 1), button)
            self.navigation.height = nbh + 20 + sep_top + sep_height
