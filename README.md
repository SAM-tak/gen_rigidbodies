# Rigid Bodies Generator（剛体ツール）
Add Rigid bones and Joints on selected bones easily.  
選択したボーンに沿ってRigid Body（剛体）とRigid Body Constraints（ジョイント）を作成します。

## Requirements（使用条件）
* Blender 2.79 / 2.80

## Functions（機能）
* Add Passive(on bones)  
基礎剛体の作成‐ボーン追従
* Add Active  
基礎剛体の作成‐物理演算
* Add Joints  
基礎Jointの作成
* Add Active & Joints  
基礎剛体／連結Jointの作成

## Usage（使い方）
1. Install & activate Addon.  
アドオンをインストールして有効にします
2. Select some bones in "pose mode".  
pose modeで剛体やジョイントを設定したいボーンを選択します。
3. Execute actions on "Rigid Body Gen" tab.  
ツールシェルフの剛体ツール（Rigid Body Gen）タブの各ボタンを押します。
4. Edit propaties on prop panel.  
プロパティパネルで剛体とジョイントの値の設定をします。

## About Options（オプションについて）
* [PASSIVE]  
OFF to Active type.  
チェックを外すとACTIVEになります。
* [animated]  
ON to transform with armature.  
アーマチュアの変形にPASSIVEを追従させるにはONに
* [Auto Constraint Object]  
Not in service.  
動作しません。（現在未実装）
* [Add Pole Object]  
Add "PASSIVE" rigid bones to root bone's parent in automatic.  
選択したボーンのルート位置の親に対してPASSIVEの剛体を自動で付加します。デフォルトはON。


## Note（ご注意）
* Go back to head of timeline before you execute.  
実行前にタイムラインは先頭に戻してから実行してください。
* Reset pose before you execute.
アーマチュアのポーズは変形前に戻してから実行してください。
* Reset Armature's position to origin before you execute.
アーマチュアを原点(0, 0, 0)に置いて実行してください

## Licenses（ライセンス）
[MIT licenses](https://opensource.org/licenses/mit-license.php)

## Bugs
* 
