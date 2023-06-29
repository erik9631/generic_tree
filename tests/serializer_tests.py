from typing import List
from tree import Tree
from json_serializer import JsonSerializer

root: Tree
tree_snapshot: List[tuple[str, str, str]] = [
    ["root", "", "root"],
    ["0", "", "root.0"],
    ["title", "Project: SOLARGIS", "root.0.title"],
    ["url", "https://rune.ableneo.com/display/slovensko/Project%3A+SOLARGIS", "root.0.url"],
    ["update_date", "2022-07-15", "root.0.update_date"],
    ["data", "", "root.0.data"],
    ["solargis", "", "root.0.data.solargis"],
    ["Project Basics", "", "root.0.data.solargis.Project Basics"],
    ["PV configurator", "", "root.0.data.solargis.Project Basics.PV configurator"],
    ["value", "editing tool for definition of PV power plants layout and parameters, needed for detailed PV output simulation\n- editing tool for definition of site conditions (terrain properties, shading objects)\n- graphical tool for visualization of designed power plant in interaction together with surrounding terrain and shading objects\n- graphical tool for visualization of preliminary simulation results in detail needed for power plant design fine-tuning\n- set of wizards, which helps users understand on-site conditions and include them into power plant design\n- optimization tool for matching electricity requirements to power plant generation\n- economy calculator where basic financing scenarios can be estimated in respect to electricity production forecasts\n- generator of configuration requests, which can be automatically/repeatedly called via existing Solargis API\n", "root.0.data.solargis.Project Basics.PV configurator.value"],
    ["WebApps", "", "root.0.data.solargis.Project Basics.WebApps"],
    ["value", "WebApps is general name for all web applications in Solargis - Prospect, Evaluate, Monitor, Forecast\nEvaluate, Monitor, Forecast are only planned apps and PV Configurator will be a part of Evaluate\nThere is just work on FE and BE of Prospect for now in our team\nProspect is a tool for an analysis of your specific PV site based on data averages", "root.0.data.solargis.Project Basics.WebApps.value"],
    ["Data analytics", "", "root.0.data.solargis.Project Basics.Data analytics"],
    ["value", "Development of analytic tools for automatic recognition of issues in solar measurements (shading, snow,  misalignment…)", "root.0.data.solargis.Project Basics.Data analytics.value"],
    ["Customer", "", "root.0.data.solargis.Customer"],
    ["value", "Data and software architects for bankable solar investments\nSince 2010 Solargis develops and operates platform for fast access to historical, recent, and forecast data for almost any location on the Earth. On several occasions, our solar resource database has been independently identified as the most accurate and reliable. Our customers value our rigorous and systematic validation approach, resulting in low data uncertainties. Hundreds of customers worldwide use our photovoltaic software applications and web-based solutions to optimise construction, evaluation and management of solar power assets.\nOur mission is to:\nSupply the most accurate and reliable solar data in the market\nSimplify the process of energy assessment\nEnable solar investors to maximise profitability\nCreate transparency and reduce risk throughout the project lifecycle", "root.0.data.solargis.Customer.value"],
]


def traverse(node: Tree):
    if len(tree_snapshot) > 0:
        key, value, path = tree_snapshot.pop(0)
        assert path == node.path
        assert node.value == value
        assert node.key == key
        assert node.root is root


def test_load_outlined_json():
    global tree_snapshot
    global root
    serializer = JsonSerializer()
    root = serializer.deserialize('test_data/inputData2.json')
    root.top_down_traverse(traverse)
