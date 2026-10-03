module full_adder (
    input  logic a,
    input  logic b,
    input  logic cin,
    output logic sum,
    output logic cout
);

    assign {cout, sum} = {1'b0, a} + {1'b0, b} + {1'b0, cin};

endmodule
