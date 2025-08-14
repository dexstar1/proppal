from fasthtml.common import *

def Typography():
    return Section(
        H3('Typography'), P('Shopper makes use of the Jost webfont for both headings and body content. This font is included in the package.', A('Font documentation', href='https://indestructibletype.com/Jost.html'), cls='text-gray-500'), Div(Div(H1('h1. Bootstrap heading'), H2('h2. Bootstrap heading'), H3('h3. Bootstrap heading'), H4('h4. Bootstrap heading'), H5('h5. Bootstrap heading'), H6('h6. Bootstrap heading'), P('Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias vero illo inventore fugiat iure itaque earum odit ratione quaerat sint! Rerum eos voluptate ad vero nihil commodi consequuntur, labore repudiandae?', cls='lead'), P('Lorem ipsum dolor, sit amet consectetur adipisicing elit. Maxime vitae ullam inventore dolorum aliquam quasi sunt autem quaerat perspiciatis voluptatum placeat expedita, atque nostrum impedit non voluptatem sint. Quidem, consectetur.'), P('Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit, quo alias facilis porro sunt vitae hic? Aliquam, ad consequatur reprehenderit ipsa doloremque facilis molestias non. Facilis veritatis enim nemo molestias.', cls='text-muted'), A('Link example', href='#!'), cls='card-body border'), cls='card'),
        cls="px-md-10 py-10"
    )

