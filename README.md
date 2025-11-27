# Handwritten Digit Recognition

A complete end-to-end project for recognizing handwritten digits using a Convolutional Neural Network (CNN) trained on the MNIST dataset, served via a Flask web application.

## Project Structure

```
digit-recognition/
├── app.py              # Flask backend application
├── train_model.py      # Script to train the CNN model
├── requirements.txt    # Python dependencies
├── mnist_model.h5      # Trained model file (generated after training)
├── templates/
│   └── index.html      # Frontend HTML
└── static/
    ├── style.css       # CSS styling
    └── script.js       # JavaScript for drawing and API communication
```

## Setup & Installation

1.  **Clone the repository** (if applicable) or download the files.

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Train the Model
Before running the web app, you need to train the model. This will download the MNIST dataset, train the CNN, and save the model as `mnist_model.h5`.

```bash
python train_model.py
```

### 2. Run the Web Application
Start the Flask server:

```bash
python app.py
```

### 3. Use the Interface
- Open your browser and go to `http://127.0.0.1:5000`.
- Draw a digit (0-9) in the black box.
- Click **Predict** to see the result.
- Click **Clear** to try again.

## Technologies Used
- **TensorFlow/Keras**: For building and training the deep learning model.
- **Flask**: A lightweight WSGI web application framework.
- **NumPy**: For numerical operations.
- **Pillow (PIL)**: For image processing.
- **HTML5/CSS3/JavaScript**: For the user interface.

## Model Architecture
The model is a simple CNN with the following layers:
- Conv2D (32 filters) + ReLU
- MaxPooling2D
- Conv2D (64 filters) + ReLU
- MaxPooling2D
- Conv2D (64 filters) + ReLU
- Flatten
- Dense (64 units) + ReLU
- Dense (10 units) + Softmax (Output)
