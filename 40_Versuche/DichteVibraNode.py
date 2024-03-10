#use dm to go direktly to liter
breite = 0.8
hohe  =0.9
fussLang = 0.4
fussDurch = 0.3
gewicht = 1.15

volumenKorper = breite**2*hohe
volumenFusse = 8*fussLang*(fussDurch/2)**2*3.141


print(volumenKorper, volumenFusse)
print("Volume of Virbarnode", volumenKorper+ volumenFusse)
print("Density of Virbarnode", gewicht/(volumenKorper+ volumenFusse), "kg/l")
