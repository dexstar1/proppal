# FastHTML Documentation

## Overview

FastHTML is a Python library designed for creating server-rendered hypermedia applications. It integrates several powerful tools, including Starlette, Uvicorn, HTMX, and Fastcore's FastTags, to provide a robust framework for web development.

## Features

- **Server-Rendered Applications**: FastHTML allows for the creation of dynamic web applications that are rendered on the server side.
- **Integration with Popular Libraries**: The library seamlessly integrates with Starlette for routing and Uvicorn for serving applications.
- **Flexible Component System**: FastHTML provides a component-based architecture, allowing developers to create reusable UI components.
- **Support for Various CSS Frameworks**: While it includes support for Pico CSS, developers can use any CSS framework of their choice.
- **Dynamic Routing**: FastHTML supports dynamic routing with variable URL segments, making it easy to create RESTful APIs.

## Installation

To install FastHTML, use pip:

```bash
pip install python-fasthtml
```

## Getting Started

To create a minimal FastHTML application, follow these steps:

1. Import the necessary components from FastHTML.
2. Define your application and routing.
3. Use the `serve()` function to run your application.

### Example

```python
from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return "Hello, FastHTML!"

serve()
```

## Documentation Modules

The project includes several documentation modules, each representing different sections of the FastHTML framework:

- **Alerts**: Documentation for the alerts component.
- **Avatars**: Documentation for the avatars component.
- **Badges**: Documentation for the badges component.
- **Brands**: Documentation for the brands component.
- **Breadcrumbs**: Documentation for the breadcrumbs component.
- **Rates**: Documentation for the rates component.

## Contributing

Contributions to FastHTML are welcome! Please feel free to submit issues or pull requests to improve the library.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.