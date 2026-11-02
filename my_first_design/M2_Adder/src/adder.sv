module adder(
    input logic clk,
    input logic rst_n,
    input logic [3:0] operand,
    input logic save_A,
    input logic save_B,
    output logic [4:0] result
);

    logic [3:0] A;
    logic [3:0] B;

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            A <= 0;
            B <= 0;
        end
        else begin 
            if (save_A) A <= operand;
            if (save_B) B <= operand;
        end
    end
    
    assign result = A + B;
endmodule

