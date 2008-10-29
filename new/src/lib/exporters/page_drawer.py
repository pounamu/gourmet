import gtk

class PageDrawer (gtk.DrawingArea):

    def __init__(self, page_width=None, page_height=None,
                 sub_areas=[],xalign=0.5,yalign=0.5
                 ):
        """Draw a page based on page areas given to us.

        The areas can be given in any scale they like.

        sub_areas are each (X1,Y1,WIDTH,HEIGHT) where the point defines
        the upper-left corner of the rectangle.
        
        """
        self.xalign = xalign
        self.yalign = yalign
        gtk.DrawingArea.__init__(self)
        self.gc = None  # initialized in realize-event handler
        self.width  = 0 # updated in size-allocate handler
        self.height = 0 # idem
        if page_width and page_height:
            self.set_page_area(page_width,page_height,sub_areas)
        self.connect('size-allocate', self.on_size_allocate)
        self.connect('expose-event',  self.on_expose_event)
        self.connect('realize',       self.on_realize)

    def set_page_area (self, page_width, page_height, sub_areas=[]):
        self.xy_ratio = page_width/page_height
        self.areas = []
        for x1,y1,w,h in sub_areas:
            width = float(w)/page_width
            height = float(h)/page_height
            x = float(x1)/page_width
            y = float(y1)/page_height
            self.areas.append(
                (x,y,width,height)
                )

    def on_realize(self, widget):
        self.gc = widget.window.new_gc()
        #self.gc.set_line_attributes(3, gtk.gdk.LINE_ON_OFF_DASH,
        #                            gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)

    def on_size_allocate(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height
        
    def on_expose_event(self, widget, event):
        if not hasattr(self,'xy_ratio'): return
        # This is where the drawing takes place
        if self.xy_ratio * self.height > self.width:
            width = int(self.width * 0.9)
            height = int((self.width / self.xy_ratio) * 0.9)
        else:
            width = int(self.xy_ratio*self.height*0.9)
            height = int(self.height*0.9)
        xpadding = int((self.width - width)*self.xalign)
        ypadding = int((self.height - height)*self.yalign)
        self.gc.set_line_attributes(3,
                               gtk.gdk.LINE_SOLID,
                               gtk.gdk.CAP_BUTT,
                               gtk.gdk.JOIN_MITER)
        widget.window.draw_rectangle(self.gc, False,
                                     xpadding, ypadding, width, height)
        self.gc.set_line_attributes(1,
                                    gtk.gdk.LINE_ON_OFF_DASH,
                                    gtk.gdk.CAP_BUTT,gtk.gdk.JOIN_MITER)
        for sub_area in self.areas:
            x,y,w,h = sub_area
            self.window.draw_rectangle(
                self.gc, False,
                int(xpadding+(x*width)),int(ypadding+(y*height)),int(w*width),int(h*height)
                )

if __name__ == '__main__':
    w = gtk.Window()
    w.add(PageDrawer(8.5,11,[(1,1,3,9.5),
                             (4.5,1,3,9.5),
                             ]))
    w.show_all()
    w.connect('delete-event',lambda *args: gtk.main_quit())
    gtk.main()