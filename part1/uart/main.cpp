#include "Vuart_tb.h"
#include "verilated.h"

/*
    To compile:
    verilator --cc uart_tb.v uart_tx.v uart_rx.v --exe main.cpp --build -o uart_tb --timing
*/
int main(int argc, char **argv) {
    Verilated::commandArgs(argc, argv);
    Vuart_tb* tb = new Vuart_tb;

    while(!Verilated::gotFinish()){
        tb->clk = !tb->clk;
        tb->eval();    
    }
    
    delete tb;
    return 0;

}