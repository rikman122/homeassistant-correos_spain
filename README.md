# Correos Spain Package Tracking

This integration allows you to retrieve tracking information from the Spain's Correos post service

### Installation

Copy `/custom_components/correos_spain/` folder to `<config_dir>/custom_components/correos_spain/`.

Add a Correos Spain Tracking integration from the UI and fill the form. You can add as new integrations as package you want to track.

### Data Provided

Each package sensor provide the following information as attributes:

  * Tracking number
  * Last event
  * Event description
  * Package location
  * Event date
  * Event time
  
The sensor's state is equal to the last event attribute

### Additional Features

* Notify when a package is in delivery process
* Auto delete sensor when package is delivered if specified

### Example Card

![Example Card](https://github.com/rikman122/homeassistant-correos_spain/blob/master/example_card1.png)
![Example Card Popup](https://github.com/rikman122/homeassistant-correos_spain/blob/master/example_card2.png)

```yaml
type: 'custom:auto-entities'
card:
  type: entities
  title: Paquetes
filter:
  include:
    - entity_id: sensor.correos_spain_package_*
      not:
        state: Unknown
      options:
        type: 'custom:multiple-entity-row'
        entity: this.entity_id
        tap_action:
          action: call-service
          service: browser_mod.popup
          service_data:
            title: Seguimiento
            card:
              type: entities
              show_header_toggle: false
              entities:
                - sensor.correos_spain_package_lb925920636be
                - entity: sensor.correos_spain_package_lb925920636be
                  icon: []
                  type: 'custom:multiple-entity-row'
                  show_state: false
                  name: []
                  entities:
                    - attribute: description
                - entity: sensor.correos_spain_package_lb925920636be
                  icon: []
                  type: 'custom:multiple-entity-row'
                  show_state: false
                  name: []
                  entities:
                    - attribute: date
                    - attribute: time
        secondary_info:
          attribute: date
```

### Disclaimer

All the data is provided by [Sociedad Estatal de Correos y Telégrafos, S.A.](https://www.correos.es/) I'm not related to this company in any way so I'm not responsible of the provided information
