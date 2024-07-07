import discord
from discord.ext import commands
import asyncio      # Import time keeping/looping

# Import reddit api. Async version
import asyncpraw

# Import keys
import misc.botInfo.apikey as key

class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit_post = []        # Store current posts
        self.reddit_instance = None

    # *************** Non-command/event Functions ***************
    async def init_Reddit(self):
        # Instance must be created within async function
        # to allow for async for to work.
        self.reddit_instance = asyncpraw.Reddit(
            client_id = key.red_clientID,
            client_secret = key.red_secret,
            username = key.red_username,
            password = key.red_password,
            user_agent = "test_bot"
        )

    async def reddit_background(self, sub_Name, get_limit, sleep_time):
        await self.client.wait_until_ready()
        # Only done once. 

        is_dup = False          # Bool, check for duplicate
        channel = self.client.get_channel(key.disc_botSpam)  # Find channel to send to

        # Time loop here
        while not self.client.is_closed():
            subreddit = await self.reddit_instance.subreddit(sub_Name, fetch = True)
            retrieved_post = subreddit.hot(limit = get_limit)
            async for submission in retrieved_post:
                # For more efficiency, use merge sort and then compare only one 
                for post in self.reddit_post:
                    # Iterate through entire running total of the list.
                    if (post.id == submission.id):
                        is_dup = True
                        break

                # If a duplicate is found, don't print it.
                if (not is_dup):
                    # Only add if it wasn't on the list already
                    self.reddit_post.append(submission)      # Add onto current list

                    # Not a duplicate, print it.
                    # Build discord message here.
                    await channel.send(submission.title + ' '\
                        + submission.url +'\n' + "https://www.reddit.com" + submission.permalink)
                # if, END
                # Otherwise, it is a duplicate. Don't do anything
                is_dup = False                      # Reset variable
            # async for, END

            await asyncio.sleep(sleep_time)         # Run every 'X' seconds

    # *************** Discord command/event Functions ***************
    @commands.command()
    async def reddit(self, ctx, arg):
        sub_valid = True        # Flag to keep track of valid subreddits

        # Validate subreddits and check conditions
        try:
            # Ensure that it has been instantiated.
            if (self.reddit_instance == None):
                await self.init_Reddit()

            # Find valid subreddits by attempting to get from them.
            # Get the subreddit
            subRed = await self.reddit_instance.subreddit(arg, fetch = True)

            # Attempt to search it
            async for submission in subRed.new(limit = 3):
                pass

            # Ensure passed subreddit does not already have a task for it.

        except:
            channel = self.client.get_channel(key.disc_botSpam)
            await channel.send("Error: Unknown or invalid subreddit provided: %s" % arg)
            sub_valid = False

        # If a valid subreddit was provied, create a task
        if (sub_valid):
            # Create time loop. Continuously run this function.
            current_tasks = self.client.loop.create_task(self.reddit_background(arg, 3, 5))

            current_tasks.set_name(arg)
            print("My name is %s" % current_tasks.get_name())
            await asyncio.sleep(5)

            current_tasks.cancel()
            print("Task %s has been canceled" % current_tasks.get_name())

async def setup(client):
    await client.add_cog(Reddit(client))
