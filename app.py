import os
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
ITEMS_DIR = BASE_DIR / "Items"

class ItemImageAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/items="):
            item_id = self.path.split("=")[1]
            clean_id = "".join(c for c in item_id if c.isalnum())
            
            if not clean_id:
                self.serve_not_found("Takla Jishan Add This Item in Items Folder")
                return
            file_path = ITEMS_DIR / f"{clean_id}.png"
            if file_path.exists() and file_path.is_file():
                with open(file_path, "rb") as image_file:
                    encoded_img = base64.b64encode(image_file.read()).decode('utf-8')

                html_content = f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Item: {clean_id}</title>
                    <style>
                        body {{
                            background-color: #0e0e11;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                        }}
                        img {{
                            width: 700px;
                            max-width: 90vw;
                            height: auto;
                            filter: drop-shadow(0px 15px 25px rgba(0,0,0,0.6));
                        }}
                    </style>
                </head>
                <body>
                    <img src="data:image/png;base64,{encoded_img}" alt="Item Image">
                </body>
                </html>"""
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.serve_not_found(clean_id)
        else:
            self.serve_not_found("Invalid_Route")

    def serve_not_found(self, item_id: str):

        svg = f"""<svg width="100vw" height="100vh" xmlns="http://www.w3.org/2000/svg" style="background-color: #0e0e11; margin: 0; padding: 0;"><rect width="100%" height="100%" fill="#0e0e11"/><text x="50%" y="45%" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="600" fill="#ef4444" text-anchor="middle" dominant-baseline="middle">Takla No Item Found</text><text x="50%" y="52%" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="400" fill="#a1a1aa" text-anchor="middle" dominant-baseline="middle">ID: {item_id}</text></svg>"""
        self.send_response(200)
        self.send_header('Content-type', 'image/svg+xml')
        self.end_headers()
        self.wfile.write(svg.strip().encode('utf-8'))

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    if not ITEMS_DIR.exists():
        ITEMS_DIR.mkdir(parents=True, exist_ok=True)
        
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, ItemImageAPI)
    print("Server running Developer Riduan Codex")
    print("Test URL: http://127.0.0.1:8000/items=")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped safely.")
        httpd.server_close()