try:
    from uni2esky import eskymap
except ImportError:
    from uni2esky import regen_map
    regen_map.main()

    from uni2esky import eskymap

from uni2esky.uni2esky import *
