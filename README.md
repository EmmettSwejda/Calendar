# Calendar 

Calendar is a django project designed to be ran on a raspberry pi in my living room <br>
the goal this project was to replace my current paper calendar that I end up having to redo every month <br>
taking up a large amount of my time and not dyamically updating everytime a new event is added to my calendar on my phone.

This project allows me to simply input the webcal link as a https link, and have all events displayed.

# Limitations
This project was designed for its application meaning:

- Optimization/Speed is not the main goal
  * Downloading and updating all events not just the current months events everytime the page is reloaded is inefficient
  * Having a single model for events storage is inefficient
- UI/Design is tailored to application
  * No extra menus or tools are added as this is meant to just have one purpose
  * UI is meant to blend into my living room and not grab attention
- Single user only
  * Designed to be ran on a LAN typically accessed by one person
  * Single Webcal configuration, cannot show multiple events from different Webcal links