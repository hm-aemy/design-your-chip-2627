module mini_calculator(
    input logic clk,
    input logic rst_n,
    input logic button,

    input logic [3:0] X,

    output logic [6:0] seg0,
    output logic [6:0] seg1
);

logic save_A;
logic save_B;
logic show_result;
logic [4:0] result;
logic [3:0] tens;
logic [3:0] ones;

controller u_ctrl(
    .clk(clk),
    .rst_n(rst_n),
    .button(button),
    .save_A(save_A),
    .save_B(save_B),
    .show_result(show_result)
);

//complete the rest of the instantiations

endmodule
