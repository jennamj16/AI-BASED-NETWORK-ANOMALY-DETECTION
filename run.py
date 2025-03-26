import threading
import time
from app import create_app, model, utils, packet_capture

# Create Flask app
app = create_app()

# Generate dataset if needed
utils.generate_dataset()

# Start packet capture in background
capture_thread = threading.Thread(target=packet_capture.start_capture, daemon=True)
capture_thread.start()

# Start Flask in a separate thread
def start_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)

flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

# Train model periodically
try:
    while True:
        model.train_model()
        print("Model trained and anomalies updated.")
        time.sleep(300)  # Retrain every 5 minutes
except KeyboardInterrupt:
    print("\nShutting down...")
