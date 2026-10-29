## Arty A7-100T - Full Adder

## Switches
set_property -dict { PACKAGE_PIN C11 IOSTANDARD LVCMOS33 } [get_ports {a}]
set_property -dict { PACKAGE_PIN C10 IOSTANDARD LVCMOS33 } [get_ports {b}]
set_property -dict { PACKAGE_PIN A10 IOSTANDARD LVCMOS33 } [get_ports {cin}]
## LEDs
set_property -dict { PACKAGE_PIN H5 IOSTANDARD LVCMOS33 } [get_ports {sum}]
set_property -dict { PACKAGE_PIN J5 IOSTANDARD LVCMOS33 } [get_ports {cout}]