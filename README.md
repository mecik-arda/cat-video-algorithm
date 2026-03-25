Paw Session

Paw Session is a Python-based desktop application designed to provide a centralized hub for cat-related media content. It features a dynamic Nyan Cat border animation, integrated YouTube video fetching, and a standardized image delivery system. The application is optimized for high-resolution displays and includes features such as persistent theme management and interactive UI elements.
Technical Specifications
Border Animation Engine

The application utilizes a multi-threaded animation loop that handles a local GIF asset. To maintain visual consistency, the GIF is pre-processed into four directional frame sets (Right, Down, Left, Up) using the Pillow library. The animation logic calculates window boundaries to rotate the sprite and its orientation at each corner of the application frame.
Visual Effects and UI

    RGB Title Rendering: The application includes a high-frequency color cycling algorithm for the main header, utilizing a custom RGB color palette to demonstrate display color accuracy.

    Standardized Media Feed: All external image assets are processed through ImageOps.fit to a fixed 400x300 resolution using Lanczos resampling. This ensures a stable UI layout regardless of the source image's aspect ratio.

    Interactive Components: Buttons feature dynamic event binding for hover states and integrated audio feedback via the Pygame mixer module.

Network and Persistence

    Asset Management: Uses local GIF assets to ensure functionality in restricted network environments such as Eduroam or behind strict firewalls.

    State Persistence: Theme preferences (Dark/Light mode) are stored in a local settings.json file and loaded during the class initialization.

Dependencies

The following Python libraries are required to run the application:

    Pillow (PIL): For advanced image processing, GIF sequencing, and frame rotation.

    Pygame: For handling audio streams and meow sound effects.

    Requests: For fetching remote cat images and YouTube metadata.

    Tkinter: For the core graphical user interface.

Installation

    Clone the repository to your local machine:
    Bash

    git clone https://github.com/ardamecik/paw-session.git
    cd paw-session

    Install the necessary dependencies:
    Bash

    pip install pillow pygame requests

    Ensure the following files are present in the root directory:

        hub_launcher.py (Main entry point)

        catyy.py (API helper module)

        nyan-cat.gif (Local animation file)

        cat.ico (Application icon)

    Execute the application:
    Bash

    python hub_launcher.py

Usage

    Summon Video: Triggers a browser-based redirect to a trending cat video via the YouTube API.

    Daily Goofy Dose: Requests a random image from a cat API, processes it to the standard resolution, and updates the display.

    Theme Toggle: Switches between Light and Dark themes, updating the UI colors and saving the state for future sessions.

License

This project is developed for educational purposes as part of a Computer Engineering portfolio.