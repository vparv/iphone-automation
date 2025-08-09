#!/usr/bin/env python3

import sys
import os
import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from batch_processor import BatchProcessor

class AutomationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('automation_launcher.html', 'r') as f:
                content = f.read()
                # Add JavaScript to communicate with server
                content = content.replace('</head>', '''
                <script>
                    async function executeAutomation(action, params = {}) {
                        try {
                            const response = await fetch('/execute', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({action: action, params: params})
                            });
                            const result = await response.json();
                            log(`🔥 ${result.message}`);
                            return result;
                        } catch (error) {
                            log(`❌ Error: ${error.message}`);
                        }
                    }
                    
                    // Override the original functions to actually execute
                    function startFromImage(imageNum) {
                        log(`🚀 Starting automation from Image #${imageNum}`);
                        executeAutomation('start_from_image', {start: imageNum, count: 4});
                    }
                    
                    function startCustom() {
                        const startImage = parseInt(document.getElementById('startImage').value);
                        const numImages = parseInt(document.getElementById('numImages').value);
                        log(`🎯 Custom automation: ${numImages} images starting from #${startImage}`);
                        executeAutomation('start_custom', {start: startImage, count: numImages});
                    }
                    
                    function processAll16() {
                        log(`🌟 Starting full 16-image automation`);
                        executeAutomation('process_all_16');
                    }
                    
                    function testSingle() {
                        log(`🧪 Testing single image automation`);
                        executeAutomation('test_single');
                    }
                    
                    function resetState() {
                        log(`🔄 Resetting to Image #1`);
                        executeAutomation('reset_state');
                    }
                    
                    function stopAutomation() {
                        log(`⏹️ Stopping automation`);
                        executeAutomation('stop');
                    }
                </script>
                </head>''')
                
            self.wfile.write(content.encode())
            
        elif self.path == '/status':
            # Return current status
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = {'running': hasattr(self.server, 'current_task') and self.server.current_task is not None}
            self.wfile.write(json.dumps(status).encode())
            
    def do_POST(self):
        if self.path == '/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            action = data['action']
            params = data.get('params', {})
            
            # Execute automation in background thread
            thread = threading.Thread(target=self.execute_automation, args=(action, params))
            thread.daemon = True
            thread.start()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'success': True, 'message': f'Started {action} automation'}
            self.wfile.write(json.dumps(response).encode())
    
    def execute_automation(self, action, params):
        """Execute the automation in a background thread."""
        try:
            processor = BatchProcessor()
            
            if action == 'start_from_image':
                start_img = params['start']
                count = params['count']
                print(f"🚀 Starting automation from Image #{start_img}, processing {count} images")
                
                for i in range(start_img, min(start_img + count, 17)):
                    self.process_single_image(processor, i)
                    
            elif action == 'start_custom':
                start_img = params['start']
                count = params['count']
                print(f"🎯 Custom automation: {count} images starting from #{start_img}")
                
                for i in range(start_img, min(start_img + count, 17)):
                    self.process_single_image(processor, i)
                    
            elif action == 'process_all_16':
                print("🌟 Starting full 16-image automation")
                for i in range(1, 17):
                    self.process_single_image(processor, i)
                    
            elif action == 'test_single':
                print("🧪 Testing single image automation")
                processor.navigator.reset_state()
                processor.navigator.navigate_to_gallery()
                time.sleep(1.5)
                processor.navigator.select_next_image()
                time.sleep(1.5)
                processor.run_core_workflow()
                
            elif action == 'reset_state':
                print("🔄 Resetting to Image #1")
                processor.navigator.reset_state()
                
            elif action == 'stop':
                print("⏹️ Stopping automation")
                # Set stop flag if needed
            elif action == 'run_gallery_loop':
                # Run android/gallery_loop.py starting at provided index, only 1 loop
                start_img = int(params.get('start', 1))
                # Enable optional end path by setting environment var for this subprocess
                cmd = [
                    sys.executable,
                    os.path.join(os.path.dirname(__file__), 'android', 'gallery_loop.py'),
                    str(start_img),
                    '1',  # count=1
                ]
                print(f"📸 Running gallery_loop.py start={start_img} count=1 (optional ending TRUE)")
                # Launch subprocess detached so server stays responsive
                subprocess.Popen(cmd)
                
        except Exception as e:
            print(f"❌ Automation error: {e}")
    
    def process_single_image(self, processor, image_num):
        """Process a single image with robust error handling."""
        print(f"\n🎯 Processing Image #{image_num}")
        
        try:
            # Calculate position
            row = (image_num - 1) // 4
            col = (image_num - 1) % 4
            
            # Set position
            processor.navigator.save_state(row, col)
            print(f"📍 Set position: Row {row + 1}, Column {col + 1}")
            
            # Navigate to gallery
            print("📂 Navigating to gallery...")
            if not processor.navigator.navigate_to_gallery():
                print(f"❌ Failed to navigate to gallery for Image #{image_num}")
                return False
            time.sleep(1.5)
            
            # Select image
            print(f"🖱️  Selecting Image #{image_num}...")
            if not processor.navigator.select_next_image():
                print(f"❌ Failed to select Image #{image_num}")
                return False
            time.sleep(1.5)
            
            # Run workflow
            print(f"⚙️  Running workflow for Image #{image_num}...")
            if not processor.run_core_workflow():
                print(f"❌ Workflow failed for Image #{image_num}")
                return False
            
            print(f"✅ Image #{image_num} completed successfully!")
            time.sleep(2)  # Brief pause between images
            return True
            
        except Exception as e:
            print(f"❌ Error processing Image #{image_num}: {e}")
            return False
    
    def log_message(self, format, *args):
        # Suppress default HTTP server logs
        pass

class AutomationServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        
    def start(self):
        """Start the automation server."""
        try:
            self.server = HTTPServer(('localhost', self.port), AutomationHandler)
            print(f"🚀 Automation Server Started!")
            print(f"📱 Open your browser to: http://localhost:{self.port}")
            print(f"🎯 Click buttons on the webpage to run automation!")
            print(f"⏹️  Press Ctrl+C to stop the server")
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n⏹️  Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            if self.server:
                self.server.server_close()

def main():
    print("🤖 Liene Photo HD Automation Server")
    print("=" * 40)
    
    server = AutomationServer()
    server.start()

if __name__ == "__main__":
    main()

