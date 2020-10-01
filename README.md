# Correos Spain Package Tracking

This integration allows you to retrieve tracking information from the Spain's Correos post service

### Installation

Copy `/custom_components/correos_spain/` folder to `<config_dir>/custom_components/correos_spain/`.

Add a Correos Spain Tracking integration from the UI and fill the form. You can add as new integration as package you want to track.

### Data Provided

Each package sensor provide the following information as attributes:

  * Tracking number
  * Last event
  * Event description
  * Package location
  * Event date
  * Event time
  
The sensor's state is equal to the last event attribute

### Aditional Features

* Notify when a package is in delivery process
* Auto delete sensor when package is delivered if specified

### Disclaimer

All the data is provided by [Sociedad Estatal de Correos y Telégrafos, S.A.](https://www.correos.es/). I'm not related to this company in any way so I'm not responsible of the provided information
