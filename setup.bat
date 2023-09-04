@ECHO OFF

CD /D %~dp0

WHOAMI /PRIV | FIND "SeDebugPrivilege" > NUL
IF %ERRORLEVEL% NEQ 0 (
    powershell -Command "Start-Process %~0 -Verb RunAs"
    EXIT
)

IF EXIST .nuget RMDIR /S /Q .nuget
MKDIR .nuget

powershell -Command "Invoke-WebRequest -Uri https://github.com/yatsuna827/PokemonPRNG/releases/download/LCG32_v3.8.0/PokemonPRNG.3.8.0.nupkg -OutFile .nuget\PokemonPRNG.3.8.0.nupkg"

IF EXIST PokemonStandardLibrary RMDIR /S /Q PokemonStandardLibrary
git clone https://github.com/yatsuna827/PokemonStandardLibrary.git --depth 1
CD PokemonStandardLibrary
dotnet new console --output ConsoleApp1
dotnet build --configuration Release
dotnet pack --configuration Release --output ..\.nuget
CD ..

IF EXIST PokemonXDRNGLibrary RMDIR /S /Q PokemonXDRNGLibrary
git clone https://github.com/yatsuna827/PokemonXDRNGLibrary.git --depth 1
CD PokemonXDRNGLibrary
RMDIR /S /Q packages
(
ECHO ^<?xml version="1.0" encoding="utf-8"?^>
ECHO ^<configuration^>
ECHO   ^<packageSources^>
ECHO     ^<add key="local" value="..\.nuget" /^>
ECHO   ^</packageSources^>
ECHO ^</configuration^>
) > nuget.config
CD PokemonXDRNGLibrary
powershell -Command "(Get-Content PokemonXDRNGLibrary.csproj -Raw) -replace '3.6.2', '3.8.0' | Set-Content PokemonXDRNGLibrary.csproj"
powershell -Command "(Get-Content PokemonXDRNGLibrary.csproj -Raw) -replace '0.3.0-alpha.1', '1.0.0' | Set-Content PokemonXDRNGLibrary.csproj"
CD ..
dotnet build --configuration Release
dotnet pack --configuration Release --output ..\.nuget
CD ..

RMDIR /S /Q PokemonStandardLibrary
RMDIR /S /Q PokemonXDRNGLibrary

CD .nuget
COPY PokemonPRNG.3.8.0.nupkg PokemonPRNG.3.8.0.zip
COPY PokemonXDRNGLibrary.1.0.0.nupkg PokemonXDRNGLibrary.1.0.0.zip
COPY PokemonXDRNGLibrary.XDDB.1.0.0.nupkg PokemonXDRNGLibrary.XDDB.1.0.0.zip
powershell -Command "Expand-Archive -Path PokemonPRNG.3.8.0.zip -DestinationPath PokemonPRNG.3.8.0"
powershell -Command "Expand-Archive -Path PokemonXDRNGLibrary.1.0.0.zip -DestinationPath PokemonXDRNGLibrary.1.0.0
powershell -Command "Expand-Archive -Path PokemonXDRNGLibrary.XDDB.1.0.0.zip -DestinationPath PokemonXDRNGLibrary.XDDB.1.0.0"
CD ..

CD nxmc2-xd-sift-initial-seed
mklink NxInterface.dll "C:\Program Files (x86)\NX Macro Controller\NxInterface.dll"
mklink OpenCvSharp.dll "C:\Program Files (x86)\NX Macro Controller\OpenCvSharp.dll"
mklink OpenCvSharp.Extensions.dll "C:\Program Files (x86)\NX Macro Controller\OpenCvSharp.Extensions.dll"
MKLINK PokemonPRNG.dll ..\.nuget\PokemonPRNG.3.8.0\lib\netstandard2.0\PokemonPRNG.dll
MKLINK PokemonXDRNGLibrary.dll ..\.nuget\PokemonXDRNGLibrary.1.0.0\lib\netstandard2.0\PokemonXDRNGLibrary.dll
MKLINK PokemonXDRNGLibrary.XDDB.dll ..\.nuget\PokemonXDRNGLibrary.XDDB.1.0.0\lib\netstandard2.0\PokemonXDRNGLibrary.XDDB.dll
CD ..

PAUSE