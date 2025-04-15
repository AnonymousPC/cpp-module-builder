#include <chrono>
#include <locale>
#include <print>

int main ( )
{
    std::println("{}", std::chrono::get_tzdb().current_zone()->name());
}