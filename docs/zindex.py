from fasthtml.common import *

def Zindex():
    return Section(
        H3('Z-index'), P('Z-index utilities', cls='text-gray-500'), Hr(), Code('.z-index-1'), '- sets the', Code('z-index'), 'property value to', Code('1'), '.', Code('.z-index-fixed'), '- sets the', Code('z-index'), 'property value to the value of the default', Code('$zindex-fixed'), 'variable.',
        cls="px-md-10 py-10"
    )
