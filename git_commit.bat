CHCP 936
@echo off 
echo **************************************准备提交代码***********************************
echo=
set input=
set /p input=请输入提交描述：
echo=
echo 您输入提交描述是：%input%
git add .
git commit -m %input%
git push origin
echo=
echo **************************************提交代码结束***********************************
pause