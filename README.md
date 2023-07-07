# znd-remote-controller

This repository contains python classes for communicating with R&S ZND Vector Network Analyzer via LAN. It uses [RsInstrument](https://pypi.org/project/RsInstrument/) package to 
conveniently write queries to the instrument. It wraps different useful query strings as class methods and introduces several custom types. For instance,

```python
    def sweep_set_mode(self, channel: int, sweep_mode: Types.SweepMode):
        self.write(f"initiate{channel}:continuous {sweep_mode.value}")

    def sweep_initiate(self, channel: int):
        self.write(f"initiate{channel}:immediate:dummy")
```

## Details

`Instrument` class provides many useful methods that involve manipulating trace, windows, sweeps, 
button events, and `write` or `query` methods for custom queries to the instrument. This python module was used to automate VNA 
and only implements the subset of available commands.

Additionally, this repository includes the `Servo` and `Stepper` classes, 
which enable serial communication with Arduino-controlled motors. 
The arduino code for these classes can be found in the `servo_controller` and `steppers_controller` folders, respectively.

`znd-rc-notebook-test.ipynb` was used to manually test the `Instrument` class. `znd-rc-notebook.ipynb` Jupyter notebook 
was created which used all these python classes to implement custom automation process, which was used to acquire useful data for the VNA.

`notebooks` folder contains initial attempts to filter and use the data, but the code may not be applicable to other use cases. This is 
the picture of the setup that was supported by this software:

<img src="https://github.com/lnadi17/znd-remote-controller/assets/19193250/b283769e-12a8-4702-8cb6-23c299c79e40" width="400">

## Further Development

This project is closely connected to my Junior Project at University, [ground-penetrating-radar](https://github.com/lnadi17/ground-penetrating-radar), 
which involved creating AI models using GPR data, but didn't involve this much data collection. This project is archived and no further 
development is planned. Feel free to explore the repository and use the code for yourself.
