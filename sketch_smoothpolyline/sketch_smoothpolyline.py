import traceback
import adsk.core
import adsk.fusion

app = adsk.core.Application.get()
ui  = app.userInterface

def run(_context: str):
    try:
        sketch = app.activeEditObject
        sel = ui.activeSelections
        if sel.count is not 1:
            raise Exception("Non single selection")

        start = None

        x = sel.item(0).entity
        if x.objectType != "adsk::fusion::SketchLine":
            raise Exception("Selection is non-SketchLine")

        points = adsk.core.ObjectCollection.create()
        lines = adsk.core.ObjectCollection.create()
        loop = False
        while True:
            lines.add(x)
            points.add(x.startSketchPoint)
            if start is None:
                start = x.startSketchPoint
            if x.endSketchPoint == start:
                loop = True
                app.log("found loop " + str(points.count))
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

        if loop:
            points.add(points[0])
            points.add(points[1])
            points.add(points[2])
            points.add(points[3])
        else:
            app.log("Doing non-loop")
            points = adsk.core.ObjectCollection.create()
            lines = adsk.core.ObjectCollection.create()
            x = sel.item(0).entity

            # iterate backwards, find start of non-loop
            while True:
                if x.startSketchPoint.connectedEntities.count == 1:
                    break
                if x.startSketchPoint.connectedEntities.count != 2:
                    raise Exception("Too many connections")
                if x.startSketchPoint.connectedEntities.item(0) != x:
                    x = x.startSketchPoint.connectedEntities.item(0)
                else:
                    x = x.startSketchPoint.connectedEntities.item(1)

            # go forward from start to end
            while True:
                lines.add(x)
                points.add(x.startSketchPoint)
                if x.endSketchPoint.connectedEntities.count != 2:
                    points.add(x.endSketchPoint)
                    break
                if x.endSketchPoint.connectedEntities.item(0) != x:
                    x = x.endSketchPoint.connectedEntities.item(0)
                else:
                    x = x.endSketchPoint.connectedEntities.item(1)
            app.log("Non-loop " + str(points.count))

        if len(points) < 4:
            raise Exception("Too few line segments")

        for i in range(len(points)-3):
            p0 = points[i+0].geometry
            p1 = points[i+1].geometry
            p2 = points[i+2].geometry
            p3 = points[i+3].geometry

            # in theory we are in 2d but just do the full 3d
            c0x = (p2.x / 6) + p1.x - (p0.x / 6);
            c0y = (p2.y / 6) + p1.y - (p0.y / 6);
            c0z = (p2.z / 6) + p1.z - (p0.z / 6);
            c1x = (p3.x / -6) + p2.x + p1.x / 6;
            c1y = (p3.y / -6) + p2.y + p1.y / 6;
            c1z = (p3.z / -6) + p2.z + p1.z / 6;

            sketch.sketchCurves.sketchControlPointSplines.add([
                points[i+1], 
                adsk.core.Point3D.create(c0x, c0y, c0z),
                adsk.core.Point3D.create(c1x, c1y, c1z),
                points[i+2]], 3)

        sel.clear()
        for x in lines:
            sel.add(x)

    except:
        app.log(f'Failed:\n{traceback.format_exc()}')
