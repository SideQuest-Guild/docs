# Discord commands

Discord hides each command from anyone without the permission listed. Server admins change who
sees what under Server Settings, Integrations. A setting saves to the API at once.

| Command | Needs | What it does |
|---|---|---|
| `/eventsync forum [channel]` | Manage Server | Picks the forum for event threads. |
| `/weeklyboard channel`, `/weeklyboard preview` | Manage Server | Picks the weekly board's channel, or shows this week's board. |
| `/badges channel`, `/badges sync` | Manage Server | Picks where badges are announced, or checks for new badges now. |
| `/announcements channel` | Manage Server | Picks where announcements from the game and the website are posted. |
| `/signups channel` | Manage Server | Picks where new sign-ins are posted, each with an **Approve** button. |
| `/guestwelcome post <channel>` | Manage Server | Posts and pins the **Start here** button. |
| `/linkroles site`, `battlenet`, `gate`, `roster` | Manage Server | Picks the four roles that come from the website. |
| `/away role <role>` | Manage Server | Picks the away role. |
| `/welcome ...` | Manage Server | Sets the welcome message and the role new members get. `/welcome test` shows it. |
| `/logging channel`, `/logging status` | Manage Server | Picks where edits, deletes, joins, leaves, role changes and voice moves are logged. |
| `/levels ...` | Manage Server | Sets level rewards, XP range, cooldown, level-up messages, and channels or roles that earn no XP. |
| `/rolemenu ...` | Manage Roles | Builds button panels that let members pick their own roles. |
| `/warn`, `/timeout`, `/untimeout` | Timeout Members | Each one DMs the member, opens a numbered case and logs it. |
| `/kick` | Kick Members | Same as above. |
| `/ban`, `/unban` | Ban Members | Same as above. |
| `/cases [member]`, `/case <n>`, `/reason <n> <text>` | Timeout Members | Look up or explain past cases. |
| `/automod ...` | Manage Server | Deletes invite links, and times people out for mention spam or floods. |

:::{note}
Nobody can moderate the server owner, the bot, themselves, or someone whose top role sits at or
above their own.
:::

See the bot's [developer page](../developers/bot/index.md) for the full command set, including the
commands every member can use.
