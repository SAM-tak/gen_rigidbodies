# GenRigidBodies

> 他の言語で読む: [English](README.md), [日本語](README.ja.md)

選択したボーンに沿ってRigid Body（剛体）とRigid Body Constraints（ジョイント）を作成する、Blender 2.80+ 用アドオンです。

## 目次

<!-- TOC -->

- [使用条件](#使用条件)
- [機能](#機能)
- [使い方](#使い方)
- [オプションについて](#オプションについて)
- [注意点](#注意点)
- [ライセンス](#ライセンス)

<!-- /TOC -->

## 使用条件

- Blender 2.80+

## 使い方

1. ZIPファイルを[リリースページ](/../../releases/latest)からダウンロードします。
1. アドオンをインストールして有効にします。
1. pose modeで剛体やジョイントを設定したいボーンを選択します。
1. ポーズメニューの剛体ツール（Gen Rigid Bodies）メニューの各メニューを実行します。
1. プロパティパネルで剛体とジョイントの値の設定をします。

## 機能

- *場所 : Pose mode / Pose メニュー → Gen Rigid Bodies*
  - **Add Passive**  
    基礎剛体の作成‐ボーン追従
  - **Add Active**  
    基礎剛体の作成‐物理演算
  - **Add Joints**  
    基礎Jointの作成
  - **Add Active & Joints**  
    基礎剛体／連結Jointの作成
- *場所 : Object mode / Object メニュー → Gen Rigid Bodies*
  - **Reparent Orphan Track Object**  
    選択されたオブジェクトが'tr.'接頭辞を持つなら、対応する'rb.'接頭辞をもつオブジェクトに
    その場でペアレントします。
    これは剛体の位置合わせのために一旦'tr.'オブジェクトの親子付けを解除した後に便利です。
  - **Repair Corresponding**  
    選択されたオブジェクトが'tr.'接頭辞を持ち、その親が'rb.'接頭辞を持つ対応した名前になって
    いない場合、リネームします。
  - **Connect Rigidbody Constraint**  
    選択されたオブジェクトの剛体コンストレイント設定のオブジェクト項の一番目を、アクティブ
    オブジェクトに一括設定します。

## オプションについて

- *PASSIVE*  
  チェックを外すとACTIVEになります。
- *animated*  
  アーマチュアの変形にPASSIVEを追従させるにはONに。
- *Add Pole Object*  
  選択したボーンのルート位置の親に対してPASSIVEの剛体を自動で付加します。デフォルトはON。

## 注意点

- 実行前にタイムラインは先頭に戻してから実行してください。
- アーマチュアのポーズは変形前に戻してから実行してください。

## ライセンス

[MIT licenses](LICENSE)
