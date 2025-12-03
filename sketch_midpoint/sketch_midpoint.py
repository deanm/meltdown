import traceback
import adsk.core
import adsk.fusion
app = adsk.core.Application.get()
ui  = app.userInterface

def run(_context: str):
    try:
        sketch = app.activeEditObject
        sel = ui.activeSelections
        points = [ ]  # avoid modifying the scene while traversing it
        for i in range(sel.count):
            x = sel.item(i).entity
            if x.objectType != "adsk::fusion::SketchLine":
                raise Exception("Selection is non-SketchLine")
            p0 = x.startSketchPoint.geometry
            p1 = x.endSketchPoint.geometry
            points.append(adsk.core.Point3D.create((p0.x+p1.x)/2, (p0.y+p1.y)/2, (p0.z+p1.z)/2))
        for x in points:
            sketch.sketchPoints.add(x)

    except:
        app.log(f'Failed:\n{traceback.format_exc()}')
