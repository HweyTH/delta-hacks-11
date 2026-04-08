<div align="center">
  <img src="gallery1.jpg" alt="Sign Streak Banner" width="600" />

  <h1>🤟 Sign Streak</h1>
  
  <strong>Gamified American Sign Language (ASL) Learning Platform</strong>

  <p>
    Built for <strong>DeltaHacks XI</strong>
  </p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow" />
    <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
    <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5" />
  </p>
</div>

---

## 📖 About The Project

Learning a new language can be daunting, and sign language is no exception. **Sign Streak** gamifies the process of learning American Sign Language (ASL) by combining real-time computer vision with a "typing test" style interface. Practice your signing speed and accuracy organically—the faster and more accurately you sign, the higher your score!

### ✨ Key Features

- **Real-Time Sign Recognition**: Translates hand gestures to letters near-instantly using a custom-trained Keras/TensorFlow model and OpenCV.
- **Gamified "Typing" Test**: Prompts the user with letters or words to sign under a time limit.
- **Immediate Visual Feedback**: Highlights correct signs in green and displays corrections for misunderstood signs in red.
- **Detailed Analytics**: Tracks your Words Per Minute (WPM) and Accuracy throughout your session, plotting your performance on an interactive line graph at the end of the test.
- **Sleek GUI**: A beautiful, intuitive cross-platform desktop application built with PyQt5.

---

## 📸 Gallery

Here’s a look at Sign Streak in action:

| **Welcome Screen** | **Preparing to Sign** |
|:---:|:---:|
| <img src="gallery1.jpg" alt="Welcome Screen" width="400"/> | <img src="gallery2.jpg" alt="Ready State" width="400"/> |

| **Correct Sign Detection** | **Incorrect Sign / Feedback** |
|:---:|:---:|
| <img src="gallery3.jpg" alt="Correct Sign" width="400"/><br/>*Successfully signing 'W'* | <img src="gallery4.jpg" alt="Incorrect Sign" width="400"/><br/>*Attempting 'O' but detecting 'K'* |

### Performance Analytics
<p align="center">
  <img src="gallery5.jpg" alt="Analytics page" width="600"/>
  <br/>
  <em>Detailed post-game WPM & Accuracy breakdown using Matplotlib</em>
</p>

---

## 🛠️ Tech Stack

- **Frontend / GUI:** [PyQt5](https://pypi.org/project/PyQt5/)
- **Computer Vision:** [OpenCV (`opencv-python`)](https://opencv.org/) for capturing live webcam feed and preprocessing frames.
- **Machine Learning:** [TensorFlow](https://www.tensorflow.org/) & [Keras](https://keras.io/) for training and running the fine-tuned ASL alphabet classification model.
- **Data Visualization:** [Matplotlib](https://matplotlib.org/) for generating end-of-game performance graphs.
- **Data Processing:** [NumPy](https://numpy.org/)

---

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sign-streak.git
   cd sign-streak
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

---

## 🧠 How It Works

1. **Video Capture:** The application hooks into the user's webcam via OpenCV to read frames frame-by-frame.
2. **Model Inference:** Each frame is processed and passed through a custom TensorFlow/Keras Convolutonal Neural Network (`sign_language_model.h5` / `fine_tuned_sign_language_model.keras`).
3. **Game Loop:** The `PlayerHandler.py` module manages game state, checking user predictions against the target letter. Correct signs progress the prompt, while accuracy and completion times are logged.
4. **Stats Generation:** Upon completion, `stats.py` calculates the net WPM and overall accuracy, utilizing Matplotlib to map the learning curve.

---

*Made with ❤️ for DeltaHacks 11.*
