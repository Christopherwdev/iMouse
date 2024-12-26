# iMouse: Assistive Technology for Precise Cursor Control

iMouse is a Python-based assistive technology application I designed to provide precise mouse control using hand gestures. This project is particularly beneficial for individuals with motor impairments, such as those experiencing conditions like amyotrophic lateral sclerosis (ALS), similar to the challenges faced by the late Stephen Hawking.  iMouse leverages cutting-edge computer vision techniques to translate subtle hand movements into cursor actions, offering a more intuitive and less physically demanding alternative to traditional input methods.
I have also uploaded this project to our school's computer society github page which I am in charge of: [https://github.com/ComputerSocietySPC/iMouse/tree/main](https://github.com/ComputerSocietySPC/iMouse/tree/main) 
It provides more advanced development of our code.

## Features and Functionality

iMouse utilizes the MediaPipe library for real-time hand tracking and OpenCV for webcam video processing. This combination allows for accurate and responsive gesture recognition. The core features include:

- **Cursor Control:** Precisely move the mouse cursor by raising the index finger and thumb. The movement of these fingers directly correlates to cursor movement on the screen. Calibration options allow for personalized sensitivity adjustments.

- **Left-Click Simulation:** Perform a left-click action by closing the thumb against the index finger, mimicking a natural clicking motion.

- **Right-Click Simulation:** Simulate a right-click by bending the index finger towards the palm.

- **Vertical Scrolling:** Efficiently scroll up or down by raising both the index and middle fingers and moving them vertically. The speed of scrolling is proportional to the speed of the hand movement.

- **Tab Switching (Browser):** Navigate between browser tabs by raising all fingers except the thumb and moving the index finger horizontally. Leftward movements switch to previous tabs, while rightward movements switch to subsequent tabs.

- **Customizable Sensitivity:** The script includes adjustable parameters to fine-tune the sensitivity of gesture recognition, accommodating individual needs and preferences. This ensures optimal performance regardless of hand size or movement style.


## System Requirements and Installation

- **Operating System:** Windows, macOS, or Linux (tested on Windows)
- **Python:** Python 3.7 or higher
- **Libraries:**
    ```bash
    pip install opencv-python mediapipe pyautogui pynput keyboard Pillow numpy
    ```

## Usage Instructions

1. **Install Dependencies:** Execute the command above in your terminal or command prompt.

2. **Run the Script:** Run the program using:
    ```bash
    python iMouse.py
    ```
3. **Control the Cursor:** Perform the designated hand gestures to control the mouse cursor and execute actions.

4. **Exit:** Press the 'Esc' key to gracefully terminate the program.

- **Biotechnology Integration Potential:** The core technology behind iMouse has significant potential for integration with broader biotechnology applications. Future development could involve:

    - **EMG Signal Integration:** Combining hand gesture recognition with electromyography (EMG) data could further enhance accuracy and responsiveness, providing a more robust and reliable control system.  [Learn more about EMG](https://en.wikipedia.org/wiki/Electromyography)
    - **Brain-Computer Interface (BCI) Compatibility:** iMouse's modular design could facilitate integration with BCI systems, potentially enabling control through brain signals for individuals with even more severe motor limitations. [Explore BCI research](https://www.braingate.org/)
    - **Personalized Calibration Profiles:** Advanced algorithms could learn and adapt to individual user characteristics, improving accuracy and reducing the need for manual calibration.


## Disclaimer and License

iMouse is provided "as is" without warranty. The author is not responsible for any damages resulting from its use. This project is released under the MIT License.


## Future Development and Contributions

This project is open to contributions and further development. Future enhancements could include:

- Improved gesture recognition algorithms for higher accuracy and robustness.
- Support for additional gestures and actions.
- Integration with other assistive technologies.
- Development of a user-friendly GUI (if somebody is willing to help, please contact us).

You can learn more about my coding projects here: [https://sites.google.com/view/wong-kin-on-christopher/computer-science](https://sites.google.com/view/wong-kin-on-christopher/computer-science)
