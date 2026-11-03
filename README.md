# Patchwork PCR: flexible PCR preparation on the Opentrons OT-2

Patchwork PCR combines an interactive 96-well selection interface with a customizable Python protocol template for PCR reaction preparation on an Opentrons OT-2.

Select individual source wells without filling complete rows or columns, configure liquid-handling parameters, and generate a Python protocol that distributes master mix and transfers the selected samples into temperature-controlled destination tubes.

This workflow prepares PCR reactions; it does not perform PCR thermocycling.

> Status: research code requiring review and validation before robot use. The current source contains implementation issues documented below. Documentation describes both implemented behavior and intended functionality; it does not establish experimental validation.

<details>
<summary>Project metadata and provenance</summary>

| Field | Description |
| --- | --- |
| Project | Opentrons Patchwork PCR |
| Repository | https://github.com/JanWoyzi/Opentrons_Patchwork_PCR |
| Script directory | https://github.com/JanWoyzi/Opentrons_Patchwork_PCR/tree/main/Scripts |
| Repository owner | JanWoyzi |
| Template author metadata | JW |
| Protocol name in template | PCR-Prep |
| Robot | Opentrons OT-2 |
| Protocol API level declared in template | 2.13 |
| Interface | Python desktop application using QtPy and a compatible Qt binding |
| Inputs | Protocol template, selected source wells, numerical run parameters |
| Output | Generated Python protocol for the OT-2 |
| Keywords | PCR preparation; liquid handling; OT-2; cherry-picking; 96-well plate; laboratory automation; research software |
| Documentation reviewed | 2026-11-03 |
| Source snapshot reviewed | a13895ae0e9da24b68667e0dd77ae8a3fda00cfa |
| Validation status | Source inspection only; no simulation or physical execution performed for this documentation |
| License | Check the repository license before reuse; no license is assigned by this README |

For reproducibility, record the exact commit, generated protocol, source-well selection, labware definitions, software versions, and experimental validation associated with each run.

</details>

## Scripts and their responsibilities

### `Patchwork_PCR.py`: graphical well selection and protocol generation

This desktop application displays an 8 × 12 plate layout covering wells A1–H12. Each well can be selected or deselected independently. Selected wells appear green, allowing scattered samples to be chosen without rearranging the source plate first.

The application:

- Provides plate tabs for selecting samples from multiple source plates.
- Offers input fields for aspiration and dispensing flow rates, movement-speed control, aspiration height, sample volume, master-mix volume, and module temperature.
- Reads a user-selected protocol template.
- Encodes each selected source as a plate identifier and well name, such as `1_A1`.
- Replaces the template placeholders with the entered values and selected sources.
- Saves the resulting protocol as a Python file.

The application generates a protocol file; it does not directly connect to or operate the robot.

### `Template_PCR.py`: OT-2 PCR preparation logic

The filename is case-sensitive: the repository uses `Template_PCR.py`.

This file defines `run(protocol)` and contains the robot instructions. It is a generation template rather than a ready-to-run protocol: placeholders must first be replaced by the graphical application or another controlled generation process.

Its workflow is:

1. Load source plates, tip racks, the master-mix block, two Temperature Modules, and pipettes.
2. Apply configured P20 aspiration and dispensing flow rates.
3. Set the first Temperature Module to the requested temperature; also set the second when more than 96 samples are selected.
4. Calculate how many master-mix aliquots fit within a nominal 20 µL aspiration.
5. Distribute master mix into sequential destination wells, including a smaller final batch when required.
6. Set the aspiration clearance above the source-well bottom.
7. Transfer selected samples into the corresponding destination wells, using a fresh tip for each sample transfer.

A P300 single-channel Gen2 is loaded on the left mount but is not used for liquid transfers in the current template. The P20 single-channel Gen2 on the right performs the transfers.

## Why use a Python template rather than Protocol Designer alone?

The reason for this project is the combination of experiment-specific selection and programmable liquid-handling behavior—not a claim that Protocol Designer cannot select wells or perform routine transfers.

Protocol Designer provides a graphical authoring workflow. Here, a dedicated interface captures changing sample selections while the Python template preserves the underlying preparation logic. Users can change which scattered samples to process without manually rebuilding the transfer sequence for every run.

The template makes the following behavior explicit and editable:

| Template feature | Purpose in this workflow |
| --- | --- |
| Source labels resolved through a plate-to-labware mapping | Converts arbitrary selected wells into robot source locations. |
| Sequential destination assignment | Consolidates scattered source samples into a compact reaction layout. |
| Conditional use of a second temperature-controlled destination | Adapts the intended workflow to selections exceeding one 96-position destination. |
| Calculated master-mix batching and remainder handling | Adapts aspiration and dispensing cycles to reaction count and aliquot volume. |
| Separate aspiration and dispensing flow rates | Allows liquid-handling behavior to be adjusted for the preparation. |
| Temporary `protocol.max_speeds['a']` changes around selected moves | Exposes targeted movement control directly in the protocol. |
| Explicit `move_to()` positions and source aspiration clearance | Makes selected movement positions and aspiration geometry visible for adjustment. |
| Different tip strategies for master mix and samples | Uses one tip during master-mix distribution and fresh tips for sample transfers. |

These features explain the value of a dedicated Python workflow for this project. Individual capabilities may overlap with Protocol Designer, and its available features can change; the distinguishing benefit is keeping selection, calculation, conditional logic, and motion settings together in an inspectable template.

The template does not include mixing, thermocycling, automatic liquid-level tracking, or a final module-deactivation step.

## Default deck configuration

The template—not the graphical deck dropdowns—currently determines the actual deck configuration.

| OT-2 slot | Template assignment |
| --- | --- |
| 1 | Source plate 1: `suedlaborpink_96_wellplate_200ul` |
| 2 | Source plate 2: `suedlaborgreen_96_wellplate_200ul` |
| 3 | Temperature Module Gen2 with `nest0.2mlpcr8striptubes_96_aluminumblock_200ul` destination labware |
| 4 | Source plate 3: `nest0.2mlpcr8striptubes_96_aluminumblock_200ul` |
| 5 | Source plate 4: `suedlabororange_96_wellplate_200ul` |
| 6 | Temperature Module Gen2 with `nest0.2mlpcr8striptubes_96_aluminumblock_200ul` destination labware |
| 7 | `opentrons_96_filtertiprack_20ul` |
| 8 | Master-mix block: `sarstedtsafeseal_24_aluminumblock_2000ul`; master mix is aspirated from A1 |
| 9 | Unused |
| 10 | `opentrons_96_filtertiprack_20ul` |
| 11 | `opentrons_96_filtertiprack_20ul` |

Make all required labware definitions available in the target Opentrons environment. Matching names alone do not establish that the definitions match the physical labware.

## Parameters and defaults

| GUI parameter | Default | Unit | Template placeholder |
| --- | --- | --- | --- |
| Aspiration flow rate | 4 | µL/s | `f_r_asp` |
| Dispensing flow rate | 4 | µL/s | `f_r_dis` |
| Maximum a-axis speed | 2 | mm/s | `m_s` |
| Source aspiration clearance | 3.5 | mm above well bottom | `w_b_c` |
| Sample transfer volume | 2 | µL per reaction | `t_v` |
| Master-mix transfer volume | 8 | µL per reaction | `m_v` |
| Module target temperature | 7 | °C | `temp_mod` |
| Selected source labels | User selection | Plate identifier and well name | `t_c_l` |

The default nominal reaction volume is 10 µL: 8 µL master mix plus 2 µL sample. Defaults are software settings, not experimentally validated recommendations.

## Requirements and use

### Requirements

- Python with `qtpy` and a compatible Qt binding for the desktop application.
- An Opentrons execution environment supporting the template's declared API level, subject to compatibility testing.
- The labware, modules, pipettes, tips, and matching labware definitions specified by the template.
- Sufficient reagent volume, including experimentally determined dead volume and handling losses.

The reviewed scripts do not specify a tested Python, Qt binding, or Opentrons App version. Record these versions when establishing a working environment.

### Workflow

1. Download both scripts and establish a compatible Python/Qt environment.
2. Launch `Patchwork_PCR.py` with Python.
3. Choose `Template_PCR.py` using “Select template file...”.
4. Enter the desired numerical parameters in the “Opentrons” tab.
5. Select individual source wells in the plate tab.
6. To add another source-plate tab, double-click the “Opentrons” tab. Double-clicking a plate tab after the first plate removes that tab.
7. Enter the correct source identifier for each plate tab; see the mapping below.
8. Click “Generate protocol!” and select the output Python file when prompted.
9. Inspect and simulate the generated protocol, resolve the known issues below, and verify the physical deck before execution.

The separate “Set protocol location...” button opens a save dialog, but its returned path is not retained. Generation opens its own save dialog.

### Source identifier mapping

Although the plate field is labeled “OT2 slot location,” the generated source identifier is used as a dictionary key, not directly as a deck-slot number:

| Entered source identifier | Actual template source slot |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 4 |
| 4 | 5 |

Only identifiers 1–4 are supported by the current template. Adding more GUI tabs does not add robot labware automatically.

Selected sources are collected by tab and widget traversal, not by the order in which wells were clicked. Check the generated source list when documenting sample-to-destination relationships. The application does not export a separate sample-mapping table.

## Known issues and validation requirements

The current source should not be presented as ready for unattended execution.

- Master-mix batching uses floating-point results in `range()`. `divmod(20, master_vol)` produces floats when the volume is a float, and `/` produces a float in Python 3. The current `range()` arguments therefore require correction to appropriate integer counts before execution.
- Second-destination sample indexing is inconsistent. Master-mix dispensing starts at destination index 0, but sample transfer uses `index - 95`. For the 97th sample this selects index 1 rather than 0, and at 192 samples it attempts index 96, outside a 96-well destination. Review and correct this mapping before using the second destination.
- Empty selections are not safely rejected. Placeholder substitution leaves an empty string entry rather than a true empty source list, which can fail during source parsing.
- Input validation is incomplete. GUI validators allow zero for volumes and rates and do not enforce a complete, physically valid experiment. Zero master-mix volume causes division by zero. Empty fields and unsupported source identifiers also require checks.
- Deck dropdowns are not connected to protocol generation. Changing them does not modify `load_labware()` or module assignments in the template.
- Capacity is not enforced. The intended destination capacity is 192 reactions, but the interface does not enforce this or confirm sufficient tips and reagents.
- Master-mix distribution reuses one tip. Assess whether the dispensing positions and workflow are suitable for the required contamination-control standard.
- Module shutdown and post-run handling are not specified. Define the required end-of-run temperature and operator actions.

Validate source mapping, destination order, volume calculations, tip usage, liquid-handling settings, labware geometry, and module behavior through simulation and an appropriate laboratory verification procedure. Successful file generation alone is not evidence that a protocol is executable or experimentally suitable.

## Applying the FAIR principles

This documentation applies Findable, Accessible, Interoperable, and Reusable principles to the scripts and their experimental provenance. It supports FAIR practice but does not claim complete FAIR compliance.

| Principle | Application here | Further work for stronger implementation |
| --- | --- | --- |
| Findable | Descriptive project title, keywords, script roles, repository links, and source snapshot identifier. | Archive versioned releases with a persistent identifier; add machine-readable metadata such as `codemeta.json` and citation metadata. |
| Accessible | Plain-text Python scripts and Markdown documentation accessible through the repository. | Preserve releases and metadata in a long-term archive; document any access restrictions. |
| Interoperable | Explicit API level, labware identifiers, units, input conventions, and generated Python output. | Distribute custom labware definitions and a tested dependency specification; define a structured sample-to-destination mapping format. |
| Reusable | Documented parameters, deck setup, workflow, limitations, and provenance requirements. | Provide a clear license, citation instructions, tests, corrected and validated example protocols, and environment/version records. |

For each experiment, preserve the exact generated protocol alongside the template version, source-to-destination mapping, parameter values, labware definitions, environment versions, and validation record. This connects the reusable software to the specific experimental procedure actually performed.

Collapsible metadata improves readability for people; it does not replace machine-readable metadata or persistent identifiers.

## Documentation sources

- [Protocol template](Template_PCR.py)
- [Graphical selection and generation application](Patchwork_PCR.py)
- [Opentrons Python Protocol API](https://docs.opentrons.com/python-api/)
- [Opentrons Protocol Designer](https://opentrons.com/protocol-designer)
- [FAIR data and software guidance](https://librarycarpentry.github.io/lc-fair-research/aio/index.html)

The relative script links assume this README is placed in the `Scripts` directory. If placed at the repository root, prefix those two links with `Scripts/`.
