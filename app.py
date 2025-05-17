import cv2
import numpy as np

class ZoomApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.window_name = "Zoom & Capture App"
        self.zoomed = False
        self.zoom_factor = 2.0
        self.selection_start = None
        self.selection_end = None
        self.selecting = False
        self.capture_mode = False
        self.saved_image_path = "captured_image.png"
        self.current_mouse_pos = (0, 0)
        self.button_rect = (0, 0, 0, 0)
        self.last_zoomed_frame = None
        
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            bx, by, bw, bh = self.button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.capture_mode = True
                return

            self.selection_start = (x, y)
            self.selecting = True
            self.zoomed = False
            
        elif event == cv2.EVENT_MOUSEMOVE and self.selecting:
            self.selection_end = (x, y)
            
        elif event == cv2.EVENT_LBUTTONUP:
            self.selecting = False
            self.selection_end = (x, y)
            if self.selection_start != self.selection_end:
                self.zoomed = True

    def apply_zoom(self, frame):
        if self.zoomed and self.selection_start and self.selection_end:
            h, w = frame.shape[:2]
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            x1, x2 = max(0, x1), min(w, x2)
            y1, y2 = max(0, y1), min(h, y2)
            
            if (x2 - x1) > 10 and (y2 - y1) > 10:
                # 1) extract and zoom
                sel = frame[y1:y2, x1:x2]
                zoomed = cv2.resize(sel, None,
                                    fx=self.zoom_factor,
                                    fy=self.zoom_factor,
                                    interpolation=cv2.INTER_LINEAR)
                zh, zw = zoomed.shape[:2]
                
                # 2) compute top-left of overlay
                overlay_x = w - zw - 20
                overlay_y = 20
                if overlay_x < 0 or overlay_y < 0:
                    return frame   # doesn't fit at all
                
                # 3) clamp to available frame space
                max_h = h - overlay_y
                max_w = w - overlay_x
                zh2 = min(zh, max_h)
                zw2 = min(zw, max_w)
                zoom_cropped = zoomed[:zh2, :zw2]
                
                # 4) build mask for the cropped zoom
                gray = cv2.cvtColor(zoom_cropped, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                
                # 5) overlay into ROI
                roi = frame[overlay_y:overlay_y+zh2, overlay_x:overlay_x+zw2]
                np.copyto(roi, zoom_cropped, where=mask.astype(bool))
                
                self.last_zoomed_frame = frame.copy()
        return frame


    def process_frame(self, frame):
        h, w = frame.shape[:2]
        self.button_rect = (w-150, h-50, 140, 40)
        
        processed_frame = self.apply_zoom(frame.copy())
        
        if self.selecting and self.selection_start and self.selection_end:
            cv2.rectangle(processed_frame, self.selection_start, self.selection_end, (0, 255, 0), 2)
        
        # Draw UI elements
        cv2.rectangle(processed_frame, 
                     (self.button_rect[0], self.button_rect[1]),
                     (self.button_rect[0]+self.button_rect[2], self.button_rect[1]+self.button_rect[3]),
                     (0, 0, 255), -1)
        cv2.putText(processed_frame, "Capture", (self.button_rect[0]+20, self.button_rect[1]+30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(processed_frame, f"Zoom: {self.zoom_factor:.1f}x", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return processed_frame
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            display_frame = self.process_frame(frame)
            cv2.imshow(self.window_name, display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            elif key in (ord('+'), ord('=')):
                self.zoom_factor = min(4.0, self.zoom_factor + 0.1)
            elif key in (ord('-'), ord('_')):
                self.zoom_factor = max(1.0, self.zoom_factor - 0.1)
            elif key == ord('c'):
                self.capture_mode = True
                
            if self.capture_mode and self.last_zoomed_frame is not None:
                cv2.imwrite(self.saved_image_path, self.last_zoomed_frame)
                print(f"Image saved to {self.saved_image_path}")
                
                confirmation = np.zeros((100, 300, 3), dtype=np.uint8)
                cv2.putText(confirmation, "Image Saved!", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Confirmation", confirmation)
                cv2.waitKey(1000)
                cv2.destroyWindow("Confirmation")
                self.capture_mode = False

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = ZoomApp()
    app.run()