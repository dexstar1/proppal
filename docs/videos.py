from fasthtml.common import *

def Videos():
    return Section(
        H3('Video'),
        P('Video utilities.', cls='text-gray-500'),
        Hr(),
        Code('.video-512'), '- sets the height of the video element to', Code('512px'),
        'keeping its width at', Code('100%'), '. Works for browsers that support',
        Code('object-fit'), "and provides a fallback for those that don't.",
        cls="px-md-10 py-10"
    )
