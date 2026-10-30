module time_multiplexer #(
    parameter integer SCAN_CYCLES = 100_000
)(
    input logic clk,
    input logic rst_n,
    input logic [6:0] seg0,
    input logic [6:0] seg1,
    output logic [6:0] seg,
    output logic [7:0] an,
    output logic dp
);

    localparam integer WIDTH = (SCAN_CYCLES > 1) ? $clog2(SCAN_CYCLES) : 1;

    logic [WIDTH-1:0] count;
    logic digit;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 0;
            digit <= 0;
        end else if (count == SCAN_CYCLES - 1) begin
            count <= 0;
            digit <= ~digit;
        end else begin
            count <= count + 1'b1;
        end
    end

    always_comb begin
        seg = 7'b1111111;
        an = 8'b11111111;
        dp = 1;
        if (rst_n) begin
            seg = digit ? ~seg1 : ~seg0;
            an = digit ? 8'b11111101 : 8'b11111110;
        end
    end

endmodule
