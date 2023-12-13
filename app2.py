from flask import Flask, render_template, request, send_file
from diffusers import DiffusionPipeline
from PIL import Image
import os
import numpy as np
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        model_name = request.form['model']
        positive_prompt = request.form['positive_prompt']
        negative_prompt = request.form['negative_prompt']
        sampler = request.form['sampler']  # Using default sampler for now
        sample_amount = int(request.form['sample_amount'])
        height = int(request.form['height'])
        width = int(request.form['width'])

        # Initialize Diffusion Pipeline
        model_path = os.path.join('/Volumes/Projects/Personal/AI/stable-diffusion-webui/models/Diffusers', model_name)
        pipeline = DiffusionPipeline.from_pretrained(model_path)

        # Generate Image
        prompt = f"{positive_prompt} | {negative_prompt}"
        image = pipeline(prompt).images[0]  # Using default sampler

        # Convert the image to a PIL Image object and save
        pil_image = Image.fromarray((image * 255).astype("uint8"))
        img_io = BytesIO()
        pil_image.save(img_io, 'JPEG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')

    # List available diffusers models from the directory
    model_dir = '/Volumes/Projects/Personal/AI/stable-diffusion-webui/models/Diffusers'
    available_models = os.listdir(model_dir)

    return render_template('index.html', models=available_models)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
