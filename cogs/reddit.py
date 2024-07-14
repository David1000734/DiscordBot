from discord.ext import commands
import asyncio      # Import time keeping/looping

# Import reddit api. Async version
import asyncpraw

# Import keys
import misc.botInfo.apikey as key

# Import custom exceptions
import misc.customException as ex

class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit_post = []        # Store current posts
        self.reddit_instance = None  # The reddit API
        self.reddit_Task = []        # Running total of tasks created
        self.usage_Msg = \
            "Usage: !reddit <command>\n" + \
            "<command>: add <subreddit>, remove <subreddit>, clear, list."

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

    async def background_Task(self, sub_Name, get_limit, sleep_time):
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
                    print("Sub name: " + submission.subreddit.display_name)
                else:
                    print("Not printing: %s." % sub_Name)
                # if, END
                # Otherwise, it is a duplicate. Don't do anything
                is_dup = False                      # Reset variable
            # async for, END

            # Check to see if we went past the limit
            # If the total number of post is greater than the number of
            # task times the limit, we went over. Remove the last few
            # Ex. limit = 10, 2 task.
            # If our total post is 23, we went over by 3 because 10 * 2 = 20
            if (len(self.reddit_post) > len(self.reddit_Task * get_limit)):
                post_Counter = 0
                # We went over, remove the diference.
                for post in self.reddit_post:
                    if (post.subreddit.display_name == sub_Name and post_Counter > get_limit):
                        # Find the correct name and remove only the
                        # post that went over the limit.
                        self.reddit_post.remove(post)
                        print("Removed some old ones: " + self.reddit_post)
                    else:
                        # Increment counter
                        post_Counter += 1
                        print("Not removing anything: " + self.reddit_post)
                # For, END
            # Check limit, END

            await asyncio.sleep(sleep_time)         # Run every 'X' seconds
        # while, END
    # background task, END

    async def reddit_Add(self, ctx, arg):
        sub_valid = True        # Flag to keep track of valid subreddits

        # Validate subreddits and check conditions
        try:
            # Used to find out if task has already been created.
            found = False

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

            # Iterate through the task list
            for idx, currSub in enumerate(self.reddit_Task):
                # Search for a task with the that subreddit name
                if (currSub.get_name() == arg):
                    found = True
                    break               # Exit loop
                # if task_name = name, END
            # For task list, END

            # If one is found, error
            if (found):
                raise ValueError("Duplicate subreddit tasks is not allowed.")

        except Exception as error:
            await ctx.send("Subreddit: \"%s\" Error: %s" % (arg, error))
            sub_valid = False

        if (sub_valid):
            # Create time loop. Continuously run this function.
            current_tasks = self.client.loop.create_task(self.background_Task(sub_Name = arg, get_limit = 3, sleep_time = 5))

            current_tasks.set_name(arg)     # Set the name to be the same as the subreddit
            self.reddit_Task.append(current_tasks)      # store to array
        # If valid sub, END
    # reddit_add, END

    async def reddit_Remove(self, ctx, arg):
        found = False

        # Iterate through the task list
        for idx, currSub in enumerate(self.reddit_Task):
            # Search for a task with the that subreddit name
            if (currSub.get_name() == arg):
                # If one is found, remove it
                currSub.cancel()

                # Remove from the list
                self.reddit_Task.remove(currSub)

                await ctx.send("Successfully removed subreddit: \"%s\", from tasks." % arg)

                found = True        # Set flag
                break               # Exit loop
        
        if (not found):
            await ctx.send("Subreddit: \"%s\" not found. Unable to remove." % arg)
        else:
            print("something")
    # removeSub, END

    async def reddit_Clear(self, ctx):
        for currSub in self.reddit_Task:
            await ctx.send("Removed subreddit: \"%s\", from tasks." % currSub.get_name())
            currSub.cancel()
        
        # Clear list
        self.reddit_Task.clear()
    # Clear all, END

    async def reddit_List(self, ctx):
        listName = []

        for currSub in self.reddit_Task:
            listName.append(currSub.get_name())

        await ctx.send("Current subreddits: %s" % ", ".join(listName))

    # *************** Discord command/event Functions ***************
    @commands.command()
    async def reddit(self, ctx, *arg):
        try:
            # arg[0] will will contain the command
            match arg[0].lower():
                # add command will add a new background task for the subreddit
                case "add":
                    if (len(arg) > 2):
                        raise ex.InvalidSubreddit()
                    else:
                        # arg[1] contains the word
                        await self.reddit_Add(ctx, arg[1])
                
                # Attempt to remove a reddit background task if one exist
                case "remove":
                    if (len(arg) > 2):
                        raise ex.InvalidSubreddit()
                    else:
                        # arg[1] contains the word
                        await self.reddit_Remove(ctx, arg[1])

                # Clear all existing reddit background task
                case "clear":
                    if (len(arg) > 1):
                        raise ex.UnknownCommand()
                    else:
                        await self.reddit_Clear(ctx)
                    
                case "list":
                    if (len(arg) > 1):
                        raise ex.UnknownCommand()
                    else:
                        await self.reddit_List(ctx)

                # Default state
                case _:
                    # Have the try catch do the message
                    raise IndexError("")
            # Match, END
        
        # Tuple out of range when ran with "!reddit"
        # Thus prompt usage error
        except IndexError:
            await ctx.send(self.usage_Msg)
        
        except ex.UnknownCommand as e:
            await ctx.send("Unknown command: \"%s\"" % " ".join(arg))
        
        except ex.InvalidSubreddit as e:
            await ctx.send("Error: Subreddit \"%s\" is not allowed." \
                                    % " ".join(arg[ 1: ]))

        except Exception as error:
            await ctx.send("Unknown error has occured: %s" % error)

        # try except, END
    # Reddit command block, END
# Reddit class, END

async def setup(client):
    await client.add_cog(Reddit(client))
