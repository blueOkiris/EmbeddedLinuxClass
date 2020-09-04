import typing
import presentation.app as app
import presentation.display as display

"""
These are just for getting things working.
They can be ignored
"""

def testDisplay(disp : display.Display) -> None:
    disp.print()
    for x in range(min(disp.size()[0], disp.size()[1])):
        disp.setPoint((x, x))
    disp.print()
    disp.clear()
    disp.print()

def testBasicApp(argv : typing.List[str]) -> None:
    cliProcessor = app.CliProcessor(argv)
    if cliProcessor.successful():
        disp = display.Display(cliProcessor.displaySize())
        application = app.CliApplication()
        application.start(simpleDraw, disp)

def simpleDraw(key : str, disp : display.Display) -> None:
    disp.clear()
    
    for col in range(disp.size()[0]):
        disp.setPoint((col, 0))
        disp.setPoint((col, disp.size()[1] - 1))
    
    for row in range(disp.size()[1] - 2):
        disp.setPoint((0, row + 1))
        disp.setPoint((disp.size()[0] - 1, row + 1))
    
    disp.print()