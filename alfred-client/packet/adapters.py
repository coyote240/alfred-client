from construct import Adapter


class MACAdapter(Adapter):

    def _encode(self, obj, context, path):
        pass

    def _decode(self, obj, context, path):
        return ':'.join(format(s, '02x') for s in obj)
