`timescale 1ns/1ps
module uart_tb;

    reg clk;
    reg rst;
    reg tx_start;
    reg [7:0] tx_data;
    wire tx;
    wire tx_busy;
    wire [7:0] rx_data;
    wire rx_done;

    parameter CLK_FREQ = 50000000;
    parameter BAUD_RATE = 9600;
    parameter CLK_PERIOD = 20;

    initial clk = 0;
    always #(CLK_PERIOD/2) clk = ~clk;


    uart_tx #(.CLK_FREQ(CLK_FREQ), .BAUD_RATE(BAUD_RATE)) uart_tx_inst (
        .clk(clk),
        .rst(rst),
        .tx_start(tx_start),
        .tx_data(tx_data),
        .tx(tx),
        .tx_busy(tx_busy)
    );

    uart_rx #(.CLK_FREQ(CLK_FREQ), .BAUD_RATE(BAUD_RATE)) uart_rx_inst (
        .clk(clk),
        .rst(rst),
        .rx(tx),
        .rx_data(rx_data),
        .rx_done(rx_done)
    );

    initial begin

        rst = 1;
        tx_start = 0;
        tx_data = 8'h00;
        #100;
        rst = 0;

        #1000;

        tx_data = 8'hA5;
        tx_start = 1;
        #CLK_PERIOD;
        tx_start = 0;

        wait(rx_done);

        if(rx_data == 8'hA5) begin
            $display("Test passed: Received data = %h", rx_data);
        end else begin
            $display("Test failed: Received data = %h", rx_data);
        end
        $finish;

    end
endmodule