# Custom Background Image Demo

A PyQt5 application demonstrating custom window background image implementation with blur effects and opacity controls.

## Tech Stack

- **PyQt5**: Core GUI framework
- **[PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)**: Modern UI components with Fluent Design System

## Core Implementation

### Background Manager (`app/background/background_manager.py`)

The `BackgroundManager` class handles all background-related operations:

- **Image Processing**: Validates, scales, and processes background images
- **Blur Effects**: Implements efficient blur algorithms with performance optimization
- **Caching System**: Caches processed images to improve performance
- **Configuration Integration**: Manages background settings through the config system

Key methods:
```python
get_background_pixmap(window_size)  # Returns processed background image
_apply_efficient_blur(pixmap, radius)  # Applies blur effects
validate_image_path(path)  # Validates image file formats
```

### Main Window Implementation (`app/view/main_window.py`)

Background rendering is handled in the `paintEvent` method:

```python
def paintEvent(self, event):
    super().paintEvent(event)
    
    if self.backgroundManager.is_background_enabled():
        painter = QPainter(self)
        background_pixmap = self.backgroundManager.get_background_pixmap(self.size())
        
        if background_pixmap:
            opacity = self.backgroundManager.get_background_opacity() / 100.0
            painter.setOpacity(opacity)
            painter.drawPixmap(x, y, background_pixmap)
```

### Settings Interface (`app/view/settings_interface.py`)

Provides user controls for:
- Enable/disable background image
- Image file selection
- Opacity adjustment (0-100%)
- Blur radius control (0-50px)

Real-time preview updates trigger window repaints when settings change.

## Installation & Running

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the demo:
```bash
python settings_demo.py
```

## Features

- **Real-time Preview**: Background changes are immediately visible
- **Performance Optimized**: Efficient blur algorithms and image caching
- **Multiple Formats**: Supports JPG, PNG, BMP, GIF, WebP
- **Responsive Scaling**: Background images adapt to window size
- **Persistent Settings**: Configuration saved to `config/config.json`

## Project Structure

```
app/
├── background/
│   └── background_manager.py    # Core background processing logic
├── view/
│   ├── main_window.py          # Main application window with paintEvent
│   └── settings_interface.py   # Background configuration UI
├── common/
│   └── config.py              # Configuration management
└── resource/                  # Application assets

settings_demo.py               # Application entry point
```

## Configuration

Background settings are managed through `QConfig`:

```python
backgroundImageEnabled = ConfigItem("Background", "ImageEnabled", False)
backgroundImagePath = ConfigItem("Background", "ImagePath", "")
backgroundOpacity = RangeConfigItem("Background", "Opacity", 80, RangeValidator(0, 100))
backgroundBlurRadius = RangeConfigItem("Background", "BlurRadius", 0, RangeValidator(0, 50))
```

## Implementation Highlights

1. **Paint-based Rendering**: Background images are drawn via `paintEvent` rather than CSS, providing better control over rendering
2. **Efficient Blur**: Uses scale-down/scale-up technique for performance optimization
3. **Smart Caching**: Maintains cache of processed images with automatic cleanup
4. **Signal-driven Updates**: Uses Qt signals for real-time UI updates when settings change 