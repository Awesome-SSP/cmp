import rpa as r
import time
r.init()
r.url('https://google.com')
r.type('search', 'Robocorp[]', 'enter')
time.sleep(5)
r.snap('page','screenshot.png' )
r.close()