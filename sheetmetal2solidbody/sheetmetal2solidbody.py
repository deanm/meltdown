import traceback
import adsk.core
import adsk.fusion
app = adsk.core.Application.get()
ui  = app.userInterface

def run(_context: str):
    try:
        sel = ui.activeSelections
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        tools = adsk.core.ObjectCollection.create()

        for i in range(sel.count):
            x = sel.item(i).entity
            if x.objectType != "adsk::fusion::BRepBody":
                raise Exception("Selection is non-BRepBody: " + x.objectType)
            if not x.isSheetMetal:
                raise Exception("Selection is non-sheetmetal")
            tools.add(x)

        rootComp = design.rootComponent
        boundaryFills = rootComp.features.boundaryFillFeatures
        boundaryFillInput = boundaryFills.createInput(tools, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        boundaryFillInput.creationOccurrence = rootComp.occurrences.item(0)
        for i in range(boundaryFillInput.bRepCells.count):
            boundaryFillInput.bRepCells.item(i).isSelected = True
        boundaryFills.add(boundaryFillInput)

    except:
        app.log(f'Failed:\n{traceback.format_exc()}')
