try:
    from uni2esky import eskymap
except ImportError:
    import regen_map
    regen_map.main()
    import eskymap

from uni2esky.uni2esky import *
