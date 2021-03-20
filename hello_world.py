# Simple example on how to use the RsInstrument module for remote-controlling yor VISA instrument
# Preconditions:
# - Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument.RsInstrument import RsInstrument

resource_string_1 = 'TCPIP::192.168.0.101::INSTR'  # Standard LAN connection (also called VXI-11)
resource_string_2 = 'TCPIP::192.168.0.101::hislip0'  # Hi-Speed LAN connection - see 1MA208
resource_string_3 = 'GPIB::20::INSTR'  # GPIB Connection
resource_string_4 = 'USB::0x0AAD::0x0119::022019943::INSTR'  # USB-TMC (Test and Measurement Class)
resource_string_5 = 'RSNRP::0x0095::104015::INSTR'  # R&S Powersensor NRP-Z86
instr = RsInstrument(resource_string_2, True, False)

idn = instr.query_str("*IDN?")
print(f"\nHello, I am: '{idn}'")
print(f'RsInstrument driver version: {instr.driver_version}')
print(f'Visa manufacturer: {instr.visa_manufacturer}')
print(f'Instrument full name: {instr.full_instrument_model_name}')
print(f'Instrument installed options: {",".join(instr.instrument_options)}')

# Reset the analyzer, creating channel no. 1 with the default trace Trc1. The trace is displayed in diagram area no. 1.
instr.reset()
instr.visa_timeout = 3000

# Update display continiously for debugging
# instr.write_str("system:display:update on")

# Default value after init is True
# instr.instrument_status_checking = False

# Rename current trace
instr.write_str("configure:trace1:name 'MainTrace'")

# Create new trace
# instr.write_str("calculate1:parameter:sdefine 'TestTrace', 'S11'")

# Switch off the measurement (after one sweep)
instr.write_str("initiate1:continuous off")
# Reduce the number of sweep points
#instr.write_str("sense1:sweep:points 2")

# Avoid a delay time between different partial measurements and before the
# start of the sweeps (is default setting).
#instr.write_str("sense1:sweep:time:auto on")
#instr.write_str("trigger1:sequence:source immediate")

# See calibration state (CAL=calibrated, CAI=calibrated but interpolated, etc.)
#instr.query_str("correction:state?")

# Write current trace to new memory
instr.write_str("trace:copy 'MemoryTrace1', 'MainTrace'")
# Display memory trace on screen (MemoryTrace1 as trace #2)
instr.write_str("display:window:trace2:feed 'MemoryTrace1'")

# Save all traces from channel 1 to file
instr.write_str("mmemory:store:trace:channel 1, 'C:\\Users\\Instrument\\Desktop\\HelloWorld.dat', formatted, complex, point, semicolon")

# Load calibration data
instr.write_str("mmemory:load:correction 1, 'SMA Ideal.cal'")

# Close the session
instr.close()



