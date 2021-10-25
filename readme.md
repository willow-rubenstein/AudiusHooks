Stupid fucking simple, about to throw this bitch on AWS to run 24/7

Requirements:
- Python >= 3.10.0
- Pip (any version)

How To Run:
- python audius.py <audius handle> <webhook url> <optional: ignore latest posts and only fetch new after hook starts (bool)> <optional: hook check interval (seconds)>
  
If you don't know how to make webhooks in your Discord, look it up. I'll work on porting
this over more efficiently in other ways, but this works 100% of the time as of the time
I posted this.
