`timescale 1ns/1ps

module uart_tx (
    input wire clk,
    input wire rst,
    input wire tx_start,
    input wire [7:0] tx_data,
    output reg tx,
    output reg tx_busy
);

    parameter CLK_FREQ = 50000000;
    parameter BAUD_RATE = 9600;

    localparam BAUD_DIV = CLK_FREQ / BAUD_RATE;
    localparam IDLE = 0, START = 1, DATA = 2, STOP = 3;

    reg [31:0] baud_cnt;
    reg [3:0] bit_cnt;
    reg [7:0] shift_reg;
    reg [1:0] state;

    always @(posedge clk or posedge rst) begin
        if(rst) begin
            tx <= 1'b1;
            tx_busy <= 1'b0;
            state <= IDLE;
            baud_cnt <= 0;
            bit_cnt <= 0;
        end else begin
            case (state)
                IDLE: begin
                    tx <= 1'b1;
                    tx_busy <= 1'b0;
                    if (tx_start) begin
                        tx_busy <= 1'b1;
                        state <= START;
                        shift_reg <= tx_data;
                        baud_cnt <= 0;
                    end
                end
                START: begin
                    if (baud_cnt < BAUD_DIV) begin
                        baud_cnt <= baud_cnt +1;
                    end else begin
                        baud_cnt <= 0;
                        tx <= 1'b0;
                        state <= DATA;
                        bit_cnt <= 0;
                    end
                end
                DATA: begin
                    if(baud_cnt < BAUD_DIV) begin
                        baud_cnt <= baud_cnt + 1;
                    end else begin
                        baud_cnt <= 0;
                        tx <= shift_reg[0];
                        shift_reg <= shift_reg >> 1;
                        if(bit_cnt < 7) begin
                            bit_cnt <= bit_cnt + 1;
                        end else begin
                            state <= STOP;
                        end
                    end
                end
                STOP: begin
                    if(baud_cnt < BAUD_DIV) begin
                        baud_cnt <= baud_cnt + 1;
                    end else begin
                        baud_cnt <= 0;
                        tx <= 1'b1;
                        state <= IDLE;
                    end
                end
        endcase
    end
    end
endmodule



