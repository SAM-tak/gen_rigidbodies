# GenRigidBodies

> Read this in other languages: [English](README.md), [日本語](README.ja.md).

Add rigid bodies and joints (Rigid Body Constraints) aligned on specified bones easily.

## Table of Contents
<!-- TOC -->

- [Requirements](#requirements)
- [Functions](#functions)
- [Usage](#usage)
- [About Options](#about-options)
- [Notes](#notes)
- [License](#license)

<!-- /TOC -->

## Requirements

- Blender 2.80+

## Usage

1. Download zip file from [release page](/../../releases/latest).
1. Install & activate this Add-on.
1. Select some bones in "pose mode".
1. Execute actions from Menu "Pose → Gen Rigid Bodies".
1. Edit parameter on properties panel.

## Functions

- *Placement : Pose mode / Pose menu → Gen Rigid Bodies*
  - **Add Passives**  
    Craete passive rigid body objects aligned to selected bones.
  - **Add Actives**  
    Craete active rigid body objects aligned to selected bones.
  - **Add Joints**  
    Create rigid body constraint objects on selected bones only.
  - **Add Actives & Joints**  
    Craete rigid body objects and constraint objects on selected bone tree.
- *Placement : Object mode / Object menu → Gen Rigid Bodies*
  - **Reparent Orphan Track Object**  
    Parent selected object that has 'tr.' prefix with coresponding rigid body object.
    It is useful after unparent 'tr.' prefix object temporary to tweak a rigid body
    position.
  - **Repair Corresponding**  
    If selected 'tr.' prefix-named objects have 'rb.' prefix-named one and the parent
    object has non-corresponding name, rename it.
  - **Connect Rigidbody Constraint**  
    Set selected objects' first element of 'Objects' paratemter in rigid body
    constraint settings to active object.

## About Options

- *PASSIVE*  
  OFF to Active type.
- *animated*  
  ON to transform with armature.
- *Add Pole Object*  
  Add "PASSIVE" rigid bones to root bone's parent in automatic.  
  default is off.

## Notes

- Go back to head of timeline before you execute.
- Reset pose before you execute.

## License

[MIT license](LICENSE)
