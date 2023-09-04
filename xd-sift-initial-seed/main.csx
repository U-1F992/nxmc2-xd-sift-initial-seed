#r "NxInterface.dll"
#r "OpenCvSharp.dll"
#r "OpenCvSharp.Extensions.dll"

#r "PokemonPRNG.dll"
#r "PokemonXDRNGLibrary.dll"
#r "PokemonXDRNGLibrary.XDDB.dll"

using System;
using System.Collections.Generic;
using System.Linq;

using NxInterface;
using OpenCvSharp;
using OpenCvSharp.Extensions;
using PokemonPRNG.LCG32.GCLCG;
using PokemonXDRNGLibrary;
using PokemonXDRNGLibrary.QuickBattle;
using PokemonXDRNGLibrary.XDDB;

var client = new XDDBClient();
var ret = client.Search(
    new QuickBattleInput(PlayerTeam.Deoxys, EnemyTeam.Zapdos, 257, 648, 326, 281),
    new QuickBattleInput(PlayerTeam.Jirachi, EnemyTeam.Zapdos, 349, 325, 336, 313)
);
Console.WriteLine(ret.ToList()[0]);

uint seed = 0;
PokemonPRNG.LCG32.GCLCG.GCLCGExtension.Advance(ref seed);
seed.Advance();
Console.WriteLine(seed);
