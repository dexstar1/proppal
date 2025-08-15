from fasthtml.common import *

def SmoothScroll():
    return Section(
        H3('Smooth Scroll'),
        P(
            'A lightweight script to animate scrolling to anchor links.',
            A('Plugin documentation', href='https://github.com/cferdinandi/smooth-scroll'),
            cls='text-gray-500'
        ),
        Hr(),
        H5(),
        Div(
            Div(
                A('Scroll down to the heading', href='#smoothScroll', cls='btn btn-primary mb-5'),
                P('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque sed purus eget enim ornare luctus a at leo. Aenean nibh massa, posuere vel ipsum id, malesuada fringilla erat. Quisque laoreet tempor leo, non tristique massa hendrerit nec. Nulla non blandit dolor, vitae ultrices enim. Vivamus nec nisi at dolor venenatis finibus. Praesent viverra justo a velit gravida vehicula. Vivamus orci tellus, imperdiet nec rhoncus non, imperdiet ac nisi. Morbi vitae elementum est.'),
                P('Donec a nulla vel erat dictum egestas. Proin aliquam pellentesque ipsum at aliquam. Maecenas finibus, dui nec tristique pharetra, est diam consequat lectus, id elementum ligula est nec elit. In non velit id ex rutrum dapibus a efficitur nulla. Phasellus venenatis, odio ac aliquam dapibus, est nulla vehicula lacus, sed rhoncus tellus risus a ipsum. Ut vel pharetra nisl. Nunc eget tincidunt lacus, vel convallis erat. Donec quam lacus, malesuada vel dictum a, tincidunt pellentesque nulla. Cras tempor vel velit at malesuada. Donec sit amet massa feugiat, gravida nulla id, cursus lorem. Nullam nec luctus velit. Donec blandit augue vitae lorem viverra, id hendrerit sem vulputate. Cras vehicula dui neque, vitae aliquet sapien consequat sit amet. Maecenas eget nulla ultricies orci posuere fringilla eu eget orci. Integer vel aliquam leo. Quisque ultrices, nisl ut auctor ornare, ex mi interdum justo, ut luctus neque diam ut mauris.'),
                P('Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Etiam velit lorem, consectetur ac nunc vitae, mattis ultricies purus. Ut eros libero, facilisis a posuere nec, hendrerit a nulla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer eu hendrerit nunc, id consectetur quam. Donec blandit mauris nec orci ornare, vitae viverra augue aliquam. Suspendisse fermentum felis nec mauris sodales ullamcorper. Donec in tincidunt sem, at lacinia diam. Suspendisse lacinia neque at metus finibus, quis tincidunt velit laoreet. Nullam congue, erat sed convallis condimentum, libero neque luctus nisi, et mattis arcu velit lacinia tortor. Curabitur imperdiet ante eleifend tellus ultrices, ac faucibus sem molestie.'),
                H2('Scroll to me!', cls='text-center my-6'),
                P('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque sed purus eget enim ornare luctus a at leo. Aenean nibh massa, posuere vel ipsum id, malesuada fringilla erat. Quisque laoreet tempor leo, non tristique massa hendrerit nec. Nulla non blandit dolor, vitae ultrices enim. Vivamus nec nisi at dolor venenatis finibus. Praesent viverra justo a velit gravida vehicula. Vivamus orci tellus, imperdiet nec rhoncus non, imperdiet ac nisi. Morbi vitae elementum est.'),
                P('Donec a nulla vel erat dictum egestas. Proin aliquam pellentesque ipsum at aliquam. Maecenas finibus, dui nec tristique pharetra, est diam consequat lectus, id elementum ligula est nec elit. In non velit id ex rutrum dapibus a efficitur nulla. Phasellus venenatis, odio ac aliquam dapibus, est nulla vehicula lacus, sed rhoncus tellus risus a ipsum. Ut vel pharetra nisl. Nunc eget tincidunt lacus, vel convallis erat. Donec quam lacus, malesuada vel dictum a, tincidunt pellentesque nulla. Cras tempor vel velit at malesuada. Donec sit amet massa feugiat, gravida nulla id, cursus lorem. Nullam nec luctus velit. Donec blandit augue vitae lorem viverra, id hendrerit sem vulputate. Cras vehicula dui neque, vitae aliquet sapien consequat sit amet. Maecenas eget nulla ultricies orci posuere fringilla eu eget orci. Integer vel aliquam leo. Quisque ultrices, nisl ut auctor ornare, ex mi interdum justo, ut luctus neque diam ut mauris.'),
                P('Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Etiam velit lorem, consectetur ac nunc vitae, mattis ultricies purus. Ut eros libero, facilisis a posuere nec, hendrerit a nulla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer eu hendrerit nunc, id consectetur quam. Donec blandit mauris nec orci ornare, vitae viverra augue aliquam. Suspendisse fermentum felis nec mauris sodales ullamcorper. Donec in tincidunt sem, at lacinia diam. Suspendisse lacinia neque at metus finibus, quis tincidunt velit laoreet. Nullam congue, erat sed convallis condimentum, libero neque luctus nisi, et mattis arcu velit lacinia tortor. Curabitur imperdiet ante eleifend tellus ultrices, ac faucibus sem molestie.'),
                cls='card-body border'
            ),
            Div(
                Code(
                    '<a\xa0class="btn\xa0btn-primary"\xa0href="#heading"\xa0data-toggle="smooth-scroll"\xa0data-offset="0">',
                    'Go\xa0to\xa0the\xa0heading',
                    '</a>',
                    '<h1\xa0id="heading">Bootstrap\xa0heading</h1>',
                    cls='highlight html'
                ),
                cls='card-footer fs-sm bg-dark'
            ),
            cls='card'
        ),
        cls="px-md-10 py-10"
    )
