from flask import Flask, render_template, request, Response
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        # get the parameters from the form data
        width = int(request.form['width'])
        height = int(request.form['height'])
        color = request.form['color']
        format = request.form['format']

        # validate the parameters
        if width <= 0 or height <= 0:
            return Response("Invalid width or height", status=400)
        if color not in ['red', 'green', 'blue']:
            return Response("Invalid color", status=400)
        if format not in ['jpeg', 'png', 'gif']:
            return Response("Invalid format", status=400)
        if width > 10000 or height > 10000:
            return Response("Width or height too large", status=400)

        # generate the image
        image_data = generate_image_array(width, height, color, format)

        # return the image as a response
        return Response(image_data, mimetype='image/' + format)
    except ValueError:
        return Response("Invalid parameter value", status=400)

def generate_image_array(width, height, color, format):
    # create a numpy array with the specified dimensions and color
    if color == 'red':
        image_array = np.full((height, width, 3), (255, 0, 0), dtype=np.uint8)
    elif color == 'green':
        image_array = np.full((height, width, 3), (0, 255, 0), dtype=np.uint8)
    elif color == 'blue':
        image_array = np.full((height, width, 3), (0, 0, 255), dtype=np.uint8)

    # create an image from the array
    image = Image.fromarray(image_array)

    # write the image to a buffer
    with io.BytesIO() as output:
        image.save(output, format=format)
        image_data = output.getvalue()

    return image_data

if __name__ == '__main__':
    app.run(debug=True)
