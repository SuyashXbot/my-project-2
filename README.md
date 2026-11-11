# Crowns of Mud and Tallow — Hosted ChoiceScript Game

A historical late-medieval ChoiceScript game set in a Hundred Years' War–era capital blending fourteenth-century London and Paris (population ~50,000) at the confluence of the rivers **Aur** and **Thel** (**Aurthel**), bounded on the north by **The Cut** canal and **Northgate Bridge**.

## Scene Files (`scenes/`)

- [`scenes/startup.txt`](scenes/startup.txt) — Title, author, `*scene_list`, all global variables (`*create`), and the `*label recalc_stats` subroutine that clamps hidden stats (`empathy`, `duty`, `cruelty`, `ambition`) to `0..100`, computes visible `honor = (duty + empathy) - cruelty` and `infamy = (cruelty + ambition) - empathy` clamped to `0..100`, and assigns reputation titles (`Knight Errant of the Mud`, `The Butcher`, `Sworn Hand of the Mews`, `Wolf of the Cut`, `Branded Drover of Bridgefoot`).
- [`scenes/choicescript_stats.txt`](scenes/choicescript_stats.txt) — The stats screen displaying only visible **Honor**, **Infamy**, and the relationship meters for the four love interests (**Lady Ysolde de Varenne**, **Clarimond of Saint Jude's**, **Cateline "Cat" Rook**, and **Alisoun Verrier**).
- [`scenes/day_one.txt`](scenes/day_one.txt) — Opening day in the hayloft of the Royal Mews, establishing the protagonist's name, sword-training under his late father **Sir Edmund Harrowmere**, his bastardization under canon precontract law (*sponsalia*) by his uncle **Lord Roderic Harrowmere** over **Lady Bellisant de Varenne**, his mother **Maren**'s labor in **Tobin** and **Agnes Hale**'s bakery alongside cousin **Wenna**, **Master Corwin Dray**'s patronage, the first clash with rival groom **Piers** (and **Wat** and **Hodge**), and first encounters with all four love interests.
- [`scenes/hub.txt`](scenes/hub.txt) — The yearly open-world city loop and mandatory-duty system:
  1. **Mews Duty Shifts & Rivalry** (with explicit neglect warnings, Piers's sabotage/framing, and hidden-stat hesitation/refusal when ordered to harm innocents).
  2. **Family Obligation at Tobin Hale's Bakery** (with explicit neglect warnings, Maren's health/employment, and Tobin's patience).
  3. **Free Roam District Visit** (1 of the 10 city districts per year, while unvisited districts dynamically shift in prosperity, fear, and control).
  4. **The Lightbearer Festival and Joust** (`*gosub_scene festival`).
  5. **The Year's Main Plot Beat** (Lord Roderic, Lady Bellisant's precontract, and the Consistory Court).
  6. **Escalating Duty Lapses (Lapses 1, 2, and 3)** and the **Year-End Summary Ledger**.
- [`scenes/festival.txt`](scenes/festival.txt) — The annual **Lightbearer Festival** candle procession, bonfires, preparing horses, protecting or tampering with **Prince Halric**'s stallion against **Lord Roderic**'s champion **Sir Morvan**, wagering on the jousts, and meeting love interests.
- **Ten District Scenes** (each featuring a 150–250 word sensory introduction, 11–18 named streets/buildings/places, state-driven events, hidden-stat hesitation checks, and royal statues):
  1. [`scenes/district_castle.txt`](scenes/district_castle.txt) — The Royal Castle (Inner Ward, Outer Ward, Royal Mews, Royal Granaries)
  2. [`scenes/district_gilded_row.txt`](scenes/district_gilded_row.txt) — The Gilded Row (Nobility townhouses, officers' townhouses, Lady Ysolde, Memorial Cross of King Caelan the Just)
  3. [`scenes/district_archivians.txt`](scenes/district_archivians.txt) — The Tower of the Archivians (Fireproof stone record tower, Clarimond of Saint Jude's, precontract rolls)
  4. [`scenes/district_market.txt`](scenes/district_market.txt) — The Market Square and Guildhall (Founder-King Aurelian I statue at the Market Cross, Court of Piepowder)
  5. [`scenes/district_craftsmens_ward.txt`](scenes/district_craftsmens_ward.txt) — The Craftsmen's Ward (Bakehouse Lane, Tobin Hale's Bakery, Alisoun Verrier's Herb-Garret)
  6. [`scenes/district_keep_cathedral.txt`](scenes/district_keep_cathedral.txt) — The Keep and Cathedral Isle (Confluence Keep, Royal Arsenal, Gallery of Kings with Beloved King Aldous III, Bishop's Palace, Consistory Court)
  7. [`scenes/district_university.txt`](scenes/district_university.txt) — The University of the Scholiasts (West bank colleges, hostels, bookshops, canon law disputations)
  8. [`scenes/district_bridgefoot.txt`](scenes/district_bridgefoot.txt) — Bridgefoot, the Stews, and the Great Bridge (House-lined Great Bridge, Bridgefoot Gaol, defaced statue of Reviled King Vortimer II the Starver)
  9. [`scenes/district_docks.txt`](scenes/district_docks.txt) — Merchant Row and the Docks (East bank wharves, Custom House, Steelyard, Cateline "Cat" Rook)
  10. [`scenes/district_northgate_abbey.txt`](scenes/district_northgate_abbey.txt) — Northgate Bridge, the Cut, the Royal Hunting Park, and Saint Wulfric's Abbey (Niches of King Edric the Wall-Maker)

## How to Run and Test

1. **Validate Syntax, Labels, Variables, and Realism Requirements**:
   ```bash
   python3 validate_choicescript.py
   ```
2. **Run in ChoiceScript / CSIDE**:
   - Copy the `.txt` files from `scenes/` into your ChoiceScript `web/mygame/scenes/` folder (or open the `scenes/` folder directly as a project in **CSIDE**).
   - Run `node serve` (or open `web/mygame/index.html`) to play in a browser, and run `node randomtest num=100` and `node quicktest` from the ChoiceScript root directory to verify all branches.
