def get_inline_style_as_dict(element):
    """
    Grab an element's inline style definition and return it as a dictionary of key/value pairs

    :param element: The element from which we need the style definition
    :return: Dictionary with CSS property names as keys and their corresponding values
    """
    style_dict = {}
    inline_style_string = element.get_attribute('style')
    for inline_style_pairs in\
            (style_declaration for style_declaration in inline_style_string.split(';') if style_declaration):
        parts = inline_style_pairs.split(':')
        property_name = parts[0].strip()
        style_dict[property_name] = parts[1].strip()

    return style_dict


def get_css_value(element, css_property_name):
    return element.value_of_css_property(css_property_name)