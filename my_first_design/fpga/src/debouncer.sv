module debouncer #(
    parameter integer DEBOUNCE_CYCLES = 1_000_000
)(
    input logic clk,
    input logic rst_n,
    input logic button,
    output logic pulse
);

    localparam integer WIDTH = (DEBOUNCE_CYCLES > 1) ? $clog2(DEBOUNCE_CYCLES) : 1;

    (* ASYNC_REG = "TRUE" *) logic button_meta;
    (* ASYNC_REG = "TRUE" *) logic button_sync;
    logic stable;
    logic [WIDTH-1:0] count;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            button_meta <= 0;
            button_sync <= 0;
        end else begin
            button_meta <= button;
            button_sync <= button_meta;
        end
    end

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            stable <= 0;
            count <= 0;
            pulse <= 0;
        end else begin
            pulse <= 0;
            if (button_sync == stable) begin
                count <= 0;
            end else if (count == DEBOUNCE_CYCLES - 1) begin
                stable <= button_sync;
                count <= 0;
                pulse <= button_sync;
            end else begin
                count <= count + 1'b1;
            end
        end
    end

endmodule
