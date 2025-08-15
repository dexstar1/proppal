from fasthtml.common import *

def Opacity():
    return Section(
        H3('Opacity'),
        P('Opacity utilities.', cls='text-gray-500'),
        Hr(),
        Code('.opacity-{10|20|30|40|50|60|70|80|90|100}'),
        '- opacity levels from 10 to 100%.',
        cls="px-md-10 py-10"
    )
