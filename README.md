# 🎤 **SAM - Voice Assistant** 🤖

A powerful **voice assistant** built using Python! SAM listens to your commands, processes them, and performs various tasks such as searching on Google, Wikipedia, controlling apps, sending WhatsApp messages, and more! 📱💻

---

## 🛠 **Requirements**

Before you start using the voice assistant, make sure you have the following installed:

- **Python 3.x**
- **Required Libraries**:
  - `speech_recognition`
  - `pyttsx3`
  - `wikipedia`
  - `webbrowser`
  - `winshell`
  - `Levenshtein`
  - `fuzzywuzzy`
  - `pywhatkit`
  - `pyautogui`
  - `sqlite3`

### Install the necessary packages:

```bash
pip install SpeechRecognition pyttsx3 wikipedia webbrowser winshell fuzzywuzzy Levenshtein pywhatkit pyautogui
```

---

## 📦 **Features**

- 🎙 **Voice Recognition**: Listen to your voice commands and respond accordingly.
- 📖 **Wikipedia Search**: Search Wikipedia for answers with a single command.
- 🔍 **Google Search**: Perform web searches on Google directly from your voice command.
- 📺 **YouTube Search**: Search and watch videos on YouTube using your voice.
- 🕒 **Time**: Ask the assistant for the current time.
- 🗑 **Recycle Bin**: Empty the Recycle Bin with a command.
- 📱 **WhatsApp Message**: Send WhatsApp messages to your contacts.
- 💻 **App Launching**: Launch installed applications by name.
- 📂 **File Search**: Search for files on your computer based on file types.
- ❓ **Error Handling**: If the assistant doesn't understand the command, it asks for clarification.
  
---

## 📝 **How to Use**

1. **Run the Program**: Start by running the script. 
   
2. **Start Listening**: The assistant will start listening for commands once it’s ready.
   
3. **Give a Command**: Say commands like:
   - "SAM, open YouTube"
   - "SAM, search Wikipedia for Python"
   - "SAM, what's the time?"
   
4. **Command Responses**: SAM will perform the task and provide spoken feedback using text-to-speech.

---

## 📂 **Project Structure**

- `voice_assistant.py` — The main Python script for running the voice assistant.
- `contacts.db` — Database for storing contacts for WhatsApp messaging.
- `apps.txt` — A text file for storing app names and their corresponding app IDs.
- `Whatsapp_contacts.txt` — A file containing contacts for WhatsApp messaging.

---

## 🛠 **How it Works**

The **SAM voice assistant** works by:

1. **Listening to Commands**: 
   - The assistant listens for your voice input using the `speech_recognition` library.
   - After recognizing the speech, it converts it into text for processing.

2. **Processing Commands**: 
   - SAM identifies keywords and matches them to predefined commands.
   - SAM handles commands like opening websites (Google, YouTube), performing searches (Google, Wikipedia), emptying the Recycle Bin, and more.

3. **Responding to the User**:
   - SAM uses the `pyttsx3` library to speak back responses based on the command results.
   - Commands can trigger actions such as opening an app, sending WhatsApp messages, or sharing files.

---

## 📑 **Detailed Command List**

### 📚 **General Commands**

- **Wikipedia Search**:  
  Command: `search Wikipedia for <query>`  
  Example: "SAM, search Wikipedia for Python"  
  Description: Fetches a summary from Wikipedia about the specified query.

- **Google Search**:  
  Command: `search Google for <query>`  
  Example: "SAM, search Google for Python programming"  
  Description: Performs a Google search for the specified query.

- **YouTube Search**:  
  Command: `search YouTube for <query>`  
  Example: "SAM, search YouTube for funny videos"  
  Description: Opens YouTube and searches for the specified query.

- **Current Time**:  
  Command: `what is the time`  
  Example: "SAM, what's the time?"  
  Description: Provides the current system time.

- **Recycle Bin**:  
  Command: `empty the recycle bin`  
  Description: Empties the Recycle Bin on your computer.

---

### 📱 **Messaging and Apps**

- **Send WhatsApp Message**:  
  Command: `send message to <contact_name>`  
  Example: "SAM, send message to John"  
  Description: Sends a WhatsApp message to the specified contact.

- **Open App**:  
  Command: `open <app_name>`  
  Example: "SAM, open YouTube"  
  Description: Launches the specified app.

---

### 📂 **File Search**

- **Search Files**:  
  Command: `search files for <file_type>`  
  Example: "SAM, search files for .pdf"  
  Description: Searches for files on your computer with the specified file extension.

- **Open, Print, or Share File**:  
  Command: `open <file_name>` / `print <file_name>` / `share <file_name>`  
  Description: Opens, prints, or shares the selected file.

---

## 🔧 **Customization**

### App Dictionary (`apps.txt`)
- You can add additional applications to the `apps.txt` file to allow SAM to open more apps.
- The format should be:  
  `app_name, app_id`

---

## 🔒 **Security Considerations**

- **WhatsApp**: Make sure the `Whatsapp_contacts.txt` file is properly secured as it contains phone numbers and contacts.
- **Database**: Ensure that the `contacts.db` file is not exposed to unauthorized users, as it stores important contact information.

---

## 🧑‍💻 **Contributions**

Feel free to fork the repository and submit issues or pull requests. If you encounter any bugs or have feature requests, please create an issue in the GitHub repository.

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
