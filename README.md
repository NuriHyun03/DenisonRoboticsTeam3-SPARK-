# S.P.A.R.K

The repository contains the necessary operational code for the Strategic Pyro Assault Rescue Kinetic - S.P.A.R.K.
It is a mobile firefighting automaton which detects, approaches, and extinguishes localized fires.


## Purpose
The robot was inspired by the problem of fire incidents in server rooms and data centers. Even a small fire in such a high-stakes location causes service disruption costing companies assets in the millions - not to mention the potential loss of life.

## Current Solutions
Present fire suppression systems include:
- Water Cannons
  Flaw: Large scale water damage to high cost equipment, irretrievable data losses
-  Clean Agent Supression:
  Flaw: Harmful to humans, requiring evacuation, thus service disruptions potentially costing millions

## Our Solution
*S.P.A.R.K*: An atonomous mobile firefighting robot designed to extinguish small-scale localized fires with minimal water damage, no need for evacuation, thus reducing service disruptions, data loss, and costly equipment replacement.

## Files
The files contain code for sensor-activation and actuator-response for the following components:
- IR/Ultrasonic Flame Sensors: To detect the presence of fire.
- Ultrasonic Sensors: To avoid obstacles when robot is mobile.
- Microservo: To adjust the height of the turet in the vertical plane
- Unipolar Stepper Motor: To rotate the turet at the precise angle to aim at the flame.
- DC Pump: To pump water from storage to the hose in the turet to extinguish the fire when detected.
- Drivers: To control the wheels of the mobile base.
