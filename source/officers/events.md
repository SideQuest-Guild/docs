# Run events

Create and edit events from the website's [Officers page](https://sidequest-guild.com/officers/).
Each event gets its own Discord event and sign-up thread on its own, so you only make it once.

## Create an event

1. Go to the [Officers page](https://sidequest-guild.com/officers/).
2. Select the **Events** tab.
3. Under **Plan a night**, choose a kind, title, location, start time and (optional) end time.
4. Set a Renown value, or leave the default for that kind of event.
5. Select **Save event**.

:::{note}
A change on the website reaches Discord in about 15 seconds. A change made in Discord reaches the
website at once, though it starts with the kind "Other" until you set it on the website.
:::

## Edit or cancel an event

1. Find the event in the **Quest board** list.
2. Select it to load it into the form.
3. Change what you need, then select **Save event**.
4. To cancel it, select **Cancel & delete event**.

:::{warning}
Deleting an event in Discord cancels it on the website and keeps its sign-ups. Deleting it on the
website removes it everywhere.
:::

## Repeat an event

1. Under **Repeats**, choose **Weekly** or **Every 2 weeks**.
2. Pick the weekday or weekdays it repeats on.
3. Set an **Until** date, or leave it open-ended.

A repeating event keeps its next 14 days filled in as ordinary events, each with its own
sign-ups. To change every occurrence at once, edit the series instead of a single event.

:::{dropdown} What syncs to Discord?
Each event gets a Discord event and a thread in the events forum with Going, Maybe and Can't
buttons. Editing the title, time, location or status on the website updates both, and the
event's weekly board card if it has one. Cancelling an event marks its card cancelled and
removes the buttons. Deleting an event in Discord only cancels it; the website keeps the record
and its sign-ups.
:::

## Run a recruitment drive

A recruitment drive is a 2 week contest: the member who brings in the most new players wins a
prize. See [Recruitment drives](../members/events.md#recruitment-drives) for the prize and the
rules a recruit has to meet.

### Create a drive

1. Go to the [Officers page](https://sidequest-guild.com/officers/).
2. Select the **Events** tab.
3. Under **Plan a night**, choose the kind **Recruitment Drive**.
4. Set a title and start time. The start must be in the future, so Discord can post the drive.
   The end time defaults to 14 days after the start; change it if this drive should run longer
   or shorter.
5. Select **Save event**.

A recruitment drive doesn't take sign-ups. Members invite in game instead.

### Put it on the in-game calendar

Your addon only knows about the drive once it has the site's latest data. With SideQuest
Companion running, type `/reload` a few minutes after creating the drive and it's there. Without
the companion, open the [Officers sync page](https://sidequest-guild.com/officers/sync/), select
**Copy game import string**, and paste it into `/sq import` in game.

Then:

1. Open the addon's Console **Sync** tab and select **Update calendar**, or type `/sq calendar`.
   Select it once for each announcement.

A recruitment drive adds two guild announcements instead of one: the drive's title at the start,
and `Ends: <title>` at the end. Both link to the drive's page on the site. The game won't add an
announcement in the past, so if the drive has already started, only the `Ends: <title>` one is
added.

### Sweep the guild log during the drive

The in-game guild log only keeps its most recent entries, so an officer's addon has to sweep the
roster and export regularly during a drive to catch every invite, join, quit and removal before
the log drops them. Sweep at least once a day while a drive is running, more often if the guild
is busy.

### Pay out

A week after a drive ends, its winner shows up under **Recruitment payouts**, or several
winners if they tied. Pay each winner one of two ways:

- **In game:** open a mailbox, then open the addon Console's **Payouts** sub-tab and select
  the row's **Mail** button (labelled with the prize, "Mail 1g"). It sends the mail straight
  away, with the winner's recruits listed in the note, and marks the row paid once the mail
  sends. If the mail fails, the row stays unpaid and the button stays there to try again.
- **By hand:** mail the gold yourself, then go to the
  [Officers page](https://sidequest-guild.com/officers/), select the **Recruitment** tab, find
  the winner under **Recruitment payouts** and select **Mark paid**.
