Softec System Notifications (SOFNO)
===================================

Sofno will be able to notify Softec's agents when one of their clients computers goes offline.

It will be configurable to notify of a computer failure via text message, phone call patch, or email.

Q? Who will it notify? The agent that installed the computer? Valentin? Jose Luis?

Q? Is this configurable by all of the computers in a restaurant, or per computer?

It will always notify via the web interface.

Features
--------

+ Can call the failed computer's corresponding Softec contact and patch him/her to the restaurant contact (Twilio).
+ Can text failure alerts to Softec agents (Twilio)
+ Can email failure alerts to Softec agents (Email)
+ These combinations are easily configurable
+ Can be set to only notify at sane times of the day
+ Can do geolocation based on the computer's ip and show an approximation of where it is with google maps
+ Can issue remote commands to the client computers

Possible DB Tables
------------------

Contact (Abstract?)
*******************

+ **name** - charField
+ **email** - charField
+ **phone** - charField (11 char max)
+ **type** - charField
+ **notes** - textField
+ **startTime** - DateTimeField
+ **endTime** - DateTimeField

Computer
********

+ **name** - charField
+ **restaurant** - foreignKey to Restaurant
+ **OS** - charField (choice)
+ **POS** - charField (choice)
+ **description** - charField (optional)
+ **online** - booleanField
+ **active** - booleanField
+ **failures** - textField
+ **lastCheckIn** - dateTimeField

Restaurant
**********

+ **contactList** - ForeignKey || CSVField
+ **computerList** - ForeignKey || CSVField
+ **name** - charField
+ **address** - charField
+ **city** - charField
+ **state** - charField (choice)
+ **email** - charField
+ **notes** - textField
+ **active** - booleanField (reject tracking if false)
+ **alert** - booleanField \[track if active, but (do || not)alert \]
+ **agent** - ForeignKey TODO: More than one?
+ **startHours** - DateTimeField
+ **endHours** - DateTimeField
+ **refusalMsg** - charField
