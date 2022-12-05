import cv2
import webcolors

filepath = "red.png"
image = cv2.imread(filepath)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
average_color = image.mean(axis=0).mean(axis=0)
normalized_color = tuple(round(channel) for channel in average_color)
print(normalized_color)
average_color = webcolors.rgb_to_hex(normalized_color)
print(average_color, type(average_color))
#color_name = webcolors.hex_to_name(average_color)
#print(color_name)