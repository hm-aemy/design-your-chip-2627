module controller(
    input logic clk,
    input logic rst_n,
    input logic button,

    output logic save_A,
    output logic save_B,
    output logic show_result
);

    enum {GET_A,GET_B, SHOW_RESULT} state, next_state;

    always_comb begin : control_logic
        save_A = 0;
        save_B = 0;
        show_result = 0;

        next_state = state;

        case (state)
            GET_A: begin
                if (button) begin
                    save_A = 1;
                    next_state = GET_B;
                end
            end
            GET_B: begin
                if (button) begin
                    save_B = 1;
                    next_state = SHOW_RESULT;
                end
            end
            SHOW_RESULT: begin
                if (button) begin
                    show_result = 1;
                    next_state = GET_A;
                end
            end
            default: next_state=GET_A;
        endcase
    end

    always_ff @(posedge clk) begin
        if (!rst_n) state <= GET_A;
        else    state <= next_state;
    end

endmodule
