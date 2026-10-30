module top(
    input logic clk,
    input logic rst_n,
    input logic button,
    input logic [3:0] X,
    output logic [6:0] seg,
    output logic [7:0] an,
    output logic dp
);

    logic button_pulse;
    logic [6:0] seg0;
    logic [6:0] seg1;

    debouncer u_debouncer(
        .clk(clk),
        .rst_n(rst_n),
        .button(button),
        .pulse(button_pulse)
    );

    mini_calculator u_calculator(
        .clk(clk),
        .rst_n(rst_n),
        .button(button_pulse),
        .X(X),
        .seg0(seg0),
        .seg1(seg1)
    );

    time_multiplexer u_mux(
        .clk(clk),
        .rst_n(rst_n),
        .seg0(seg0),
        .seg1(seg1),
        .seg(seg),
        .an(an),
        .dp(dp)
    );

endmodule
