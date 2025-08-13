python3 -c "
from batch_processor import BatchProcessor
processor = BatchProcessor()
# Reset to start from image #1
processor.navigator.reset_state()
print(\"🚀 Starting 16-image batch processing from Image #1\")
# Run 16 loops starting from first image
processor.run_batch_processing(16, reset_position=True)
"
