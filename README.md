# CommandPad
---
A 5-key macropad with rotary encoder, and rgb LEDs. 


Note: This ReadME is writtern by Syed Ihteshamuddin (human ofc), So if some mistakes are occurred please highlight.   

## Overview 
---
This is my first complete hardware project, I have spent over 20+ hours on this project.

<img width="1029" height="624" alt="CommandPad3dView" src="https://github.com/user-attachments/assets/3494a347-4813-42b4-af7a-1b0767b6cebc" />

---

## Project Gallery

### SCHEMATIC

<img width="1234" height="876" alt="CommandPad_SchmmView" src="https://github.com/user-attachments/assets/9e3bb3bf-4570-4cd5-833f-f71be00758d1" />

I have used global tags in my schematic to make it clean and clear, But Assigning footprints and finding relevant 3d models for the components for me was a very difficult task :) 

---

### PCB LAYOUT

<img width="1046" height="829" alt="PCB_routingView" src="https://github.com/user-attachments/assets/2bb232c8-5da1-4884-be43-256cf412c634" />


<img width="1078" height="870" alt="3dPCB_TopView" src="https://github.com/user-attachments/assets/f8b69f79-b958-4db8-b0ae-0c5877868865" />

I have manually routed the PCB , it was somewhat challenging to overcome the *Board Clearance* issues. The PCB has 0 errors (DRC) except silkscreen warnings. 

---

### CAD Designing 


I was CAD designing FIRST TIME. So, it was not easy for me. I have designed this case in Autodesk Fusion. This design is a "SANDWITCH STYLE MACROPAD" where it consists of two plates; Top plate, Bottom Case and PCB gets sandwiched between them. They are all screwed up with M3 Screws. All the design was done in +0.04 tolerance for better results!


#### Assembly View

<img width="1920" height="722" alt="CommandPad_AssemblyView" src="https://github.com/user-attachments/assets/6ef99a66-ea17-4d34-be62-a46b01b65623" />


#### Top Plate

<img width="569" height="326" alt="Top_Case" src="https://github.com/user-attachments/assets/77172a3f-c33f-4716-9cbe-5c1524efec0b" />


#### Bottom Plate

<img width="575" height="477" alt="Bottom_Case" src="https://github.com/user-attachments/assets/c134f0a8-b3a7-4013-9b66-156bc4ccaa6a" />

---

## BOM - Bill of Materials


| # | Component | Qty | Source |
|---:|---|---:|---|
| 1 | Seeed Studio XIAO RP2040 | 1 | Hack Club Kit |
| 2 | Gateron KS-3 MX Switches | 5 | Hack Club Kit |
| 3 | 1N4148 Through-hole Diodes | 5 | Hack Club Kit |
| 4 | Alps EC11E Rotary Encoder | 1 | Hack Club Kit |
| 5 | SK6812 MINI-E RGB LEDs | 5 | Hack Club Kit |
| 6 | 0.91-inch SSD1306 OLED Display (128×32) | 1 | Hack Club Kit |
| 7 | White DSA Keycaps | 5 | Hack Club Kit |
| 8 | M3×16 mm Screws (trim to 13 mm) | 4 | Hack Club Kit |
| 9 | M3×5 mm × 4 mm Heat-set Inserts | 4 | Hack Club Kit |
| 10 | 3D-Printed Case (Base + Top Plate) | 1 set | Self-fabricated |


## Notes

- **Controller:** Seeed Studio XIAO RP2040.
- **Input:** 5 MX-style mechanical switches and one rotary encoder with push switch.
- **Display:** 0.91-inch SSD1306 OLED, 128×32 resolution.
- **Lighting:** 5 SK6812 MINI-E addressable RGB LEDs.
- **Enclosure:** 3D-printed base and top plate.


---

## Function


| Key / Component | Shortcut / Input | Function |
|---|---|---|
| Key 1 (SW1) | `Ctrl + C` | Copies selected text, files, or items |
| Key 2 (SW2) | `Ctrl + V` | Pastes copied content |
| Key 3 (SW3) | `Ctrl + Z` | Undoes the last action in supported applications |
| Key 4 (SW4) | `Alt + Tab` | Switches between open windows |
| Key 5 (SW5) | `Win + Shift + S` | Opens the Windows screenshot/snipping interface |
| Rotary Encoder (Clockwise) | Volume Up | Increases system volume |
| Rotary Encoder (Counterclockwise) | Volume Down | Decreases system volume |
| Rotary Encoder (Press) | Mute Toggle | Toggles system mute |
| OLED Display | I²C | Displays a greeting and action/status messages |
| 5 × RGB LEDs | Addressable LED control | Provides visual feedback when keys are pressed |
| XIAO RP2040 | CircuitPython + USB HID | Processes inputs and sends keyboard/media commands |

> **status:** The displayed volume percentage is an estimate, not the computer's actual volume reading.


---
## AI Usage

I used AI to gather resources for footprints and 3d models, and also for Firmware. Rest all work is done by me! [ For Proof : You can check Lapse recording ] 

---

## Credits

- **HackClub:** - for organizing the program
- **CircuitPython:** - Python Firmware
- **Hackpad Team:** - for tutorials and resources
- Special thanks to "https://github.com/damnitzhemanth-oss" (hemanth) for personally helping me build this project!

---

## License

OPEN SOURCE, enjoy :) 

( I aint responsible if it turns out to be a time bomb).





