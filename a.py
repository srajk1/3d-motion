import tkinter as tk
import math
import time

class BBSul3DLogo:
    def __init__(self, root):
        self.root = root
        self.root.title("3D BBSul Logo Animation")
        self.root.geometry("800x600")
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        # Logo parameters
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.scale = 100
        self.center_x = 400
        self.center_y = 300
        
        # Define the 3D points for the BBSul logo
        # We'll create a stylized "BBSul" text in 3D
        self.points = self.generate_logo_points()
        
        # Define edges connecting the points
        self.edges = self.generate_logo_edges()
        
        # Colors for different parts of the logo
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        # Start animation
        self.animate()
        
    def generate_logo_points(self):
        # Create points for a stylized "BBSul" text in 3D
        points = []
        
        # First 'B'
        points.extend(self.generate_letter_b(0, 0, 0))
        # Second 'B'
        points.extend(self.generate_letter_b(3, 0, 0))
        # 'S'
        points.extend(self.generate_letter_s(6, 0, 0))
        # 'u'
        points.extend(self.generate_letter_u(9, 0, 0))
        # 'l'
        points.extend(self.generate_letter_l(12, 0, 0))
        
        return points
    
    def generate_letter_b(self, offset_x, offset_y, offset_z):
        # Generate points for letter 'B'
        points = []
        # Outer shape of B
        for i in range(10):
            angle = i * math.pi / 9
            x = offset_x + math.cos(angle) * 0.8
            y = offset_y + math.sin(angle) * 0.8
            z = offset_z
            points.append((x, y, z))
            
            # Inner points for 3D effect
            points.append((x, y, z + 0.3))
            
        return points
    
    def generate_letter_s(self, offset_x, offset_y, offset_z):
        # Generate points for letter 'S'
        points = []
        # S shape
        for i in range(10):
            t = i / 9
            x = offset_x + 1.5 * t
            y = offset_y + math.sin(t * math.pi * 2) * 0.8
            z = offset_z
            points.append((x, y, z))
            
            # Inner points for 3D effect
            points.append((x, y, z + 0.3))
            
        return points
    
    def generate_letter_u(self, offset_x, offset_y, offset_z):
        # Generate points for letter 'u'
        points = []
        # U shape
        for i in range(10):
            t = i / 9
            x = offset_x + 1.5 * t
            y = offset_y + (1 - t) * 0.8
            z = offset_z
            points.append((x, y, z))
            
            # Inner points for 3D effect
            points.append((x, y, z + 0.3))
            
        return points
    
    def generate_letter_l(self, offset_x, offset_y, offset_z):
        # Generate points for letter 'l'
        points = []
        # L shape
        for i in range(10):
            t = i / 9
            x = offset_x
            y = offset_y + t * 1.6
            z = offset_z
            points.append((x, y, z))
            
            # Inner points for 3D effect
            points.append((x, y, z + 0.3))
            
        return points
    
    def generate_logo_edges(self):
        # Create edges between points to form the 3D structure
        edges = []
        
        # For each letter, connect points to form the 3D shape
        letter_point_count = 20  # 10 outer + 10 inner points per letter
        for letter_idx in range(5):  # 5 letters in "BBSul"
            start_idx = letter_idx * letter_point_count
            
            # Connect outer points
            for i in range(9):
                edges.append((start_idx + i, start_idx + i + 1))
                # Connect to inner points
                edges.append((start_idx + i, start_idx + i + 10))
                # Connect inner points
                edges.append((start_idx + i + 10, start_idx + i + 11))
            
            # Close the shapes
            edges.append((start_idx + 9, start_idx))
            edges.append((start_idx + 19, start_idx + 10))
            
        return edges
    
    def rotate_point(self, point, angle_x, angle_y, angle_z):
        x, y, z = point
        
        # Rotate around X axis
        y_rot = y * math.cos(angle_x) - z * math.sin(angle_x)
        z_rot = y * math.sin(angle_x) + z * math.cos(angle_x)
        y, z = y_rot, z_rot
        
        # Rotate around Y axis
        x_rot = x * math.cos(angle_y) + z * math.sin(angle_y)
        z_rot = -x * math.sin(angle_y) + z * math.cos(angle_y)
        x, z = x_rot, z_rot
        
        # Rotate around Z axis
        x_rot = x * math.cos(angle_z) - y * math.sin(angle_z)
        y_rot = x * math.sin(angle_z) + y * math.cos(angle_z)
        x, y = x_rot, y_rot
        
        return (x, y, z)
    
    def project_point(self, point):
        x, y, z = point
        
        # Apply perspective
        factor = 500 / (z + 5)
        x_proj = x * factor + self.center_x
        y_proj = y * factor + self.center_y
        
        return (x_proj, y_proj)
    
    def draw_logo(self):
        self.canvas.delete("all")
        
        # Transform and project all points
        transformed_points = []
        for point in self.points:
            rotated = self.rotate_point(point, self.angle_x, self.angle_y, self.angle_z)
            projected = self.project_point(rotated)
            transformed_points.append(projected)
        
        # Draw edges
        for i, edge in enumerate(self.edges):
            start_idx, end_idx = edge
            x1, y1 = transformed_points[start_idx]
            x2, y2 = transformed_points[end_idx]
            
            # Use different colors for different parts of the logo
            color_idx = start_idx // 20 % len(self.colors)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.colors[color_idx], width=2)
        
        # Add some decorative elements
        self.draw_background()
        
    def draw_background(self):
        # Draw a simple background with circles
        for i in range(5):
            radius = 50 + i * 20
            self.canvas.create_oval(
                self.center_x - radius, self.center_y - radius,
                self.center_x + radius, self.center_y + radius,
                outline=self.colors[i % len(self.colors)], width=1
            )
    
    def animate(self):
        # Update rotation angles
        self.angle_x += 0.01
        self.angle_y += 0.015
        self.angle_z += 0.005
        
        # Redraw the logo
        self.draw_logo()
        
        # Schedule next frame
        self.root.after(30, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = BBSul3DLogo(root)
    root.mainloop()