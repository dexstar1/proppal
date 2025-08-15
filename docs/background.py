from fasthtml.common import *

def Background():
    return Section(
        H3('Background'),
        P(
            'Background utilities to easily change background sizing, position, and color properties.',
            cls='text-gray-500'
        ),
        Hr(),
        H5('Sizing'),
        Code('.bg-cover'), '- sets the background image position to', Code('cover'), 'and centers it.',
        Code('.bg-h-100'), '- sets the background image size to', Code('auto 100%'), 'and centers it.',
        Hr(),
        H5('Positioning'),
        Code('.bg-start'), '- sets the background image positioning to', Code('center left'), '.',
        Hr(),
        H5('Clip'),
        Code('.bg-clip-content'), 'changes the background clip property to', Code('content-box'), '.',
        Hr(),
        H5('Images'),
        Code('.bg-pattern'), '- adds a semi-transparent background pattern image and repeats it to fit the whole available space.',
        Hr(),
        H5('Colors'),
        Code('.bg-white-90'), '- sets the background color to', Code('$white'), 'with 10% opacity.',
        Code('.bg-dark-5'), '- sets the background color to', Code('$dark'), 'with 95% opacity.',
        Code('.bg-dark-10'), '- sets the background color to', Code('$dark'), 'with 90% opacity.',
        Code('.bg-dark-20'), '- sets the background color to', Code('$dark'), 'with 80% opacity.',
        Code('.bg-dark-40'), '- sets the background color to', Code('$dark'), 'with 60% opacity.',
        Code('.bg-{$color}-soft'), '- changes the background color to the soft variation of the specified theme color. E.g.', Code('.bg-primary-soft'), '.',
        Hr(),
        H5('None'),
        Code('.bg-none'), '- removes the background color.',
        cls="px-md-10 py-10"
    )
