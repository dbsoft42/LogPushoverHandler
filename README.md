LogPushoverHandler
======
## A Python logging handler to push messages as [Pushover](https://pushover.net) notifications

### What does this do?
If you use the standard Python *logging* module and would like to push some of your messages to [Pushover](https://pushover.net), you may use this custom *handler* to do so easily.

### Installation and setup
Download the files.
```
git clone https://github.com/dbsoft42/LogPushoverHandler.git
```
Put the *LogPushoverHandler.py* file in a place from where it can be imported in your application. This can also be the same directory where your application script resides.

### Usage
Instantiate the handler. Following code snippet shows the necessary and optional parameters.
```python
from LogPushoverHandler import LogPushoverHandler

pushover_handler = LogPushoverHandler(
                    token='your Pushover app token',
                    user='your Pushover user string',
                    **kwargs
                    )
```                         
The *token* and *user* are necessary parameters. You can get these by logging in to your Pushover dashboard.

The **kwargs can be used to add or override any of the parameters that can be sent to Pushover. Please refer to the [Pushover documentation](https://pushover.net/api) for these parameters.

You can also specify your custom Pushover priority mapping here. More on this below.

Here is a sample usage code snippet.
```python
from LogPushoverHandler import LogPushoverHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

pushover_handler = LogPushoverHandler(
                    token='your Pushover app token',
                    user='your Pushover user string'
                    )
pushover_handler.setFormatter(logging.Formatter('%(message)s'))
pushover_handler.setLevel(logging.CRITICAL)
logger.addHandler(pushover_handler)
```

### A Few Pointers
* Although a lot of Pushover parameters can be passed while instantiating the handler, it is recommended to let as many of them as possible come from the log message itself. For example, we automatically get the time the log message was generated and use that (you don't need to format the message to have the time for this to work). Likewise the Pushover notification priority is determined from the log level (details below). However, if you supply any of these parameters while instantiating the handler, those will be used instead. You can see that doing so for some parameters like the timestamp may not be accurate.
* We use the log level to assign the priority for the Pushover notification. Below is the mapping.

  Python Log Level | Pushover Priority
  :----------------|-----------------:
  DEBUG            |-2
  INFO             |-1
  WARNING          |-1
  ERROR            |0
  CRITICAL         |1

* You can override the default priority mapping seen above with your customized mapping by supplying dictionary as the *priorities* parameter to LogPushoverHandler. Pushover priorities are detailed [here](https://pushover.net/api#priority). Here is an example of overriding the default priorities.
```python
my_priorities = {
                'DEBUG':    -2,
                'INFO':     0,
                'WARNING':  0,
                'ERROR':    1,
                'CRITICAL': 2
                }
pushover_handler = LogPushoverHandler(
                    token='your Pushover app token',
                    user='your Pushover user string',
                    priorities = my_priorities
                    )
```
* It is recommended to set the log-level for this to ERROR or higher depending on how your app is set up to write to these levels, so that you can use the Pushover notifications only for the really important things and not get inundated by too many messages. This also important so that you don't exceed your Pushover quota.
* As this handler is only an extension of the standard Python HTTPhandler class, there is no way to check if the request was sent to the Pushover API correctly and their response. So please test your app to ensure that all cases which may send a Pushover notification do so correctly and the notifications are received as expected. In case of repeated incorrect requests, the Pushover API may block access to your IP address temporarily.
