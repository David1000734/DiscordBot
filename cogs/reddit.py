from discord.ext import commands
import asyncio      # Import time keeping/looping
from discord import SyncWebhook         # Connect to webhooks

# Import reddit api. Async version
import asyncpraw
import asyncprawcore as apc

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
            "<command>: add <subreddit> <webhook_URL>, remove <subreddit>, clear, list."

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

    async def background_Task(self, sub_Name, get_limit, sleep_time, hook_URL):
        await self.client.wait_until_ready()        # Don't run while sleeping
        # Only done once. 
        is_dup = False          # Bool, check for duplicate
        flip = True             # Flip how we append onto the list
        webhook = SyncWebhook.from_url(hook_URL)        # Connect to webhook

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

                    # We must flip how we add it from the first run and the continuous ones.
                    if (flip):
                        self.reddit_post.append(submission)      # Add to end of list
                    else:
                        self.reddit_post.insert(0, submission)   # Add to beginning of list

                    # Not a duplicate, print it.
                    # Build discord message here.
                    webhook.send(submission.title + ' '\
                        + submission.url +'\n' + "https://www.reddit.com" + submission.permalink)
                # if, END
                # Otherwise, it is a duplicate. Don't do anything
                is_dup = False                      # Reset variable
            # async for, END

            # Check to see if we went past the limit
            # If the total number of post is greater than the number of
            # task times the limit, we went over. Remove the last few
            # Ex. limit = 10, 2 task.
            # If our total post is 23, we went over by 3 because 10 * 2 = 20
            if (len(self.reddit_post) >= len(self.reddit_Task) * get_limit):
                post_Counter = 0
                # We went over, remove the diference. Last to First
                for post in self.reddit_post:
                    # If the counter went over limit, remove the very last posts
                    if (post.subreddit.display_name == sub_Name and post_Counter >= get_limit):
                        # Find the correct name and remove only the
                        # post that went over the limit. (The very last few or oldest)
                        self.reddit_post.remove(post)

                    # Limit not reached, increment here
                    elif (post.subreddit.display_name == sub_Name):
                        # Increment counter
                        post_Counter += 1

                    # The subreddit we found is not related to
                    # this one, don't increment.
                    else:
                        # Just keep swimming
                        pass
                    # if else, END
                # For, END
            # Check limit, END

            # Change it to flip, This value will never change back
            flip = False

            await asyncio.sleep(sleep_time)         # Run every 'X' seconds
        # while, END
    # background task, END

    async def reddit_Add(self, ctx, arg, URL):
        # Used to find out if task has already been created.
        found = False

        # Error check below, any exceptions will be caught by the 
        # calling function.
        # *************** Check for Duplicate Subs ***************
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
            raise apc.AsyncPrawcoreException("Duplicate subreddit tasks is not allowed.")
        # *************** Duplicate Subs, END ***************

        # *************** Check for Valid Subreddits ***************
        # Ensure that it has been instantiated.
        if (self.reddit_instance == None):
            await self.init_Reddit()

        # Find valid subreddits by attempting to get from them.
        # Get the subreddit
        subRed = await self.reddit_instance.subreddit(arg, fetch = True)

        # Attempt to search it
        async for submission in subRed.new(limit = 3):
            pass
        # *************** Valid Subs, END ***************

        # *************** Check for Webhook URL ***************
        SyncWebhook.from_url(URL)       # Throws an exception if not found

        # *************** Webhook URL, END ***************
        # No exceptions were raised, thus, valid input

        # Create time loop. Continuously run this function.
        current_tasks = self.client.loop.create_task(self.background_Task(\
                        sub_Name = arg, get_limit = 5,\
                        sleep_time = 900, hook_URL = URL))

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
    # removeSub, END

    async def reddit_List(self, ctx):
        listName = []

        for currSub in self.reddit_Task:
            listName.append(currSub.get_name())

        await ctx.send("Current subreddits: %s" % ", ".join(listName))
    # list, END

    async def reddit_Clear(self, ctx):
        for currSub in self.reddit_Task:
            await ctx.send("Removed subreddit: \"%s\", from tasks." % currSub.get_name())
            currSub.cancel()
        
        # Clear list
        self.reddit_Task.clear()
    # Clear all, END

    async def reddit_Help(self, ctx):
        # Send help message. Formating...
        await ctx.send("```\n"     \
            + " Help ".center(50, '_') + "\n\n" \
            + "usage: !reddit [commands] ...\n"  \
            + "\t[commands]: add <subreddit> <webhook_URL>, remove <subreddit>, clear, list, help.\n\n" \
            + "\t[subreddit]: Whatever the name of the subreddit it may be. Remember, " \
            + "banned or subreddits containing spaces are not allowed.\n\n" \
            + "\t[webhook_URL]: Please provide the URL of a webhook that is created and set it up " \
            + "within the server. Refer to this link for help https://www.youtube.com/watch?v=fKksxz2Gdnc.\n\n" \
            + "add: Add the specified subreddit into the queue and post using the provided webhook.\n" \
            + "remove: Remove the specified subreddit from tasks if it exist.\n" \
            + "clear: Clear all subreddit from tasks.\n" \
            + "list: Show all current subreddits running.\n" \
            + "```")

    # *************** Discord command/event Functions ***************
    @commands.command()
    async def reddit(self, ctx, *arg):
        try:
            # arg[0] will will contain the command
            match arg[0].lower():
                # add command will add a new background task for the subreddit
                case "add":
                    # await self.reddit_Add(ctx, arg[1], key.disc_botSpam)        # DEBUG
                    
                    # 3 is the correct number of arguments for this command
                    if (len(arg) != 3):
                        # 3 arguments were not provided, error
                        raise ex.UnknownCommand()
                    else:
                        # arg[1] contains the word
                        await self.reddit_Add(ctx, arg[1], arg[2])
                
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

                case "help":
                    if (len(arg) > 1):
                        raise ex.UnknownCommand()
                    else:
                        await self.reddit_Help(ctx)

                # Default state
                case _:
                    # Have the try catch do the message
                    raise IndexError("")
            # Match, END
        
        # Tuple out of range when ran with "!reddit"
        # Thus prompt usage error
        except IndexError:
            await ctx.send("Usage: !reddit <command>\n" \
                           "Use `!reddit help` for more info!")

        # Custom exceptions, unknowns
        except ex.UnknownCommand as e:
            await ctx.send("Unknown command: \"%s\"" % " ".join(arg))
        
        # Custom exception, invalid subreddits
        except ex.InvalidSubreddit as e:
            await ctx.send("Error: Subreddit \"%s\" is not allowed." \
                                    % " ".join(arg[ 1: ]))

        # Handle exceptions that comes from inside reddit_add function.
        except apc.AsyncPrawcoreException as error:
            await ctx.send("Subreddit: \"%s\" Error: %s" % (arg[1], error))        

        # Default catch all exceptions
        except Exception as error:
            await ctx.send("Unknown error has occured: %s" % error)

        # try except, END
    # Reddit command block, END
# Reddit class, END

async def setup(client):
    await client.add_cog(Reddit(client))
