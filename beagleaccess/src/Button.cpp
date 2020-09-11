#include <iostream>
#include <vector>
#include <GpioLine.hpp>
#include <Button.hpp>

using namespace beagleaccess;

static std::vector<GpioLine> buttonLines_g;

void ButtonCtl::initAt(GpioIndex ind) {
    for(auto line : buttonLines_g) {
        if(line.index() == ind) {
            std::cout
                << "Button ( " << GpioLine::chipStr(ind.first)
                << ", " << ind.second << " ) has already been initialized."
                << std::endl;
            return;
        }
    }

    buttonLines_g.push_back(GpioLine());
    buttonLines_g.back().open(ind, false);
}

bool ButtonCtl::isPressed(GpioIndex ind) {
    for(auto line : buttonLines_g) {
        if(line.index() == ind) {
            return line.get() != 0;
        }
    }

    std::cout
        << "No button defined at ( " << GpioLine::chipStr(ind.first)
        << ", " << ind.second << " ).";
    return false;
}

void ButtonCtl::shutDownAt(GpioIndex ind) {
    for(auto it = buttonLines_g.begin(); it != buttonLines_g.end(); ++it) {
        if(it->index() == ind) {
            it->close();
            buttonLines_g.erase(it);
            return;
        }
    }
}
