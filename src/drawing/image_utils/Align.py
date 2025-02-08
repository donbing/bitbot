from . import padding


class Align:
    def TopRight(display, message_size):
        return (display.size[0] - message_size[0] - padding - 1, padding)

    def BottomRight(display, message_size):
        return (display.size[0] - message_size[0], display.size[1] - message_size[1])

    def BottomLeft(display, message_size):
        return (0, display.size[1] - message_size[1])

    def TopLeft(display, message_size):
        return (0 + padding + 1, 0 + padding + 1)

    def Centre(display, message_size):
        message_y = (display.size[1][1] - message_size[1]) / 2
        message_x = (display.size[1][0] - message_size[0]) / 2
        return (message_y, message_x)

    # 🏳️ select image area with the most white pixels
    def LeastIntrusive(display, block):
        possiblePositions = Align.possible_block_positions(display, block)
        block_width, block_height = block

        # 🔢 count the white pixels in an area of the image
        def count_white_pixels(x, y, height, width, image):
            count = 0
            x_range = range(x, x + width)
            y_range = range(y, y + height)
            for x in x_range:
                for y in y_range:
                    pix = image.getpixel((x, y))
                    count += 1 if pix == (255, 255, 255) else 0
            return count

        rgb_im = display.convert('RGB')
        ordredByAveColour = sorted(
            possiblePositions,
            key=lambda item: (
                count_white_pixels(*item, block_height, block_width, rgb_im),
                (item[0],-item[1])) # order by pos, for top-right
            )
        if len(ordredByAveColour) > 0:
            return ordredByAveColour[-1]
        return (0, 0)

    def possible_block_positions(image, text_size):
        image_width, image_height = image.size
        text_width, text_height = text_size
        left_pad, top_pad = (0, 0)

        x_range = range(left_pad, image_width - text_width, 10)
        y_range = [top_pad, image_height // 2, image_height - text_height]
        return Align.flatten(
            map(lambda y: map(lambda x: (x, y), x_range), y_range)
        )

    def flatten(t):
        return [item for sublist in t for item in sublist]