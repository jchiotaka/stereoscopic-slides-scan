from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import os

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Create a socket to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Doesn't actually connect
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Could not determine IP"

def start_server(port=8000):
    # Bind to all available interfaces
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    local_ip = get_local_ip()
    
    print("\n=== Stereo VR Viewer ===")
    print(f"\nServer started on all interfaces (0.0.0.0:{port})")
    print(f"\nAccess from this computer: http://localhost:{port}")
    print(f"Access from other devices: http://{local_ip}:{port}")
    print("\nTo view in Oculus:")
    print("1. Open Oculus Browser")
    print(f"2. Navigate to: http://{local_ip}:{port}")
    print("3. Click anywhere for fullscreen mode")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    start_server()