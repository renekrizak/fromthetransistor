#include "Vled_blink_tb.h"
#include "verilated.h"
#include "verilated_vcd_c.h"


int main(int argc, char **argv, char **env) {
    Verilated::commandArgs(argc, argv);

    Vled_blink_tb* top = new Vled_blink_tb;

    Verilated::traceEverOn(true);
    VerilatedVcdC* tfp = new VerilatedVcdC;
    top->trace(tfp, 99);
    tfp->open("led_blink_tb.vcd");

    vluint64_t main_time = 0;
    top->clk = 0;

    while(!Verilated::gotFinish() && main_time < 20000000) {
        top->clk = !top->clk;
        top->eval();
        tfp->dump(main_time);
        main_time++;
    }

    tfp->close();
    delete top;
    return 0;
}