"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    """
    Checks if a falling object is caught by the basket.
    Requires both horizontal overlap and vertical contact/intersection
    between the object's circular bounds and the basket rectangle.
    """
    horizontal_overlap = basket_rect.left <= obj.x <= basket_rect.right
    vertical_overlap = (
        basket_rect.top <= obj.y + obj.radius and
        obj.y - obj.radius <= basket_rect.bottom
    )
    return horizontal_overlap and vertical_overlap

