import traceback
import adsk.core
import adsk.fusion

app = adsk.core.Application.get()
ui  = app.userInterface

def run(_context: str):
    try:
        sketch = app.activeEditObject
        sel = ui.activeSelections

        orig_sel = adsk.core.ObjectCollection.create()
        for i in range(sel.count):
            orig_sel.add(sel.item(0).entity)

        sel.clear()

        for x in orig_sel:
            if x.objectType != "adsk::fusion::SketchLine":
                continue

            loop = False
            start = None
            while True:
                sel.add(x)
                if start is None:
                    start = x.startSketchPoint
                if x.endSketchPoint == start:
                    loop = True
                    break
                if x.endSketchPoint.connectedEntities.count == 1:
                    loop = False
                    break
                if x.endSketchPoint.connectedEntities.count != 2:
                    raise Exception("Too many connections")
                if x.endSketchPoint.connectedEntities.item(0) != x:
                    x = x.endSketchPoint.connectedEntities.item(0)
                else:
                    x = x.endSketchPoint.connectedEntities.item(1)

            if not loop: # we are at the end iterate backwards to start
                while True:
                    sel.add(x)
                    if x.startSketchPoint.connectedEntities.count == 1:
                        break
                    if x.startSketchPoint.connectedEntities.count != 2:
                        raise Exception("Too many connections")
                    if x.startSketchPoint.connectedEntities.item(0) != x:
                        x = x.startSketchPoint.connectedEntities.item(0)
                    else:
                        x = x.startSketchPoint.connectedEntities.item(1)

    except:
        app.log(f'Failed:\n{traceback.format_exc()}')
