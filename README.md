# Telegram Bot for Lifecell Tariff Recommendation

This repository contains the source code for a Telegram bot built with Python that provides tariff recommendations for Lifecell, a leading mobile network operator in Ukraine.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Lifecell Tariff Recommendation Bot is designed to assist users in selecting the most advantageous tariff plan based on their needs. The bot interacts with users through Telegram and asks a series of questions to gather information about their usage patterns. It then analyzes the data and provides personalized recommendations.

## Features

- User-friendly interaction through a Telegram bot interface
- Personalized tariff recommendations based on user preferences
- Integration with Lifecell's tariff database for up-to-date information
- Support for multiple languages
- Easy-to-use and extendable codebase

## Installation

To run the bot, follow these steps:

1. Clone this repository to your local machine using the following command:

   ```shell
   git clone https://github.com/managerof/GameOFTeens2023_PYTHON
   ```
2. Navigate to project folder:
   ```shell
   cd GameOFTeens2023_PYTHON
   ```
3. Once you have installed the bot open the main.py file and change 'BOT_API_KEY' to your own:
    ```shell
    bot = telebot.TeleBot('BOT_API_KEY')
    ```
4. Run the bot:
    ```shell
    python main.py
    ```


## Usage
Once the bot is up and running, users can interact with it through Telegram. The bot will greet users and help them to find best phone-package. Users will be prompted to answer a series of questions about their usage requirements, such as internet usage, call minutes, and budget. Based on the responses, the bot will provide a personalized tariff recommendation using built-in neural network.

Users can also update their information by sending commands or interacting with the bot's menu options.

## Contributing
Contributions to the Lifecell Tariff Bot are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository on GitHub.

2. Clone your forked repository to your local machine.

3. Create a new branch for your feature or bug fix.

4. Make your changes and commit them with descriptive commit messages.

5. Push your changes to your forked repository.

6. Submit a pull request to the main repository.

Please ensure that your contributions align with the project's coding style, guidelines, and licensing.

## License
The Lifecell Tariff Bot is open-source software released under the MIT License.

Feel free to customize this guide page based on your specific bot implementation and project requirements.
