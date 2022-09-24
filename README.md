# [Floorball Tournament](http://vanocniflorbalovyturnaj.pythonanywhere.com/)
### Second version of this project can be found [**here**](https://github.com/Pavlyuchenko/VanocniFlorbalovyTurnaj2.0)

This project was created for my high school's floorball (sport similar to hockey) tournament. There is a simple timer with score for admin. The score and result is sent every 2 seconds to database, so that it can be viewed live on other devices. There are also groups implemented and all the matches are automatically generated based on the previous results.

The app is created using jQuery alongside with plain Javascript on the front end and Flask on the back end. 

### The timer for admin with score
![Timer](/desc_img/Timer.png)

### The match schedule
![Match Schedule](/desc_img/Rozpis.png)

### Group with played matches
![Group](/desc_img/Group.png)

### The knockout stage
![Knockout Stage](/desc_img/knockout_stage.png)
*The matches are made automatically based on the previous matches. The bottom part is made of teams who lost once, so they have another chance.*
<br />
<br />
*Note that the code is quite messy, as it was made under extreme time pressure.*
