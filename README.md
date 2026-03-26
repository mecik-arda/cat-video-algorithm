# Paw Session v2.6

Paw Session is a professional, Python-based desktop application designed as a high-performance hub for cat-related media. Optimized for high-resolution displays, it features advanced API integration, multi-threaded animations, and a customizable user experience.

---

## Key Features

* **YouTube Data API v3 Integration:** Real-time cat video summoning with advanced search algorithms (Popular, Recent, Random).
* **Setup Wizard:** An intuitive first-launch experience that guides users through API configuration.
* **Ghost Mode (Nyan Opacity):** Adjustable transparency for the Nyan Cat border animation, perfect for OLED eye-comfort.
* **ASCII Art Library:** Choose between different cat-themed ASCII styles (Classic, Grumpy, Minimal) directly from settings.
* **Real-time System Logs:** Live monitoring of API requests, blacklist filters, and asset delivery.
* **Multi-Language Support:** Full UI localization for **English (EN)**, **Turkish (TR)**, and **German (DE)**.
* **Theme Management:** Persistent Dark/Light mode synchronization via `settings.json`.

---

## Technical Specifications

### Animation Engine
Utilizes a **multi-threaded loop** to process local GIF assets. The engine pre-calculates window boundaries to rotate the Nyan Cat sprite and its orientation at each corner of the application frame, ensuring zero-lag UI performance.

### Visual & Audio Effects
* **RGB Title Rendering:** High-frequency color cycling algorithm for the main header, optimized for high-refresh-rate displays.
* **Standardized Media Feed:** Remote assets are processed using `ImageOps.fit` with **Lanczos resampling** to maintain a fixed 400x300 layout.
* **Pygame Mixer:** Integrated low-latency audio feedback for interactive components.

---

## Dependencies

Ensure you have Python 3.x installed. The following libraries are required:

```
pip install pillow pygame requests
```
## Installation & Setup

    Clone the repository:
    git clone https://github.com/mecik-arda/cat-video-algorithm.git
    cd cat-video-algorithm

    Run the application:

    python hub_launcher.py

    API Configuration:
    On the first launch, follow the Setup Wizard instructions to obtain and activate your YouTube Data API v3 key.

## Project Structure

    hub_launcher.py: Main entry point containing the core logic and UI.

    catyy.py: API helper module for YouTube and Image fetching.

    settings.json: Local storage for user preferences and API credentials.

    nyan-cat.gif: Core animation asset.

## License

Developed for educational purposes as part of a Computer Engineering portfolio. Created by Arda Meçik.
