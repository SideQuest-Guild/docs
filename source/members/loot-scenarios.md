# Loot: what happens when...

Progression loot runs on SQL (SideQuest Loot). If
you haven't yet, read [Understand your points](points.md) and the site's
[raids page](https://sidequest-guild.com/raids/#loot) first; this page walks through common raid
situations and what SQL does for each one. It's for progression raids. Casual and alt nights use
soft reserve instead; see the raids page's casual loot section for that.

Every number below is a labelled example, not a current rule. The
[Ledger](https://sidequest-guild.com/ledger/) always has the live EP values, GP by slot, decay
and off-spec price.

## A normal item with several main-spec bids

Everyone who wants it for their main spec bids main spec. The highest PR wins it and pays the
full GP for its slot.

::::{note}
Example: two raiders bid main spec on a chest piece. One has a PR of 2.1, the other 1.6. The
first wins and pays the chest's GP cost.
::::

## Nobody bids main spec, but someone wants it for an off spec

The item goes to the highest PR among the off-spec bids. Off spec pays 10% of the item's GP
cost instead of the full price.

## Nobody bids, but an alt needs it

An alt filling a raid slot can take an unwanted item for free. Your main still earns the EP for
the night; the item doesn't cost your alt any GP.

## Nobody wants it

The item is disenchanted. The Essence goes to the guild bank, where it's used for crafted tier.

## A tie on PR

Ties go to the higher EP. If EP is tied too, it's a roll.

## The boss's chase item drops

Each boss has one chase item. It isn't bid on; it goes to the {ref}`loot council <the-loot-council>`
to decide. Whoever the council picks still pays GP for it, at the usual slot cost times the
chase multiplier.

## A legendary, special or rare item drops

Same as a chase item: the council decides, and the winner still pays GP, at the flat legendary
or special-item rate.

## Crafted tier

Crafted tier also goes to the council. It pays GP at the usual slot cost, same as a tier token.
Besides who wants it most, the council checks who can still equip one: everyone starts with one
crafted piece allowed, and Guardians of Hyjal reputation raises that limit.

## A tier token

A tier token isn't a council item. It's bid on like any other drop, main spec then off spec then
alt, and its GP cost is whatever its slot would normally cost.

## Week one, before priorities sort

Everyone starts the tier at the same EP and GP, so week one plays out as main spec, then off
spec, then rolls within each group, same as every week. Priority only starts separating people
from week two, once EP differs.

## A new raider on trial

A trial earns EP from their first night in the raid. For their first two raid weeks, a full
raider's main-spec bid beats a trial's, even on a lower PR. After that window, the trial is a
full raider and keeps whatever EP they earned while on trial.

## An officer awards to the wrong person

An officer undoes the award and records the correct one. The addon keeps both the original
award and the correction in the history instead of erasing the mistake, so the Ledger's loot
history still shows what happened.

## Someone on the council wants the item

The loot council is the raid leader, two officers and one rotating raider. Anyone on the council
who wants the item sits that vote out, and the rest of the council decides without them.

## The council's decision

Whichever item type it's deciding, an officer records the council's pick in the addon with a
one-line reason. When that raid night syncs to the site, the reason shows under the award in the
[Ledger](https://sidequest-guild.com/ledger/)'s recent loot, and the bot posts it to #loot-log so
the raid can see who won what and why.

## You miss a raid: decay and points over weeks

EP and GP both shrink by a set percentage every weekly reset, so a raid you miss doesn't just
stay flat, it falls behind raids you attended. Your PR (EP divided by GP) still reflects your
recent attendance more than your oldest raids. Check the Ledger for the current decay rate and
your own history.

::::{note}
Example: with 15% decay, a week with no raiding leaves 85% of the old value. Four weeks away in a
row leaves about 85% to the fourth power, roughly half of the original EP and GP. The actual rate
is on the [Ledger](https://sidequest-guild.com/ledger/).
::::

(the-loot-council)=
## The loot council

The council only decides chase items, legendary or special items and crafted tier; everything
else is bid on. See the site's [loot council section](https://sidequest-guild.com/raids/#council)
for who sits on it and how a decision gets made.
