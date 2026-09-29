/* src/main.c */
#include <zephyr/kernel.h>

#ifndef FIRMWARE_VERSION
#define FIRMWARE_VERSION "OLD"
#endif

int main()
{
    printk("Hello World! - %s FIRMWARE - %s\n", FIRMWARE_VERSION, CONFIG_BOARD_TARGET);
    return 0;
}
