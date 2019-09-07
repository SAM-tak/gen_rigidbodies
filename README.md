# GenRigidBodies

*Read this in other languages: [English](README.md), [日本語](README.ja.md).*

Add Rigidbodies aligned on specified bones and joints (Rigid body constraints) easily.

## Table of Contents
<!-- TOC -->

- [Requirements](#requirements)
- [Functions](#functions)
- [Usage](#usage)
- [About Options](#about-options)
  - [**PASSIVE**](#passive)
  - [**animated**](#animated)
  - [**Add Pole Object**](#add-pole-object)
- [Notes](#notes)
- [License](#license)

<!-- /TOC -->

## Requirements

- Blender 2.80+

## Functions

- Add Passive Rigidbody objects on bones
- Add Active Rigidbody objects on bones
- Add Joints between two bones
- Add Active & Joints

## Usage

1. Install & activate this Add-on.
1. Select some bones in "pose mode".
1. Execute actions from Menu "Pose→Gen Rigidbodies".
1. Edit propaties on prop panel.

## About Options

### **PASSIVE**

OFF to Active type.

### **animated**

ON to transform with armature.

### **Add Pole Object**

Add "PASSIVE" rigid bones to root bone's parent in automatic.

default is off.

## Notes

- Go back to head of timeline before you execute.
- Reset pose before you execute.
- Reset Armature's position to origin before you execute.

## License

[MIT license](LICENSE)
