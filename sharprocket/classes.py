import shortuuid

from sharprocket.constants import SCALING_FACTOR


class Box:
    """
    Stores all the data for a box.
    """

    def __init__(self, x, y, w, h, old_id=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.xf = x + w
        self.yf = y + h

        self.area = w * h

        if old_id:
            self.id = old_id
        else:
            self.id = shortuuid.uuid()[:8]

    def scale(self, downscale=False):
        """
        Scales by a small factor to try and hide the drawn boxes
        """

        factor = (
            int(self.w / SCALING_FACTOR)
            if self.w > self.h
            else int(self.h / SCALING_FACTOR)
        )

        if downscale:
            factor = -factor

        new_x = self.x - factor
        new_y = self.y - factor
        new_w = self.w + 2 * factor
        new_h = self.h + 2 * factor

        return Box(new_x, new_y, new_w, new_h, old_id=self.id)

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y and self.w == o.w and self.h == o.h

    def __repr__(self):
        box_args = f"{self.x}, {self.y}, {self.w}, {self.h}"
        return f"(*{self.id}) Box({box_args}) Area: {self.area}"
