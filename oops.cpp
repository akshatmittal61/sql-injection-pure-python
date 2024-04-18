#include <iostream>
#include <bits/stdc++.h>

class LivingBeing
{
private:
    int age;
    string name;

public:
    string getName()
    {
        return this.name;
    }
    int getAge()
    {
        return this.age;
    }
    void setName(string name)
    {
        this.name = name;
    }
    void setAge(int age)
    {
        this.age = age;
    }
};

int main()
{
    return 0;
}