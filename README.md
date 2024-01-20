# Overview
Are you able to track HP, initiative, and conditions for 5 players and as many monsters as it takes to thwart them? I'm certainly not. Thankfully someone  has created an excellent solution! The **fight_sheet_v1.xlsm**! An excel sheet made to help DMs track all the essentials in an encounter for 5e D&D games. Although it has many features 
(see the original reddit post, and YouTube tutorial for details), it lacked one thing. Monsters! Thankfully all 335 monsters from the SRD are available via API thanks to **5e bits**.

Using python and the openpyxl module I loaded all the SRD monsters into the original fightsheet to create **fight_sheet_v335-SRD.xlsm** and would like to share it with you!

You can find both files in the **Encounter Trackers** directory of this project.
- [fight_sheet_v335-SRD.xlsm](https://github.com/mcclellangg/DND-DE/blob/master/Encounter%20Trackers/fight_sheet_v335-SRD.xlsm)
- [fight_sheet_v1.xlsm](https://github.com/mcclellangg/DND-DE/blob/master/Encounter%20Trackers/fight_sheet_v1.xlsm)

I hope that you enjoy it! 😄

## Sources

### Original encounter tracker by u/cgammage
* [An excel sheet for 5e DMs for tracking initiative, damage and more - reddit post ](https://www.reddit.com/r/DnDBehindTheScreen/comments/32doon/an_excel_sheet_for_5e_dms_for_tracking_initiative/)
    - [Original - Fight Sheet (Dropbox)](https://www.dropbox.com/s/dzdxizp426s6dxg/fight_sheet_v1.xlsm?dl=0)
    - [Original - YouTube tutorial](https://www.youtube.com/watch?v=bkmUClAIZXQ&ab_channel=ChristopherGammage)

### 5e Bits
* [5e SRD API](https://github.com/5e-bits/5e-srd-api)
* [5e SRD database](https://github.com/5e-bits/5e-database/tree/main/src)

## Encounter Tracker Preview
![xlsm preview](https://github.com/mcclellangg/DND-DE/blob/master/images/fight_sheet_preview.png?raw=true)
