module led_blink_tb;
    reg clk;
    wire led;

    //instantiate led_blink mod
    led_blink uut (
        .clk(clk),
        .led(led)
    );

    //clk gen
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        $dumpfile("led_blink_tb.vcd");
        $dumpvars(0, led_blink_tb);


        $monitor($time, ": led = %b", led);

        #200000000 $finish;
    end
endmodule

