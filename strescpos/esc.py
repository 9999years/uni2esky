class Escape:
    def enc(self, val):
        """
        encode a variable (bytes, int, str, ...) to bytes
        """
        if isinstance(val, bytes):
            return val
        elif isinstance(val, str):
            return val.encode('latin-1')
        else:
            return val.to_bytes(1, 'little')

    def __init__(self, cmd, prefix=b'\x1b'):
        """
        set prefix (usually \x1b) and command
        """
        self.prefix = self.enc(prefix)
        self.cmd = self.enc(cmd)

    def escape(self, arg):
        """
        generate an escape from an argument, which can be None
        """
        if arg is None:
            return self.prefix + self.enc(self.cmd)
        else:
            return self.prefix + self.enc(self.cmd) + self.enc(arg)

    def arg(self, txt, val):
        setattr(self, txt, self.escape(val))

    def var(self, txt):
        setattr(self, txt, self.escape(val))

underline = Escape(0x2d)
underline.arg('off', 0x00)
underline.arg('on',  0x01)
underline.arg('on2', 0x02)
initialize = Escape(0x40)
emph = Escape(0x45)
emph.arg('on', 0x00)
emph.arg('off', 0x01)
