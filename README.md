# 🕐 Time Reminder

A modern, elegant time-based reminder system with playlist support and automated scheduling. Perfect for schools, factories, offices, or any environment requiring scheduled audio notifications.

![Time Reminder Screenshot]([screenshot.png](https://github.com/ChandupaJay1/Time-Reminder/blob/c0b231d6c0e25b628c8e42395b17442ae9dcafd7/Screenshot%202025-07-25%20010336.png))

## ✨ Features

### 🎯 **Core Functionality**
- **CSV-based scheduling** - Easy to configure reminder times and audio files
- **Real-time monitoring** - Precise time-based triggers with visual feedback
- **Multiple audio formats** - Supports MP3, WAV, and other common audio formats
- **Cross-platform compatibility** - Works on Windows, macOS, and Linux

### 🎵 **Advanced Audio Features**
- **Playlist support** - Automatically plays sequential audio tracks
- **Continuous playback** - Seamless transitions between playlist items
- **Manual playlist trigger** - Test playlists anytime with dedicated button
- **Multiple audio fallbacks** - Uses pygame, system audio, or native audio APIs

### 🖥️ **Modern UI**
- **Dark theme interface** - Professional, easy-on-the-eyes design
- **Real-time clock display** - Always shows current time prominently
- **Live status updates** - Visual indicators for system state
- **Progress tracking** - Shows completed vs. total reminders
- **Activity logging** - Detailed log of all system activities

### 🤖 **Smart Automation**
- **Auto-completion detection** - Knows when all reminders are finished
- **Automatic shutdown** - Closes program 1 minute after all reminders complete
- **Center window positioning** - Professional appearance on any screen size
- **Error handling** - Graceful handling of missing files or audio issues

## 🚀 Quick Start

### Prerequisites
```bash
pip install pygame tkinter
```

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/time-reminder.git
   cd time-reminder
   ```

2. **Prepare your audio files**
   - Place all audio files in the same directory as `main.py`
   - Supported formats: MP3, WAV, OGG

3. **Configure your schedule**
   - Edit `reminders.csv` with your desired schedule (see format below)

4. **Run the application**
   ```bash
   python main.py
   ```

## 📋 CSV Format

Create a `reminders.csv` file with the following format:

```csv
time,name,sound
07:30,First Bell,school bell sound effect.mp3
07:43,National Anthem,sri-lanka-matha-national-anthems.mp3
07:45,Work Start Bell,school bell sound effect.mp3
12:00,Lunch Break,lunch-bell.mp3
17:35,End of Day,closing-bell.mp3
```

### CSV Fields:
- **time**: Time in HH:MM or HH:MM:SS format (24-hour)
- **name**: Description of the reminder
- **sound**: Filename of the audio file to play

## 🎵 Playlist Feature

The system includes special playlist functionality for continuous audio playback:

### Automatic Playlist Trigger
When a reminder named **"Karaniya Meththa Suthraya"** is triggered, it automatically starts an 8-track playlist for continuous 31:45 minute playback.

### Manual Playlist Control
Use the **"🎵 Start Playlist"** button to manually trigger the playlist anytime.

### Playlist Configuration
Edit the playlist files in the code:
```python
playlist_files = [
    "karaneeya-meththa-suthraya.mp3",
    "track1.mp3",  # Replace with your actual filenames
    "track2.mp3",
    "track3.mp3",
    "track4.mp3",
    "track5.mp3",
    "track6.mp3",
    "track7.mp3",
    "track8.mp3"
]
```

## 🎛️ Usage

### Starting the System
1. **Launch the application** - Double-click `main.py` or run from terminal
2. **Review your schedule** - Check the "Upcoming Reminders" section
3. **Click "Start Monitoring"** - Begin automatic reminder monitoring
4. **Optional**: Use "Start Playlist" for manual playlist testing

### During Operation
- **Monitor status** - Watch the Status section for current system state
- **Check activity log** - Review all triggered reminders and system events
- **View progress** - Track completion percentage in real-time

### Automatic Completion
- System automatically detects when all reminders are completed
- Shows "All reminders completed - Closing in 1 min" message
- Automatically closes after 60-second countdown

## 🔧 Customization

### Audio Settings
The system supports multiple audio playback methods with automatic fallbacks:
- **pygame.mixer.music** (primary)
- **pygame.mixer.Sound** (secondary)
- **System audio commands** (fallback)

### UI Customization
Modify colors and styling in the `ModernReminder` class:
```python
# Color scheme
bg_primary = "#0f0f23"    # Main background
bg_secondary = "#1a1a2e"  # Card backgrounds  
accent_color = "#64ffda"  # Accent elements
```

### Window Settings
Adjust window size and positioning:
```python
window_width = 700
window_height = 600
```

## 🏢 Use Cases

### Educational Institutions
- **Class period bells** - Automated school bell system
- **Break notifications** - Recess and lunch reminders
- **Assembly announcements** - Special event notifications

### Industrial/Corporate
- **Shift changes** - Work period transitions
- **Break times** - Rest period notifications
- **Safety announcements** - Scheduled safety reminders

### Religious/Cultural
- **Prayer times** - Automated prayer call system
- **Ceremony schedules** - Event timing coordination
- **Cultural programs** - Performance and activity timing

## 🛠️ Troubleshooting

### Audio Issues
- **No sound playing**: Check if audio files exist in the correct directory
- **File not found errors**: Verify audio file names match CSV entries exactly
- **Audio cutting off**: Increase timeout values in `play_sound()` function

### CSV Issues
- **No reminders loading**: Ensure CSV has proper headers (time,name,sound)
- **Time format errors**: Use HH:MM or HH:MM:SS format (24-hour)
- **Encoding issues**: Save CSV as UTF-8 encoding

### System Issues
- **Window not centering**: Check screen resolution compatibility
- **High CPU usage**: Reduce monitoring frequency if needed
- **Memory issues**: Clear old log entries periodically

## 📱 System Requirements

### Minimum Requirements
- **Python 3.6+**
- **tkinter** (usually included with Python)
- **pygame 2.0+**
- **50MB available disk space**
- **Audio output device**

### Recommended Requirements
- **Python 3.8+**
- **4GB RAM**
- **Speakers or headphones**
- **1920x1080+ display resolution**

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Areas for Contribution
- **Additional audio format support**
- **Web-based configuration interface**
- **Mobile app companion**
- **Database integration**
- **Multi-language support**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **pygame community** for excellent audio handling
- **tkinter team** for the GUI framework
- **Contributors** who help improve this project

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/time-reminder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/time-reminder/discussions)
- **Email**: your.email@example.com

---

**Made with ❤️ for automated scheduling needs**

*Star ⭐ this repository if you find it helpful!*
