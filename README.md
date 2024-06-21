# Bondi: Intergenerational Asynchronous Game

[![Watch the video](https://img.youtube.com/vi/1oRz7jxbk9O_OTCZbscWdY61ZSWOPgCNI/0.jpg)](https://drive.google.com/file/d/1oRz7jxbk9O_OTCZbscWdY61ZSWOPgCNI/view?usp=sharing)

## Welcome to Bondi!

Bondi is an asynchronous game designed to encourage interaction between a grandparent living alone and one of their grandchildren. The technology enables a playful interactive experience between them with the aim of fostering intergenerational bonds.

### Project Overview

We all know how important it is to keep in touch with grandma and grandpa, but we are still not good enough at it. Due to busy daily routines and geographical distances, we find less time to meet and keep in touch. Most of the time, phone calls or visits are seen as chores rather than actions motivated by genuine desire.

Bondi offers an experiential, fun, and non-binding way of communication for both parties, taking place during their free time. The aim is to maintain contact and create a good feeling of togetherness for both.

### How It Works

Bondi is based on the classic game 'Submarines'. Each player has a board in their home. One player, typically the grandmother, places her submarines on her board, acting as the defensive side. The granddaughter, the attacking party, aims to sink the fleet by guessing the locations of the submarines within 25 guesses.

The game uses voice messages sent between the players. The granddaughter records the location on the board where she thinks she is diving and sends it to the grandmother. The recording is received on the grandmother's board, where a white light indicates a new message. The grandmother listens to the recording, marks on her board whether there was a hit or miss, and sends a recording back.

This use of voice messages allows the game to continue over an extended period, fitting into the daily routines of both players.

### Technological Details

- **Components**:
  - Two panels made with a laser cutter
  - 3 buttons on each board
  - 4 LED lights in different colors
  - A microphone and a speaker
  - Raspberry Pi 4 controllers
  - WiFi connection to Google Drive

- **Functionality**:
  - Asynchronously, each player can click the record button to record a voice message.
  - By clicking the send button, the recording is uploaded to Google Drive and sent to the other controller.
  - When a message is received, a white light flashes, and pressing the white button plays the message on the second controller.
  - Each time a message is sent, the previous recording is overwritten, ensuring there are always two audio files in Google Drive, one from each controller.

### Benefits of Intergenerational Interaction

Research shows that maintaining relationships between grandparents and other family members contributes to successful aging. Such connections foster optimism, positivity, a healthy lifestyle, and normal cognitive functioning in the elderly.

### Project Resources

- [Explanatory Video](https://drive.google.com/file/d/1oRz7jxbk9O_OTCZbscWdY61ZSWOPgCNI/view?usp=sharing)
- [Project Blog](https://ergatee.wixsite.com/iot-final-project)

## Getting Started

To set up and run the Bondi project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/bondi.git
   cd bondi
