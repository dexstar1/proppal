from fasthtml.common import *

def SimpleBar():
    return Section(
        H3('Simplebar'),
        P(
            'SimpleBar is a plugin that tries to solve a long time problem: how to get custom scrollbars for your web-app while keeping a good user experience? SimpleBar does NOT implement a custom scroll behaviour. It keeps the native',
            Code('overflow: auto'),
            'scroll and only replaces the scrollbar visual appearance.',
            A(
                'Plugin documentation',
                href='https://github.com/Grsmto/simplebar/tree/master/packages/simplebar'
            ),
            cls='text-gray-500'
        ),
        Hr(),
        H5(),
        Div(
            Div(
                Div(
                    'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Laudantium doloremque, necessitatibus voluptates, praesentium saepe odio dolor dignissimos officiis laborum magni sint repellat laboriosam. Et quo earum laborum quis distinctio maxime. Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos perspiciatis ad cumque aperiam soluta provident quae cum temporibus facere magnam dolores laudantium quaerat, nostrum voluptate! Inventore quo qui magnam est. Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quam quasi minima necessitatibus fugiat nisi exercitationem molestiae, quo assumenda corporis enim voluptas quidem veniam nobis earum numquam nostrum optio blanditiis recusandae. Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ullam repellendus veritatis iusto aperiam nisi aliquid qui, reprehenderit, dolorem, tenetur animi expedita sunt commodi similique soluta dolore nobis labore cum nihil? Lorem ipsum dolor sit, amet consectetur adipisicing\n                  elit. Laudantium doloremque, necessitatibus voluptates, praesentium saepe odio dolor dignissimos officiis laborum magni sint repellat laboriosam. Et quo earum laborum quis distinctio maxime. Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos perspiciatis ad cumque aperiam soluta provident quae cum temporibus facere magnam dolores laudantium quaerat, nostrum voluptate! Inventore quo qui magnam est. Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quam quasi minima necessitatibus fugiat nisi exercitationem molestiae, quo assumenda corporis enim voluptas quidem veniam nobis earum numquam nostrum optio blanditiis recusandae. Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ullam repellendus veritatis iusto aperiam nisi aliquid qui, reprehenderit, dolorem, tenetur animi expedita sunt commodi similique soluta dolore nobis labore cum nihil?'
                ),
                cls='card-body border'
            ),
            Div(
                Code(
                    '<div\xa0data-simplebar\xa0style="max-height:\xa0160px;">',
                    'Lorem\xa0ipsum\xa0dolor\xa0sit\xa0amet\xa0consectetur\xa0adipisicing\xa0elit.\xa0Maxime\xa0ratione\xa0ullam\xa0totam\xa0tempore\xa0quasi,\xa0provident\xa0eos\xa0saepe\xa0reprehenderit\xa0aperiam\xa0laborum\xa0sed,\xa0voluptas\xa0non\xa0corporis\xa0id\xa0minus\xa0doloribus\xa0sint\xa0sapiente\xa0aliquam.',
                    '</div>',
                    cls='highlight html'
                ),
                cls='card-footer fs-sm bg-dark'
            ),
            cls='card'
        ),
        cls="px-md-10 py-10"
    )
