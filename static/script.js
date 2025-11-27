document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    const clearBtn = document.getElementById('clearBtn');
    const predictBtn = document.getElementById('predictBtn');
    const resultDisplay = document.getElementById('result');
    const confidenceDisplay = document.getElementById('confidence');

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    // Setup canvas
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 25;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Drawing functions
    function startDrawing(e) {
        isDrawing = true;
        [lastX, lastY] = getCoordinates(e);
    }

    function draw(e) {
        if (!isDrawing) return;
        e.preventDefault();

        const [x, y] = getCoordinates(e);

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.stroke();

        [lastX, lastY] = [x, y];
    }

    function stopDrawing() {
        isDrawing = false;
    }

    function getCoordinates(e) {
        const rect = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return [
            clientX - rect.left,
            clientY - rect.top
        ];
    }

    // Event listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    // Touch support
    canvas.addEventListener('touchstart', startDrawing);
    canvas.addEventListener('touchmove', draw);
    canvas.addEventListener('touchend', stopDrawing);

    // Clear canvas
    clearBtn.addEventListener('click', () => {
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        resultDisplay.textContent = '?';
        confidenceDisplay.textContent = 'Confidence: -';
    });

    // Predict
    predictBtn.addEventListener('click', async () => {
        // Get image data
        const imageData = canvas.toDataURL('image/png');

        try {
            resultDisplay.textContent = '...';
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: imageData })
            });

            const data = await response.json();

            if (response.ok) {
                resultDisplay.textContent = data.digit;
                confidenceDisplay.textContent = `Confidence: ${(data.confidence * 100).toFixed(2)}%`;
            } else {
                resultDisplay.textContent = 'Err';
                console.error('Error:', data.error);
                alert('Error predicting digit: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            resultDisplay.textContent = 'Err';
            alert('Error connecting to server');
        }
    });
});
