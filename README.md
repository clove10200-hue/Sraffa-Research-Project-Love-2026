# Sraffa-Research-Project-Love-2026

Sraffa Model Calculator

## Setup

Follow the instructions on the [uv website](https://docs.astral.sh/uv/getting-started/installation/) to install uv.

Then, run the following command to install the project dependencies:

```bash
uv sync
```

## Usage

Run scripts in the `src` directory using uv:

```bash
uv run src/solve_prices.py
```

# Runescape PvM Economy Dataset Generator Readme

## Intent

Take in a data structure of drop rates and item consumption rates for boss drops, output a file containing the Sraffan matrix M and q
for this PvM economy, ready to be processed by the price calculator.

## Structure

Input file for commodity consumption will contain a list of boss drops, their drop rate, and the average number of overload doses, sailfin soups, and armor needed for each kill,
Like so:

Seismic_Wand 0.0005 1.25 2.20
Saradomin_Godsword 0.001 0.25 0.2
Sirenic_Hauberk 0.0001 1.0 2.0
ect.

While the input file for the commodity output vector will be similar, but derived from market data, like so:

Seismic_Wand 112
Saradomin_Godsword 345
Sirenic_Hauberk 54
ect.

## Basic Goods

The Sraffan basic goods under consideration in this model will be doses of overload potion and sailfin soup, the gold standards for PvM consumables. The right-hand side coefficient of these equations will be found by utilizing market volume data for the Grand Exchange for those items over a given period.
However, because overload potions are not directly sold on the open player market, an approximation will need to be made using its ingredients instead, which are directly sold.
Example: 100,000 doses overload potion, 20,000 sailfin soup, ..... , 0 Saradomin Godsword -> 300,000 doses overload potion(note: calculated from overload ingredients sold on grand exchange)

## Non-basic Goods

The boss drops will account as non-basic goods in the Sraffan framework and their equations will be calculated as follows. Each boss drop will have its right-hand side calculated from market volume data, something that is made publicly available to players. The left-hand side will start with the assumed amount of each basic good needed for one boss kill(eg 1 overload, 2 sailfins) and then each term will be multiplied by the inverse of the boss drop rate(i.e. if rate is 1/50 then it becomes 50 overload, 100 sailfins -> 1 boss drop). Then the entire equation will be multiplied by the amount of the drop sold from the market data(i.e. if 100 were sold from the previous example then it becomes 5,000 overload, 10,000 sailfins, 500 armor repairs -> 1 boss drop). All other coefficients are assumed to be zero as no other goods are _directly_ consumed in the boss killing production process.

Therefore, the inputs this generator will need will be as such:

1. A text matrix of market volume data for overload potion ingredients, sailfin soup, and boss armor drops
2. A text matrix of boss drop names, their droprates, and the amounts of each basic good they consume for each drop.
   The generator will then ouput a text file containing the Sraffan equation matrix for this PvM economy, ready to be processed by the calculator in solve_prices.py

## Possibilities for extentions in the future

in reality, armor degrades as it is used in high-level Runescape content. This means that armor is itself 'consumed' when it is used
to produce other boss drops. Jagex could track this economic data directly(by, say, tracking how many points of damage each piece of armor takes after each boss kill and aggregating that data for a period of time) but it is difficult to approximate with publicly available market data, as it is unknown to what extent boss drops are bought to replace degraded armor, least of all how much of each individual armor is used in the production of each individual drop. A future model may simply act as though we were Jagex and had access to that data and create an entirely fictional dataset to prove a proof of concept.
