#include <iostream>
#include <vector>
#include <utility>
#include <GpioLine.hpp>
#include <Button.hpp>

using namespace beagleaccess;

static std::vector<ButtonLine> buttonLines_g;

void ButtonCtl::initAt(GpioIndex ind, bool activeLow) {
    for(auto line : buttonLines_g) {
        if(line.first.index() == ind) {
            std::cout
                << "Button ( " << GpioLine::chipStr(ind.first)
                << ", " << ind.second << " ) has already been initialized."
                << std::endl;
            return;
        }
    }

    buttonLines_g.push_back(std::make_pair(GpioLine(), activeLow));
    buttonLines_g.back().first.open(ind, false);
}

bool ButtonCtl::isPressed(GpioIndex ind) {
    for(auto line : buttonLines_g) {
        if(line.first.index() == ind) {
            if(line.second) {
                return line.first.get() != 0;
            } else {
                return line.first.get() == 0;
            }
        }
    }

    std::cout
        << "No button defined at ( " << GpioLine::chipStr(ind.first)
        << ", " << ind.second << " ).";
    return false;
}

void ButtonCtl::shutDownAt(GpioIndex ind) {
    for(auto it = buttonLines_g.begin(); it != buttonLines_g.end(); ++it) {
        if(it->first.index() == ind) {
            it->first.close();
            buttonLines_g.erase(it);
            return;
        }
    }
}
