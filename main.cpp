import std;

int main ( )
{
    auto str = std::string("Hello");
    std::println("{}", typeid(str).name());    
}