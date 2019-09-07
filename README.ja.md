# GenRigidBodies

*他の言語で読む: [English](README.md), [日本語](README.ja.md).*

選択したボーンに沿ってRigid Body（剛体）とRigid Body Constraints（ジョイント）を作成する、Blender 2.80+ 用アドオンです。

## 目次

<!-- TOC -->

- [使用条件](#使用条件)
- [機能](#機能)
- [使い方](#使い方)
- [オプションについて](#オプションについて)
  - [**PASSIVE**](#passive)
  - [**animated**](#animated)
  - [**Add Pole Object**](#add-pole-object)
- [注意点](#注意点)
- [ライセンス](#ライセンス)

<!-- /TOC -->

## 使用条件

- Blender 2.80+

## 機能

- Add Passive(on bones)
  - 基礎剛体の作成‐ボーン追従
- Add Active
  - 基礎剛体の作成‐物理演算
- Add Joints
  - 基礎Jointの作成
- Add Active & Joints
  - 基礎剛体／連結Jointの作成

## 使い方

1. アドオンをインストールして有効にします。
1. pose modeで剛体やジョイントを設定したいボーンを選択します。
1. ツールシェルフの剛体ツール（Rigid Body Gen）タブの各ボタンを押します。
1. プロパティパネルで剛体とジョイントの値の設定をします。

## オプションについて

### **PASSIVE**

チェックを外すとACTIVEになります。

### **animated**

アーマチュアの変形にPASSIVEを追従させるにはONに。

### **Add Pole Object**

選択したボーンのルート位置の親に対してPASSIVEの剛体を自動で付加します。デフォルトはON。

## 注意点

- 実行前にタイムラインは先頭に戻してから実行してください。
- アーマチュアのポーズは変形前に戻してから実行してください。
- アーマチュアを原点(0, 0, 0)に置いて実行してください。

## ライセンス

[MIT licenses](LICENSE)
